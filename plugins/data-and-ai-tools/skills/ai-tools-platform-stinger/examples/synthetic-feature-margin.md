# Complete synthetic feature margin exercise

Every monetary rate, customer price, billing rule and usage figure below is fictional. USD is an explicit worksheet currency, not a vendor quote. The observation date records this assumption worksheet, 2026-10-07. No provider calls, account settings, invoice evidence or actual profit are involved.

Base activity: 1,000 attempted account-months, ten successful answers/account, 10,000 successful customer answers. Normal and cache-miss assume 10,000 model attempts; retry assumes 12,000 including 2,000 additional failed/retried attempts; downside assumes 20,000 including 10,000 additional attempts. All attempt tokens are assumed billable in this fictional contract, including failures. Never infer actual failed-request billing from rate-limit consumption.

| Fictional rate | USD per unit |
|---|---:|
| Uncached input / million tokens | 2 |
| Cache-read input / million tokens | 0.5 |
| Cache-write input / million tokens | 2.5 |
| Output / million tokens | 6 |
| Retrieval / query | 0.0002 |
| Tool / operation | 0.0003 |
| Storage / GB-month | 0.1 |
| Network / GB | 0.1 |
| Embedding / million tokens | 1 |
| Rerank / operation | 0.0002 |

Cache-write, cache-read and uncached quantities are disjoint input partitions under this fictional contract. Normal: 6M + 3M + 1M = 10M input, 2M output. Retry: 7.2M + 3.6M + 1.2M = 12M input, 2.4M output. Cache-miss: 10M + 0 + 0 = 10M input, 2M output. Downside: 36M + 3M + 1M = 40M input, 16M output. No second cache discount is applied. Downside represents both more attempts and larger prompts/outputs.

Normal: 20,000 retrieval queries, 10,000 tools/rerank operations and 20 GB network. Retry: 24,000 queries, 12,000 tools/rerank and 24 GB. Cache-miss retains normal non-token activity. Downside: 40,000 queries, 20,000 tools/rerank and 40 GB. Storage 50 GB-month and embedding maintenance 1M tokens stay fixed in all cases. Explicit zero allowances and credits are fictional assumptions, not missing-value substitutions. Gateway fee is USD 20/month additive; paid operations are two hours at USD 25/hour.

Each stress case also has low/base/high activity factors 0.1/1/3. Variable meters scale with activity; storage, embedding, gateway and labor stay fixed. This sensitivity assumes linear rates without tiers, FX, taxes, allowance eligibility, invoice rounding, proration or retention extensions. Peak concurrency is separate and no enforced control is exercised.

Economics uses the hypothetical supplied price USD 1/account-month, payment fee 3% plus USD 0.10/collected transaction, no fee returns and no extra refund fee. Downside alone assumes 10% failed payments and 10% full refunds of successful charges. Service costs continue for all attempted billing units even when payment fails or refunds occur. These are modeling assumptions, not customer billing implementation.

Activity-dependent metered cost is classified variable cost-of-revenue. Storage and embedding maintenance USD 6/month are fixed cost-of-revenue. Gateway and paid labor USD 70/month are fixed operating costs. Payment fees are cost-of-revenue. Fixed amounts enter once, with no second provider-cost total added. Definitions follow the selected economics contract.

| Case | Meter cost USD | Operating cash USD | Net revenue USD | Payment fees USD | Contribution USD | Gross margin fraction | Modeled surplus USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| normal | 45 | 115 | 1000 | 130 | 831 | 0.825 | 755 |
| retry | 52.8 | 122.8 | 1000 | 130 | 823.2 | 0.8172 | 747.2 |
| cache-miss | 49 | 119 | 1000 | 130 | 827 | 0.821 | 751 |
| downside | 200 | 270 | 810 | 117 | 499 | 0.60864197 | 423 |

The downside gross-margin fraction is displayed truncated; retain full precision in [economics output](../references/examples/feature-margin/economics-output.json). For normal, token cost is 12 + 1.5 + 2.5 + 12 = USD 28; other meters sum USD 17; cash estimate is 45 + 20 + 50 = USD 115. Net revenue 1,000 minus payment fees 130 and variable meters 39 gives contribution 831; subtract fixed costs 76 for modeled surplus 755. Fixed cost-of-revenue is included in gross margin, which differs from contribution margin.

These hypothetical results support checking arithmetic and sensitivity. They do not establish demand, acceptable output quality, actual charges, realized margins or working controls. The [incomplete example](hypothetical-ledger.md) still blocks monetary totals.

- normal: [operating input](../references/examples/feature-margin/normal-operating-input.json), [output](../references/examples/feature-margin/normal-operating-output.json), [Unknown-rate rejection fixture](../references/examples/feature-margin/normal-unknown-input.json).
- retry: [operating input](../references/examples/feature-margin/retry-operating-input.json), [output](../references/examples/feature-margin/retry-operating-output.json), [Unknown-rate rejection fixture](../references/examples/feature-margin/retry-unknown-input.json).
- cache-miss: [operating input](../references/examples/feature-margin/cache-miss-operating-input.json), [output](../references/examples/feature-margin/cache-miss-operating-output.json), [Unknown-rate rejection fixture](../references/examples/feature-margin/cache-miss-unknown-input.json).
- downside: [operating input](../references/examples/feature-margin/downside-operating-input.json), [output](../references/examples/feature-margin/downside-operating-output.json), [Unknown-rate rejection fixture](../references/examples/feature-margin/downside-unknown-input.json).
- [Economics input](../references/examples/feature-margin/economics-input.json) and [output](../references/examples/feature-margin/economics-output.json).

To reproduce, resolve the selected Operating Cost or Unit Economics skill, open its `scripts/README.md`, and run its existing `scripts/calculate.py --input <explicit fixture path>` through host tools. No second calculator is installed here. In this source checkout, owner paths are obtained from `plugin-catalog.json`; installed dispatch requires selected-owner availability. A missing owner is a handoff gap.

All four Unknown fixtures returned exit 2 and `Input error: numeric field: expected unsigned decimal notation`, with empty stdout. Unknown is not zero.

Grounding: update digest.
