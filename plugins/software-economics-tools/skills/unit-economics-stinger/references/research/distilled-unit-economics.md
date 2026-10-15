# Distilled unit economics

Retrieved 2026-10-07. Sources are freshly fetched maintained official pages, not a claim that every page was published within six months. American Express's article metadata records an original publication of 2023-02-23 and modification of 2026-06-02; this sweep uses its current June 2026 revision. The source ledger preserves retrieval, provenance, and content hashes. No historical fee numbers are adopted. The attempted SEC education URL failed and does not support any claim here.

| Claim | Source and implication |
|---|---|
| A single-product break-even quantity divides period fixed cost by the selling price less variable unit cost. | SBA raw. The calculator uses effective net revenue and variable costs per attempted billing unit, states that adaptation, and rounds fractional required units upward. |
| Fixed costs, unit price, sales volume, and variable cost must share a period and unit. Break-even is an estimate. | SBA raw. Do not mix annual costs with monthly volume or add unlike customer/transaction units. |
| SBA uses the label contribution margin for its ratio in the sales-dollar formula. | SBA raw. This component explicitly calls the currency amount contribution and the dimensionless quotient contribution-margin ratio, avoiding an ambiguous label. |
| Gross profit subtracts cost of goods sold from revenue; gross-margin percentage divides gross profit by revenue. Indirect administration and selling expenses are outside the article's direct production costs. | American Express raw. The worksheet requires an explicit cost-of-revenue classification and uses net modeled revenue as its denominator. This is management modeling, not an accounting-policy decision. |
| A successful payment can be partly or wholly refunded. Original Stripe processing fees are retained and refunds might incur additional fees. | Stripe refunds raw. Never assume a fee refund accompanies a revenue refund; read the operator's actual fee agreement and geography before using rates. |
| Decimal supports exact decimal inputs and testing finiteness. Floating-point construction can retain binary approximation. | Python raw. Parse strings or JSON numbers directly into Decimal, reject booleans and nonfinite numbers, and calculate before presentation rounding. |

## Model decisions derived from those sources

The deterministic tool is a transparent single-period expected-value model. One unit is an attempted account-period or sale; each successful attempt produces one transaction. Failed-payment units still incur the supplied service costs. Refund rate denotes a fraction of successful transactions fully refunded in that period, rather than partial-refund amounts. No cross-period receivables, revenue recognition, tax, FX, financing, vendor-tier discontinuities, or acquisitions are hidden in the formulas. These are bounded model choices, not vendor claims. For partial refunds, mixed products, and late collections, build an explicit worksheet outside the calculator and label the extension.

Every cost gets two independent attributes: fixed/variable behavior and cost-of-revenue/operating classification. Both kinds affect modeled operating surplus; only cost-of-revenue affects gross profit. Payment fees have their own explicit classification. This makes contribution and gross margin independently interpretable. Source basis: SBA, American Express.

## Research limits

The Stripe support page initially returned a client shell; the maintained refunds documentation supplied usable policy text. No fee percentage or fixed fee was retrieved or promoted as a live rate. No generic target margin, universal AI discount, tax treatment, or accounting conformance claim is supported. Refresh actual provider fees for each user and retain source/date/region/contract. The calculator's fictional rates are mathematical exercises.
