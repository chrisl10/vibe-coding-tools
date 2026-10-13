# Example: first useful version at three hours per weekday

All effort and money values below are hypothetical supplied inputs, dated 2026-10-07. They are not a claim about vendor prices or AI productivity. Input: [example-input.json](../references/ai-assisted-forecast/example-input.json).

The user wants a small app version, works three hours Monday through Friday, starts 2026-10-12, and reserves 80% of those blocks for project activities. The rest covers interruptions, not review. Account approval is an independent release gate ready fourteen calendar days after starting. The exact acceptance scope must be agreed before using these figures for a real forecast.

| Input/output | Lower scenario | Upper scenario |
|---|---:|---:|
| Engineering hours | 24 | 40 |
| Learning hours | 6 | 12 |
| Verification hours | 8 | 14 |
| Rework hours | 4 | 10 |
| Effective project hours | 42 | 76 |
| Scheduled owner hours after usable fraction | 52.5 | 95 |
| Working days, rounded upward | 18 | 32 |
| Build and release readiness date | 2026-11-04 | 2026-11-24 |
| Elapsed calendar days after start | 23 | 43 |
| Inclusive active calendar span | 24 days | 44 days |
| Started 30-day recurring cash blocks | 1 | 2 |
| Direct cash, USD | 76.25 | 127.50 |
| Owner-time valuation, USD | 1,312.50 | 2,375.00 |

The cash assumptions are USD 20 one-time, USD 30 for each started 30-day block, USD 0.50 per scheduled owner hour, and USD 25 per owner hour as a separate time valuation. The calculator never adds that valuation to cash spending.

Diagnosis: an estimate counting generated code alone would omit learning, review and repair. Recommend measuring one representative accepted feature before using this full-project range. These endpoints are conditional scenarios, without probability claims.

At six hours daily, the lower scenario needs nine working days. Build completes October 22, but approval at offset fourteen delays release readiness to October 26. Scheduled owner hours remain 52.5; more hours each day changes the schedule, not the total estimated effort. If independent approvals take 40 and 35 days from the start, release readiness is offset 40, not 75 or build duration plus 75. If either approval blocks coding, this independent-release-gate model does not apply.

Source-supported reason to retain verification: [official inline guidance](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/estimation-stinger/references/ai-assisted-forecast/research/raw/github-inline.md) and [official agent guidance](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/estimation-stinger/references/ai-assisted-forecast/research/raw/github-agents.md). The mathematical model is the declared convention in the [guide](../guides/06-ai-assisted-forecast.md), not an empirical result attributed to those sources.
