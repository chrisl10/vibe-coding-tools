# Choose one readable price unit

Source definition: Stripe models. Decision rules below are this component's explicit advisory policy, not a Stripe recommendation about any particular market.

| Model | Plain explanation | Evidence needed to choose it |
|---|---|---|
| Flat | One stated price for a stated plan/period | Similar bounded workload and clear included limits |
| Seats | Each licensed person is one priced unit | Buyer tracks people, user value rises with participation, seat lifecycle is clear |
| Tiers | Different plans or quantity/usage bands | Distinct customer jobs/features; explain volume versus graduated band charging before implementation |
| Usage | Bill for a measured action or resource | Customer understands the meter; cost/value tracks it; disputes and bill predictability are manageable |
| Credits | Buy or receive an allowance applied to defined usage | Clear unit-to-credit mapping, redemption/expiry rules, residual balance and included versus purchased allowance |

Do not equate flat feature plans with quantity-band pricing. A seat is not necessarily an account, workspace or active session; specify which is billed. Credits are a commercial allowance, not proof of prepaid revenue treatment or permission for a wallet. Stripe credit scope.

Compare cost/value alignment, understandable bills, support burden, measurement quality and buyer procurement fit. Then recommend one model with one reason, preserving rejected alternatives only when they explain a real tradeoff. Unknown metering accuracy blocks a usage-price recommendation until its definition is testable.

A fixed fee plus overage can fit a predictable base with variable consumption, but choosing the included allowance and overage rate requires supplied workload/cost/customer evidence. No default discount, margin, annual conversion or credit exchange rate is supplied by this component.
