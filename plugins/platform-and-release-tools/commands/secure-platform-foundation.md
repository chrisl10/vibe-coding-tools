---
description: "Prepare and implement an authorized platform foundation with identity, secrets, environment and data-access boundaries."
argument-hint: "[product/repository] [outcome and constraints]"
---

# /secure-platform-foundation

## Mandatory process

1. Load the installed `pest-controller-suit` Core skill and consult its roster before making any routing decision. This is the first instruction, always, no exceptions. Source work resolves component ownership from root `plugin-catalog.json`; installed work uses Core's explicit selected-plugin registry and resolver. Missing Core blocks routing. Load each selected pair's Stinger and required guides before work, and verify actual host tools/delegation. Cached files do not prove selection. Dispatch registered Drones at top level only when delegation is authorized; otherwise execute the selected paired procedure directly and report that fallback truthfully. No invented roles or nested dispatch.

2. Confirm authorized repository/environment scope, existing identity/provider/runtime, tenant model, data-access paths and secret injection mechanism. Read manifests, redacted environment-name examples and architecture before recommending changes. Inventory names and purpose of secrets without retrieving or printing values.
3. Route provider/session/RBAC decisions to auth-wasp-drone; route WorkOS depth to workos-wasp-drone only when WorkOS is selected. Route data schema and tenant-access requirements to db-wasp-drone in data-and-ai-tools. Doppler work belongs to doppler-wasp-drone only when the user has chosen it; raw environment injection does not silently authorize adding Doppler.
4. Have library-wasp-drone specify authentication, authorization, tenant membership, administrative/service identities, logout/revocation, recovery and environment separation. Have contract-writing-wasp-drone freeze shared identity/session/tenant claims and consumer denial behavior. Pin the same accepted CTR revision into provider and consumer requirements before implementation.
5. Assign implementation to actual selected runtime owners, with separate files. Authentication alone is not authorization: require tenant-scoped checks at server/data boundaries and deny untrusted caller-supplied actor/tenant claims. Require tests for anonymous, wrong-role, removed-member and cross-tenant access. If the framework/provider adapter lacks an implementer, stop only that boundary and name the missing owner.
6. Prepare source changes for secret-name mapping, server/client exposure restrictions, environment separation and failure handling within authorization. Account creation, credentials, provider permissions, environment writes, sync, rotation, infrastructure apply and deploy require their applicable explicit approval. Do not infer these effects from permission to draft or edit source.
7. Verify the affected source boundary using relevant local checks and scoped denial cases. security-wasp-drone reviews first; resolve findings and re-evaluate the changed candidate before quality-wasp-drone checks requirements. The orchestrator then loads github-repo-health-stinger. Record untested provider behavior and native-host limits without calling the platform secure solely because static checks pass.

## Selected-owner map

| Capability | Catalog owner | Activation |
|---|---|---|
| `pest-controller-suit` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `library-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `contract-writing-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `security-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `quality-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `github-repo-health-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `auth-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `doppler-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `workos-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `db-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |

## Inputs and host qualification

Use trailing invocation text exposed by the actual host; `$ARGUMENTS` is supported only where documented. Reuse answered inputs and accepted decisions. Ask one concrete batch for unresolved material inputs before dependent work, while continuing independent authorized work. Claude/Cowork uses the owner flat command, Cursor its generated command projection, and Codex the owner's generated `source-command-secure-platform-foundation` skill. Source generation is not installation, role discovery, or runtime proof. Resolve all resources against the selected carrier root. A missing required owner blocks its dependent boundary and is named in the report; optional branches require only their own selected dependencies.

## Output contract

Write advisory evidence to the receiving repository's `library/requirements/reports/secure-platform-foundation/<date>-report.md` when local artifact writing is authorized, or return the same fields in the response. Library owns any PRD at its current Schema v2 path; never create a competing plan folder or overwrite another agent's active artifact.

Report status, selected owner/version and paired procedure, concrete artifacts, accepted contract pins, actual checks and their results, evidence limits, unfinished boundaries and the smallest unresolved user decision. Keep source/static checks, mock/browser behavior, native execution, packaged artifacts and provider evidence separate. Permission to create a source workflow does not authorize installation, provider writes, credentials, spend, commits, push or publication.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
