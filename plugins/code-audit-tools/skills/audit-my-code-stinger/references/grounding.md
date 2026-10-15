# Grounding for the Audit My Code orchestrator

This orchestrator has no external domain of its own: it sequences Drones whose domains are researched in their own Stingers. Its rules come from three places.

| Rule | Source |
| --- | --- |
| Tier definitions, read-only discipline, bands for duplication, dead code, and file size, the "lift the jscpd large-file limit" and "spot-check knip" habits | A hand-run reference bloat audit (2026-09-30), encoded in `code-bloat-stinger` and its research archive |
| Drones cannot spawn Drones, so the main session dispatches every wave; concurrent dispatch in one turn on Claude Code; sequential fallback on Cursor and Codex; Cowork prefers `commands/` | `queen-wasp-stinger/references/research/distilled-research-articles.md` and `guides/harness-support-matrix.md` (harness-format research, shared across the Nest) |
| Security before quality; reports per dimension; Library Schema v2 for Mario-tier documents | `pest-controller-suit`, `security-stinger`, `quality-stinger`, `library-stinger`, `knowledge-stinger` in the Wasp Nest core |

Domain research for each dimension lives in the paired Stinger's own `references/research/raw/` and distilled article.
