# Field and formula contract

Sources: [distillation](research/distilled-unit-economics.md), with SBA, American Express, Stripe, and Python raw links. All formulas below are explicit management-model adaptations.

Input is an object with exactly `scenarios`, a list of 1 to 20 full scenario objects. Each scenario has every field below. No default rate is silently inserted. Unknown fields, duplicate JSON keys, empty lists, duplicate scenario/cost names, and malformed types are errors.

| Field | Unit / meaning |
|---|---|
| `name` | Distinct scenario name, 1 to 200 printable characters |
| `currency` | Three uppercase letters; one currency throughout, no conversion |
| `period` | Explicit time basis such as month; 1 to 200 characters |
| `unit` | Explicit attempted billing unit, such as account-month |
| `observed_at` | ISO date for the input assumptions, validated as a calendar date |
| `evidence` | Short provenance/assumption note; never secrets or customer PII |
| `units` | Nonnegative expected attempted units during period |
| `price_per_unit` | Currency per successful unit; supplied commercial assumption |
| `failed_payment_rate` | Fraction of attempts with no collected payment, 0 through 1 |
| `refund_rate` | Fraction of successful transactions fully refunded, 0 through 1 |
| `payment_fee_rate` | Fraction of successful gross charge assessed as fee, 0 through 1 |
| `payment_fee_fixed` | Currency per successful transaction |
| `payment_fee_return_rate` | Fraction of original processing fee returned on fully refunded transactions, 0 through 1; never guessed |
| `refund_fee_fixed` | Currency fee per full refund, supplied explicitly |
| `payment_fee_classification` | `cost_of_revenue` or `operating`; user supplies policy |
| `costs` | 0 to 100 distinct entries, each with `name`, `behavior`, `classification`, `amount` |

Cost `behavior` is `fixed` (currency/period) or `variable` (currency/attempted-unit). Classification is `cost_of_revenue` or `operating`, independent of behavior. Amounts must be finite and nonnegative. Strings or JSON numbers are accepted, with at most 24 digits and six fractional places, maximum 10^12. Rates max 1. Negative zero is rejected. String exponent syntax is rejected; ordinary JSON scientific notation normalizes through Decimal and is still bounded. All scenarios repeat all fields to make assumptions reviewable.

Let n = attempted units, p = price, f = failed-payment fraction, r = full-refund fraction, a = percentage fee, b = fixed fee, t = processing-fee return fraction, h = additional refund fee, v = sum of variable cost amounts, F = sum of fixed amounts.

| Output | Formula and unit |
|---|---|
| successful units | n × (1 − f), transactions/period |
| gross collected revenue | successful units × p, currency/period |
| refunds | gross collected revenue × r, currency/period |
| net revenue | gross collected revenue − refunds, currency/period |
| processing fees before returns | successful units × (p × a + b) |
| processing-fee returns | processing fees before returns × r × t |
| refund fees | successful units × r × h |
| payment fees | processing fees before returns − returns + refund fees |
| variable cost | n × v + payment fees |
| contribution | net revenue − variable cost |
| contribution per attempted unit | (1 − f) × [p × (1 − r) − (p × a + b) × (1 − r × t) − r × h] − v |
| contribution-margin ratio | contribution / net revenue; null if net revenue is zero |
| cost of revenue | Fixed and variable costs classified cost_of_revenue, plus fees when so classified |
| gross profit | net revenue − cost of revenue |
| gross-margin ratio | gross profit / net revenue; null if zero revenue |
| modeled operating surplus | contribution − F; includes losses as negative outputs |
| break-even units | ceil(F / contribution per attempted unit) if positive contribution; see below |

Break-even status is `finite` when unit contribution is positive, `all_volumes` when unit contribution and fixed cost are zero, `zero_volume_only` when unit contribution is negative and fixed cost zero, and `impossible` when unit contribution is zero/negative with positive fixed cost. Null required units means increasing volume cannot satisfy the model. The zero-volume-only case is not a profitable scalable business.

Decimal calculations run with precision 64. Outputs are decimal strings without a monetary quantization step. A repeating division is represented to that context precision. Preserve raw values and round only display columns; provider per-transaction rounding is not modeled. Ratios are fractions, not percentages. Multiple scenarios are independent, never added across currencies/periods/units.
