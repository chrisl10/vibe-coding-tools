# TARS-T3 manager handoff: <effort>

Saved: <UTC> | Current task: <ask> | Manager thread: <threadId> on env
<desk|macdev>

| Item | Value |
|---|---|
| State folder and ledger | |
| Owner profile | |
| Tick timer (where it runs, verification time) | |
| T3 token location for this env | `~/.t3/t3ctl/<env>.token` (name only, never the value) |

## Threads and state

<threadId, title, state, PR, last real progress, owned worktrees and
branches. Old worktrees stay read-only unless specifically authorized.>

## Decisions and gates

<Exact owner decisions and their sources and times; Jev CASE rulings
verbatim with conditions; unresolved gates and approvals still required.>

## Cards and Feature Desk

<Card paths, numbering, priorities, overlaps, KIPP thread ids if any.>

## Restoration steps

<Verify t3ctl snapshot; re-record the manager thread id; re-verify the
tick timer can reach the thread; resume the ledger before spawning
anything. Archive and merge decisions never carry over without their
recorded source.>
