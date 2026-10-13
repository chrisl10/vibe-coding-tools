# Network Boundaries routing proposal

Plugin owner: infrastructure-decision-tools; prerequisite wasp-nest-core. Proposed source Stinger: packs/infrastructure-decision-tools/skills/network-boundaries-stinger/SKILL.md. Proposed source Drone: packs/infrastructure-decision-tools/agents/network-boundaries-wasp-drone.md. These are proposed canonical paths, not existing registration proof; parent promotes the staged owner tree.

## Trigger phrases

- Which firewall, WAF and rate-limit layers fit this topology?
- Where should public, private and admin traffic be controlled?
- Can clients bypass the proxy or spoof the rate-limit identity?

## Do NOT route when

- Hosting/provider topology selection: Infrastructure Fit.
- Actual Vercel controls or tailnet policies: selected Vercel/Tailscale owners under action authorization.
- Authorization/security audit: Core Security.
- Costs: selected Operating Cost.
- Unsupported provider or OS firewall implementation: precise OWNER_GAP; do not invent another owner.

## Inputs and outputs

Actual topology/revision, environments/providers/plans, proxy chain, listener protocols and addresses/ports, authenticated identity, bursts, costs and outage/recovery authority. Missing material facts produce one provisional recommendation and UNKNOWN rows. Output is read-only chat advice, flow/control worksheet and owner/proof handoff; orchestrator saves authorized reports.

## Sequence and directives

Infrastructure Fit supplies topology; this pair selects boundary controls; selected implementation owners and Security receive the handoff. Resolve selected plugin/version/paired skill through trusted Core before installed dispatch. No cached sibling, rule edit, installer, provider change or runtime enforcement claim. Parent must register roster/catalog/command and run ordered gates before qualification.
