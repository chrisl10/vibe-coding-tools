# TARS-T3 ledger: <effort name>

Owner: <name>. Manager thread: <threadId> on env <desk|macdev>, model
<instance:model>. Started: <UTC>. State folder: <path>.

## Tick

| What | Detail | Armed (UTC) | Notes |
|---|---|---|---|
| External tick timer | <where it runs: cron, launchd, agent loop> | | verified by test TICK at <UTC>, or "not armed; owner-prompted ticks" |

## Sessions

| Chip title | threadId | Project | Scope | PR | State | Last real progress (UTC) |
|---|---|---|---|---|---|---|

States: OFFERED (created, brief not delivered) to RUNNING, then DONE,
BLOCKED, STOPPED, or WITHDRAWN. Archive only with the owner's yes.

## Log

Append only. One line per event:
`- <UTC> <event>. Decision: <what>. By: <TARS-T3 | Jev (CASE) | owner>.`

## Cards

| Card path | Priority | Numbering | CASE ruling | Library chip threadId | State |
|---|---|---|---|---|---|
