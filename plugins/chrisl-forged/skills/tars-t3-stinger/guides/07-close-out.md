# 07. Close out

1. **Reconcile.** Match each chip thread, PR, and proof against current
   observed state (`t3ctl snapshot`, `gh pr view`). Mark local-only,
   queued, unproven and handed-off work honestly: a plan, an offer, or an
   unbriefed thread is not shipment.

2. **Stop the tick expectation.** The owner disables the external timer
   (the manager cannot stop it from inside the thread), or the ledger
   records that ticks ended at close-out. Confirm in one line which
   happened; a timer still armed against a stopped manager is a gap to
   report, not to hide.

3. **Archive finished chips only with the owner's consent**, one line per
   chip, recommendation first, then `t3ctl archive <threadId> --yes`. Never
   archive a thread the manager did not create without an explicit yes.
   WITHDRAWN and STOPPED threads are archived or left in place exactly as
   the owner answers.

4. **Save the handoff.** Fill
   [references/templates/manager-handoff.md](../references/templates/manager-handoff.md)
   into the ledger folder before stopping: manager thread id and
   environment, tick timer location, every thread's final state, owner
   decision sources, Jev CASE rulings verbatim, cards and numbering, owned
   worktrees and branches, pending questions.

5. **Final report** per the global report rules, and as short as the work:
   Status (DONE, or PARTIAL, BLOCKED, or STOPPED with the wall named),
   Delivered (paths), Verified (checks and actual results, quoted),
   Decisions (Jev picks and judgment calls: question, pick, one line why),
   Not done (with the wall), Questions for Chris. No automatic commit,
   push, promotion, or deployment follows close-out.
