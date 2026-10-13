# Traffic capacity measurement worksheet
Status: DRAFT / SOURCE_REVIEWED / TARGET_OBSERVED. Date UTC: __. Decision owner: __. Approval source: __.

## Target and observation
Service/journey/environment/release/artifact/region: __. Provider plan/runtime/Fluid Compute: __.
Baseline and peak inclusive UTC windows/resolution: __. Export/query/hash: __. Sample counts, sampling/filter/drop rules and ingestion lag: __.
Burst magnitude/duration and route/customer-class mix: __. Retry and timeout treatment: __. Sensitive fields omitted: __.

| Boundary | Attempts/s | Admitted/s | Completed/s | Reject/error/timeout | Mean/p50/p95/p99 latency ms | CPU/core basis | Memory/limit/OOM | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Application | __ | __ | __ | __ | __ | __ | __ | __ |
| DB/pool | __ | __ | __ | __ | __ | __ | __ | __ |
| External API | __ | __ | __ | __ | __ | __ | __ | __ |

DB active/max connections, pool wait p95, query/lock wait: __.
Queue depth/oldest age, ingress/completions/retries/DLQ per second and slope: __.
Suspected bottleneck, competing explanation, distinguishing measurement: __.

## Policy and calculations
Journey SLI numerator/denominator/objective/percentile/window and adopted owner policy: __.
Error budget allowed/used/remaining with units and evidence: __.
Little law boundary, admitted lambda, mean W seconds, observed mean L, stability evidence: __.
If unstable or mismatched: NOT_APPLICABLE, reason __. Tail compliance uses actual distribution: __.
Burst/drain assumptions and calculation: __. No positive net drain: INDETERMINATE.

| Provider constraint/meter | Plan/runtime/region | Configured versus documented | URL/date/hash | Low/base/high usage/rate | Currency/allowance/floor/credit | Unknown |
| --- | --- | --- | --- | --- | --- | --- |
| __ | __ | __ | __ | __ | __ | __ |

Per-operation/customer-class cost and retries: __. User/cost budget and impact: __.
Admission trigger/window/priority/queue bound/rejection cost and owner acceptance: __.
Timeout/attempt/deadline/idempotency/backoff/jitter inventory: __.
Recovery evidence/window/hysteresis/reopen/reconciliation/rollback/owner: __.

## Future validation scope
Actual owner acceptance source: __. Owned target/endpoints/revision/dependencies: __.
Synthetic data/auth scope: __. Model/mix/ramp/rate/concurrency/duration/request budget/money budget: __.
Existing test tool and generator limits: __. Stop thresholds/operator: __. Recovery observations/destination: __.
Missing acceptance: DRAFT, no execution. Native execution: NOT_RUN. Server/runtime: NOT_RUN. Customer acceptance: NOT_RUN. Performance/load test: NOT_RUN.

Recommendation with one reason: __. Unknowns and blocked decisions: __.
