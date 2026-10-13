# Billing lifecycle worksheet

Policy status: DRAFT. Decision owner: UNRESOLVED. No provider write or access mutation.

| Case/time | Verified provider state/version | Current local payment facts | Approved policy/version | Feature set and validity | Server request expectation | UI expectation | Actual proof or gap |
|---|---|---|---|---|---|---|---|
| Trial starts | | | | | | | |
| Trial ends without payment | | | | | | | |
| Initial authentication pending | | | | | | | |
| Invoice paid and current subscription checked | | | | | | | |
| Past due / before grace expiry | | | | | | | |
| Exactly at grace expiry / after expiry | | | | | | | |
| Recovery verified / late prior failure | | | | | | | |
| Cancellation requested / paid period remains | | | | | | | |
| Cancellation actual / late old active event | | | | | | | |
| Plan change pending / effective | | | | | | | |
| Partial refund / dispute open / dispute closed | | | | | | | |
| Approved restoration and current-state check | | | | | | | |

Record effective timestamp source and timezone, applicable subscription items/invoices, paid-through derivation, monotonic local policy revision, refresh age, pending job semantics and semantic idempotency keys. Do not deduce object ordering from `event.created` seconds. Missing settlement, relationship or policy evidence stays unresolved.
