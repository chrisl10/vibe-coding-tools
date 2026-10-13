# Fictional cohort adapter examples

These invented USD/month inputs test arithmetic only. They are not provider rates, measured customers, conversion forecasts or fraud findings. Run `python3 -B -m scripts.calculate --input examples/free-trial-input.json` from this skill root. [Input](free-trial-input.json), [observed output](free-trial-output.json), and [procedure](../guides/03-free-trial-and-abuse-costs.md) are retained together.

Baseline: 100 attempted paid account-months, supplied price 20, failed-payment fraction 0.1, full-refund fraction 0.1. Successful transactions 90; collected gross 1800; full refunds 180; net revenue 1620. Fictional fee 0.03 plus 0.30 gives 81 retained fees. Service cost 2 on all 100 attempted paid units gives 200, including the failed and refunded service, so it is not added again. Paid-attempt contribution is 1339.

Held period totals: legitimate free service 100, trial service 40, failed signup processing 20, blocked request processing 10, acquisition spend 60, shared floor 100, overhead 100. Sum 430. Fictional underlying totals are free service 50 account-months × 2, trial service 20 trial intervals × 2, failed signup 100 attempts × 0.20, blocked request 1000 attempts × 0.01, and acquisition 300 leads × 0.20. Leads overlap trial/paid stages and are never summed as unique users. The shared floor and overhead are 100 each. These invented quantity/rate assumptions remain separate from the calculator. Combined surplus = 1620 − 81 − 200 − 430 = 909. The worksheet must retain underlying cohort quantities/rates before applying this adapter to a real business.

| Constructed case | Changed assumption | Combined period surplus | Conditional attempted-paid break-even |
|---|---|---|---|
| Baseline | Held totals 430 | 909 | 33 |
| Abuse served spike | Extra suspected served cost 250 | 659 | 51 |
| Eligible credit applied once | Gross floor 100 minus eligible allocated credit 40 = 60 | 949 | 30 |
| No paying customers | Attempted paid units 0; held totals unchanged | −430 | 33, hypothetical threshold only |
| High paid usage | Paid cost per attempted unit rises 2 to 8 | 309 | 59 |
| Mitigation sensitivity | Five legitimate attempted paid units incorrectly blocked; suspected served cost 50, mitigation overhead 30, extra blocked cost 10 | 752.05 | 39 |
| More legitimate free service | Legitimate free cost rises 100 to 300 | 709 | 48 |

No-paid case has null margin ratios; its threshold is conditional on hypothetical additional paid units with otherwise held costs. Credits are applied once to the eligible floor, never as revenue or independently across cohorts. Growing legitimate free service is not labeled abuse. A blocked request's processing cost remains even though downstream service was not performed. Changing cohort mix or reaching a new vendor tier invalidates this constant-volume break-even interpretation and requires another scenario or explicit model extension.

Mitigation case compares with the abuse spike. It assumes suspected served costs drop 250 to 50 and adds control costs 40 while losing five legitimate attempted paid units. The resulting improvement is 93.05 under those fictional assumptions. No prevented bill, customer loss or effective protection was measured.
