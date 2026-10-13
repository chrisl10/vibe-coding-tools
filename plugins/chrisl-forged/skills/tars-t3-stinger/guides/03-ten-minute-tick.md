# 03. The ten-minute tick

Fired by the external timer: a TICK user message arrives in the manager
thread with the exact text from
[references/templates/tick-prompt.md](../references/templates/tick-prompt.md).
Timer jitter exists: measure progress by elapsed real work since the
ledger's last recorded progress, not by exact 10-minute spacing. Target:
under two minutes of manager time, then end the turn and go idle.

1. **Snapshot.** `t3ctl snapshot`. Note new threads, session state changes,
   and PR count changes since the last tick.

2. **Check every managed thread** in the ledger's Sessions table with state
   `RUNNING` or `BLOCKED`:
   - Read the tail with `t3ctl thread <threadId> --turns 5`. Progress means
     new messages with real work since the ledger's "Last real progress"
     entry: files changed, commands run, commits, PR events, or a question
     asked. A chip's own "working on it" text is not progress.
   - **Waiting on an approval or input request is not a stall.** Read
     `t3ctl thread <threadId> --json` for the pending request; answer it
     within the chip's delegated scope with
     `t3ctl respond <threadId> <requestId> <decision>`, or route it to the
     owner in one line when it touches a Hard stop gate. Never change a
     thread's mode or settings to unblock it.
   - **No progress for one tick:** nudge once with
     `t3ctl append <threadId> "<what you see, the one next step you expect,
     reply with a blocker if there is one>"`. One batched message per thread
     per tick.
   - **No progress for two ticks:** stop the turn: `t3ctl interrupt
     <threadId>`, then `t3ctl stop <threadId>` if the session is still
     running. Then decide: re-brief the same thread with a narrower task
     (`t3ctl prompt` with the changed brief), or spawn a fresh chip with a
     changed brief per [02-spawn-and-track-chips.md](02-spawn-and-track-chips.md).
     Archive the old thread only with the owner's consent
     ([07-close-out.md](07-close-out.md)). Record which path and why.
   - Update "Last real progress (UTC)" in the ledger.

3. **Check OFFERED threads.** A created-but-unbriefed thread is waiting on
   the manager, not stalled: deliver the brief or withdraw it (guide 02,
   step 8). Remind the owner in one line about any offer left undelivered
   because a gate is open.

4. **Run the CI watch** now, for every `pr` line in `watch.txt`:
   [04-ci-watch.md](04-ci-watch.md).

5. **Append one ledger line**: threads running, blocked, done; CI state;
   every ruling taken this tick.

6. **Report to the owner only if something changed** that they would act
   on, one line per item, recommended answer first. Otherwise stay silent
   and end the turn.
