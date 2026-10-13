# Request budget review exercises
These are fictional control-review cases, not live enforcement or provider prices.

| Given | Correct disposition | Evidence still needed |
|---|---|---|
| App allows three calls; SDK allows two retries per call | Up to nine transport attempts before gateway/fallback multiplication. Bound one owner across layers. | Actual SDK settings/version and call graph |
| Two workers see ten units remaining; each needs eight | Both cannot independently admit. Atomic reservation admits at most one with those hypothetical units. | Concurrent implementation proof; unit/rate mapping |
| Primary consumes an attempt, then times out | Keep uncertain charges reserved; timeout does not prove no processing. Retry only with remaining attempt/time/money allowance. | Request ID, actual usage/billing and reconciliation policy |
| Cache reads were forecast but all requests miss | Reserve and model uncached input and any cache creation, without discounting output. | Selected provider cache/billing contract |
| Fallback fits money but fails task quality or crosses egress boundary | Reject fallback and use approved exhaustion response. | Mind evaluation and Security boundary qualification |
| Duplicate settlement and late usage arrive after cancellation | Settle once under idempotent identity; no double release; preserve uncertain/late cost policy. | Implementation and invoice evidence |

For numeric monthly arithmetic reuse the already checked [synthetic margin exercise](synthetic-feature-margin.md) and [input](../references/examples/feature-margin/economics-input.json). Its fictional rates stay fictional; no price claim follows. For actual supplied rates use guide 08's selected-owner workflow. Unknown rates block estimates.
