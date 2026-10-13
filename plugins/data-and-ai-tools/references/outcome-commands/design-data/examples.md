# Acceptance cases: design-data

## Invocation

Request: Design an existing Postgres product schema for tenant-scoped invoices.

Expected: Inspect actual schema/version/workloads, propose constraints and indexes, review authorization negatives, and produce additive migration/backfill/rollback proposals without execution.

## Boundary case

Historical ownership is unknown. Leave unknowns explicit and refuse a guessed backfill; do not run ORM push or EXPLAIN ANALYZE implicitly.

## Evidence rule

Retain source dates and revision identity. Queued jobs, proposed actions, draft artifacts and unavailable tools never become claimed completed results.
