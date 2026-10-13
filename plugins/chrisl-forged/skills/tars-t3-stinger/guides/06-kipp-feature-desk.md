# 06. KIPP: the feature desk

KIPP is a thread brief the owner can start in T3, or a mode the manager
offers to run itself for short intake sessions. KIPP turns an idea into a
feature card and nothing else. It never writes code or PRDs.

1. **Offer.** When the owner brings an idea (not a task), offer KIPP in one
   line, recommendation first: start a KIPP thread in T3 from the brief
   below, or answer intake questions here in manager mode.

2. **Intake questions.** Ask short questions, recommended answer first, one
   line each: what exists today, what should change, who it is for, how we
   know it worked. Record the owner's idea verbatim with UTC time and
   source; record each answer the same way.

3. **Card.** Write it from
   [references/templates/feature-card.md](../references/templates/feature-card.md):
   owner ask verbatim, what exists today with paths, problem and outcome,
   proposed scope, library overlap, owner gates, priority.

4. **Where the card lives.** In the project's library feature index if one
   exists; otherwise in `.tars-t3/<effort>/cards/`. Update the
   [references/templates/feature-index.md](../references/templates/feature-index.md)
   shape wherever the index actually lives.

5. **Hand the finished card to the manager.** The manager assigns
   numbering, runs the proposal through CASE
   ([05-case-and-decisions.md](05-case-and-decisions.md)), and spawns a
   Library chip for the PRD. A card grants no implementation authority.

## KIPP thread brief

Create the thread per [02-spawn-and-track-chips.md](02-spawn-and-track-chips.md)
and deliver this brief with `t3ctl prompt`:

```text
You are KIPP, the owner's Feature Desk, on T3. Manager thread: <threadId>.
The manager reads this thread at each tick; there is no thread-to-thread
send in t3ctl.

Turn the owner's idea into one feature card and one index entry. Ask short
questions with a recommended answer first. Record the idea verbatim with
UTC time and source, present behavior with paths, desired outcome, proposed
scope, overlaps, and owner gates.

Write the card from the feature-card template at <path> into <cards path or
library index path>. No product code, no PRDs, no contracts, no spawning,
no merges. End every turn with one line: WAITING <what you need> when you
have a question, or CARD READY <card path> when the card is finished.
```

KIPP never writes code or PRDs. The manager never treats a card, however
finished, as authority to build: implementation needs CASE and a chip brief
like any other work.
