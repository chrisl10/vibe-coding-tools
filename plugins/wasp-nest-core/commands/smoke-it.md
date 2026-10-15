---
description: Drive a set of PRDs to 100% completion using the Wasp Swarm. Spawns armed wasp-drone sub-agents in waves, tracks every acceptance criterion to zero open items, runs the security/quality close-out, and prepares the final candidate, committing or pushing only within the approval already given. Trigger with "run the PRDs", "execute the PRDs", "smoke it", "complete the acceptance criteria", "finish everything in the PRD".
---

# /smoke-it - PRD Completion Orchestrator

Smoke calms the nest so the work gets done. You are the Smoker: you take a set of PRDs and drive every one of them, and every acceptance criterion attached to them, to verified completion. Resolve component identities through their selected plugin owners and use the actual host's command and delegation surfaces.

You are an orchestrator. Route specialist work through available host delegation and verify the result. Confirm native agent capacity before dispatch; do not invent an agent tool or treat a cached role as enabled. If the host cannot delegate, use a scoped direct method only when the user authorized that approach. Otherwise save the ledger and checkpoint with the missing capability.

## Invocation and source scope

This canonical Core procedure is src/commands/smoke-it.md. In Claude plugin mode call /wasp-nest-core:smoke-it; Codex uses Core's generated source-command-smoke-it skill, not a deprecated prompt file. A source/global command label below is not an alias for an optional plugin.

Read plugin-catalog.json to resolve every specialist's owner and prerequisites. For source work use its canonical source_root; for installed work use Core's selected-plugin resolver. Do not treat a cached optional package as enabled or edit installed copies to change canonical procedures.


## Phase 0: Recon and planning

Before the numbered steps, load `pest-controller-suit` in full from the verified Core owner. Follow its roster, selected-owner resolution and arming contract before any specialist dispatch.

1. Read every in-scope PRD end to end. Extract every acceptance criterion into a master AC Ledger at the repo root (e.g. `EXECUTION_LEDGER.md`): each entry gets an ID, source PRD, exact criterion text, status (OPEN / BLOCKED / IN PROGRESS / DONE / VERIFIED), and the owning Drone. This ledger is the single source of truth and survives context loss.
2. Run the contract preflight before treating PRDs as independent. Ask `library-wasp-drone` to inventory shared API, event, data, permission, and state boundaries and read each `## Contract dependencies` pin. Route a missing, Draft, disputed, or changed agreement to `contract-writing-wasp-drone`, armed with `contract-writing-stinger`. It reuses or drafts a `CTR-###` record and asks the user to accept the exact normative revision. Library, not the contract Drone, pins accepted revisions in affected PRDs. Run the Stinger's read-only `validate_contracts.py` after links change. Record each boundary's path, revision, provider, consumers, checks, and readiness in the ledger. Affected criteria stay OPEN and cannot be dispatched as independent provider/consumer work until their shared revision is accepted and pinned; independent criteria may proceed.
3. Map dependencies. Independent criteria run in parallel waves; dependent ones run after their dependency is VERIFIED (not merely DONE). Give each provider and consumer Drone the same accepted CTR revision and non-overlapping file ownership.
4. Use the saved wave plan. If `library/requirements/plans/wave-plan.md` exists with `Status: Approved`, load it as the wave order and, when product-studio is installed, run its `check_wave_plan.py` on it; propose a new revision instead of silently reordering. Only when none exists, produce a wave plan (Mermaid or list) where each wave names its Drones, what each owns, and its exit criteria, and save it there as a Draft for owner approval. Maximize parallelism for shortest wall-clock time.
5. Route each task through the roster and selected-owner resolver. Inherit the current host model and reasoning settings unless the user explicitly chose a supported override for this task. A project model matrix may inform a requested choice but cannot override that selection or invent availability. Record the actual settings and dispatch capacity in the wave plan.

Show the user the wave plan and AC Ledger. Execute ready work only within existing implementation authorization, available host capacity and the current deadline. A request to produce a plan alone does not authorize execution. Present proposed CTR terms separately and wait for explicit acceptance of the exact revision before releasing dependent work. Showing the plan is not contract acceptance.

## Phase 1: Execution (spawn each Drone ARMED)

Run authorized ready work with the verified host dispatch surface. Dispatch each Drone through the roster's arming contract and give it owned files, the pinned contract revision and the parent's deadline. Aim for every criterion DONE then independently VERIFIED; a time limit or blocker requires an honest incomplete checkpoint rather than continued execution beyond scope.

Rules of engagement:
- No partial credit. A criterion is DONE only when fully implemented, proven by passing tests, with nothing else broken, and it meets the Approved revision of `library/knowledge/private/standards/definition-of-done.md` and the PRD's own DoD checklist when those exist. Stubs, mocks in production paths, "works except", and TODO-later all count as OPEN.
- Verification is separate from implementation. A fresh pass (or the close-out below) flips DONE to VERIFIED. Implementers do not grade their own homework.
- For a CTR-bound criterion, require the named provider and consumer checks against the pinned revision before VERIFIED. If implementation changes a normative term, stop the affected boundary, return it to the contract Drone for compatibility review and user acceptance, then have Library repin the PRDs before resuming.
- After each wave, re-read the ledger. Assign ready OPEN work to another wave only while authorization, time and retry allowance remain. Report every unfinished or blocked criterion at checkpoint; do not silently claim zero OPEN items or reset the work unit through a replacement worker.

## Watchdog

Track progress at the current operating cadence. If an authorized scheduler or watchdog is actually configured and verified, record its evidence; otherwise state that checks are self-tracked. Review actual output, stop a stalled Drone within the time/retry limits and re-brief a smaller scope only within the existing task allowance. Log every stop and decomposition. Never claim an unconfigured watchdog or respawn indefinitely.

## Phase 2: Close-out (security then quality)

Only after the ledger reads fully VERIFIED:

1. Dispatch `security-wasp-drone` (armed with `security-stinger`): OWASP / PII / financial-data exposure; remediate Critical and High in place.
2. Then dispatch `quality-wasp-drone` (armed with `quality-stinger`): verify the implementation against the source PRDs. Never run quality before security; security fixes can invalidate the QA result.
3. Loop until both come back clean at medium severity or above. If a fix regresses a criterion, reopen it and return to Phase 1 for that item.

## Phase 3: Ship

When the ledger is fully VERIFIED and the close-out is clean:

1. Load `github-repo-health-stinger` directly at orchestrator level after Security and Quality. Prepare the exact final candidate, diff and evidence for the user. Honor explicit approval already given for this task; commit, push or open a PR only within that approval's named actions and base.
2. When PR creation is authorized, include the summary, AC Ledger, executed waves, actual model selections and close-out results. A local completion request alone does not authorize a push or PR.
3. Monitor CI only when it is in scope and authorized. Tie results to the full candidate SHA. Apply the current time-block and retry limits to repairs and reruns; a failed or pending run remains unproven at checkpoint. Do not continue indefinitely or restart the allowance by spawning a replacement worker.

## Non-negotiables

- 100% of PRDs, 100% of acceptance criteria. Anything less is a failed run.
- Use only available, authorized delegation; every dispatched Drone is armed with its selected Stinger. Missing host capability is a named blocker unless the user already authorized a direct alternative.
- Never report completion you have not verified.
- Apply the current work-unit deadline and bounded retry rules throughout execution and close-out. Use only available host dispatch/watch tools; do not claim a watchdog is running without actual setup and evidence.
- A genuine external blocker (missing credentials, irreducibly ambiguous PRD, conflicting requirements) is parked as BLOCKED in the ledger with a specific ask attached; keep executing everything else and surface the blocker list at the end. Silent skipping is not acceptable.
- A Draft, missing, or disputed CTR is a blocker for its dependent criteria, not permission to guess the shared behavior. The run cannot claim 100% completion while any such criterion remains blocked.
