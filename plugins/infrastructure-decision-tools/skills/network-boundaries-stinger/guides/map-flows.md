# Map the actual paths

1. Obtain the topology revision, environments, regions, domain/origin names, network boundaries and selected providers. Ask for material missing facts. If none are supplied, return a provisional memo, with every actual address, port, association and policy UNKNOWN.
2. Fill the [flow/control worksheet](../references/templates/flow-control-worksheet.md). Include public HTTP APIs, non-HTTP ingress, operator/admin access, service-to-service links, database/storage links, DNS/updates/provider APIs, workers/webhooks and return paths. Record where TLS terminates and what reaches each hop. Do not invent listening ports.
3. For every hop record initiator, authenticated principal, protocol, actual destination, allowed purpose and data sensitivity. Distinguish app tenant/user identity from a network address, shared proxy or device identity.
4. Trace direct origin access, alternate domains, IPv6, health checks, admin routes, failover and local-network paths. A diagram does not prove those paths are blocked. Tailscale policy does not itself constrain local-network traffic.
5. Mark facts SUPPLIED, SOURCE_CAPTURED, DERIVED or UNKNOWN and pin the artifact revision. Give Infrastructure Fit unresolved hosting changes rather than selecting a new hosting architecture here.

Grounding: AWS resource associations/state, subnet crossings/return flow, origin bypass, tailnet limits. The worksheet and classifications are derived procedure, not tested controls.
