# Fictional decision exercise
This example is unexecuted and fictional. It proves neither native operation nor a customer's platform suitability.

Supplied scenario: two-person team, container-compatible Node API and continuous queue worker, external managed Postgres, no local durable files, users near Virginia, retryable jobs, moderate but unmeasured traffic. Owner accepts one-region service recovery while requiring external DB export; budget and latency target are still unknown.

Recommendation: provisional Railway persistent services for API and worker. The service model fits their lifecycle, and the archived Virginia region is a geographic candidate. The worker is not a cron task because it runs continuously. Runtime compatibility, resource demand, DB endpoint exposure/latency and region entitlement still need validation. Services, regions, cron

External DB connectivity is not assumed to be Railway private DNS. Private service communication applies within a Railway project environment. Keep the API stateless rather than attaching a volume merely because it is available. Network, volumes

Cost handoff: collect low/base/high RAM-time, CPU-time and outbound GB for both services plus external DB rates and operator labor; apply included usage once to aggregate eligible Railway charges. No numeric bill is produced because quantities and real plan evidence are missing. Plans

Owners: app team for image updates, graceful shutdown, retries, monitoring and incident response; selected DB owner for backup/export/restore consistency; Operating Cost for budget envelope. Actual Railway deployment owner remains a catalog-resolution gap until supplied. Acceptance waits for budget, latency, RPO/RTO and workload measurement. No service was created.
