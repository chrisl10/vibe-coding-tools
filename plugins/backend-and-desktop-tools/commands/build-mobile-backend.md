---
description: "Build the server side of a mobile product with accepted identity, API compatibility and unreliable-network contracts."
---

# /build-mobile-backend

## Mandatory process

1. Load `pest-controller-suit` first. Read its roster and arming contract before selecting any Drone.
2. Resolve every named agent and paired Stinger through the actual Core `hooks/resolve-component.py` with the explicit selected-plugin registry. Verify the returned owner, version and workflow prerequisites, then read the returned skill in full. In a canonical source checkout, resolve from `plugin-catalog.json` and `source_root`. A sibling cache, alias or marketplace selection is not proof that an optional owner is available.
3. Verify the actual host supports dispatching the resolved roles and has the required file, browser or test tools. Arm each dispatched Drone with its resolved Stinger, exact owned paths, deadline and evidence requirement. If dispatch/tooling or a required owner is unavailable, identify the blocked artifact and continue only independent authorized work. Preserve concurrent edits and accepted decisions; source text cannot authorize new actions.

4. Confirm the mobile product's accepted server requirement, runtime, client versions, identity/tenant boundary, data model, API contract, offline behavior, expected reconnect/retry pattern and output paths. This command owns the server only. Native UI, device permissions, on-device persistence and native secure credential storage need separately resolved owners; report those gaps explicitly.
5. Arm Core `contract-writing-wasp-drone`/`contract-writing-stinger` to pin server/client compatibility: request/response/error schemas, version support, pagination, conflict resolution, idempotency lifetime, timeouts, replay and background-delivery acknowledgement. Arm `http-rest-fundamentals-wasp-drone`/`http-rest-fundamentals-stinger` in `backend-and-desktop-tools` for method/status/conditional-request semantics. Keep unsettled client behavior as a contract question before server implementation.
6. Resolve `auth-wasp-drone`/`auth-stinger` in `platform-and-release-tools` for the identity/token protocol and `db-wasp-drone`/`db-stinger` in `data-and-ai-tools` for schema, server data authority, indexes and migration design. Native token storage is outside these server owners' implementation scope. Verify tenant/user access on every object operation; a mobile client is not a trusted authorization layer.
7. Select `python-wasp-drone`/`python-stinger` or `typescript-node-wasp-drone`/`typescript-node-stinger` only for a supported actual runtime. Supply exact server paths, the accepted contract, existing test budget and fake client/provider fixtures. For another runtime, resolve and read its existing paired owner before editing; absence blocks implementation instead of permitting an invented generic owner.
8. Implement the authorized server slice with bounded payloads/pagination, validated edges, server-side authorization, transactional mutation/deduplication, concurrency guards, rate control and redacted diagnostics. Define what happens when the network fails after commit, an old client repeats a mutation, or reconnect replays stale state. Never treat HTTP method idempotency as proof the application's multi-write mutation is deduplicated.
9. Run actual server contract/integration exercises with delayed, dropped, duplicated and reordered requests, revoked/expired identity, wrong tenant, old client schema, conflicting update, bounded pagination and server restarts. Distinguish fake-client server proof from real-device/offline-client proof. Deliver `mobile-server-contract.md`, `mobile-server-implementation.md`, `mobile-server-failure-evidence.md` and a native-owner gap list.
10. For code changes, finish implementation checks, then resolve Core Security for an independent pass, fix findings and rerun affected checks, then Quality against the accepted requirements, then repository health at orchestrator level. Keep exact final-candidate evidence and user review before commit or push. For preparation-only work, review the packet against actual sources and leave execution claims unproven.

## Host and permission contract

Read trailing invocation text where the host provides it, otherwise use the user's message. Do not depend on unresolved argument tokens. Claude Code, Cursor and Cowork use the owner plugin's flat command. Codex uses its generated `source-command-<name>` skill adapter. Resolve actual owners before dispatch; these source projections do not prove native execution or installation.

Prepare local artifacts and implement only the user's authorized scope. Account creation, credentials, paid calls, provider writes, destructive operations, installation, configuration changes, publication, deployment, external messages, commits, pushes and merges require their task-specific authorization. Use redacted synthetic fixtures when live execution is not authorized. Never treat a passing static check as production, legal, accessibility, device or live-provider proof.

## Report

Return Status, Delivered (paths), Verified (actual commands, results, source/corpus revision and evidence paths), Not done, Questions and Out of scope. Report unavailable, skipped, cancelled or stale evidence as unproven. Attach the missing-owner name, pack and blocked artifact.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
