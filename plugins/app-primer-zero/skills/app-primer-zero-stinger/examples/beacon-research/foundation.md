# Beacon Research foundation baseline

> Fictional project | Foundation specification: Draft | Implementation: Missing

Goal: let a workspace member submit a public URL and receive a cited brief, with durable progress and scope-safe access. Non-goals: billing, public anonymous sharing, CRM, healthcare decisions and production deployment. Do not infer those features from another app's worked example.

## Required foundation coverage

- Platform: request host, data authority, durable engine, acquisition/model boundaries, progress projection, scoped artifact storage.
- Schema: every field in [the example ledger](schema-ledger.md), scope-safe relations, status/version/content identity, immutable captured text and outbox/effect records.
- Contracts: the two Draft interfaces in [the seam map](contracts-and-seams.md). Their exact revisions and owner evidence block implementation readiness.
- Reuse: none selected. A later module selection needs committed identity, license/runtime adaptation and checks in the consuming app.
- Verification: malformed input, wrong workspace, same-key changed input, duplicate dispatch, stale attempt, fabricated quote, wrong-source citation and failed artifact cannot produce a ready brief.

## Acceptance criteria for future implementation

| ID | Observable criterion |
|---|---|
| B-01 | A member of workspace A cannot submit/read/update workspace B's request by substituting an ID. |
| B-02 | Request admission and execution intent commit together; retrying the same request does not duplicate domain work. |
| B-03 | Captured text and source hashes belong to the same request/version as each cited claim. |
| B-04 | Invalid structured output fails explicitly within the repair budget; no default brief replaces failure. |
| B-05 | Browser disconnect leaves durable work resumable; projected progress excludes secrets/private payloads. |
| B-06 | Artifact readiness checks the exact current required output set and validation, never only a counter. |

All are Planned. There is no runtime result. Open decisions are provider versions/budgets, scope/lifetimes, retention/deletion and exact CTR acceptance. Schema drafting may continue independently, but its unanswered policy is explicit.
