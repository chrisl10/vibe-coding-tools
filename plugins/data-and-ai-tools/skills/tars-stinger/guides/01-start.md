# 01. Start: arm TARS before any work chip

Derived from `distilled-tars.md` D1, D3, D4, D5.

1. **Load the tools** in one call: `ToolSearch` with `select:mcp__ccd_session__spawn_task,mcp__ccd_session__dismiss_task,mcp__ccd_session_mgmt__list_sessions,mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__list_events,mcp__ccd_session_mgmt__stop_session,mcp__ccd_session_mgmt__archive_session,mcp__ccd_pr__get_status,SendMessage,ReadNotifications,CronCreate,CronList,CronDelete,Monitor,TaskStop`. Skip any already loaded. If `spawn_task` or `list_events` is missing, stop: this is not a Claude Code desktop session, and TARS cannot manage here. Say so in one line.
2. **Load the manager profile and roles.** Read `07-case-and-kipp.md`; fill or restore `references/templates/owner-profile.md` from current owner instructions. Verify the chosen model and effort, repo/ref, domain map, delegation and contact cadence. Do not change session settings.
3. **Make the state folder** (`references/REFERENCE.md`, State layout), copy `references/templates/ledger.md` to `ledger.md`, and create an empty `watch.txt`.
4. **Take stock.** `list_sessions` (and `linked: true`). Record any session already doing work the owner asked for; manage it instead of spawning a duplicate, after the owner says yes in one line. Never stop or re-brief a session TARS did not spawn without that yes.
5. **Offer CASE first, then KIPP** from `references/templates/case-brief.md` and `kipp-brief.md`. Restore prior transcript tails and handoff read-only. Record each task ID and link the actual desktop session when it starts. Use the owner's accessible interface; an offered chip is not a running session.
6. **Arm the 10-minute tick**: `CronCreate` with cron `*/10 * * * *` and the prompt from `references/templates/tick-prompt.md`. Record the id. Tell the owner once that recurring jobs expire after 7 days and live only in this session.
7. **Arm the CI poller** as a `Monitor`: command `bash <skill>/scripts/ci-poll.sh <state-folder>` with `IGNORE_CHECKS` and `REQUIRED_CHECK` set for the repo, `timeout_ms` 1800000, description "TARS CI poll (1 min)". Record it. An empty `watch.txt` is fine; the poller re-reads it every loop.
8. **Verify once by hand**: confirm the health URL or required check name you will trust actually exists (one `curl` or `gh pr checks` on a recent PR). Record the result.
9. Then, and only then, spawn work chips (`02-spawn-and-track-chips.md`).

If CASE has not started within ten minutes, apply the scoped fallback and waiting rules in `07-case-and-kipp.md`. Never substitute a background adviser for the separate Desktop manager team without recording that limitation.
