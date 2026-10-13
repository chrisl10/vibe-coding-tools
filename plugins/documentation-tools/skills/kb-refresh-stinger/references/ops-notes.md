# Ops notes: pause, resume, provider pacing

Field notes from the reference run. Load before stopping or amending anything.

## Pausing

- TaskStop the workflow run. It stops cleanly; the journal keeps finished work.
- Before stopping to switch networks or models, tell the owner the resume cost: finished agent work is cached, in-flight agent work is re-paid.

## Resuming by amend, not replay

1. Edit the persisted script file first. Prepend a unique `// resume marker: <why>` comment so the bytes change; an amend with identical bytes is refused.
2. Never touch any `ask()` text. Cache matches agents by name plus byte-identical ask text; a one-word change to a brief re-pays every agent holding that brief.
3. Amend with `path` (the script file), not a fresh inline `script`, and not a bare settings-only call unless settings are the only change.
4. A settings-only amend mints a NEW run id that imports the old journal as cache. Record the new id immediately; the old one is dead.

## The replay trap

If `ResumeWorkflowRun` fails with a nondeterministic replay error (the shape seen in the reference run: `Replay hit at report#N@K but inputHash differs`), the cause was interleaved `report()` calls inside concurrent callbacks. Fix: strip or determinize those `report()` calls in the script, then amend with `path`. Resume via replay will keep failing; do not retry it.

## Duplicate runs

After any run settings change from the GUI, list the project's runs before doing anything else. A settings change can mint a successor while the original still lives, and two fleets writing the same files produce "file modified since read" failures and subagent escalations. Keep the run with fresh progress; stop the rest.

## Provider pacing and caps

- The runtime paces concurrency to what the provider accepts. Run health like `concurrency=4/12 (rate_limited)` means the provider, not the script, is the bottleneck. Log it; do not widen.
- Cap code 1308 is a rolling usage window (the provider quotes raw reset times in UTC+8; subtract 8 hours for UTC). Code 1005 is plan balance exhausted. Neither is fixed by retrying: schedule a resume after the reset, or get the owner's decision to switch accounts or models. Model and provider choices belong to the owner.
- While capped, stop, preserve, and report. Do not fill the wait with unrequested work.

## Shipping while the fleet runs

Branch and PR work happens in a throwaway `git worktree add --detach` worktree, never in a worktree a writer can touch. Commits on the shared docs branch use explicit file paths only. `git worktree remove` the throwaway when the wave ships.
