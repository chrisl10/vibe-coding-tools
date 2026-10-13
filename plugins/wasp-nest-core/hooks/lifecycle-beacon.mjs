#!/usr/bin/env node
// Lifecycle beacon: one observer hook registered on every hook event of
// Claude Code, Codex, and ZCode. On each event it:
//   1. stamps the time twice, local (native timezone) and UTC+0, clearly delineated;
//   2. reports how long the session and the current turn have run;
//   3. records a heartbeat TARS can read without opening a transcript: last
//      event, last real progress, per-event counts, branch, cwd, cadence flags.
//
// Usage:  node lifecycle-beacon.mjs <claude|codex|zcode> [EventName]
//   EventName is a fallback for payloads that omit hook_event_name.
//   On UserPromptSubmit the stamp also carries "last turn", the length of the turn
//   that just finished, measured from UserPromptSubmit to Stop (or Interrupt).
// State:  $WASP_BEACON_DIR (default ~/.wasp-nest/beacon)
//   sessions/<harness>-<session>.json   latest heartbeat, rewritten atomically
//   events/<harness>-<session>.jsonl    append-only event log (rotates at 1 MB)
//
// Observer contract: never block, never decide. Exit 0 always, never exit 2,
// never emit continue/decision/permissionDecision. Fail open to "{}".
// Never send additionalContext on Stop or SubagentStop: Claude Code and ZCode treat
// it as feedback that continues the turn (Claude up to 8 times in a row, ZCode 3),
// so an observer stamp there would force extra model turns. The length of the
// finished turn rides on the next UserPromptSubmit stamp instead.
// WorktreeCreate is deliberately NOT a registered event in Claude Code: a hook
// there replaces git's worktree creation and must print a path.
import {
  closeSync, constants, existsSync, fchmodSync, fstatSync, linkSync, lstatSync, mkdirSync, openSync,
  readFileSync, readSync, readdirSync, realpathSync, renameSync, statSync, unlinkSync, writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const MINUTE = 60_000;
const LOG_ROTATE_BYTES = 1_000_000;
const POLLER_STALE_MS = 3 * MINUTE; // TARS: heartbeat older than 3 minutes = dead poller
const MAX_EFFORTS = 32; // bound the .tars scan, which runs on every hook event
const EFFORT_NAME = /^[A-Za-z0-9._-]{1,64}$/; // repo-controlled names reach model context
const TOKEN = /^[A-Za-z0-9_.:@/[\]-]{1,80}$/; // enum-like payload values only; free text is never stored
const LOCK_WAIT_MS = 1000; // parallel tool calls fire hooks concurrently; serialize the state update
const LOCK_STALE_MS = 5000; // a lock older than the hook timeout belongs to a killed process

// Events whose hookSpecificOutput.additionalContext reaches the model without side
// effects, per harness docs. Stop and SubagentStop are left out on purpose (see header).
const CONTEXT_EVENTS = {
  claude: new Set(["SessionStart", "SubagentStart", "UserPromptSubmit", "UserPromptExpansion",
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PostToolBatch", "PostModelSwitch"]),
  codex: new Set(["SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "SubagentStart"]),
  zcode: new Set(["SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse",
    "PostToolUseFailure"]),
};

// Where systemMessage reaches the human. Claude Code discards it on these events;
// Codex documents it only on the listed ones; ZCode is treated as Claude-shaped.
const CLAUDE_NO_SYSTEM_MESSAGE = new Set(["Setup", "InstructionsLoaded", "MessageDisplay",
  "Notification", "ConfigChange", "WorktreeRemove", "PreCompact", "PostCompact", "SessionEnd",
  "Elicitation", "ElicitationResult", "StopFailure"]);
const CODEX_SYSTEM_MESSAGE = new Set(["SessionStart", "PreCompact", "PostCompact",
  "UserPromptSubmit", "SubagentStart", "SubagentStop", "Stop", "PreToolUse", "PostToolUse",
  "PermissionRequest", "Interrupt"]);

export function showsUser(harness, event) {
  if (SILENT_EVENTS.has(event)) return false;
  return harness === "codex" ? CODEX_SYSTEM_MESSAGE.has(event) : !CLAUDE_NO_SYSTEM_MESSAGE.has(event);
}

// An alert counts as delivered to the model only on a main-thread event whose context
// the host injects. Inside a subagent (agent_id set, or SubagentStart) the context lands
// in the subagent, so the alert stays pending for the main conversation.
export function deliversContext(harness, event, data = {}) {
  return (CONTEXT_EVENTS[harness] || CONTEXT_EVENTS.claude).has(event) &&
    event !== "SubagentStart" && !data.agent_id;
}

// Events whose stdout the host discards; skip the work of formatting output.
const SILENT_EVENTS = new Set(["SessionEnd", "WorktreeRemove", "MessageDisplay"]);

const FILE_TOOLS = /^(Edit|Write|MultiEdit|NotebookEdit|apply_patch|ApplyPatch)$/;
const CHECK_COMMANDS = /\b(git\s+(commit|push|merge|rebase|cherry-pick)|gh\s+(pr|run)|npm\s+(test|run)|pnpm\s+\S+|yarn\s+\S+|bun\s+(test|run)|pytest|vitest|jest|tsc|cargo\s+(test|build|check)|go\s+(test|build)|make\b|python3?\s+\S*test\S*)/;

// ---------------------------------------------------------------- input

function readPayload() {
  try { return JSON.parse(readFileSync(0, "utf8") || "{}"); } catch { return {}; }
}

function safeId(value) {
  return String(value || "unknown").replace(/[^A-Za-z0-9._-]/g, "_").slice(0, 120) || "unknown";
}

function token(value) {
  return typeof value === "string" && TOKEN.test(value) ? value : undefined;
}

// Paths and refs come from the filesystem and can carry newlines or prompt text.
function clean(value, max = 240) {
  return typeof value === "string" ? value.replace(/[\u0000-\u001f\u007f-\u009f\u2028\u2029]/g, "?").slice(0, max) : null;
}

function sessionIdOf(data) {
  return data.session_id || data.sessionId || data.thread_id ||
    process.env.CODEX_SESSION_ID || process.env.CODEX_THREAD_ID || "unknown";
}

// ---------------------------------------------------------------- time

function pad(n) { return String(n).padStart(2, "0"); }

function offsetLabel(date) {
  const minutes = -date.getTimezoneOffset();
  const sign = minutes >= 0 ? "+" : "-";
  const abs = Math.abs(minutes);
  return `UTC${sign}${pad(Math.floor(abs / 60))}:${pad(abs % 60)}`;
}

export function stamps(date = new Date()) {
  const zone = Intl.DateTimeFormat().resolvedOptions().timeZone || "local";
  const abbrev = new Intl.DateTimeFormat("en-US", { timeZoneName: "short" })
    .formatToParts(date).find((part) => part.type === "timeZoneName")?.value || "";
  const local = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
    `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  const utc = date.toISOString().slice(0, 19).replace("T", " ");
  return {
    local: `${local} ${abbrev} (${offsetLabel(date)}, ${zone})`.replace("  ", " "),
    utc: `${utc} UTC+00:00`,
    iso: date.toISOString(),
  };
}

export function span(ms) {
  if (!Number.isFinite(ms) || ms < 0) return "n/a";
  const s = Math.floor(ms / 1000);
  const d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600);
  const m = Math.floor((s % 3600) / 60), sec = s % 60;
  if (d) return `${d}d ${h}h ${pad(m)}m`;
  if (h) return `${h}h ${pad(m)}m`;
  if (m) return `${m}m ${pad(sec)}s`;
  return `${sec}s`;
}

// ---------------------------------------------------------------- repo + TARS

function repoRoot(start) {
  let path = resolve(start || process.cwd());
  for (let i = 0; i < 64; i++) {
    if (existsSync(join(path, ".git"))) return path;
    const parent = dirname(path);
    if (parent === path) return null;
    path = parent;
  }
  return null;
}

// Read a small regular file without blocking: a FIFO or device planted as .git/HEAD
// would otherwise stall every hook firing until the host timeout.
function readSmallFile(path, limit = 4096) {
  const fd = openSync(path, constants.O_RDONLY | constants.O_NONBLOCK);
  try {
    const st = fstatSync(fd);
    if (!st.isFile() || st.size > limit) return null;
    const buf = Buffer.alloc(st.size);
    return buf.toString("utf8", 0, readSync(fd, buf, 0, st.size, 0));
  } finally { closeSync(fd); }
}

function gitBranch(root) {
  try {
    let gitDir = join(root, ".git");
    if (statSync(gitDir).isFile()) {
      const pointer = readSmallFile(gitDir)?.match(/^gitdir:\s*(.+)$/m)?.[1]?.trim();
      if (!pointer) return null;
      gitDir = resolve(root, pointer);
    }
    const head = (readSmallFile(join(gitDir, "HEAD")) || "").split("\n")[0].trim();
    if (head.startsWith("ref: refs/heads/")) return head.slice(16).replace(/[^A-Za-z0-9._/@+-]/g, "_").slice(0, 120) || null;
    return /^[0-9a-f]{8,}$/i.test(head) ? `detached@${head.slice(0, 8)}` : null;
  } catch { return null; }
}

// TARS keeps one folder per effort at <repo>/.tars/<effort>/ with ledger.md and
// the ci-poll.sh heartbeat. Report every effort so TARS sees a dead poller fast.
function tarsEfforts(root, now) {
  if (!root) return [];
  const base = join(root, ".tars");
  try {
    return readdirSync(base, { withFileTypes: true })
      .filter((e) => e.isDirectory() && EFFORT_NAME.test(e.name)).slice(0, MAX_EFFORTS).map((e) => {
      const dir = join(base, e.name);
      let heartbeatAgeMs = null;
      try { heartbeatAgeMs = now - statSync(join(dir, "heartbeat")).mtimeMs; } catch { /* no poller yet */ }
      return {
        effort: e.name,
        ledger: existsSync(join(dir, "ledger.md")),
        heartbeatAgeMs,
        pollerStale: heartbeatAgeMs !== null && heartbeatAgeMs > POLLER_STALE_MS,
      };
    });
  } catch { return []; }
}

// ---------------------------------------------------------------- state

function stateDir() {
  return process.env.WASP_BEACON_DIR || join(homedir(), ".wasp-nest", "beacon");
}

function assertNoStorageLinks(file) {
  const target = resolve(file);
  let current = target;
  for (;;) {
    try {
      const st = lstatSync(current);
      if (st.isSymbolicLink()) {
        const systemAlias = process.platform === "darwin" && ["/tmp", "/var", "/etc"].includes(current);
        if (!systemAlias || realpathSync(current) !== `/private${current}`) throw new Error("linked beacon storage path");
      } else if (current === target ? !st.isFile() : !st.isDirectory()) {
        throw new Error("beacon storage requires regular files and directory ancestors");
      }
    } catch (error) { if (error.code !== "ENOENT") throw error; }
    const parent = dirname(current);
    if (parent === current) break;
    current = parent;
  }
}

function assertStoragePath(file) {
  const base = resolve(stateDir());
  const target = resolve(file);
  if (target === base || !target.startsWith(base + sep)) throw new Error("beacon storage path escapes its selected directory");
  assertNoStorageLinks(target);
}

function readJson(path) {
  let descriptor;
  try {
    assertStoragePath(path);
    descriptor = openSync(path, constants.O_RDONLY | (constants.O_NOFOLLOW || 0) | constants.O_NONBLOCK);
    if (!fstatSync(descriptor).isFile()) return null;
    return JSON.parse(readFileSync(descriptor, "utf8"));
  } catch { return null; }
  finally { if (descriptor !== undefined) closeSync(descriptor); }
}

function writeAtomic(path, text) {
  assertStoragePath(path);
  mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
  const tmp = `${path}.${process.pid}.${Date.now()}.tmp`;
  let descriptor, created = false;
  try {
    assertStoragePath(tmp);
    descriptor = openSync(tmp, "wx", 0o600);
    created = true;
    writeFileSync(descriptor, text);
    closeSync(descriptor);
    descriptor = undefined;
    assertStoragePath(path);
    renameSync(tmp, path);
    created = false;
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
    if (created) try { unlinkSync(tmp); } catch { /* best-effort private temp cleanup */ }
  }
}

// Serialize one session's read-modify-write. Parallel tool calls fire hooks at the same
// time; without this, concurrent firings drop each other's counts and lastProgressAt.
// Fails open: if the lock cannot be taken in LOCK_WAIT_MS, fn runs with locked=false and
// must not write, so a stuck lock costs one unrecorded event, never committed state or
// the printed stamp. Every retry path re-checks the deadline: a dangling symlink at the
// lock path (open says it exists, stat says it does not) or an unremovable stale lock
// must not spin.
// Locks are identified by inode, so neither stale cleanup nor release can delete a lock
// another process created in the meantime. Best effort: a sub-millisecond window remains
// between the inode check and the unlink, which costs at most one lost counter update.
function withLock(path, fn) {
  const lock = `${path}.lock`;
  assertStoragePath(path);
  mkdirSync(dirname(lock), { recursive: true, mode: 0o700 });
  const deadline = Date.now() + LOCK_WAIT_MS;
  const nap = new Int32Array(new SharedArrayBuffer(4));
  let fd = null;
  while (fd === null && Date.now() < deadline) {
    try { fd = openSync(lock, "wx", 0o600); break; } catch (error) {
      if (error.code !== "EEXIST") break;
    }
    try {
      const seen = lstatSync(lock);
      // Keep the observer stamp but never follow, remove or write through an
      // unsafe lock. This also preserves dangling-link fail-open behavior.
      if (!seen.isFile()) break;
      if (Date.now() - seen.mtimeMs > LOCK_STALE_MS && removeStaleLock(lock, seen.ino)) continue;
    } catch { /* vanished or a dangling link: wait and retry until the deadline */ }
    Atomics.wait(nap, 0, 0, 5);
  }
  const mine = fd !== null ? fstatSync(fd).ino : null;
  try { return fn(fd !== null); } finally {
    if (fd !== null) {
      closeSync(fd);
      try { if (lstatSync(lock).ino === mine) unlinkSync(lock); } catch { /* already gone */ }
    }
  }
}

// Move the lock aside under a unique name, then delete it only if it is the same inode
// that was judged stale. If another process replaced it first, put that live lock back
// (linkSync fails rather than overwrite a newer one) and leave it alone.
// Returns true when the lock path was cleared, so the caller retries at once.
export function removeStaleLock(lock, staleIno) {
  const aside = `${lock}.${process.pid}.${Date.now()}.stale`;
  try { assertNoStorageLinks(lock); assertNoStorageLinks(aside); } catch { return false; }
  try { renameSync(lock, aside); } catch { return false; }
  let cleared = true;
  try {
    if (lstatSync(aside).ino !== staleIno) { cleared = false; try { linkSync(aside, lock); } catch { /* a newer lock exists */ } }
  } finally {
    try { unlinkSync(aside); } catch { /* already gone */ }
  }
  return cleared;
}

function appendEvent(path, record) {
  assertStoragePath(path);
  assertStoragePath(`${path}.1`);
  mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
  const flags = constants.O_WRONLY | constants.O_CREAT | constants.O_APPEND |
    (constants.O_NOFOLLOW || 0) | constants.O_NONBLOCK;
  let descriptor = openSync(path, flags, 0o600);
  try {
    const st = fstatSync(descriptor);
    if (!st.isFile()) throw new Error("beacon event log is not a regular file");
    fchmodSync(descriptor, 0o600);
    if (st.size > LOG_ROTATE_BYTES) {
      closeSync(descriptor);
      descriptor = null;
      assertStoragePath(path);
      assertStoragePath(`${path}.1`);
      if (lstatSync(path).ino !== st.ino) throw new Error("beacon event log changed before rollover");
      renameSync(path, `${path}.1`);
      descriptor = openSync(path, flags, 0o600);
      if (!fstatSync(descriptor).isFile()) throw new Error("beacon event log is not a regular file");
      fchmodSync(descriptor, 0o600);
    }
    writeFileSync(descriptor, JSON.stringify(record) + "\n");
  } finally { if (descriptor !== null) closeSync(descriptor); }
}

function transcriptBirth(path) {
  if (typeof path !== "string" || !path) return null;
  try {
    const st = statSync(path);
    const born = st.birthtimeMs > 0 ? st.birthtimeMs : st.ctimeMs;
    return born > 0 ? born : null;
  } catch { return null; }
}

export function isProgress(event, data) {
  if (event === "SubagentStop" || event === "TaskCompleted") return true;
  if (event !== "PostToolUse") return false;
  const tool = String(data.tool_name || "");
  if (FILE_TOOLS.test(tool)) return true;
  const command = data.tool_input?.command;
  return /^(Bash|shell|local_shell|exec_command)$/i.test(tool) &&
    typeof command === "string" && CHECK_COMMANDS.test(command);
}

// ---------------------------------------------------------------- core

export function observe(harness, event, data, now = Date.now()) {
  const sid = safeId(sessionIdOf(data));
  const key = `${safeId(harness)}-${sid}`;
  const statePath = join(stateDir(), "sessions", `${key}.json`);
  const eventPath = join(stateDir(), "events", `${key}.jsonl`);
  // Validate both sides before any state/lock write, so an unsafe event log
  // cannot produce a partially updated heartbeat or an external append.
  assertStoragePath(statePath);
  assertStoragePath(eventPath);
  assertStoragePath(`${eventPath}.1`);
  return withLock(statePath, (locked) => update(harness, event, data, now, sid, key, statePath, locked));
}

// persist=false (lock not acquired): compute the stamp and alerts from the last saved
// state but write nothing, so a concurrent holder's committed update is never clobbered.
function update(harness, event, data, now, sid, key, statePath, persist = true) {
  const dir = stateDir();
  const previous = readJson(statePath) || {};

  const born = transcriptBirth(data.transcript_path);
  const startedAt = Math.min(previous.startedAt ?? now, born ?? now);
  const state = {
    harness,
    sessionId: sid,
    startedAt,
    startedAtSource: born !== null && born <= (previous.startedAt ?? now) ? "transcript" : (previous.startedAtSource || "first-event"),
    cwd: clean(data.cwd, 1024) || previous.cwd || process.cwd(),
    model: token(data.model) || previous.model || null,
    // Subagent events carry the subagent's type; only a main-thread agent_type describes the session.
    agentType: (data.agent_id ? null : token(data.agent_type)) || previous.agentType || null,
    turnStartedAt: previous.turnStartedAt ?? null,
    turnEndedAt: previous.turnEndedAt ?? null,
    lastTurnMs: previous.lastTurnMs ?? null,
    lastProgressAt: previous.lastProgressAt ?? null,
    lastProgressWhat: previous.lastProgressWhat ?? null,
    lastEvent: event,
    lastEventAt: now,
    previousEventAt: previous.lastEventAt ?? null,
    counts: { ...(previous.counts || {}) },
    ended: false,
  };
  state.counts[event] = (state.counts[event] || 0) + 1;

  const turnOpen = state.turnStartedAt !== null && state.turnEndedAt === null;
  if (event === "UserPromptSubmit") { state.turnStartedAt = now; state.turnEndedAt = null; }
  // A later Stop (another hook continued the turn) moves the end forward.
  if (state.turnStartedAt !== null && (event === "Stop" || event === "Interrupt" || event === "StopFailure")) {
    state.turnEndedAt = now;
  }
  // A new start, resume, clear, or fork means the old turn is over even if no Stop fired
  // (a crash, or an interrupt in Claude Code, fires none). Only compaction keeps a turn open.
  if (turnOpen && event === "SessionStart" && data.source !== "compact") {
    state.turnEndedAt = previous.lastEventAt ?? now;
  }
  if (state.turnStartedAt !== null && state.turnEndedAt !== null && state.turnEndedAt !== previous.turnEndedAt) {
    state.lastTurnMs = state.turnEndedAt - state.turnStartedAt;
  }
  if (event === "SessionEnd") state.ended = true;
  if (isProgress(event, data)) {
    state.lastProgressAt = now;
    state.lastProgressWhat = token(data.tool_name) || event;
  }

  const root = repoRoot(state.cwd);
  state.repo = root;
  state.branch = root ? gitBranch(root) : null;
  state.tars = tarsEfforts(root, now);

  const turnActive = state.turnStartedAt !== null && state.turnEndedAt === null;
  const turnMs = state.turnStartedAt !== null ? (state.turnEndedAt ?? now) - state.turnStartedAt : null;
  const sinceProgressMs = turnActive ? now - Math.max(state.lastProgressAt ?? 0, state.turnStartedAt) : null;
  state.flags = {
    turnActive,
    turnWarn45: turnActive && turnMs >= 45 * MINUTE,
    turnDeadline60: turnActive && turnMs >= 60 * MINUTE,
    noProgress10: turnActive && sinceProgressMs >= 10 * MINUTE,
    noProgress20: turnActive && sinceProgressMs >= 20 * MINUTE,
    pollerStale: state.tars.some((t) => t.pollerStale),
  };
  // Each channel tracks its own delivered keys: an alert reaches the model once (on the
  // first main-thread context event) and the human once (on the first event that shows
  // systemMessage). Until then it stays pending.
  const current = alerts(state);
  const contextSent = new Set(previous.alertKeys || []);
  const userSent = new Set(previous.userAlertKeys || []);
  const toContext = deliversContext(harness, event, data);
  const toUser = showsUser(harness, event);
  const contextAlerts = toContext ? current.filter((a) => !contextSent.has(a.key)).map((a) => a.text) : [];
  const userAlerts = toUser ? current.filter((a) => !userSent.has(a.key)).map((a) => a.text) : [];
  state.alertKeys = current.filter((a) => contextSent.has(a.key) || toContext).map((a) => a.key);
  state.userAlertKeys = current.filter((a) => userSent.has(a.key) || toUser).map((a) => a.key);

  if (persist) {
    writeAtomic(statePath, JSON.stringify(state, null, 2) + "\n");
    appendEvent(join(dir, "events", `${key}.jsonl`), {
      at: new Date(now).toISOString(), event, harness,
      tool: token(data.tool_name), source: token(data.source) || token(data.reason) || token(data.trigger),
      progress: state.lastProgressAt === now || undefined,
    });
  }

  const lastTurnMs = event === "UserPromptSubmit" ? state.lastTurnMs : null;
  // Report a turn length while the turn runs and on the event that ends it, not afterwards.
  const shownTurnMs = turnActive || state.turnEndedAt === now ? turnMs : null;
  return { state, statePath, contextAlerts, userAlerts,
    metrics: { sessionMs: now - state.startedAt, turnMs: shownTurnMs, sinceProgressMs, lastTurnMs } };
}

// ---------------------------------------------------------------- output

export function stampLine(event, harness, metrics, now = new Date()) {
  const t = stamps(now);
  const parts = [`[beacon ${harness}] ${event}`, `Local: ${t.local}`, `UTC: ${t.utc}`,
    `session ${span(metrics.sessionMs)}`];
  if (metrics.lastTurnMs != null) parts.push(`last turn ${span(metrics.lastTurnMs)}`);
  if (metrics.turnMs !== null) parts.push(`turn ${span(metrics.turnMs)}`);
  if (metrics.sinceProgressMs !== null) parts.push(`since progress ${span(metrics.sinceProgressMs)}`);
  return parts.join(" | ");
}

// Each alert carries a key scoped to what it is about (this turn, this stall, this
// poller), so it surfaces once per occurrence instead of on every following event.
export function alerts(state) {
  const out = [];
  const f = state.flags;
  const turn = state.turnStartedAt;
  const stall = Math.max(state.lastProgressAt ?? 0, turn ?? 0);
  if (f.turnDeadline60) out.push({ key: `turn60@${turn}`, text: "Cadence: this turn passed 60 minutes. Checkpoint and stop unless continuing was authorized." });
  else if (f.turnWarn45) out.push({ key: `turn45@${turn}`, text: "Cadence: this turn passed 45 minutes. Give a one-line status (done / remaining / ETA)." });
  if (f.noProgress20) out.push({ key: `stall20@${stall}`, text: "Cadence: 20 minutes without real progress (no file change, check, or commit). Stop, preserve work, report." });
  else if (f.noProgress10) out.push({ key: `stall10@${stall}`, text: "Cadence: 10 minutes without real progress. Notify the owner in one line." });
  for (const t of state.tars) {
    if (t.pollerStale) out.push({ key: `poller@${t.effort}`, text: `TARS: CI poller heartbeat for effort "${t.effort}" is ${span(t.heartbeatAgeMs)} old (over 3m). If this session is the TARS manager, re-arm the Monitor; any other session leaves it to TARS.` });
  }
  return out;
}

function sessionBriefing(state, statePath) {
  const lines = [
    `Beacon heartbeat for this session: ${statePath}`,
    `Session id: ${state.sessionId}. Branch: ${state.branch || "n/a"}. Repo: ${clean(state.repo) || "n/a"}.`,
    `Every hook event rewrites that file (lastEventAt, lastProgressAt, counts, flags) and appends to events/${state.harness}-${state.sessionId}.jsonl beside it.`,
  ];
  if (state.tars.length) {
    lines.push(`TARS efforts in this repo: ${state.tars.map((t) =>
      `${t.effort} (ledger ${t.ledger ? "yes" : "no"}, poller heartbeat ${t.heartbeatAgeMs === null ? "none" : span(t.heartbeatAgeMs) + " old"})`).join("; ")}.`);
    lines.push("TARS can read every managed session's heartbeat from the sessions/ folder as a second progress source next to list_events.");
  }
  return lines.join("\n");
}

// Decide which channels carry this event's stamp.
//   context: model-visible additionalContext (costs tokens on every firing)
//   user:    systemMessage shown to the human in the UI
// Policy: the model gets the clock at turn boundaries and whenever an alert fires;
// the human sees session start and alerts. Per-tool events stay on disk only.
// Turn ends (Stop, SubagentStop) never carry context, because there it would restart the
// turn; the next UserPromptSubmit stamp reports the finished turn as "last turn".
const CONTEXT_ANCHORS = new Set(["SessionStart", "UserPromptSubmit", "SubagentStart"]);
const USER_ANCHORS = new Set(["SessionStart"]);

export function render(harness, event, observed, now = new Date()) {
  if (SILENT_EVENTS.has(event)) return {};
  const { state, statePath, metrics } = observed;
  const contextAlerts = observed.contextAlerts || [];
  const userAlerts = observed.userAlerts || [];
  const line = stampLine(event, harness, metrics, now);
  const out = {};
  if ((USER_ANCHORS.has(event) || userAlerts.length) && showsUser(harness, event)) {
    out.systemMessage = [line, ...userAlerts].join("\n");
  }
  if ((CONTEXT_ANCHORS.has(event) || contextAlerts.length) && (CONTEXT_EVENTS[harness] || CONTEXT_EVENTS.claude).has(event)) {
    const body = [line, ...contextAlerts];
    if (event === "SessionStart" || event === "SubagentStart") body.push(sessionBriefing(state, statePath));
    out.hookSpecificOutput = { hookEventName: event, additionalContext: body.join("\n") };
  }
  return out;
}

// ---------------------------------------------------------------- main

// Compare real paths: the hook is often reached through a symlinked home or a path with spaces.
function invokedDirectly() {
  try { return Boolean(process.argv[1]) && realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url)); } catch { return false; }
}
if (invokedDirectly()) {
  let output = {};
  try {
    const harness = (process.argv[2] || "claude").toLowerCase();
    const data = readPayload();
    const event = String(data.hook_event_name || data.hookEventName || process.argv[3] || "Unknown");
    const now = Date.now();
    output = render(harness, event, observe(harness, event, data, now), new Date(now));
  } catch {
    output = {};
  }
  process.stdout.write(JSON.stringify(output));
  process.exit(0);
}
