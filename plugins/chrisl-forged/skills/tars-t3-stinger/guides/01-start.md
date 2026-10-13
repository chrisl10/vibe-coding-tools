# 01. Start: arm TARS-T3 before any work chip

1. **Verify the control surface.** Run `t3ctl snapshot` with the effort's
   environment (`--env desk` or `--env macdev`, or `--url`). It must print
   the project and thread list. Common failures, each a stop: no token (mint
   with `t3 auth session issue --ttl 30d --label t3ctl --token-only` into
   `~/.t3/t3ctl/<env>.token` on a machine with the t3 CLI), server
   unreachable (the T3 app is not running, or the wrong environment), skill
   not loaded (this guide's parent skill). Report exactly which one and stop.

2. **Load the owner profile.** Fill or restore
   [references/templates/owner-profile.md](../references/templates/owner-profile.md)
   inside the effort folder from the owner's current instructions: default
   environment (desk or macdev), default chip model, contact cadence, allowed
   sends, action-specific approvals. Unset fields grant no authority.

3. **Make the state folder** `.tars-t3/<effort-slug>/` inside the target
   project, in an already ignored location (editing `.git/info/exclude`
   needs authorization). Copy
   [references/templates/ledger.md](../references/templates/ledger.md) to
   `ledger.md`, create an empty `watch.txt`, and write a `manager-thread.md`
   note recording: manager thread id, environment, model, start UTC.

4. **Record the manager thread id in the ledger.** This session is a T3
   thread. Find it in `t3ctl snapshot` output by title (or take the id from
   the T3 GUI) and record it. The tick timer needs this id.

5. **Stock-take.** Read `t3ctl snapshot --json`. List live threads per
   project. Any thread already doing work the owner asked for gets managed,
   not duplicated, after the owner says yes in one line. Never stop, re-brief
   or archive a thread TARS-T3 did not create without that yes.

6. **Offer CASE and KIPP to the owner**, one line each, recommendation
   first:
   - CASE is the Jev decision lane ([05-case-and-decisions.md](05-case-and-decisions.md)).
     There is no session to start; noting the lane is enough.
   - KIPP is a thread brief ([06-kipp-feature-desk.md](06-kipp-feature-desk.md)).
     The owner can start a KIPP thread in T3, or ask the manager to run
     intake as a mode. Record the owner's choice in the ledger.

7. **Verify the tick can reach this thread.** The external timer (cron,
   launchd, or an agent loop the owner controls) posts the exact text from
   [references/templates/tick-prompt.md](../references/templates/tick-prompt.md)
   into the manager thread as a normal user message, roughly every 10
   minutes, with `t3ctl prompt <managerThreadId> "<tick text>"`. The manager
   cannot arm or stop this timer from inside the thread. Verify by receiving
   one test TICK: ask the owner to fire one manually if the timer is not yet
   armed. Record the timer's location and the verified time in the ledger.
   If no timer can be armed, say so plainly: the manager degrades to
   owner-prompted ticks (the owner pastes the TICK text on demand); it never
   pretends a timer exists.

8. Then, and only then, spawn work chips
   ([02-spawn-and-track-chips.md](02-spawn-and-track-chips.md)).
