# Traffic capacity research digest
Captured 2026-10-08. Raw response hashes and final URLs are in sources.json. Official provider documentation is a dated constraint snapshot, never proof of a user's entitlement. Source-backed observations below are separate from the derived worksheet policy.

| Source-backed observation | Own primary capture | Derived procedural consequence |
| --- | --- | --- |
| Traffic, latency, errors and saturation reveal different aspects of system behavior; latency distributions need attention. | Google monitoring | Record eligible counts, failed/timeout durations and p50/p95/p99 separately by journey and window. Mean latency cannot prove tail compliance. |
| Different requests consume different resources; request rate alone is insufficient for capacity. Rejections also consume resources. | Google overload | Separate route mix, CPU time, memory pressure and expensive downstream calls. Preserve rejection cost and legitimate-user impact. |
| SLO implementation needs agreed indicators, objectives and an error-budget policy. | Google SLOs | Missing owner/adopted thresholds leaves DRAFT. Error budget uses the actual eligible denominator and interval. |
| Queue backlogs and message-processing failures need deliberate management and latency measurement. | AWS queue | Record oldest age, arrivals, completions, retries, failures and backlog slope, not depth alone. Admission and recovery remain proposals. |
| SDK retries use backoff/jitter and bounded attempts with documented mode behavior. | AWS retries | Inventory actual clients and retry layers. SDK-specific defaults cannot be generalized to an entire app. Timeouts do not prove side effects were absent. |
| Vercel function ceilings and metering depend on plan/runtime and configuration. CPU time and provisioned memory time are distinct meters. | Vercel limits | Capture plan, region, runtime, Fluid Compute applicability and actual configured duration. A published concurrency ceiling is not measured sustainable throughput. |
| Closed and open workload models differ; closed iteration arrivals slow when response times rise. | k6 models | A later owner-approved test must match real arrival behavior and account for coordinated omission and generator limits. No benchmark/tool execution in this skill. |
| Little's law relates average occupancy, arrival rate and residence time in a stationary regime without M/M/1 distribution assumptions. | MIT queueing, original PDF | Use matched steady-state averages and consistent boundaries only. Do not substitute p95 for the mean or use transient spike arithmetic as sustainable capacity. |

## Constraint snapshot and gaps
The captured Vercel table lists 1,024 file descriptors shared across concurrent executions, including runtime usage. It distinguishes Hobby versus Pro/Enterprise memory and duration limits and contains extended-duration Beta qualifications. This capture is a document observation only. Re-read the relevant row and requirements at planning time; report unknown entitlement/configuration as unknown. Source

DB pool limits, query latency, connection wait, provider quotas, regional availability, actual cost rates and customer SLOs were not supplied. No rate, benchmark, scaling promise or deployment recommendation is inferred. SDK retry guidance supports backoff/jitter mechanics but does not prove the target's timeout, idempotency or retry safety. Sources do not identify a universal safe CPU utilization, queue age or headroom percentage. All thresholds in the fictional case are deliberately invented example policies.
