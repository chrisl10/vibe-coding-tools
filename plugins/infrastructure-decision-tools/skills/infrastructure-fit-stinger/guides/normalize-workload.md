# Normalize the workload

1. Read the intake worksheet and supplied product decisions. Ask missing material questions about runtime, job duration/state, data, geography, recovery promise, budget and operator capacity. Do not make price comparison before the work is comparable.
2. Separate static delivery, HTTP requests, completion jobs and continuous workers. Preserve CPU versus wall time, memory, binary/OS needs and persisted versus ephemeral state.
3. Record low/base/high traffic/storage/egress estimates in consistent units, with measured versus assumed status. Paid users change support/recovery needs; they do not establish traffic or SLA automatically.
4. Record hard constraints before preferences. Treat user concerns about AWS price/GCP complexity as constraints to evaluate through the actual services and skill burden.
5. Return the normalized worksheet and only blockers that change selection. Do not interrogate the user about irrelevant services.

Grounding: Cloud Run workload types, Workers CPU/wall limits, AWS architectural review. Intake design derives from the locked topic.
