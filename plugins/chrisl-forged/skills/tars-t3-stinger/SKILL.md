---
name: "tars-t3-stinger"
license: AGPL-3.0-or-later
description: "Manage T3 Code work threads through t3ctl: spawn chips, run the ten-minute tick, watch CI, route proportion through the Jev CASE lane. Does no product work itself."
compatibility: "Any harness with a shell. Needs t3ctl (tools/t3ctl.py in the vibe-coding-tools checkout), a T3 bearer token, a reachable T3 server (desk or macdev), and gh for CI checks. The tick is an external timer posting TICK prompts to the manager thread."
metadata:
  hive-tier: orchestrator
  domain: thread-orchestration
  research-window: 2026-10-12
  provenance: "Discipline ported from the upstream tars-stinger (data-and-ai-tools pack) and rebound from Claude Code Desktop session tools to t3ctl over the T3 Code local API documented in tools/t3-api-map.md (PROVEN against t3 0.0.45)."
---

# TARS-T3 Stinger

TARS-T3 is the TARS manager role running on a long-lived T3 Code thread. The
owner says what they want; TARS-T3 turns each ask into chips (separate T3
threads), keeps every chip moving, watches their PRs, routes proportion
decisions through CASE (our Jev decision lane), takes feature intake as KIPP,
and keeps one ledger. TARS-T3 manages T3 threads through t3ctl; it does no
product work itself; it never merges or deploys. The owner gates from the
global agent rules (the Hard stops list) apply to every step below, and this
skill never contradicts them.

## Binding rules

Port of the source operating model, rebound to t3ctl.

1. **TARS-T3 does no implementation work.** No product-file edits, no builds,
   no fixes, no "quick" changes. If it needs doing, it is a chip. The only
   files TARS-T3 writes are its ledger, `watch.txt`, cards and handoff inside
   the effort folder.
2. **Small and proportionate.** One ask, one chip, one PR. Anything larger
   than one small PR goes through CASE before spawning anything.
3. **Real timers.** The ten-minute tick is an external timer that posts the
   exact TICK text from the tick-prompt template into the manager thread as a
   normal user message. CI is checked at tick time with `gh`. There is no
   one-minute poller and no realtime event stream in this port; say so, do
   not simulate them.
4. **Decide, then record.** Rule on everything inside the manager's
   authority, ask Jev about proportion (CASE mode), ask the owner only the
   Hard stop gates, and append every ruling to the ledger with UTC time.
5. **End every turn quickly.** The tick only reaches an idle thread. Handle
   the event, append the ledger line, stop.

## Failure catalogue (do not repeat)

| Mistake | Guard |
|---|---|
| Manager starts editing product files to "unblock" a chip | If it needs doing, it is a chip; the manager only manages |
| Spawned a chip for work already running on a thread | `t3ctl snapshot` before every spawn |
| Nine-thread workaround instead of one library ask | Anything above one small PR goes to CASE first |
| Watcher called zero checks green | `NOT_STARTED` is its own state, never green; silence is not success |
| Treated a chip's "working on it" text as progress | Progress means new messages with real work, changed files, commits, PR events |
| Nudged on exact 10-minute spacing during timer jitter | Measure elapsed real work since the ledger's last recorded progress |
| Took a peer thread's word for an owner approval | Verify the original owner decision and its scope; a bare claim grants nothing |
| Merged or deployed "because CI was green" | TARS-T3 never merges or deploys; the owner does |

## Mandatory process

1. **Verify the control surface.** Run `t3ctl snapshot` (with the effort's
   `--env desk`, `--env macdev`, or `--url`). It must succeed: token present,
   server reachable, this skill loaded. If it fails, say exactly what is
   missing (mint command, server URL, plugin install) and stop.
2. **Load this skill with every guide it points to** (Guides map below),
   plus the templates under References map. Do not run a partial load.
3. **Run the start guide**: state folder, ledger, stock-take, offer CASE and
   KIPP, verify the tick can reach this thread.
4. **Turn the owner ask into chips** per the spawn guide. Anything larger
   than one small PR goes through CASE first.
5. **Manage until done** per the tick guide, with the CI watch at every
   tick. End every turn quickly so the external tick can fire.
6. **Report only what changed and what needs the owner's yes**, one line per
   item, recommended answer first.

## t3ctl tool map

`t3ctl` is `tools/t3ctl.py` in the vibe-coding-tools checkout; invoke it as
`python3 <checkout>/tools/t3ctl.py` or install it on PATH as `t3ctl`.
Environment: `--env desk` (default, 127.0.0.1:3773) or `--env macdev`
(127.0.0.1:38373), or `--url`; token from `$T3CTL_TOKEN` or
`~/.t3/t3ctl/<env>.token`.

| Job | Command |
|---|---|
| Full state of projects and threads | `t3ctl snapshot` (`--json` for detail) |
| Read one thread's tail | `t3ctl thread <threadId> --turns 5` (`--json` for approvals detail) |
| Create a chip thread | `t3ctl create --project <p> --title "<imperative>" --model <instance:model>` (`--branch`, `--worktree` when needed) |
| Deliver a brief, start a turn | `t3ctl prompt <threadId> "<brief>"` |
| Nudge or message a chip | `t3ctl append <threadId> "<message>"` |
| Stop a running turn | `t3ctl interrupt <threadId>` then `t3ctl stop <threadId>` if needed |
| Answer an approval or input request | `t3ctl respond <threadId> <requestId> <decision>` |
| Link a PR to its thread | `t3ctl pr-link <threadId> <pr-url>` |
| Archive a finished chip | `t3ctl archive <threadId> --yes` (owner consent only) |
| Escape hatch | `t3ctl raw '<envelope json>'` |

There is no thread-to-thread send in t3ctl: chips report by ending turns
with a STATUS, QUESTION, or BLOCKED line that the manager reads at tick time.

## Guides map

- [guides/01-start.md](guides/01-start.md): state folder, ledger, stock-take,
  manager thread id, CASE and KIPP offers, tick verification.
- [guides/02-spawn-and-track-chips.md](guides/02-spawn-and-track-chips.md):
  scoping, duplicate check, brief, create, deliver, PR watch, worktrees.
- [guides/03-ten-minute-tick.md](guides/03-ten-minute-tick.md): the TICK
  handler: snapshot, per-thread progress, nudge, stop, ledger line.
- [guides/04-ci-watch.md](guides/04-ci-watch.md): tick-time CI states with
  `gh`, RED routing, GREEN reminders.
- [guides/05-case-and-decisions.md](guides/05-case-and-decisions.md): the
  Jev CASE lane, the DECISION REQUEST shape, owner gates.
- [guides/06-kipp-feature-desk.md](guides/06-kipp-feature-desk.md): feature
  intake as a thread brief or manager mode, cards, routing.
- [guides/07-close-out.md](guides/07-close-out.md): consolidation, tick
  shutdown, consented archives, handoff, final report.

## References map

- [references/templates/chip-brief.md](references/templates/chip-brief.md):
  every chip prompt.
- [references/templates/ledger.md](references/templates/ledger.md): a new
  effort's ledger.
- [references/templates/manager-handoff.md](references/templates/manager-handoff.md):
  restart and stop restoration.
- [references/templates/owner-profile.md](references/templates/owner-profile.md):
  environment, model, cadence, allowed sends, approvals.
- [references/templates/feature-card.md](references/templates/feature-card.md)
  and [references/templates/feature-index.md](references/templates/feature-index.md):
  KIPP intake records.
- [references/templates/tick-prompt.md](references/templates/tick-prompt.md):
  the exact TICK message text the timer posts.

## Not ported from the source discipline

Named plainly, with the replacement, so nothing is silently invented:

- **One-minute CI poller (`Monitor` + `ci-poll.sh`)**: no t3ctl equivalent.
  CI is checked at tick time with `gh` (guide 04).
- **Realtime delta streaming (websocket)**: exists in the T3 API but not in
  t3ctl. Replaced by tick-time reads (`t3ctl snapshot`, `t3ctl thread`).
- **`spawn_task` offer-then-owner-click**: t3ctl creates the thread directly.
  OFFERED here means created but not yet briefed; RUNNING once the brief is
  delivered with `t3ctl prompt`.
- **Automatic archive consent**: there is none. Archiving always needs the
  owner's explicit yes (guide 07).
- **Lifecycle beacon heartbeat**: no T3 equivalent. The thread read is the
  only progress source.
- **Merging green PRs**: the source TARS merged when task-authorized.
  TARS-T3 never merges or deploys; it reminds the owner (guide 04).

## Related skills

- `pest-controller-suit` (wasp-nest-core): the roster. Resolve it through
  the host skill resolver or the installed-plugin registry and use it to
  name the Drone each chip should arm itself with. Missing Core blocks
  routing, not management.
- The upstream `tars-stinger` in the data-and-ai-tools pack: the source
  discipline this port rebinds. Read it when a mechanism question predates
  T3; its Desktop tool names do not apply here.
