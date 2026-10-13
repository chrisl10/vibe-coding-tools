# Monthly cost contract

Source basis and limits: [distillation](research/distilled-operating-cost.md). This worksheet uses one currency and the period `month`. Dates, provider region, plan identity, billed unit and source are mandatory. Every number is an explicit assumption or dated rate.

The root object has exactly `currency`, `period`, `observed_at`, `evidence`, and `scenarios`. Scenarios are exactly three objects whose distinct names are `low`, `base`, `high`. Each contains `name`, `providers`, `credit_pools`, and `labor`.

| Object | Required fields |
|---|---|
| Provider | `name`, `region`, `plan`, `observed_at`, `source`, `fee_mode`, `fee_amount`, `meters`, `credit_allocations` |
| Meter | `name`, `unit`, `quantity`, `allowance`, `rate` |
| Credit pool | `name`, `amount`, `scope` (`usage` or `total`), `eligible_providers` (distinct provider names) |
| Allocation | `pool`, `amount` |
| Labor | `name`, `hours`, `hourly_rate`, `kind` (`paid` or `unpaid`) |

Fee mode is `additive` or `minimum`. The latter means the fee is a floor inclusive of eligible usage; it is not added again. Meter quantity and allowance have the same unit for this month; rate is currency per that exact unit. Convert GB versus GiB, requests versus millions, seconds versus hours and stored-month quantities before input. Cost guesses based only on user count do not establish workload.

For each meter: `billable = max(0, quantity − allowance)`; `usage = billable × rate`. Sum meter usage into U. Sum explicitly allocated eligible usage credits into Cᵤ, which must not exceed U. Net usage is U − Cᵤ. Pre-total-credit charge is `fee_amount + net_usage` in additive mode or `max(fee_amount, net_usage)` in minimum mode. Subtract allocated total credits Cₜ, which must not exceed that charge. Every allocation must name an existing pool and eligible provider, and sums across providers must not exceed each pool's available amount. Multiple allocations of the same pool in one provider are rejected. Unallocated credit is reported.

Paid labor = sum paid hours × supplied hourly rate. Unpaid labor value = sum unpaid hours × supplied hourly value (same field, clearly labeled). Monthly cash estimate = provider cash + paid labor. Monthly cost including time valuation = monthly cash estimate + unpaid labor value. Show both, never represent unpaid time as an actual vendor bill.

Numbers: decimal strings or JSON numbers, finite nonnegative, max 10^12, max 24 digits and six fractional places. Rates are currency quantities and may exceed 1. Maximum input 256 KiB, 30 providers/scenario, 100 meters/provider, 30 pools/scenario and 100 labor entries/scenario. Unknown or duplicate JSON fields and names are errors. Decimal precision 64; output decimal strings are not currency-rounded. One currency across the input; no FX. Text max 200 characters, no control characters. Dates are valid ISO calendar dates. The calculator does not prove ISO currency registration or plan eligibility.

Credits apply in the documented generic order only. If the real provider applies a total credit before a floor, prorates allowances, rounds each metered item, or charges step/tier costs, keep an explicitly reviewed worksheet extension. No hidden contingency multiplier is applied.
