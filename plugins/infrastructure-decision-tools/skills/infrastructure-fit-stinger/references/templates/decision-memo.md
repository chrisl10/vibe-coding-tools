# Infrastructure decision memo

Date and workload reference: [same intake used for every candidate]
Recommendation: [ONE topology and why it fits the hard constraints]
Status: [supported recommendation, provisional, or blocked; missing facts]

| Candidate considered | Eligibility evidence | Reason retained/rejected | Cost/proof limitation |
|---|---|---|---|
| [provider/service/plan/runtime/region] | [official source/date + workload comparison] | [concrete discriminator] | [unpriced/unknown/test pending] |

Selected components: request/static compute; worker/job compute if needed; DB; object storage; network/access; secrets; monitoring/support. Name only required pieces. Application/environment separation and ownership: [who does what].

Cost handoff: [selected Operating Cost owner, normalized workload, dated rates/units/region/currency, floor/included usage, storage/egress/backups/support, low/base/high assumptions, separately valued operator time]. If that owner/rates are unavailable, say totals unavailable and what is missing. Do not invent arithmetic or pricing.

Recovery: [failure, backup scope/retention, restore target, owner, evidence request]. Exit: [data/export/dependencies, downtime/egress/operator work]. Expansion triggers: [measured metric + threshold supplied by owner/source, action, reviewer]. A threshold invented for illustration stays a fictional assumption.

Deferred components: [layer, reason, event that would justify it]. Source limits: [failed retrievals, unsupported regions/rates/performance]. Acceptance needed: [specific owner decision, not automatic provisioning permission].
