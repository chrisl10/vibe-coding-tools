# Traffic capacity
O173 measured traffic-spike planning. Specialist owner: platform-and-release-tools. Pair: traffic-capacity-wasp-drone. Runtime reads supplied metrics and produces an advisory packet. Existing Capacity Planning owns staffing and make/buy decisions.

| Work | Read |
| --- | --- |
| Measurement quality and bottlenecks | [guide 01](guides/01-measure-traffic-and-bottlenecks.md) |
| Units, constraints, SLO and cost | [guide 02](guides/02-bound-capacity-slo-and-cost.md) |
| Admission, recovery, future acceptance | [guide 03](guides/03-propose-admission-recovery-and-validation.md) |
| Complete field contract | [worksheet](references/templates/measurement-worksheet.md) |
| Arithmetic and negative branches | [fictional packet](examples/fictional-spike.md) |
| Facts and provenance | [digest](references/research/distillation.md), ledger |

Resolve installed owners through trusted Core's selected-plugin registry before handoff: Sentry for instrumentation/sampling/alerts, Vercel and DevOps for platform/implementation, Operating Cost for dated billing model, DB for query/pool design, Security for privacy/tenant/abuse policy. Missing optional selection is a gap, not implicit installation. Source work consults root plugin-catalog.json. No new benchmark framework, probe, load execution, provision/autoscaler change, spending or credential access is authorized by this skill. Construction checks remain separate from native and target execution.
