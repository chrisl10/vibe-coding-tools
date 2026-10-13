# Foundation PRD authoring scaffold

Use the installed Library method for exact repo-local naming, mandatory sections and lifecycle. This scaffold supplements that method. It is not an accepted PRD and does not reserve number 000.

## Index

Record project, selected stack decisions with owner evidence, Draft/Backlog status, actual starting SHA/source archive identity, goals/non-goals, numbered observable acceptance criteria, exact contract dependencies, proposed touched paths, known current implementation and unresolved decisions.

## Platform execution sub-PRD

Request/runtime hosting; bounded request lifetimes; durable engine; data authority; model/acquisition adapters if needed; identity baseline; environment isolation; browser progress; storage/render/delivery; retries/timeouts/uncertain outcomes; secrets resolved server-side; operational qualification and owner gates. Distinguish selected provider from detailed policy acceptance.

## Database/schema sub-PRD

Inventory every source entity/field using the actual storage model. When no database exists or is planned, record the decision and file/config schemas instead of inventing SQL. Include complete table/enum/index/constraint/trigger/relationship definitions, ownership and version semantics, deletion/retention, JSON/native validation, approved dialect/runtime, migrations and source-field ledger. Pin the reference SQL/schema artifact hash. Report actual native execution and substituted test limitations separately.

## Shared contracts and seams sub-PRD

Delegate normative CTR authoring to Contract Writing. The PRD maps every producer/consumer to the exact CTR revision, native DTO/schema and observable positive/refusal evidence. Public projection excludes secrets/private payloads. Identify idempotency scope, unknown provider outcomes, correction/approval/version propagation, outbox/delivery and readiness.

## Reuse sub-PRD

Specific source modules/full SHAs/licenses/runtime; dependencies and product coupling; replacement adapters; target owner; source read-only boundary; tests here for both adapter and consumer. No invented reuse percentage.

## Verification sub-PRD

Schema refusal/positive cases, wrong-tenant/source/version fixtures, malformed model/provider outputs where applicable, retry/recovery/concurrency, exact output-set readiness, visual/keyboard/contrast comparison where UI exists, meaningful local checks and CI preference, ordered Security/Quality/health, final candidate identity, unanswered decisions and explicit release gates.

## Completion state

Specification coverage, Accepted agreement readiness, native schema qualification, application behavior and deployment are separate statuses. A complete document does not mark the feature implemented. Use real criterion results; do not move a feature to Completed because its planning files exist.
