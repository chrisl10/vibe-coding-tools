# Fictional monthly operation

Observed 2026-10-07, USD/month. No figure is a live vendor price. This prices a supplied fictional host, not a provider recommendation.

The host has a $10 minimum usage floor, 10 included compute-hours/month, a fictional rate of $2 per additional hour, and a $10 shared usage-credit pool. Low/base/high quantities are 5, 30, and 60 hours. Low allocates zero credit because it has no chargeable usage; base and high each allocate $10 in their independent scenario. Credits apply to usage before the floor, so the floor cannot be erased by that usage credit.

| Scenario | Gross usage after unit allowance | Usage credit used | Charge after floor | Paid operator labor | Monthly cash | Unpaid time valuation | Cash plus time valuation |
|---|---|---|---|---|---|---|---|
| Low | $0 | $0 | $10 | $40 | $50 | $100 | $150 |
| Base | $40 | $10 | $30 | $40 | $70 | $100 | $170 |
| High | $100 | $10 | $90 | $40 | $130 | $100 | $230 |

Paid labor is two hours at $20/hour; unpaid founder time is four hours valued at $25/hour. The latter is an explicit opportunity-cost assumption, not a payable invoice. If the $10 platform amount were additive, base provider cash would instead be $40. A total-invoice credit has different semantics from a usage credit. Both distinctions are tested.

The largest variable here is billed compute-hours. Verify measured active compute time and the actual plan's allowance, floor and credit eligibility before using a live estimate. Unpriced backup, egress, support and observability remain unknown until supplied; these fictional entries do not cover them.

Input is [the template](../references/templates/input.json); [expected output](fictional-output.json) records the local calculation. The source-grounded distinctions are in [the distillation](../references/research/distilled-operating-cost.md).
