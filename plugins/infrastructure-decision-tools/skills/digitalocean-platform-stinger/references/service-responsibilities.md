# Service and responsibility map

Derived from the [digest](research/distilled-digitalocean.md); responsibility assignments below are architectural inference, not provider guarantees.

| Layer | Candidate | Retained work and required proof |
|---|---|---|
| HTTP app | App Platform service | Image/build dependencies, authorized releases, app security, health behavior, capacity/load evidence, rollback; no local durable state |
| Continuous background task | App Platform worker | Queue durability, idempotency/retries, backlog observation, lifecycle/shutdown; service request autoscaling does not establish worker scaling |
| OS/native/persistent path need | Droplet | OS/runtime patches, SSH/admin policy, firewall/network topology, TLS, observability, capacity, app/data recovery and coverage during absence |
| Relational data | Managed PostgreSQL | Edition/region/version/extensions eligibility, schema/tenant policy, pool sizing, migrations, restore rehearsal, exports and recovery credentials owned by human |
| Uploaded assets | Separate object storage candidate | Exact endpoint/region, access policy, lifecycle, version/backup behavior, egress, recovery; Spaces price/capacity deliberately unqualified until sourced |
| Multiple app backends | Regional LB if justified | Independent healthy backends, protocol/timeouts, certificates and state dependency availability; adding LB alone is insufficient |

Pick RPO/RTO from business tolerance, then request evidence of a restore and cutover achieving them. Backups, HA, DR and portability are separate. Export/rebuild steps, DNS/connection changes and all provider writes need a separately authorized implementation scope. This pair prepares that handoff and performs none of them.
