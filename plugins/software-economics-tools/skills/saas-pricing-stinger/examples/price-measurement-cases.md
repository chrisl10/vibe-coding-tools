# Fictional price measurement and negative cases

All numbers are invented USD examples, not observed customer results, vendor fee quotes, statistical evidence or approved prices. Pure arithmetic was executed with Decimal; interpretation cases below are constructed, not native/provider tests.

Each arm has 100 assigned accounts and 80 observed price exposures during an identical fictional follow-up window. A has 40 attempted account-month payments at $20, 10% failure, zero full refunds, invented 3% + $0.30 processing fees and $5 delivery per attempted payment. B has 32 attempts at $30, 0% failure, 25% full refunds, the same invented processing fees with no fee returns, and $5 delivery per attempt. Remaining assigned accounts have zero collected cash; their trial/free/support costs are UNKNOWN and are excluded from this narrow paid-unit calculator example, so total cohort contribution is NOT established.

| Narrow paid-unit result | A | B |
| --- | --- | --- |
| Gross collected cash | 720 | 960 |
| Successful full refunds | 0 | 240 |
| Net cash before disputes | 720 | 720 |
| Processing fees | 32.40 | 38.40 |
| Variable delivery | 200 | 160 |
| Paid-unit contribution | 487.60 | 521.60 |
| Gross cash per assigned account | 7.20 | 9.60 |
| Net cash per assigned account | 7.20 | 7.20 |
| Net cash per exposed account | 9.00 | 9.00 |

Gross cash rises 33.333...%, net cash is unchanged, and narrow paid-unit contribution rises $34 (about 6.973% before excluded costs). **Conditional recommendation:** retain the baseline commercial decision while collecting equal-maturity reconciliation and free/trial/support costs, because gross lift did not improve net cash and total cohort contribution remains unknown. This recommendation does not claim B is harmful or beneficial, causal significance or any experiment having run. No dispute events exist in this constructed input; that is an assumption, not a real missing-event guarantee.

Reuse the selected Unit Economics calculator with [the fictional input](price-measurement-input.json) and retain [its output](price-measurement-output.json). The calculator models attempted paid units only. Assigned/exposed denominators are supplied worksheet facts in this fictional example and are not calculator inputs. No exposure/statistics helper is added.

| Constructed negative case | Required outcome |
| --- | --- |
| Gross lift hides refunds | Show gross and net separately; no winner from gross alone. |
| Only buyers used as denominator | Retain assigned/exposed zero-spend accounts; label buyer-only values separately. |
| B starts later, most trials unexpired | Mark immature observation; no equal-window claim. |
| Refund requested but pending/failed | Reconcile statuses and future exposure; no invented successful refund. |
| Price switch produces unpaid proration | Separate price, amount owed, credit and collection; Payments owns implementation. |
| Shared account sees A and B | Record contamination and chosen predeclared handling, no clean assignment claim. |
| Before/after includes a marketing launch | Descriptive association and confounder; no causal attribution. |
| Dashboard mean called total revenue | Pin aggregation and denominators; reconcile actual totals. |
| Partial refund/dispute requested in calculator | Unsupported field-model gap; do not coerce full-refund rates. |
| Exposure denominator zero | Ratio unavailable; no divide-by-zero or zero-performance claim. |
| Heavy buyers clamped after seeing results | Retain raw totals and report changed analysis; no unbiased predeclared result. |
| Missing free/support costs | Paid-unit contribution only; total cohort recommendation remains conditional. |
