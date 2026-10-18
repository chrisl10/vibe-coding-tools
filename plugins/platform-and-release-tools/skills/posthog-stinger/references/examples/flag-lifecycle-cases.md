# Worked flag lifecycle cases

All cases are HYPOTHETICAL exercises derived from the current digest. No project, installed SDK, requests, telemetry, rollout or provider changes were observed.

## Case A: Dashboard release

Purpose: replace a dashboard layout. Owner: synthetic release owner. Review: 2026-11-07 UTC. Retained path: not decided. Client/server versions, source/config revisions and project region: UNKNOWN. Tenant identifiers are synthetic labels `tenant-a` and `tenant-b`; no customer identities are used. Server membership and subscription are checked independently.

A server evaluation returns `test`, while an old bootstrap cache renders `control`. Do not claim bucketing drift. Compare identity, definition version, contexts, property inputs and response completeness. The source documents that partial/errored responses can preserve earlier values. Freeze the next rollout stage until target refresh and first-paint proof exists. A false result is an explicit branch; undefined is unresolved. No universal fallback decision is assumed.

Expected blocked action: broader rollout. Missing proof: actual SDK behavior, cache age, matching input record, measured refresh convergence and product-approved default. Bootstrap source.

## Case B: Server export switch and entitlement

Purpose: controlled release of an export implementation. Owner: synthetic export owner. Review/expiry decision: UNKNOWN. Group bucketing: company, from server membership. A modified browser claims `export-v2=true`, but the signed-in user lacks export entitlement. Expected result: server denies export before any job is queued, regardless of flag value. Browser flag and group headers cannot authorize the operation.

During provider outage a local definition cache still returns true. That does not prove a requested kill has reached the worker. Record last definition age/version, process lifetime, refresh/retry behavior and an independently controlled server incident fallback. A durable queued export is not cancelled just by disabling a UI flag. No kill propagation bound is claimed without worker proof. Local mechanics.

Expected blocked action: declaring incident stop complete. Missing proof: exact SDK and cache implementation, operator action, protected-action exercise and measured convergence.

## Case C: Experiment retirement with old client

Purpose: retire a completed checkout-copy experiment; it changes display copy, not prices or billing authority. Owner: synthetic experiment owner. Retained variant: approved hypothetically as control. A 100% dashboard state exists in the hypothetical input, but a supported old mobile release still reads the flag and a survey depends on it.

Expected result: prepare a scoped code diff preserving control and server payment checks, review all consumers, preserve the key until the old release and survey dependency are resolved, then verify authorized deployments before a separate provider-disable action. A stale flag label alone cannot choose the winning branch or approve deletion. Exposure checks must use a value accessor at the experience decision and record missing ingestion proof explicitly. Cleanup source, exposure source.

Expected blocked action: provider disable and retirement-complete claim. Missing proof: deployed revision inventory, experiment decision evidence, old-client policy, survey replacement and authorized provider result.
