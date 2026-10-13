# Tick prompt (exact text)

The external timer posts this text into the manager thread as a normal user
message, roughly every 10 minutes. The manager cannot arm, edit, or stop
this timer from inside the thread; the owner owns it.

```text
TICK. You are TARS-T3. Run the ten-minute tick now per tars-t3-stinger
guide 03: t3ctl snapshot, check each managed thread against the ledger's
last real progress, nudge or stop stalled chips, answer scoped approvals,
run the CI watch (guide 04), append one ledger line, report only changes,
then end the turn. Do no implementation work.
```

Arm it with any scheduler that can run t3ctl with the effort's environment
and token:

```text
t3ctl prompt <managerThreadId> "<the text above>"
```

Verify at start (guide 01) by receiving one test TICK, armed by the owner
or fired manually. If no timer can be armed, the manager runs on
owner-prompted ticks: the owner pastes the text above on demand.
