# Server entitlement contract

Status: DRAFT. This template contains no approved policy and performs no operations.

| Contract field | Observed evidence or unresolved value |
|---|---|
| Target repository/runtime and implementation owner | |
| Exact installed server/browser SDK versions and lockfile paths | |
| Outbound Stripe API version / event destination version / event format | |
| Stripe account and sandbox/live scope, no secrets | |
| Authenticated user → tenant membership and action permission | |
| Server-owned tenant → customer → subscription mapping | |
| Product/price/feature mapping and effective dates | |
| Feature authority: Stripe Entitlements OR app-owned policy | |
| Subscription/invoice/feature projection responsibilities | |
| Policy ID/version/approver and evidence | |
| Trial end / paid-through / grace expiry / stale-state bounds | |
| Unknown mapping, invalid signature, unsupported payload behavior | |
| Complete pagination and refresh-failure behavior | |
| Durable inbox/event claim key, lease and recovery | |
| Subject serialization and current-state refresh ordering | |
| Transaction projection + outbox + completion boundaries | |
| Semantic action key for each fulfillment/period/transition | |
| Direct server route/job admission/data-query enforcement | |
| UI projection and stale-session behavior | |
| Reconciliation cadence, authorized reads, audit and alert ownership | |
| External operation identity/result inspection, approval source | |

For each premium action: authenticated subject, tenant, permission, feature, expiry, usage admission, expected denied result, displayed UI state, actual implementation test evidence. Do not put secret values, raw webhook payloads or customer PII into public proof artifacts.

Acceptance includes duplicate/concurrent deliveries, cross-tenant access, database rollback, outbox retries, late snapshots, equal timestamps, missing objects, full pagination and revoked-session direct requests. Missing evidence is unverified.
