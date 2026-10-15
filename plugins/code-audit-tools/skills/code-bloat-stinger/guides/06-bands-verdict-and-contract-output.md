# 06. Bands, verdict, and writing the contract outputs

Goal: band every measure, set the dimension verdict, write a verdict paragraph that answers the user's real question, and write `metrics.json`, `findings.jsonl`, and `notes.md` exactly as the contract says.

Loads: [../references/bands.md](../references/bands.md), [../references/output-templates.md](../references/output-templates.md), `../scripts/validate_outputs.py`, and the contract (`audit-my-code-stinger/references/audit-contract.md`).

## 1. Band every measure

Use [../references/bands.md](../references/bands.md). Duplication: under 5% healthy, over 10% bloated (Mario's). Truly dead: under 3% healthy, over 8% bloated (heuristic). Code in files over 1,000 lines: under 15% healthy, over 30% bloated (heuristic). Map healthy, between, bloated, and twice-bloated onto `healthy`, `moderate`, `at-risk`, `critical`. The largest function is banded too: under 200 lines healthy, over 1,000 bloated (heuristic). A step that did not run gets `not-run`. The contract has no `n/a` band, so pure counts are not measures; report them in `notes.md`.

## 2. Set the verdict

Apply the contract's section 8 rule as written in [../references/bands.md](../references/bands.md). Do not soften it. `validate_outputs.py` fails a verdict milder than the rule.

## 3. Write the verdict paragraph

This paragraph is the `summary` in `metrics.json` (one or two sentences) and the opening of `notes.md` (a full paragraph). It answers the question the user asked, in their words. For a vibe-coded app the question is usually "is it bloated because it was vibe coded?"

Rules:

1. Answer first: "Mostly no", "Yes", "Partly". Then the reason in plain words.
2. Separate the three kinds of bloat, because they have different causes and fixes: pasted code (duplication), dead code (unused files, exports, dependencies), and shape (giant files, giant functions, closures).
3. Back every clause with a number from the measures.
4. Name the vibe-coding cost only where the numbers show it. The pattern in WHIPT: little paste and little dead code, but "agents keep adding to whatever giant file they are already in", shown by the big-file share, the closure factories, and the largest function [../references/research/raw/gold--whipt-bloat-audit-method.md]. That pattern matches research that finds AI-involved code more verbose and layered, with less consolidation, while the duplication evidence is mixed [../references/research/raw/research--arxiv-2603-27130-ai-vs-human-duplication.md] [../references/research/raw/research--gitclear-2026-maintainability-gap.md (source-repository research, not shipped)].
5. Do not claim a cause the repo cannot show. You cannot tell from the code who wrote it. Say "the shape is what agent-driven growth typically produces", not "the agent did this". Humans introduce most clone lineages in mixed projects [../references/research/raw/research--msr-2026-clone-genealogies.md (source-repository research, not shipped)].
6. When duplication is low, add the limit in one clause: token-based detection does not catch the same logic written twice in different words [../references/research/raw/research--msr-2026-more-code-less-reuse.md (source-repository research, not shipped)].
7. No jargon the reader has to look up. Say "copy-pasted", "unused", "one function that is 5,527 lines long", not "Type-2 clones" or "low cohesion".

Shape to follow (WHIPT, paraphrased):

> Mostly no, it is not bloated because it was vibe coded. Most of the million lines are real, used, and not copy-pasted. The vibe-coding cost shows up in the shape: agents keep adding to whatever giant file they are already in. So nearly half the code sits in files over 1,000 lines, four services are single closures of 5K to 19K lines, and one function is 5,527 lines long.

## 4. Write metrics.json

Follow [../references/output-templates.md](../references/output-templates.md) and contract section 6:

- `dimension: "bloat"`, the verdict, the summary.
- Every measure key from the template table, each with `label`, `value`, `unit`, `band`, `threshold` (say whose band), `source` (tool and version).
- `coverage.files_scanned`, `coverage.lines_scanned` (duplication scope), `coverage.skipped` (excluded paths, submodules, languages without a dead-code tool), and `coverage.caps`: every silent limit lifted or hit. At minimum: the jscpd size or line cap and that it was lifted, cloc's uniqueness default, any knip plugin disabled, any dependency install in the copy. An empty `caps` array claims no limit applied; that is almost never true for this dimension.

## 5. Write findings.jsonl

One JSON object per line, ids `BLOAT-DUP-NNN`, `BLOAT-DEAD-NNN`, `BLOAT-SIZE-NNN`, `BLOAT-STRUCT-NNN`. Every finding has evidence you saw (a recount figure and pair ranges, a lizard row, a search with no hits). Paths are repo-relative, never the scratch copy's. Severity per [../references/bands.md](../references/bands.md); `possible` never above `medium`. Titles are one plain sentence. Remediation names the file and the change. Group by cause, not one finding per file.

## 6. Write notes.md

Use the outline in [../references/output-templates.md](../references/output-templates.md): header with tools and "Repo changes: none", verdict and the measure table, duplication, unused code with the spot-check and the estimate, structure with the split plan, next steps ordered by savings, "Not confirmed", coverage and caps, and the raw-versus-code lines footnote.

Next steps are the payoff. Order them by lines saved and risk, and name the concrete move (one shared base for a copy family; import instead of a fork; type copies import from the shared package; delete about N lines of confirmed-dead files; split the largest file in stages behind a context object, starting with its largest function).

## 7. Evidence index, check, clean up

1. For every raw file you cite, list each raw file under an `## Evidence` heading in your own notes file, one line each (`` `path` - what it is``); the orchestrator builds `evidence-index.md` from those sections, so never write `evidence-index.md` yourself.
2. Run `python3 scripts/validate_outputs.py --dir <workspace>/01-bloat`. Fix every ERROR. Read every WARN and either fix it or explain it in `notes.md`.
3. Scan your own prose for em and en dashes; the validator checks findings, the summary, and notes.
4. Confirm the audited repo is unchanged: `git -C <repo> status --porcelain` matches the capture from guide 00.
5. Remove `<workspace>/.scratch/` after every cited artifact is in `raw/`. If you used `git worktree add`, run `git worktree remove` for it. State "the copy was removed afterwards" in `notes.md`.

## Sources

The notes listed below are source-repository research, not shipped.

- ../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)
- ../references/research/raw/research--gitclear-2026-maintainability-gap.md (source-repository research, not shipped)
- ../references/research/raw/research--arxiv-2603-27130-ai-vs-human-duplication.md (source-repository research, not shipped)
- ../references/research/raw/research--msr-2026-more-code-less-reuse.md (source-repository research, not shipped)
- ../references/research/raw/research--msr-2026-clone-genealogies.md (source-repository research, not shipped)
- ../references/research/raw/research--arxiv-2603-28592-ai-technical-debt.md (source-repository research, not shipped)
