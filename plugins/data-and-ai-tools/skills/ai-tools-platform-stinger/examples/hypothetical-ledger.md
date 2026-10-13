# Hypothetical retrieval-answer feature ledger

This worksheet is an illustrative workload, not an observed bill or vendor price. Currency, every vendor rate, customer price and actual billing terms remain Unknown. Therefore monthly cash, contribution and gross margin cannot be calculated. No calculator output is fabricated.

Assumptions: base 10,000 successful customer answers/month; 2,000 additional failed/retry/fallback model attempts/month; 12,000 total model attempts/month. Average input is 1,000 tokens/attempt and output is 200 tokens/attempt across all attempts, including partial failures. These averages are hypotheses, not measured logs. Reconcile actual provider attempt records before use.

| Meter | Base quantity | Full unit/rate dimension | Rate/evidence | Boundary |
|---|---:|---|---|---|
| Uncached model input | 9,000,000 | tokens/month × currency/1,000,000 tokens | Unknown | Includes assumed failed/retry input |
| Cache-read model input | 3,000,000 | tokens/month × currency/1,000,000 cache-read tokens | Unknown | Partition of 12M total input; no second discount |
| Cache creation/write | Unknown | tokens/month × currency/1,000,000 cache-write tokens | Unknown | Provider treatment and overlap need evidence |
| Model output | 2,400,000 | tokens/month × currency/1,000,000 output tokens | Unknown | All attempts; no cache-read discount |
| Retrieval | 20,000 plus unknown failed/retry queries | queries/month × currency/query | Unknown | Two successful-query attempts/answer is hypothetical |
| Embedding/backfill | Unknown | input tokens/month × currency/1,000,000 embedding tokens | Unknown | Fresh ingestion and updates not included in generation tokens |
| Reranking | Unknown | billable units/month × currency/unit | Unknown | Define the selected API's actual unit |
| External tool operations | 10,000 plus unknown repeats | operations/month × currency/operation | Unknown | One per successful answer assumed; failed tool billing open |
| Stored data | 50 | GB-month/month × currency/GB-month | Unknown | Assumed average; indexes/backups scope open |
| Network transfer | 20 | GB/month × currency/GB | Unknown | Destination/region/allowances open |
| Gateway/plan floor | Unknown | currency/month | Unknown | Fee versus minimum floor ordering open |
| Paid operations labor | Unknown | hours/month × currency/hour | Unknown | Separate from unpaid founder-time valuation |

Low/base/high successful answers: 1,000/10,000/30,000 per month, all hypothetical. Each scenario needs its own retry, token, cache, retrieval, tool and storage assumptions; do not scale every line blindly. Peak: hypothetical 20 simultaneous in-flight operations, not a monthly multiplier. Reserve: method, per-attempt maximum cost and overshoot Unknown until rates/output/tool/retry ceilings and enforcement are accepted.

Map completed monthly meter inputs to selected Operating Cost's existing worksheet/calculator. Pass accepted customer-price, fee/refund and classified cost assumptions to selected Unit Economics afterward. Unknown fields prevent a complete numerical model. Proposed control: reserve worst-case approved attempt/tool budget before admission, reconcile actual usage, and stop additional attempts at the accepted boundary. This is an implementation proposal, not existing provider enforcement.
