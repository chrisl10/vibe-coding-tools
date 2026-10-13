# Schema coverage and qualification ledger

## Source coverage

| Source path/commit and original field | Target table/field | Disposition | Type/null/default | Scope/key/constraint/index | Reason and owner decision | Native proof |
|---|---|---|---|---|---|---|
| [source identity] | [target identity] | Retained/Changed/Replaced/Deferred | [full definition] | [explicit membership/version rule] | [evidence] | Planned/Executed with result |

Every source field must appear exactly once as a source mapping, with additional relationship mappings explicit. Totals state source fields, retained/changed/replaced/deferred fields, proposed supporting fields and unresolved mappings. A declared omission with its blocking decision is better than an invented full-schema claim.

## Entity and lifecycle coverage

| Entity | Owning aggregate/scope | Relations | Mutation/version rule | Retention/deletion | Consumers | Applicable CTR pins |
|---|---|---|---|---|---|---|
| [entity] | [trusted scope] | [keys] | [append/update/immutable] | [policy] | [names] | [exact revisions/status] |

Inventory enums, indexes, triggers, checks, FKs and JSON schemas as distinct controls. Define current-version/signoff/content identity where needed. Counter-based readiness is not a substitute for the exact expected set. Include supporting execution/inbox/outbox/access-grant records only where the app requires them.

## Qualification evidence

Record native DB engine/version, extensions, roles, artifact SHA, generated migration order, exact SQL/schema exercised, commands/results and positive/refusal assertions. List every modification/substitution to a test copy, including omitted extensions or changed vector types. Distinguish local relational proof, full native target proof and production migration. Never expose credentials in the ledger.
