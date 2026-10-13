# Distilled: the kb-refresh process, from the WHIPT run

Every claim below cites a file in `raw/` (see `MANIFEST.md` for provenance). Where a number is measured, the raw file is the measurement. Harness format facts are out of scope here; they live in queen-wasp-stinger's research.

## The assignment that shaped the process

The WHIPT handoff defined a documentation refresh as: inventory the existing knowledge docs, split them into units, run writer agents per unit, then up to 3 adversarial verification rounds with fixes per unit, then a security gate with fix and recheck, then a quality gate with fix and recheck, then ship one ready (never draft) PR per unit against `staging`, and send the merge owner the PR numbers in one batched message [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].

The same handoff fixed the constraints this stinger treats as law:

- Every behavioral claim in a doc cites `path:line` on the pinned ref, and the writer re-opens the file before citing. Unverifiable claims are marked `(unverified)` [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].
- Writes land only inside `library/knowledge/private/`; a frozen read-only set (`contracts/**`, ADRs, architecture history, coverage ledgers) is never edited [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].
- Secret values, tokens, keys, passwords, private hostnames, and customer data never enter docs or PR bodies; environment variable names are fine [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].
- No em dashes or en dashes in new prose [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].
- Drift between docs and PRDs/IRDs is reported to the merge owner, never self-fixed; no new GitHub issues [raw/kb-refresh--directive--whipt-handoff-2026-10-03.md].

## Measured outcome of the reference run

- 320 docs touched: 173 written, 136 updated, 11 kept; 30 domains (4 new); 43 units [raw/kb-refresh--evidence--run-statistics-2026-10-04.md].
- 434 gate passes across the pipeline; 7,507,502,927 tokens total; about 28 working hours inside a roughly 40 hour wall clock window (the rest was provider caps and waits) [raw/kb-refresh--evidence--run-statistics-2026-10-04.md].
- 43 PRs shipped, one per unit, all ready not draft, all against `staging`, gate evidence in every PR body [raw/kb-refresh--evidence--merge-brief-2026-10-04.md].
- The read-only fleet surfaced 88 drift and suspect notes (doc claims disagreeing with PRDs/IRDs) without changing a PRD or opening an issue [raw/kb-refresh--evidence--sus-list-whipt-2026-10-04.md].

## What the run taught about mechanics

- **Unit split.** Units are domain-scoped file sets with no overlap, so every unit can be written, verified, gated, and shipped independently and in any order. The map of unit to files is the inventory's deliverable [raw/kb-refresh--evidence--unit-split-2026-10-04.json].
- **Fleet shape.** Each shard workflow runs the same chain per unit: write, adversarial verify (re-open every citation independently), fix, repeat to the round budget, then gates. The surviving shard script is the runnable reference [raw/kb-refresh--script--fleet-shard-D-2026-10-04.ts]. Fleet discipline (check-in cadence, kill and respawn, coverage ledger, concurrency caps) comes from swarm-audit-stinger; this run kept its 10 minute cadence and coverage ledger rules.
- **Ship isolation.** The first ship script checked out branches in the writer worktree and was replaced: while other units were still writing, that collides. The working pattern ships each unit from a throwaway detached worktree: branch from the base ref, check out just that unit's files from the docs branch, commit with explicit paths only, run the repo's validation script, push, open the ready PR with gate results in the body [raw/kb-refresh--script--ship-unit-2026-10-04.sh, raw/kb-refresh--script--ship-shard-2026-10-04.sh].
- **Resume cost.** Pauses (network switches, provider caps) are survivable, but resuming needs care: amend the persisted script file with a byte-changing comment marker so cached work matches by name plus identical agent ask text; interleaved `report()` calls inside concurrent callbacks made one journal replay nondeterministic, and stripping them fixed every later resume [raw/kb-refresh--script--fleet-shard-D-2026-10-04.ts, run operations, see `../ops-notes.md`].
- **Gate evidence travels with the PR.** Each PR body embeds the unit's gate summary and repo health line, so the merge owner never has to trust the pipeline's word [raw/kb-refresh--evidence--gate-summary-example-2026-10-04.md, raw/kb-refresh--evidence--merge-brief-2026-10-04.md].

## Research gaps

- Concurrency pacing numbers (what fraction of configured width a provider accepts before throttling) were observed live but not archived; treat pacing as runtime behavior to log, not a constant to plan against.
- Thesus-list severities in the reference run were drift-shaped (docs vs PRD/IRD). Code quality, security, and functionality suspects were seen anecdotally but not systematically tallied, which is why the sus log protocol in this stinger is stricter than what the run itself kept.
