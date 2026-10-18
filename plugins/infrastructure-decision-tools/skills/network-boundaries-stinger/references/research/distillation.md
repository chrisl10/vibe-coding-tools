# Network boundary selection, captured 2026-10-07

These are current-document captures, not claims of publication within six months. Raw HTML remains byte-preserved; text extracts have fetch headers. Publication is unknown in the ledger; some pages display their own update date. No actual network was supplied or tested.

| Captured fact | Selection implication | Evidence |
| --- | --- | --- |
| AWS security groups govern associated resource ingress/egress and are stateful; response traffic for accepted connections is allowed independently of reverse-direction rules. | Record exact association and connection direction. Do not copy stateless return-path reasoning into a security group. | AWS security groups |
| AWS NACLs govern subnet crossings, evaluate numbered rules in order and are stateless; return traffic is not automatically allowed. DNS/metadata exclusions are documented. | An NACL requires an explicit return-flow assessment; neither AWS layer proves complete egress filtering. | AWS NACLs |
| AWS WAF rate rules aggregate requests using configured criteria; separate rule instances maintain separate tracking. | Record aggregation scope and actual application attachment; do not assume one global budget across instances. | AWS WAF |
| Cloudflare rate rules use match, characteristics, period, limit, duration and action. Availability depends on plan. Counters can lag and allow excess origin requests. | Edge mitigation cannot prove an exact paid-operation ceiling. Record legitimate bursts and application-side admission needs. | Cloudflare rate rules |
| Cloudflare proxy traffic arrives from shared Cloudflare IP ranges. A discovered reachable origin can bypass edge protection. | Document all origin paths and provider-supported origin restriction/authentication; shared range membership alone is not a tenant identity. | Cloudflare origin |
| Cloudflare supplies client-IP headers, with special Worker and IPv6/Pseudo IPv4 behavior. | Record the real chain and product behavior before trusting a header as a rate bucket. | Cloudflare headers |
| Express proxy trust changes IP/host/protocol interpretation. Blanket trust needs the last trusted proxy to overwrite headers; variable hop counts can expose spoofing. | Request identity must bind to a verified ingress chain. Never prescribe trust proxy true or a guessed hop count. | Express proxies |
| Tailscale ACLs/grants follow deny-by-default semantics, but a new tailnet starts with broad communication and omitted ACL policies may invoke default allow-all. ACLs do not govern local-network access. | Inspect actual policy and non-tailnet paths. Do not infer isolation merely from using Tailscale. | Tailscale ACLs |

## Derived workflow policy

The guides derive a selection process from these constraints: one row per actual flow, one control per stated boundary, application authorization independently reviewed, and target-specific proof separated from design. Failure handling, thresholds, cost ceilings and rollback authority are decisions requiring actual workload/owner facts, not vendor facts established here. Framework-specific implementation must be refreshed by its selected owner.

## Thin evidence and retained gaps

The Vercel web reader returned `Internal Error` for its rate-limit page during research. Existing source Vercel ownership is known, but this archive makes no new Vercel capability/plan/default claim. Other clouds, OS firewalls, API gateways, load balancers and DDoS service specifics require current exact product evidence. No universal protection, price, latency, throughput or legal-compliance guarantee follows from this digest.
