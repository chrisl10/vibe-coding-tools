# Distilled research: managing Claude Code desktop sessions as TARS

Stage 3 of the forge for `tars-stinger`. Every row ends with the raw file it derives from (under `raw/`). Retrieval 2026-09-28. Tool names and limits are dated observations of the Claude Code desktop app; confirm against the live tool list at run time, since several tools are deferred and must be loaded with `ToolSearch` (`select:<name>`) before first use [claude-code-desktop--live-tool-schemas].

## Current role guidance

This archive preserves the September mechanism and operating evidence. The October owner-supplied CASE/KIPP record is applied generically in [07-case-and-kipp.md](../../guides/07-case-and-kipp.md). Current owner instructions and host rules control: historical blanket relay refusals and project-specific delegation do not override verified scoped authorization. CASE/KIPP are Desktop helper sessions, not universal agents.

## D1. Spawning work: chips

| Fact | Detail | Source |
|---|---|---|
| A chip is a suggestion, not a session | `spawn_task` puts a chip in the chat; the owner's click starts a new session with its own worktree. TARS cannot start the session itself | [claude-code-desktop--live-tool-schemas], [claude-code--desktop-sessions] |
| The brief must stand alone | "include file paths and enough context to act without this conversation"; title under 60 characters, imperative | [claude-code-desktop--live-tool-schemas] |
| Stale chips can be withdrawn | `dismiss_task(task_id)` works only while the owner has not acted on it | [claude-code-desktop--live-tool-schemas] |
| Finding the started session | After the click, the session appears in `list_sessions`; `linked: true` lists this session's family, which includes tasks the owner launched from this session's suggestions. Match by title | [claude-code-desktop--live-tool-schemas] |
| Duplicates are a known failure | A chip was once spawned for work the owner had already started; check `list_sessions` first | [field-notes--prd-179-tars-swarm] |

## D2. Managing sessions

| Fact | Detail | Source |
|---|---|---|
| Read real output, not claims | `list_events(session_id, limit)` returns the session's recent turns and tool calls | [claude-code-desktop--live-tool-schemas] |
| Messaging | `SendMessage` with `to` = the `local_...` id is preferred; the legacy `send_message` reports delivered or queued. A send reaching a session does not mean it was read; silence is not agreement | [claude-code-desktop--live-tool-schemas] |
| Replies come back as notifications | Incoming messages, PR activity, and scheduled triggers queue for `ReadNotifications`; read them before other work | [claude-code-desktop--live-tool-schemas] |
| Idle notice | `SendMessage` with `notify_when_idle: true` gives one notice when that session next goes idle; never poll with "are you done?" | [claude-code-desktop--live-tool-schemas] |
| Stop, archive | `stop_session` interrupts a turn (no prompt for sessions launched from this session's suggestions). `archive_session` only after the owner explicitly agrees; it is reversible | [claude-code-desktop--live-tool-schemas] |
| No permission laundering | Never ask a peer to do what was denied or blocked here | [claude-code-desktop--live-tool-schemas] |
| Send budget | In the PRD-179 deployment cross-session sends were capped at 10 per owner message. Not documented; treat as a possible limit and batch | [field-notes--prd-179-tars-swarm] |
| Unattended sessions | Messaging does not work to or from scheduled-task runs | [claude-code--desktop-sessions], [claude-code-desktop--live-tool-schemas] |

## D3. Timers: the 10-minute tick

| Fact | Detail | Source |
|---|---|---|
| CronCreate is the timer | 5-field cron, local time; `*/10 * * * *` fires every 10 minutes; returns an 8-character id for `CronDelete` | [claude-code-desktop--live-tool-schemas], [claude-code--scheduled-tasks] |
| Fires only when idle | "Jobs only fire while the REPL is idle"; no catch-up for missed fires, one fire when idle again | [claude-code-desktop--live-tool-schemas], [claude-code--scheduled-tasks] |
| Jitter and expiry | Recurring fires can be late: the tool contract says up to 10% of the period, the docs say up to half the interval for tasks more frequent than hourly (so a 10-minute tick may slip by 1 to 5 minutes; see G4). Recurring tasks expire after 7 days; up to 50 tasks per session | [claude-code-desktop--live-tool-schemas], [claude-code--scheduled-tasks] |
| Session-scoped | Gone when the session ends; restored on resume except expired ones. Background Bash and Monitor tasks are never restored on resume | [claude-code--scheduled-tasks] |
| Durable alternative | Desktop scheduled tasks persist across restarts (1-minute minimum) but run as unattended sessions, which cannot message other sessions, so they cannot manage | [claude-code--scheduled-tasks], [claude-code--desktop-sessions] |
| Owner requirement | The check bound must be "a timer, not just an annoying sub-script" | [field-notes--prd-179-tars-swarm] |

Implication: TARS must end its turns promptly and sit idle between events, or the tick never fires. A manager that does work of its own starves its own timer.

## D4. CI: one-minute poll plus watchdog

| Fact | Detail | Source |
|---|---|---|
| Monitor streams events | Each stdout line of a background script becomes a notification; exit ends the watch | [claude-code-desktop--live-tool-schemas] |
| Monitor expires | Default 5 minutes, maximum 30; re-arm on expiry | [claude-code-desktop--live-tool-schemas] |
| Coverage | "silence is not success"; the filter must emit on every terminal state; handle transient failures with `|| true` | [claude-code-desktop--live-tool-schemas] |
| Poll interval | 30 seconds or more for remote APIs; 60 seconds meets the owner's one-minute ask | [claude-code-desktop--live-tool-schemas], [field-notes--prd-179-tars-swarm] |
| App-level PR status | `ccd_pr get_status(session_id)` reads any session's bound PR: check counts, failing names, mergeability, from the app cache, independent of TARS's scripts | [claude-code-desktop--live-tool-schemas] |
| Desktop PR monitor | The app polls checks with `gh` and can wake a session on CI failure (`set_monitor auto_fix`); switching it needs the owner's ask | [claude-code--desktop-sessions], [claude-code-desktop--live-tool-schemas] |
| Past failures | No watcher at all; "0 checks = green"; an unsupported regex; a dead health URL | [field-notes--prd-179-tars-swarm] |

Implication: two independent sources. Source 1 is the Monitor poller (every 60 seconds, emits only changes and terminal states, writes a heartbeat). Source 2 is the watchdog, run on every 10-minute tick: re-arm the poller if its heartbeat is stale or the Monitor expired, and cross-check each managed session's `get_status` plus `gh run list` for anything the poller missed.

## D5. The adviser

| Fact | Detail | Source |
|---|---|---|
| Owner requirement | A separate session that says whether a plan or answer is overkill or can proceed; spawned first, as a chip (owner's choice) or a running subagent | [field-notes--prd-179-tars-swarm] |
| Chip form | Persistent, visible, survives TARS compaction; costs the owner one click | [claude-code-desktop--live-tool-schemas] |
| Subagent fallback | Background by default; resumable by name with `SendMessage`; its report is not shown to the owner | [claude-code-desktop--live-tool-schemas] |
| Why it exists | Both major PRD-179 failures were disproportion: a nine-agent phone fix and an unrequested rebuild | [field-notes--prd-179-tars-swarm] |

## D6. Authority and discipline

| Fact | Detail | Source |
|---|---|---|
| Decide and record | TARS rules within its authority and appends the ruling to the ledger | [field-notes--prd-179-tars-swarm] |
| Owner-only gates | Tailscale, money, credentials, production data changes; new dependencies or other gate workarounds get a one-line question first | [field-notes--prd-179-tars-swarm] |
| Relayed approvals | Historical incident: an unverified sibling claim was refused; current instructions require verifying the original owner decision and scope | [field-notes--prd-179-tars-swarm] |
| Workflows | Only on explicit request | [claude-code-desktop--live-tool-schemas], [field-notes--prd-179-tars-swarm] |
| Pinned merges | `gh pr merge --match-head-commit <sha>` | [field-notes--prd-179-tars-swarm] |
| Chip briefs name pre-approved risk | A blanket "never touch production" blocked an approved backfill | [field-notes--prd-179-tars-swarm] |

## D7. Running TARS as the main thread

| Fact | Detail | Source |
|---|---|---|
| `--agent` | `claude --agent <name>` or the `agent` setting runs the whole session with the agent's prompt, tool restrictions, and model | [claude-code--sub-agents] |
| Restrictions | `disallowedTools` removes tools from the inherited set; `initialPrompt` auto-submits a first turn for a main-thread agent; `skills` preloads full skill content | [claude-code--sub-agents] |
| Desktop entry | The desktop Code tab starts ordinary sessions; the practical entry there is the `/tars` command, which loads this Stinger into the current session | [claude-code--desktop-sessions] |

## Conflicts and gaps

- G1. The send cap (10 per owner message) is observed, not documented. Batch messages regardless.
- G2. Whether a session started from a chip always appears under `linked: true` is inferred from the `stop_session` wording, not stated outright. Fall back to title match.
- G3. `disallowedTools` applies only when TARS runs as `--agent`; under `/tars` in a normal desktop session, "no implementation work" is enforced by the Stinger's rules, not by tool removal. `claude --agent` starts a terminal CLI session, and the desktop session surface covers only sessions the desktop app runs [claude-code--desktop-sessions], so a terminal TARS has no chip or session tools. Whether the project `agent` setting applies to desktop sessions is not documented in the archive.
- G4. Recurring jitter conflicts: 10% of the period in the `CronCreate` contract, up to half the interval in the scheduled-tasks docs. Measure stalls by elapsed time since last real progress, not by an assumed exact 10-minute spacing.
