# Qualify Railway against the workload
Read the [digest](../references/research/distilled-railway.md) and [worksheet](../references/templates/fit-worksheet.md). Record supplied facts, estimates and unknowns separately. Obtain runtime/version, container architecture/native libraries, start command, HTTP ports, persistent versus completion lifecycle, concurrency, job duration/schedule, CPU/memory demand, state paths, DB topology, external integrations, user/data regions, traffic/egress, budget and named operator.

1. Persistent API or queue worker is a container-service candidate; a terminating scheduled task is a cron candidate. Container support alone does not prove a native binary or privileged workload. Services evidence
2. For cron, inspect exit/connection closing and overlap expectations. Reject sub-five-minute schedules and exact-minute promises; a running prior job skips the next. Require idempotency/retry ownership separately. Cron evidence
3. For persistent state, map every write path to external DB/storage or one attached volume. Replicated service plus attached volume is incompatible with the archived constraint; return the topology to Infrastructure Fit before choosing. Volume evidence
4. Match the requested location to a sourced region and qualify data placement independently. Exact residency or regulatory approval cannot be inferred from a region name. Region evidence
5. Mark each hard requirement eligible, rejected or unresolved. A missing actual workload yields a provisional candidate or one batched question, never a firm Railway selection. Give one recommendation only after eligibility, operator and recovery requirements are supplied.

Output the completed worksheet with decisive constraints, exclusions and the smallest missing fact that changes the decision. Follow [operations and recovery](03-decision-and-handoff.md) before acceptance.
