# Fictional software service worksheet

Observation: 2026-10-07. Currency: USD. Period: month. Unit: attempted account-month. All prices and fees below are invented math assumptions. They are not Stripe or any vendor's current prices.

Each attempted account costs $5 in delivery. Successful charge price is $30. The fictional processor charges 3% plus $0.30 per successful transaction. It returns none of that fee on refund. Fixed delivery is $100 and administrative overhead $200. Delivery is classified cost-of-revenue; fees and administration are classified operating expenses. This distinction is explicit modeling input, not an accounting recommendation.

| Scenario | Attempts | Failed-payment rate | Full-refund rate | Delivery / attempt | Additional refund fee |
|---|---|---|---|---|---|
| Baseline | 20 | 0% | 0% | $5 | $0 |
| Collection and refund downside | 20 | 10% | 50% | $5 | $1 |
| High usage | 20 | 0% | 0% | $40 | $0 |

| Result | Baseline | Collection and refund downside | High usage |
|---|---|---|---|
| Net revenue | $600 | $270 | $600 |
| Payment fees, including refund fees | $24 | $30.60 | $24 |
| Total variable cost | $124 | $130.60 | $824 |
| Contribution per attempted unit | $23.80 | $6.97 | −$11.20 |
| Contribution | $476 | $139.40 | −$224 |
| Gross profit | $400 | $70 | −$300 |
| Gross-margin ratio | 2/3 | 7/27 | −1/2 |
| Modeled operating surplus | $176 | −$160.60 | −$524 |
| Whole-unit break-even | 13 | 44 | Impossible with $300 fixed cost |

The downside consumes service cost on all 20 attempts while charging only 18. Refunds return $270 in revenue; the original $21.60 processing fee stays in the model, with $9 added refund fees. That is why refunds are not just fewer customers in the fee calculation.

The high-usage scenario's negative contribution means increasing volume increases losses. Verify measured per-account service usage and fulfillment on failed payments before trusting the baseline. Demand, conversion, acquisition payback and collection timing remain separate questions.

Run [fictional input](fictional-scenarios.json) through the [calculator](../scripts/README.md). The baseline test checks that fixed cost and operating classification are not mixed into contribution or gross profit twice. Theory and boundary support live in the [distillation](../references/research/distilled-unit-economics.md).
