# Beacon Research illustrative schema ledger

> Logical field inventory only | No DDL or migration executed

This is the complete logical inventory for this deliberately small fictional example. Actual apps require their own exhaustive source-field ledger, native SQL/ORM reference, keys/constraints/indexes/triggers and target qualification. These rows demonstrate the ledger format, not database enforcement.

| Entity | Fields | Scope/relation | Lifecycle rule |
|---|---|---|---|
| workspaces | id, name, created_at | Root workspace ID | Owner-controlled lifecycle |
| members | id, workspace_id, actor_id, role, created_at | Scoped membership, unique workspace/actor pair | Role changes authorized by workspace authority |
| requests | id, workspace_id, member_id, url, input_digest, request_key, status, created_at | Member and request share workspace; replay key scoped to actor/operation | Status follows accepted state machine; changed input conflicts |
| executions | id, workspace_id, request_id, state, attempt, fence, created_at, updated_at | Request membership enforced; attempt/fence must match active lease | Durable replay, no false completion |
| evidence | id, workspace_id, request_id, source_url, captured_at, captured_text, content_hash, acquisition_status | Same request/source membership | Captured bytes/version are immutable |
| briefs | id, workspace_id, request_id, version, body, content_hash, validation_id, status | Same scope and current source set | Revisions append; required proof binds exact bytes |
| brief_sources | workspace_id, brief_id, brief_version, evidence_id, quote | Composite scope/version relationships | Quote must be supported by captured text |
| artifacts | id, workspace_id, brief_id, brief_version, object_key, bytes_hash, status | Same current brief revision; object access scoped | Production seals payload; new content yields new version |
| outbox | id, workspace_id, aggregate_id, aggregate_version, event_type, payload, effect_key, state, created_at | Scoped aggregate/version; durable dedupe | Domain output and effect intent commit atomically |
| effect_attempts | id, workspace_id, outbox_id, attempt, provider_request_id, state, result_digest | Outbox scope/admission identity | Unknown outcomes reconcile before repeat effect |

Field disposition: example fields are proposed additions; none was extracted from real source. Retention/deletion, exact enums/types/nullability/indexes and provider acknowledgement terms remain normative decisions for a real design. Do not label this logical table list a qualified PostgreSQL schema.

Native verification: Not run. Target engine/extensions/roles: Unbound. Source SHA: Illustrative fixture only. Refusal fixtures: B-01 through B-06 plus replay/fencing/source-version cases.
