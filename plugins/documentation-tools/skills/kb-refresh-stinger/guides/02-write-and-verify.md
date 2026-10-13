# Guide 02: Write and verify

The fleet stage. Writers produce grounded docs; verifiers try to break every citation; fixers apply what survived. Read-only against code, always.

## Author the shard scripts

1. Start from `swarm-audit-stinger`'s workflow template (`swarm-audit-stinger/references/templates/swarm-audit-workflow.js`). Keep `withRetry`, the coverage ledger, and the checkpoints. Replace the lenses and report specs with the per-unit chain below.
2. Shard the unit list across parallel workflows when one workflow's concurrency cap would drag the wall clock. Each shard gets its own script file, its own run, and a disjoint unit slice. Reference implementation of one shard: `references/research/raw/kb-refresh--script--fleet-shard-D-2026-10-04.ts`.
3. Width: start at the runtime cap (`min(16, CPUs - 2)` per swarm-audit's rule, and never more than 100 in-flight across every workflow). The provider may pace below that; expect run health like `concurrency=9/12 (rate_limited)`. Log the pacing; never respond to throttling by widening.
4. Every agent ask embeds the grounding law from `references/grounding-law.md` verbatim, plus: the pinned commit, the unit's file list, the doc format (`knowledge-stinger`), the write paths, and the sus log path.

## The per-unit chain

```
write -> adversarial verify (round 1..3) -> fix -> gates (guide 03)
```

- **Writer.** Produces or rewrites the unit's docs to `knowledge-stinger` format, grounding every behavioral claim in a fresh re-open of the cited `path:line` on the pinned commit. Appends to its sus log anything suspicious it saw in code while documenting.
- **Adversarial verifier.** A different agent from the writer. Its job is to kill claims, not to like the doc: independently re-open every citation on the pinned commit and mark each pass, fail, or unverifiable. Check the doc set against the unit's file list for completeness. Round budget: up to 3 rounds, then ship with residuals labeled.
- **Fixer.** Applies verified corrections only. A fix must trace to a verifier finding; a fixer never "improves" claims on its own authority, because that reopens the grounding debt.
- **Sus logging.** Writer, verifier, and fixer all append to the unit's sus log as they go, per `references/sus-log-protocol.md`. Suspecting is continuous, not a final step.

## Observing the run

- Check-in every 10 minutes from launch: read actual output (journal events, files appearing, transcript growth), never claimed status. Judge stalled agents against the role thresholds; stop and respawn with a narrower brief.
- Keep the coverage ledger current: every unit has a writer, a verifier, and a gate record, or a re-dispatch. A null return is a re-dispatch, never a drop.
- Anything still missing at the end prints under "unreviewed" with its resume command.

## Pausing and resuming

See `references/ops-notes.md` before stopping anything. The short version: amend the persisted script with a byte-changing comment marker and resume via amend (cache matches by agent name plus byte-identical ask text), never via raw journal replay if the script interleaved `report()` calls inside concurrent callbacks; and after any settings change, list runs and kill duplicates before two fleets write the same files.
