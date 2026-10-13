# Four infrastructure decisions and failure exercises

These are fictional workload decisions, not current quotes, benchmarks or deployments. They apply the workflow contract to the archived provider capabilities. Real recommendations need exact plan/runtime/region evidence and the selected Operating Cost model.

## A: minimal website

Workload: static brochure files, no login/data/payment/runtime search; owner wants a public address and has no server operator. Recommendation: Cloudflare Pages static delivery. It fits a static site track without requiring a VM, SQL/vector DB, auth service or worker. Use the Pages archive for supported deployment shape; domain/TLS and plan eligibility need current scoped qualification.

Owner responsibilities: approved content/rights, domain access, release review, support contact and rollback evidence. Costs: unresolved until the actual plan/usage/domain rates are handed to Operating Cost; "static" is not proof of zero cost. Expansion trigger: accepted dynamic data/payment feature, then reassess compute/data. Exclude load balancer/Terraform/Tailscale absent a real topology need.

Failure candidate: "Use a VPS plus database and firewall because production requires servers." Reject the unsupported requirement and extra operator burden. Recovery: retain the minimum static track and state which accepted feature would justify more components.

## B: paid web app

Workload: SvelteKit HTTP requests, customer records in SQL, short measured request execution, no long worker or arbitrary OS requirement; small team familiar with managed deployment. Recommendation: Vercel request hosting plus managed Neon Postgres, conditional on exact runtime/plan/region and connection/recovery qualification. The archive supports function limits and managed Postgres shape, not the user's availability promise.

Responsibilities: app auth/tenant/payment correctness, chosen DB schema/migrations, connection capacity, backup/restore evidence, billing/egress budget, alerts/support. Keep production/test identities separate. Costs: Operating Cost receives traffic/duration/memory/data/egress/backups/logs plus rate evidence and operator hours; totals unknown before its report. Expansion trigger: request limits, sustained DB connection saturation or accepted long-running jobs, using measured evidence and owner-set thresholds.

Failure candidate: "The platform autoscaling means no outages, support or backups are needed." Reject. Managed infrastructure does not prove application recovery or eliminate downstream limits. No SLA is promised from provider overviews.

## C: scheduled completion worker

Workload: a containerized batch task runs to completion on a schedule, can restart/retry safely under its accepted job contract, and exceeds the qualified HTTP-handler limits; no singleton device/kernel dependency. Recommendation: Cloud Run job for completion execution, with request frontend only if the product also needs it. This is a job lifecycle, not an endlessly running HTTP handler. Continuous queue consumers would require reassessing a worker-pool/service track.

Responsibilities: job idempotency/retry/queue contracts, persistence/results, scheduler owner, task duration/resources, failure alerts and recovery. Exact execution/region/quota/current-price eligibility is unresolved until official chosen-plan data is captured. Costs: job runs/resources/storage/egress plus operator time are Operating Cost inputs. Expansion trigger: continuous ingestion or job backlog beyond the owner-approved target.

Failure candidate: "Workers means unlimited native background CPU." Reject. Workers distinguishes CPU/wall time and invocation types; its name does not establish required native/runtime/lifecycle behavior. Missing resource/runtime evidence is a blocker.

## D: backend needing host control

Workload: a Go/Rust native service requires a documented OS/device/kernel capability that the reviewed managed tracks have not established; a named Linux operator can patch, harden, observe and restore it. Recommendation: qualify a DigitalOcean Droplet VM topology for the required host control, using a separately managed SQL service if accepted persistence needs it. Droplets documentation supports Linux VM shape, not the exact capability or throughput; those proofs remain blockers before acceptance.

Responsibilities: host patching/SSH/access policy, service supervision, TLS, backups, recovery, application security, observability/on-call and release rollback. Do not infer that Go/Rust always needs a VM; a plain HTTP native container would reopen managed-container fit. Costs: VM/storage/network/recovery/support plus explicit operator time go to Operating Cost. Exit: rebuild automation and portable state export evidence; no automatic migration.

Failure candidate: "Vultr is cheapest and supports the required capability." Reject because the relevant Vultr source failed retrieval and no current rates/control proof exists. Keep it unqualified/unpriced, with the exact source needed. AWS expense and GCP complexity are also compared using this workload/operator evidence rather than universal labels.

## Exercise record

For each case recover workload, single topology, decisive fit, remaining eligibility/cost proof, operator and expansion trigger. Encoded self-checks validate one recommendation, unknown-cost preservation and refusal of unsourced eligibility. They are structural/contract exercises, not model-generated recommendation tests, runtime benchmarks or human review.
