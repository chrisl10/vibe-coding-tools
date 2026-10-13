# 01. Section map per tier

Which sections the brief contains, in order, and where each one's content comes from. The tier in `intake.json` decides; the renderer never adds a dimension the tier did not run.

## Tier to dimensions (contract section 1)

| Tier | Dimension sections, in order |
| --- | --- |
| `foundation` | Foundation |
| `vibe` | Foundation, Bloat |
| `basic` | Foundation, Bloat, Security |
| `full` | Foundation, Bloat, Security, Quality |
| `mario` | Foundation, Bloat, Security, Quality, Remediation roadmap |

## Page order

| # | Section | Built from | Field Guide element |
| --- | --- | --- | --- |
| 1 | Cover | `intake.json` repo, tier, requested_by, started_at, tools, stacks | Grey panel, "01 A LEGION CODE INC. CODE AUDIT" eyebrow, amber bar, heavy headline, meta strip (By, Tier, Repo), logo |
| 2 | Contents | tier dimensions plus each verdict | "00 CONTENTS" page and color key |
| 3 | The whole audit in one paragraph | each dimension's `metrics.summary`, in tier order, then the same as numbered sentences | "Start here" page, "five sentences" list |
| 4 | Verdict | `rollup_verdict` of dimension verdicts; scorecard table; all-findings severity chart | Big verdict word, measures-style table |
| 5..n | One part per dimension | see below | Heavy black top rule, "N · tool" eyebrow |
| n+1 | Fix these first | top 10 non-info findings across the run | Numbered list |
| n+2 | Coverage and caps | every `coverage` block, every cap, data checks, merges | "Limits, said out loud" (grey rule) |
| n+3 | Method and evidence index | fixed method text, `evidence-index.md`, `raw/` listing | "The end" (green rule) |
| foot | Running footer | `brand.json` footer template | Mono footer on every printed page |

## Inside a dimension part

1. Eyebrow `N · <tool names from measure sources>`, h2, the plain question this dimension answers.
2. Dimension verdict pill and the scope line (files, lines, excluded paths).
3. REMEMBER callout with `metrics.summary`: the one takeaway.
4. One amber "Tool limit, handled." box per `coverage.caps` entry.
5. Cards: the first two measures and a findings count.
6. Measures table (Measure, Result, Band, Threshold, Source).
7. "Measures, to scale" bar chart when two or more measures use `%`; each row draws its own threshold ticks.
8. Findings by severity bar chart.
9. Findings table: ID, Severity pill, Location, Finding (with confidence), Fix, Effort.
10. Spot checks table: ID, confidence, `verified_by`.
11. "Where the real savings are": the top five actionable findings with their fixes.
12. Finding details: evidence, why it matters, standards, sources; open for critical, high, and medium.
13. `notes.md`: "Not confirmed" as a box, the rest collapsed.

A dimension without `metrics.json`, or with `verdict: not-run`, renders as a "Not run" box with the reason (the folder is missing, the file is missing plus the first line of `notes.md`, or the Drone's own summary), followed by any findings it did write.

## Remediation part (mario only)

Lease-style timeline Now, Next, Later from `plan.json.waves`, a REMEMBER line for the first Now item, the work package table, the `library/` consent state, then `roadmap.md` rendered as written. Missing both files renders "Not run". Schema owner: [plan-schema.md](../../remediation-planning-stinger/references/plan-schema.md).

## Sources

- [../references/research/raw/design--whipt-bloat-audit-html.md]
- [../references/research/raw/design--legion-field-guide-pdf.md]
