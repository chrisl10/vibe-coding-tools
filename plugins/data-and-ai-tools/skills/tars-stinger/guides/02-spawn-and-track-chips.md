# 02. Spawn and track chips

Derived from `distilled-tars.md` D1, D2, D6.

1. **Scope the ask.** Write one sentence: the outcome the owner asked for, in their words. If it is more than one small PR, draft the split and send it to CASE (`05-questions-and-decisions.md`) before spawning anything.
2. **Check for duplicates.** `list_sessions`; if a live session already owns the work, manage or message it only within the owner's explicit session-coordination authorization and record that.
3. **Write the brief** from `references/templates/chip-brief.md`. Fill in the TARS session id (`get_session("self")`), the base branch, exact scope, pre-approved risks with source and scope, CASE conditions, and the done checks.
4. **Spawn** with `spawn_task`. Record title, `task_id`, and scope in the ledger's Sessions table with state `OFFERED`.
5. **Link the session** on the next tick: find the new session in `list_sessions` (family first, then exact title). Record its `local_...` id; state `RUNNING`.
6. **When it opens a PR**, add `pr <n> <owner/repo> [required-check]` to `watch.txt` and record the PR number.
7. **Withdraw stale chips** the owner has not started with `dismiss_task` when the ask changes, and say why in the ledger.

Never give a chip more than one outcome. Never spawn a chip for TARS's own bookkeeping.

Feature requests start in KIPP, using `07-case-and-kipp.md`. TARS confirms numbers and routes new PRDs/contracts through CASE before a Library chip. KIPP does not spawn work chips. CASE and KIPP are helper sessions, not implementation chips.
