# International pricing preparation cases

All entities, prices, rates and fee inputs below are fictional arithmetic assumptions. They are not UK or Canadian rates or Stripe prices. No actual tax liability is calculated.

## Case A: supplied inclusive rate, one currency

Fictional seller A and fictional consumer B use currency X. An external reviewer supplies a scenario rate of 25%, an inclusive total of X125, a payment fee of 4% of the charged total plus X1, and no refunds. This is a transparent sensitivity exercise.

- Amount excluding the assumed tax = 125 / (1 + 0.25) = X100.
- Assumed tax portion = 125 - 100 = X25.
- Fee = 125 × 0.04 + 1 = X6.
- Scenario cash after assumed tax reserve and payment fee = 125 - 25 - 6 = X94.

X94 is neither profit nor proven remittable tax accounting. It excludes operating costs, withholding, discounts, FX, disputes, delayed settlement and refund adjustments. The rate's applicability and registration remain Unknown.

For an exclusive X100 price using the same fictional assumptions: charged total X125, assumed tax X25 and fee X6. These scenarios reconcile only because the same rate and fee base were expressly supplied. Never add 25% to an already inclusive X125 total.

Use the existing selected `unit-economics-stinger` worksheet for further one-currency contribution modeling. Its calculator does not resolve tax or FX: carry the tax reserve and gross fee base in an explicit worksheet extension rather than silently substituting net sales for the processor's fee base.

## Case B: Canada customer, location missing

Seller establishment: supplied outside Canada. Buyer location: Canada, province Unknown. Product classification and registration regime: Unknown. Customer registration status: Unknown. Price mode: Unknown. No tax rate or net revenue result is produced. Packet lists CRA registration/place-of-supply questions and reviewer decisions, not a registration recommendation.

## Case C: UK customer, B2B status unverified

Buyer claims to be a business but tax ID and location evidence are absent. Product includes both software and live consultation. B2B/B2C and digital-service classification remain Unknown. HMRC guidance is a question source; no reverse-charge or exemption conclusion follows.

## Case D: different currencies and refund

Presentment EUR, settlement USD; conversion timing, fee retention and refund FX are Unknown. Stop dependent margin arithmetic. Request supplied dated contract terms and settlement/refund records. Do not select a currency policy or force this into the existing single-currency calculator.

This is a generated draft for reference. Have a qualified attorney licensed in your jurisdiction review all legal documents before publishing or countersigning.
