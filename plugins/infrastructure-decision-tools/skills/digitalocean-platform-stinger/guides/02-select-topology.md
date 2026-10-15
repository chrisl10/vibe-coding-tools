# Select one eligible topology

Read the [digest](../references/research/distilled-digitalocean.md) and [responsibility map](../references/service-responsibilities.md). Compare the same supplied workload across App Platform and Droplets, with managed PostgreSQL evaluated separately. Reject hard mismatches before discussing price.

For an eligible stateless HTTP app whose owner cannot operate servers, provisionally recommend App Platform with external durable state. Check build/image, native architecture/syscalls, job lifecycle, selected region and scaling eligibility; never equate managed infrastructure with managed application security. An unresolved hard dependency blocks a supported fit claim.

For a workload that requires an OS feature or durable filesystem App Platform cannot provide, consider a Droplet only when operator coverage, hardening, patching, backups, recovery and monitoring are credibly assigned. If that capacity is absent, return UNRESOLVED_FIT and route Infrastructure Fit for a different managed design. Cheap compute does not supply an operator.

Managed DB is an independent decision. Use features, limits and dated pricing/transition. Verify edition, connection budget/pooling, engine/extension constraints and future create date. A standby is not a cross-region DR plan; a replica is not a tested restore. If region or legal residency evidence is missing, preserve it as blocking rather than equating a CDN-facing IP with data location.

Document one recommendation and why the other eligible track loses for this workload. Specify validation needed before adoption, data/network boundaries, operator duties, recovery/exit and a supplied measurable review trigger. No provisioning commands, shell scripts, Terraform, account probes, secret reads or deploy button use belong in this workflow.
