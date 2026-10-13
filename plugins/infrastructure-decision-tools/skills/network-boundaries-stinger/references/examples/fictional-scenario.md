# Fictional paid document service

Synthetic facts: public HTTP API behind an edge proxy, worker calling a paid conversion provider, private database, operators using a tailnet. Provider, plan, exact addresses/listeners, port numbers, session system and load are unspecified. This is an authored reasoning case, not a customer topology or executed test.

ONE provisional recommendation: keep public HTTP abuse controls at the verified edge path, use server-authorized tenant/operation admission before starting costly conversion work, and separately constrain operator/service reachability at the actual network boundaries. Infrastructure Fit retains hosting selection; selected runtime/provider owners implement each decision. Security verifies tenant/authorization and alternate-origin coverage.

| Flow | Proposed control and reason | Unknown preventing implementation |
| --- | --- | --- |
| Public to edge to API | WAF/rate mitigation at the actual HTTP ingress; proxy identity validated from a trusted chain | Edge plan/attachment, bypass origin, forwarding behavior, real burst distribution |
| Authenticated user to conversion job | Application admission tied to verified tenant/operation and bounded work before provider expense | Session/tenant source, durable queue/idempotency and limit-store/outage decisions |
| Worker to provider; API to DB | Reachability/egress decision for named protocols/endpoints, with return flow recorded | Actual network, endpoint churn, DNS/metadata constraints, provider capabilities |
| Operator to administration | Review actual tailnet policy and separate app/admin authorization | Actual identity/policy, tags/routes, non-tailnet path, recovery authority |

No limits, open ports or default allowlist are guessed. Edge counter lag means it cannot prove an exact paid-work ceiling. A shared proxy source address is not a tenant. Tailnet presence does not prove private admin traffic. All traffic/enforcement/penetration proof: NOT_RUN.

Grounding: [Cloudflare counter lag](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/network-boundaries-stinger/references/research/raw/cloudflare-rate-limits.txt), [proxy/origin](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/network-boundaries-stinger/references/research/raw/cloudflare-origin.txt), [identity trust](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/network-boundaries-stinger/references/research/raw/express-trusted-proxies.txt), [tailnet defaults](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/network-boundaries-stinger/references/research/raw/tailscale-acls.txt). Remaining statements are derived recommendations under the synthetic assumptions.
