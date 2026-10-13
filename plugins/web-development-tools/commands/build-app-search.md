---
description: "Build tenant-safe application search with an accepted query/result contract, stable pagination and measured retrieval quality."
argument-hint: "[product/repository] [outcome and constraints]"
---

# /build-app-search

## Mandatory process

1. Load the installed `pest-controller-suit` Core skill and consult its roster before making any routing decision. This is the first instruction, always, no exceptions. Source work resolves component ownership from root `plugin-catalog.json`; installed work uses Core's explicit selected-plugin registry and resolver. Missing Core blocks routing. Load each selected pair's Stinger and required guides before work, and verify actual host tools/delegation. Cached files do not prove selection. Dispatch registered Drones at top level only when delegation is authorized; otherwise execute the selected paired procedure directly and report that fallback truthfully. No invented roles or nested dispatch.

2. Confirm the searched records, actors/tenants, visibility rules, query intent, existing datastore, expected result volume, latency/cost target, and selected UI/backend runtime. Read schema and actual query paths. Retrieval's Postgres default is guidance, not permission to migrate an existing store or add embeddings.
3. Have retrieval-wasp-drone classify exact keyword/full-text, semantic or hybrid needs and identify which arms actually run. db-wasp-drone owns relational schema/indexing; vector-store-wasp-drone owns vector column/index/operator requirements and embeddings-runtime-wasp-drone owns model/dimension/batching only if semantic search is chosen. Keep lexical-only scope valid when that is the accepted design.
4. Have contract-writing-wasp-drone define the request query length/encoding, allowlisted filters/sorts, page-size maximum, cursor format/expiry/version, identity source and malformed-input behavior. Define result id/title/snippet/score semantics, empty results, unavailable-arm signaling and error shape. Specify unique ordering/tie-breaker, query/filter binding of cursors and concurrent-write consistency limits; do not promise a snapshot without implementing one. Library pins the exact accepted revision into API provider and UI consumer requirements.
5. Assign API/query implementation to the actual selected backend owner; UI to svelte-wasp-drone or react-wasp-drone within their remit; HTTP method/status/error review to http-rest-fundamentals-wasp-drone. Missing runtime ownership blocks dependent implementation. Parameterize values and allowlist structural choices. Apply tenant/resource authorization before retrieving candidate content and before returning snippets/counts. An inaccessible record must not appear through a count, score, autocomplete or cached response.
6. Implement bounded pagination with deterministic unique ordering. Validate malformed or tampered cursors, mismatched query/filter cursors, negative/oversized page sizes, unsupported sorts and empty/Unicode query input. Verify no duplicate/omitted records on the documented consistency model, including tied scores. Record offset costs or cursor tradeoffs using actual query evidence rather than claiming universal speed.
7. Evaluate a fixed labeled query set with permission-denied, exact-identifier, paraphrase, no-result and multilingual cases appropriate to the corpus. Record before/after relevance metrics, latency and cost; separate retrieval evidence from any generated answer score. Optional unavailable-vector fallback must retain the same authorization and expose the documented fallback state. A lexical fallback cannot count as a measured semantic pass.
8. Run provider/consumer contract checks, denial/input/pagination cases and retrieval evaluation. Enter Security, Quality then orchestrator Repository Health. Deliver query contract revision, source/index changes, UI states, actual queried arms, evidence and untested load limits.

## Selected-owner map

| Capability | Catalog owner | Activation |
|---|---|---|
| `pest-controller-suit` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `library-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `contract-writing-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `security-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `quality-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `github-repo-health-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `retrieval-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |
| `db-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |
| `vector-store-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |
| `embeddings-runtime-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |
| `svelte-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `react-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `http-rest-fundamentals-stinger` | `backend-and-desktop-tools` | Required for its chosen branch; do not imply sibling selection |

## Inputs and host qualification

Use trailing invocation text exposed by the actual host; `$ARGUMENTS` is supported only where documented. Reuse answered inputs and accepted decisions. Ask one concrete batch for unresolved material inputs before dependent work, while continuing independent authorized work. Claude/Cowork uses the owner flat command, Cursor its generated command projection, and Codex the owner's generated `source-command-build-app-search` skill. Source generation is not installation, role discovery, or runtime proof. Resolve all resources against the selected carrier root. A missing required owner blocks its dependent boundary and is named in the report; optional branches require only their own selected dependencies.

## Output contract

Write advisory evidence to the receiving repository's `library/requirements/reports/build-app-search/<date>-report.md` when local artifact writing is authorized, or return the same fields in the response. Library owns any PRD at its current Schema v2 path; never create a competing plan folder or overwrite another agent's active artifact.

Report status, selected owner/version and paired procedure, concrete artifacts, accepted contract pins, actual checks and their results, evidence limits, unfinished boundaries and the smallest unresolved user decision. Keep source/static checks, mock/browser behavior, native execution, packaged artifacts and provider evidence separate. Permission to create a source workflow does not authorize installation, provider writes, credentials, spend, commits, push or publication.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
