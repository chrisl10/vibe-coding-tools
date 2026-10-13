# Flag lifecycle worksheet

Status: DRAFT / PREPARED / OBSERVED / RETIRED (choose with proof)
Evidence classes: SOURCE / HYPOTHETICAL / OBSERVED / UNKNOWN

## Ownership and decisions

- Flag key and aliases:
- Purpose and type (release / experiment / retained operational switch):
- Owner / backup / incident operator:
- Created / review / expiry date and timezone:
- Authorized task, exact code files, live action approvals:
- Desired retained path and decision source:
- Feature/PRD and dependency inventory:

## Version-bound evaluation

- Source revision / config revision / lockfile:
- Client SDK exact version and installed types / server SDK exact version and installed types:
- Environment / project label / region (no secrets):
- API / evaluation origin / mode / supported contexts:
- Bucketing unit / authoritative identity source / group source:
- Required properties / synthetic examples / approved event allowlist:
- Identity-before-evaluation / login / reset / tenant switch behavior:
- Protected server checks and entitlement source, independent of flag:
- Timeout / retry / polling / initialization / cache scope:
- Definition version / observed age / maximum age decision:
- Result lifetime / invalidation / provider-unreachable alternative:

## Rollout and observation

- Hypothesis or feature goal / assignment and exposure points:
- Synthetic/internal cohort / initial audience / progressive stages:
- Metric definitions / baseline / observation window / stop thresholds:
- Exposure accessor / client-server deduplication / conversion snapshot:
- Telemetry opt-out, transport failure and ingestion proof policy:
- Payload validation and allowed variants:

| Case | Expected behavior and authority | Observed value/origin/version/age | Exposure proof or absent reason | Artifact and result |
| --- | --- | --- | --- | --- |
| Pending or missing | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| False / each valid variant | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Invalid payload/variant | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Timeout or provider error | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Partial response with old value | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Cold/stale local cache | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Missing targeting property | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Anonymous to login / logout | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Tenant/group change | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Enabled but entitlement denied | Deny server effect | UNKNOWN | UNKNOWN | UNKNOWN |
| Kill/rollback convergence | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Retirement and handoff

- Dependencies: current/old deployed clients, wrappers, background jobs, config, tests, dashboards, experiments, surveys, other flags:
- Intentionally retained switch decision:
- Exact retained-path diff / Security / Quality / Repository Health:
- Authorized deployment and every supported consumer proof:
- Rollback-compatible interval and effects not undone by a flag:
- Separate authorized provider disable/archive/delete action and proof:
- Remaining unknowns and blocked actions:

Template completion alone is neither observed behavior nor authorization. Never include key values, real identities, PII or raw sensitive logs.
