# Review recovery, exit and expansion triggers

1. Name outage, lost-data, overload, provider incident and operator-unavailable failure modes relevant to the product. Use owner-approved recovery time/data-loss targets or mark them unresolved.
2. Describe who detects, communicates, restores and verifies recovery. Separate provider features from rehearsed application recovery. No unsupported high-availability/SLA claim.
3. Specify exit data format/dependency inventory, export/egress, migration downtime and operator tasks. "Portable container" alone does not prove portable identity/storage/database semantics.
4. Define review triggers from measured load, budget variance, observed latency/errors, job backlog or required capabilities. Thresholds need owner/source evidence; fictional examples remain assumptions.
5. Return the decision memo and deferred layers with concrete triggers. A trigger authorizes reassessment, not automatic purchase, migration or production change.

Grounding: [AWS architecture review](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/infrastructure-fit-stinger/references/research/raw/aws-framework.html), [Supabase availability/recovery concerns](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/infrastructure-fit-stinger/references/research/raw/supabase-prod.html), [runtime limits](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/infrastructure-fit-stinger/references/research/raw/vercel-functions.html). Exit/triggers are the locked topic's decision contract.
