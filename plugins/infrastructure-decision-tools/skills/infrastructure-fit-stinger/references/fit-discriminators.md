# Fit discriminators and responsibility boundaries

Use hard eligibility before preference scoring. Source support is in the [digest](research/distilled-infrastructure-fit.md); decision rules below are workflow recommendations.

| Workload question | If true | If unresolved |
|---|---|---|
| Only static files, no server state? | Static delivery track; defer DB/auth/queues | Clarify forms, payments and data before deciding |
| Request-oriented code fits documented runtime/duration/memory? | Managed function/app track remains eligible | Record exact runtime/plan proof needed |
| Continuous worker or long completion job? | Persistent service/job track; separate from request handler | Ask maximum run duration, queue semantics and restart behavior |
| Native binary/container needed? | Container track, with architecture/library checks | Do not assume edge runtime or container supports device/kernel privileges |
| OS customization, special ports or kernel/device access required? | Qualify VPS/VM or specialist service | Missing privilege details block topology acceptance |
| Small team cannot patch/restore/respond to VM incidents? | Prefer eligible managed track, subject to budget | Name the operator rather than assuming "AI will operate it" |
| Required region/network/compliance capability missing? | Exclude provider/plan until supported | Explicit blocker; no invented regional feature |
| Paid-user recovery promise? | Define acceptable data loss/time and evidence owner | No SLA/availability promise until those are supplied |

## Operating responsibility comparison

| Duty | Managed platform | VPS/VM |
|---|---|---|
| App correctness/auth/tenant boundaries | App owner | App owner |
| Host OS maintenance | Verify provider boundary | Named operator patches/hardens hosts |
| Deployment/rollback | App owner qualifies platform behavior | Operator owns process/service/build/rollback |
| DB backup/restore | Verify plan and test responsibility | Operator owns backup storage/restore drills unless DB separately managed |
| TLS/domain | Verify host-managed scope; app/domain owner remains | Operator schedules issuance/renewal and route checks |
| Monitoring/incident response | App owner defines alerts/support | Operator covers host plus application failures |
| Availability/scale | Validate selected plan/topology and downstream limits | Operator designs redundancy and recovery |
| Budget/exit | Owner handles service charges/egress/export | Owner handles VM/storage/network plus operator labor and migration |

Neither column guarantees uptime or zero labor. A low VM invoice can coexist with substantial operator work. A managed service can still be a poor fit when runtime, region, egress or required control conflicts.

## Keep optional layers conditional

Load balancing requires an actual routing/availability/scaling need. A firewall/network policy follows exposed attack paths and provider controls. Terraform/Ansible follow repeatable provisioning/configuration needs and accepted ownership; they are not mandatory accounts. Tailscale follows private access needs; Doppler follows accepted secret-delivery needs. A vector DB follows a retrieval requirement that the selected DB cannot satisfy. Resolve selected specialists; this workflow does not enable those layers.
