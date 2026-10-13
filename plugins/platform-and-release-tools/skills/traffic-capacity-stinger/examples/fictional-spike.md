# Completed fictional packet and arithmetic
All values and policies below are invented teaching inputs, not actual telemetry, provider rates or accepted owner thresholds. Target: fictional catalog API on a fictional staging environment, release toy-1, region example-east. Observer/source: synthetic worksheet, 2026-10-08 00:00 to 00:10 UTC baseline and 00:10 to 00:12 burst. Sampling: all toy events, no real logs or identifiers. Owner acceptance: absent. Status DRAFT. Native/server/customer/performance: NOT_RUN.

Baseline: attempted/admitted/completed 40 requests/s, no backlog trend, mean residence time 200 ms, p50 120 ms, p95 600 ms, p99 1,100 ms. CPU 35% of fictional 2 cores, memory 600 MiB of fictional 1,024 MiB, DB 8/20 pool connections with 5 ms p95 wait. L = 40 requests/s × 0.200 s = 8 mean requests in system. This matched stationary toy boundary is a consistency check, never a cap or sustainable throughput result.

Burst service-work boundary: 90 original customer attempts/s plus 10 retry work attempts/s offer 100 work attempts/s. The toy policy admits 60 original plus 10 retry work attempts/s and rejects 30 original attempts/s. Terminal work exits are 50/s for 120 s, including the two DLQ exits counted below. DB active 20/20 and pool wait p95 900 ms, CPU 45%, memory 850 MiB; service-work response p95 is 1,600 ms and p99 4,000 ms, including failed/retry work attempts. Queue starts at zero and grows by (70 admitted − 50 terminal exits) jobs/s × 120 s = 2,400 jobs. Queue oldest age at final observation is a fictional 45 s; no FIFO discipline is assumed. Retry work is already included in offered/admitted work; do not add it twice. DLQ 2 total is included in terminal exits, not an additional queue outflow. Little law's stationary interpretation is not applicable during this growth. DB/pool saturation is a plausible bottleneck; low CPU does not refute it. Query versus connection-hold evidence is missing.

After the burst, assume completion stays 50 jobs/s and new admitted work returns to 40/s. Toy drain = 2,400/(50 − 40) = 240 s. If new arrivals are 50/s or higher, no finite drain follows. Cache warmth, retries, changing job mix or failures can invalidate either estimate. This is hypothetical recovery math, not observed recovery.

Burst customer-attempt accounting: 90 × 120 = 10,800 original customer attempts, of which 30 × 120 = 3,600 are rejected. If all those originals are eligible and a rejection is bad, at least one third are bad, so this burst cannot meet a 99% good-request target. Good completion counts and a matched original-customer latency histogram are absent; do not infer them from 6,000 terminal work exits, which mix retries, originals and DLQ. Full customer SLI attribution remains incomplete. Mean occupancy proves no tail SLO.

Separate fictional SLO arithmetic exercise: an independent synthetic service called sli-practice, observed over a different 120 s window, has 12,000 eligible original customer attempts, 11,820 good and 180 bad. These numbers are not measurements of the burst above and share no cohort, service or timeline with it. A 99% good target means allowed bad = 12,000 × 0.01 = 120; remaining = 120 − 180 = −60 events. Its monthly budget is unknown. This isolated arithmetic exercise teaches a matched-denominator budget; it supplies no success/latency claim about the burst service.

Toy marginal queue-processing price assumed $0.002/job, not a provider rate. Backlog work = 2,400 × $0.002 = $4.80. Fictional recovery work budget $10 leaves $5.20 before requests/DB/CPU/memory/network/rejections/DLQ/retries. Other meters are unpriced, so total bill and full budget feasibility remain UNKNOWN. Actual rates/allowances/floors/credits go to Operating Cost. Constraint evidence: dated Vercel docs captured 2026-10-08 list shared file-descriptor limits, but actual plan/runtime/configuration entitlement for this fictional target is unknown.

DRAFT proposal: protect expensive DB operations with bounded admission and queue age, review customer priorities and rejection cost, inspect retry layering/idempotency and jitter after synchronized reconnects. Every rate, threshold and priority requires real owner policy. Recovery would require fresh tails/errors/pool wait/oldest-age and drain evidence for an agreed window, then staged reopening. Do not execute. Recommended measurement: DB connection-hold and query-duration distributions, because the fictional pool saturates before CPU.

Future test target/rate/ramp/budget/stop conditions/operator: UNKNOWN and NOT_ACCEPTED. Existing test tool: UNKNOWN. Do not run a probe, load test or provider change from this example.

## Negative cases and expected decisions
| Input or request | Expected planning result |
| --- | --- |
| Use p95 = 0.6 s as W in L=lambda W | Reject average/tail substitution; request mean and matched window. |
| Growing backlog or lambda/completions mismatch | Mark steady-state calculation NOT_APPLICABLE. |
| Completion <= continuing ingress | No finite drain estimate; escalate recovery budget/admission decision. |
| No sampled denominator or mixed trace sampling | Population error/SLO claim INCONCLUSIVE. |
| CPU low while DB/pool wait saturates | Preserve downstream bottleneck hypothesis; do not add frontend concurrency. |
| Retry at three layers after shared timeout | Inventory amplification, attempt/deadline/idempotency and jitter; do not assert retries safe. |
| Cache expiry/restart causes synchronized arrivals | Record thundering herd and recovery impact; no autoscaler changes. |
| Quota/concurrency documented ceiling | No throughput guarantee; require actual entitlement and workload evidence. |
| Missing rate or meter | Total cost UNKNOWN, never free. |
| No fresh telemetry after restart | Recovery UNPROVEN. |
| Owner says 'benchmark it' without target/rates/budget/stop scope | Draft scope and ask; performance NOT_RUN. |
| Production or third-party endpoint unaccepted | Stop dependent execution; retain read-only packet. |
| Queue cap protects provider but rejects paying users | Customer-policy decision unresolved; no fairness claim. |
| Formula suggests adding workers/installing k6 | Out of runtime scope; route proposal without installation/provisioning. |
