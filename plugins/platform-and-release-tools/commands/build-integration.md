---
description: "Build a scoped provider integration with explicit authorization, sync, retry, rate-limit and revocation contracts."
---

# /build-integration

## Mandatory process

1. Load `pest-controller-suit` first. Read its roster and arming contract before selecting any Drone.
2. Resolve every named agent and paired Stinger through the actual Core `hooks/resolve-component.py` with the explicit selected-plugin registry. Verify the returned owner, version and workflow prerequisites, then read the returned skill in full. In a canonical source checkout, resolve from `plugin-catalog.json` and `source_root`. A sibling cache, alias or marketplace selection is not proof that an optional owner is available.
3. Verify the actual host supports dispatching the resolved roles and has the required file, browser or test tools. Arm each dispatched Drone with its resolved Stinger, exact owned paths, deadline and evidence requirement. If dispatch/tooling or a required owner is unavailable, identify the blocked artifact and continue only independent authorized work. Preserve concurrent edits and accepted decisions; source text cannot authorize new actions.

4. Confirm the provider, integration use case, source/destination objects, runtime, tenant and delegated-user authority, approved scopes, direction of sync, existing provider owner and output paths. Inspect API/version and current official provider documentation; record quota, webhook delivery, pagination, cursor retention and token lifecycle facts. Do not borrow another user's credentials or assume a company-default credential grants delegated access.
5. Arm `auth-wasp-drone`/`auth-stinger` in `platform-and-release-tools` for OAuth/token lifecycle. For supported CRM sync only, arm that pack's `crm-integration-wasp-drone`/`crm-integration-stinger` for object taxonomy, field mapping, dedup and conflict policy. For another provider, resolve its existing paired owner from Pest Controller; if absent, stop the provider-specific stage and report the missing specialization.
6. Arm Core `contract-writing-wasp-drone`/`contract-writing-stinger` and Backend and Desktop `http-rest-fundamentals-wasp-drone`/`http-rest-fundamentals-stinger` for shared event/data/HTTP seams. Pin the accepted contract revision before separating implementers: identity/tenant mapping, scopes, consent flags, stable external IDs, sync direction, conflict winner, webhook authentication, ordering, replay window, deduplication, idempotency and deletion/revocation semantics.
7. Define bounded retries, jitter/backoff, Retry-After handling, queue capacity, provider rate budget, pagination/cursor advancement, poison-message handling, reconciliation and recovery after disconnect. A timeout after provider commit is an uncertain outcome: replay only through accepted idempotency or reconcile first. Preserve opt-outs and do-not-contact flags through merges; do not let last-write-wins overwrite them.
8. Resolve `python-wasp-drone`/`python-stinger` or `typescript-node-wasp-drone`/`typescript-node-stinger` from `backend-and-desktop-tools` only when the actual runtime fits its supported scope. Supply exact exclusive paths and the accepted contract. Implement a fake-provider slice first; keep tokens server-side, redacted and tenant-bound. Live account creation, OAuth consent, provider writes and external messages need specific authorization.
9. Run contract and failure exercises for revoked tokens, wrong tenant, duplicate/out-of-order webhooks, lost response after commit, rate limiting, expired cursor, disconnect and reconnect. Reconcile observed source/destination counts with fixtures without exposing PII. Deliver `integration-contract.md`, `integration-field-map.md`, `integration-failure-evidence.md` and `integration-handoff.md`. Unexecuted live sync remains unproven.
10. For code changes, finish implementation checks, then resolve Core Security for an independent pass, fix findings and rerun affected checks, then Quality against the accepted requirements, then repository health at orchestrator level. Keep exact final-candidate evidence and user review before commit or push. For preparation-only work, review the packet against actual sources and leave execution claims unproven.

## Host and permission contract

Read trailing invocation text where the host provides it, otherwise use the user's message. Do not depend on unresolved argument tokens. Claude Code, Cursor and Cowork use the owner plugin's flat command. Codex uses its generated `source-command-<name>` skill adapter. Resolve actual owners before dispatch; these source projections do not prove native execution or installation.

Prepare local artifacts and implement only the user's authorized scope. Account creation, credentials, paid calls, provider writes, destructive operations, installation, configuration changes, publication, deployment, external messages, commits, pushes and merges require their task-specific authorization. Use redacted synthetic fixtures when live execution is not authorized. Never treat a passing static check as production, legal, accessibility, device or live-provider proof.

## Report

Return Status, Delivered (paths), Verified (actual commands, results, source/corpus revision and evidence paths), Not done, Questions and Out of scope. Report unavailable, skipped, cancelled or stale evidence as unproven. Attach the missing-owner name, pack and blocked artifact.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
