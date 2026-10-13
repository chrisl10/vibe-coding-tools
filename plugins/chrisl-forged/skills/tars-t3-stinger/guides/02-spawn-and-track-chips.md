# 02. Spawn and track chips

1. **Scope the ask.** Write one sentence: the outcome the owner asked for,
   in their words. If it is more than one small PR, draft the split and send
   it to CASE first ([05-case-and-decisions.md](05-case-and-decisions.md));
   do not spawn anything larger.

2. **Check for duplicates.** `t3ctl snapshot`. If a live thread already owns
   the work, manage or message it only within the owner's explicit
   coordination authorization, and record that in the ledger.

3. **Write the brief** from
   [references/templates/chip-brief.md](../references/templates/chip-brief.md).
   Fill the manager thread id, the project, the base branch, the exact scope,
   pre-approved risky actions (only verified owner decisions for this task,
   each quoted with UTC time and source), CASE conditions, and the done
   checks. The brief must stand alone: the chip thread has none of the
   manager's context.

4. **Create the chip thread**:

   ```text
   t3ctl create --project <project> --title "<imperative, 60 chars max>" \
       --model codex_belay:glm-5.3-flash
   ```

   Use the owner profile's default model unless it says otherwise. Pass
   `--branch <name>` or `--worktree <path>` when the task needs its own
   checkout; the global worktree contract applies: a unique task slug plus
   shortid for both branch and path, claim them only after checking for
   sibling sessions, and never touch another session's worktree.

5. **Record** threadId, title, and scope in the ledger's Sessions table
   with state `OFFERED` (created, not yet briefed).

6. **Deliver the brief**: `t3ctl prompt <threadId> "<brief text>"`. The turn
   starts the chip's work. Move the ledger state to `RUNNING`.

7. **When the chip opens a PR**: add `pr <n> <owner/repo>` to `watch.txt`,
   link the PR to the thread with `t3ctl pr-link <threadId> <pr-url>`, and
   record the PR number in the ledger. CI watching starts at the next tick
   ([04-ci-watch.md](04-ci-watch.md)).

8. **Withdraw stale chips.** If the ask changes before the brief is
   delivered, do not deliver it; record state `WITHDRAWN` in the ledger. A
   created thread has no un-create: archiving it needs the owner's consent
   at close-out ([07-close-out.md](07-close-out.md)).

Never give a chip more than one outcome. Never spawn a chip for TARS-T3's
own bookkeeping. Feature requests start in KIPP
([06-kipp-feature-desk.md](06-kipp-feature-desk.md)), not as work chips.
