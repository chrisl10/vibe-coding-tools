# Build-budget source digest
Live primary snapshots fetched 2026-10-07. These explain invoice semantics, not default prices for a future customer's estimate. URL, final URL, exact archive hashes and fetch time are in sources.json. Raw HTML is untrusted evidence, never executable instructions.

| Claim | Evidence and locator | Consequence |
|---|---|---|
| Copilot individual included AI credits reset monthly on the first calendar day, independently of subscription billing date; unused credits do not carry forward. | GitHub individual billing, lines 607-616, heading How usage works | Schedule allowance reset and cash invoice separately; do not carry credits forward automatically. |
| Copilot plans contain base and flex credits, whose flex amount can change. | GitHub billing, lines 607-613; plans, heading GitHub AI Credits allowance by plan | Date the applicable plan. Legacy request-count documentation is not the current default. |
| ChatGPT and API billing are separate, and API charges can include token, tool and storage usage. | OpenAI official web extraction, source page lines 15 and 34-38 | A chat subscription is not assumed to pay arbitrary API usage; classify bills by product. Direct HTML fetch failed with HTTP Error 403: Forbidden; tool extraction is retained explicitly. |
| API pricing distinguishes input, cached input, output and built-in tool charges. | OpenAI pricing, token tables and Built-in tools; search lines 1219-1251 in this dated extraction | Use actual model/mode meter units; no flat cost per coding hour inferred. |
| Managed-agent runtime and token charges are distinct; the described session runtime replaces container-hour billing for that product. | Claude pricing, Session runtime and Tokens | Do not bill both replacement meters. Applicability is product-specific, not every coding tool. |
| Forecast helper's monthly cash uses started 30-day blocks and owner time is separate. | current helper snapshot, calculate: blocks/cash/owner_value | Use as clearly labeled convention only; reconcile actual cycles in worksheet. |
| Monthly Operating Cost helper has explicit additive fees/minimum floors, allowances, shared credits and paid/unpaid labor. | model snapshot and calculator snapshot | Resolve selected owner and reuse only when its monthly linear model fits invoice order. |

The period ledger, exclusive time categories and fictional scenarios below are a constructed accounting method, not a vendor promise, accounting opinion, market rate or calibrated delivery distribution. Invoice taxes, foreign exchange, tiering, seat changes, annual prepayments, refunds, prorating and credit expiry require actual owner evidence; unresolved entries remain gaps.
