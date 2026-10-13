---
description: "Produce a reviewable economic worksheet from supplied prices, costs, refunds and usage scenarios. No provider writes."
argument-hint: "[business or supplied JSON input]"
---

# /model-unit-economics

## Mandatory process

1. Load the pest-controller-suit skill and consult its roster before making any routing decision. For source work use the canonical Core catalog. For installed work resolve it from trusted selected Core; do not assume a neighboring cache is selected.
2. Resolve `unit-economics-wasp-drone` and `unit-economics-stinger` from their `software-economics-tools` catalog owner. Installed work uses Core's `hooks/resolve-component.py` with `--kind agent` and `--kind skill`, respectively, against the explicit selected-plugin registry. Report an unavailable owner instead of loading a cached copy.
3. Arm the Drone with the resolved paired skill before work. Collect one currency, period, attempted billing unit, supplied price, costs, collections/refunds assumptions and dated evidence. Batch missing inputs; unknown costs remain unknown.
4. Follow the skill's field contract and calculator guide. Produce baseline, high-usage and downside calculations with explicit fixed/variable and cost-of-revenue/operating classifications. Do not silently apply guessed provider rates or propose a live price change.
For a service-limit proposal, read the paired skill's fair-service-limits guide and worksheet. Resolve selected SaaS Pricing for its value/overflow proposal. Map entitlement, usage unit/window/aggregation, cost, legitimate and suspected-abuse/incorrect-blocking scenarios, proposed limit/recovery, owner-selected fairness criterion and actual policy authority. Missing criteria, rates or accepted decisions remain Unknown. This advisory creates no billing, rate limit or abuse control; separately accepted implementation retains Payments and Security owners.

5. Deliver the reviewable worksheet with complete input/output JSON, contributions and gross margins, losses, break-even statuses, evidence dates, model limitations and remaining user questions. Verify the arithmetic using the bundled local calculator when the single-period full-refund model fits.

## Arguments

Use supplied business context or an explicit local JSON file. If no inputs are provided, collect the required economic assumptions in one compact question. Input rates are supplied assumptions, never authorization to write billing settings. Partial refunds, tiers, mixed products and late collections require a disclosed worksheet extension rather than an unqualified calculator claim.

<!-- Ship Gate removed: research-only command, produces no implementation code or provider writes. -->
