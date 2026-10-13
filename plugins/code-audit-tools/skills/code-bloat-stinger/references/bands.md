# Bands, contract mapping, severity, and verdict

## Source bands

| Measure | Healthy | Bloated | Owner |
| --- | --- | --- | --- |
| Duplication, both jscpd figures (standard and both copies), at 50 and 100 tokens | under 5% | over 10% | Mario |
| Truly dead code, after the spot-check, as % of core code lines | under 3% | over 8% | heuristic |
| Code in files over 1,000 lines, as % of core code lines | under 15% | over 30% | heuristic |
| Largest single function | under 200 lines | over 1,000 lines | heuristic; 1,000 is lizard's default function-length warning [research/raw/lizard--readme-and-csv-test.md] |

Source: [research/raw/gold--whipt-bloat-audit-method.md]. In the report, always footnote that the duplication bands are Mario's and the other two are heuristics.

## Mapping onto the contract scale

The contract scale is `healthy`, `moderate`, `at-risk`, `critical` (plus `not-run`). The source bands have three levels. This skill maps them as follows (a design decision, not a sourced fact):

| Source level | Contract band | Rule |
| --- | --- | --- |
| Healthy | `healthy` | below the healthy line |
| Between the lines | `moderate` | from the healthy line up to the bloated line |
| Bloated | `at-risk` | above the bloated line, up to twice it |
| Far past bloated | `critical` | more than twice the bloated line |

Concrete cut-offs:

| Measure | healthy | moderate | at-risk | critical |
| --- | --- | --- | --- | --- |
| Duplication (each figure) | < 5% | 5% to 10% | > 10% to 20% | > 20% |
| Truly dead code | < 3% | 3% to 8% | > 8% to 16% | > 16% |
| Code in files over 1,000 lines | < 15% | 15% to 30% | > 30% to 60% | > 60% |
| Largest single function | < 200 lines | 200 to 1,000 | > 1,000 to 2,000 | > 2,000 |

Why "bloated" maps to `at-risk` and not `critical`: in the contract, `critical` is reserved for exploitable or data-loss level problems, and two `critical` measures already force the dimension to `at-risk`. Bloat slows a team down; it rarely breaks production by itself. Reserving `critical` for extreme outliers keeps the overall verdict honest.

WHIPT check: 3.58% healthy, 7.32% moderate, 1.18% and 2.41% healthy, about 1.5% dead healthy, 45.7% in big files at-risk (the report's "Bloated"), largest function 5,527 lines critical (the report's "Bloated"). One measure in `critical` and no `high` findings: contract verdict moderate. The hand-run verdict was Moderate. The mapping reproduces it.

## Severity for bloat findings

Bloat findings top out at `medium` unless a stricter rule applies. The contract's own example of `medium` is "a 5,000-line function".

| Finding | Severity | Effort |
| --- | --- | --- |
| Function over 1,000 lines, or a factory closure over 5,000 lines | `medium` | `L` |
| File over 5,000 lines that mixes several unrelated concerns | `medium` | `L` |
| A family of copied modules (an area over 10% both copies, and over 1,000 duplicated lines) | `medium` | `M` or `L` |
| A forked copy of another package's source | `medium` | `M` |
| Type or schema copies of a shared package | `low` | `S` or `M` |
| Short repeated snippets across one file (big drop from 50 to 100 tokens) | `low` | `M` |
| Confirmed dead files or exports (spot-checked) | `low` | `S` |
| Unused dependency confirmed by reading the code | `low` | `S` |
| Unlisted dependency (imported but not in package.json) | `low`, or `medium` when it only works through hoisting in a production build | `S` |
| Unresolved import that is not a native addon or generated file | `low` | `S` |
| Repo-wide context (tool versions, caps lifted) | `info` | `S` |

Confidence:

- `confirmed`: you read the code and traced it (for example: searched every reference, read the importer, ran the build entry list).
- `likely`: tool output plus a manual read of the flagged spot.
- `possible`: tool output only. Never above `medium` (contract rule 3). Prefer to leave unsampled knip items out of `findings.jsonl` and report them as counts in `metrics.json` and `notes.md`.

## Dimension verdict

Apply the contract's section 8 default, which this skill does not tighten:

- `critical`: any `critical` finding at `confirmed` or `likely`
- `at-risk`: any `high` finding, or two or more measures in the `critical` band
- `moderate`: any `medium` finding, or any measure in `at-risk` or `moderate`
- `healthy`: none of the above

`scripts/validate_outputs.py` errors if `metrics.json.verdict` is milder than this rule.
