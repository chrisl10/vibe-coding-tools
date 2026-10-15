# Unit economics

Produces a reviewable economic worksheet with explicit assumptions, contribution and gross margins, break-even, losses, and scenarios. It evaluates supplied prices and costs without choosing a price or changing live billing.

| Load | Purpose |
|---|---|
| [Intake and classify](guides/01-intake-and-classify.md) | Collect units, dates, prices and evidence; distinguish unknowns from zero |
| [Free/trial and abuse costs](guides/03-free-trial-and-abuse-costs.md) | Cohort cost allocation, blocked attempts, credits and conditional break-even |
| [Model and review](guides/02-model-and-review.md) | Run scenarios, reconcile fees/costs and explain the result |
| [Fields and formulas](references/model.md) | Exact contract, limits, break-even statuses and exclusions |
| [Input template](references/templates/input.json) | Explicit fictional scenario to replace with the user's inputs |
| [Worksheet](references/templates/worksheet.md) | Review table, evidence and unresolved assumptions |
| [Worked examples](examples/fictional-scenarios.md) | Baseline, refunds and loss-making high usage |
| [Research distillation](references/research/distilled-unit-economics.md) | Current source evidence and model adaptations |
| [Offline calculator and tests](scripts/README.md) | stdlib CLI, bounds, JSON output and behavioral checks |

Installed dispatch resolves `unit-economics-stinger` from selected software-economics-tools through trusted Core. Source dispatch uses its registered catalog source root. Cross-pack owners are resolved individually; they are not assumed installed.

For O281 read [fair service limits](guides/04-fair-service-limits.md), the [joined worksheet](references/templates/fair-service-limits-worksheet.md), dated mechanism digest and [completed fictional cases](examples/fair-service-limits-cases.md). This joins cost evidence with proposed allowance/recovery and owner fairness decisions; it establishes no accepted policy or functioning control.
