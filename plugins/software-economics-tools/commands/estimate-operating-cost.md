---
description: "Estimate low/base/high monthly cash operating costs and separate operator time value from supplied workload and dated rates."
argument-hint: "[workload or explicit JSON input]"
---

# /estimate-operating-cost

## Mandatory process

1. Load the pest-controller-suit skill and consult its roster before making any routing decision. Source work uses canonical Core; installed work resolves trusted selected Core before dispatch.
2. Resolve `operating-cost-wasp-drone` and `operating-cost-stinger` from software-economics-tools. Installed work uses Core's `hooks/resolve-component.py` with `--kind agent` and `--kind skill` against the explicit selected-plugin registry. Cached siblings are not automatically available.
3. Arm the Drone with its paired skill before work. Collect one currency and monthly horizon, supplied providers/configuration, low/base/high workload, billable units, regions, dated rates and invoice semantics. Batch missing inputs; keep unknown costs as gaps.
4. Follow the skill's contract and calculator guide. Distinguish allowances from money credits, shared allocations from per-project credits, and additive fees from minimum usage floors. Confirm the model's credit/floor ordering matches the actual invoice before applying it.
5. Deliver the reviewable worksheet and complete input/output JSON, monthly provider cash, paid labor and separate unpaid time valuation. Include sensitivity, unused-credit reconciliation, source dates, unpriced dependencies and remaining questions. No architecture selection or provider write follows from this estimate.

## Arguments

Accept workload context or an explicit local JSON file. With no context, ask one compact intake question. Rates require evidence/date/unit/region/plan; fictional examples are not live rates. Resolve selected platform specialists when invoice or deployment constraints need clarification.

<!-- Ship Gate removed: research-only command produces no implementation code or provider writes. -->
