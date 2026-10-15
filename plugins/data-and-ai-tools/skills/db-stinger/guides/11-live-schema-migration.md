# 11: Preserve facts while changing a live schema

Use this procedure for a live change with old and new clients. Start with the [migration packet](../templates/live-schema-migration-packet.md). The research distillation establishes PostgreSQL 18 behavior and separates derived policy from server facts. The [worked cases](../examples/live-schema-cases.md) demonstrate decisions; the [SQL sketch](../examples/migration-review.sql) is unexecuted review material.

## 1. Pin what exists

Read actual DDL, migration history, generated SQL, ORM/client lockfile versions and the exact client revision. Record server major/minor, provider/region, pooler mode, migration runner and whether it automatically wraps files in a transaction. Enumerate web deployments, long-running workers, scheduled jobs, imports, direct SQL writers, replica consumers and offline clients. Unknown writer coverage blocks contract. A client revision is not a schema revision; record both and their compatibility mapping.

## 2. Decide the meaning before the SQL

For every field, document provenance, valid derivation, null meaning, overwrite rule and authoritative writer. Distinguish a new observable fact from a renamed representation. If a historical paid timestamp was never recorded, do not copy created_at, current time or a guessed status into it. Keep that timestamp nullable and state the unresolved population. If an invertible rename is required, show both transformations and the representable domain. Lossy conversion requires an explicit retention/rollback decision.

## 3. Expand and prove mixed writers

Add the nullable field without an invented default; state ACCESS EXCLUSIVE acquisition even when the change does not rewrite data. Assign separate transaction-local lock and statement budgets for the authorized invocation. Prove old-only and new-only insert/update paths, retries, conflicting updates, deletes and partial failures in a disposable representative environment. Dual writes must be atomic where they share a database transaction. Across stores, document the reconciliation/outbox owner rather than claiming atomicity. Source: ALTER TABLE and explicit-locking captures in the distillation.

The new reader's fallback must preserve semantic equivalence. If the old field cannot establish the new fact, return unknown instead of silently deriving it. Do not add a non-null CHECK NOT VALID until every affected writer can meet it: it still constrains future writes and updated existing rows.

## 4. Backfill in separately committed batches

Use only the documented derivation. The driver commits each bounded batch, records its cursor/result after commit, and can resume after crash without treating attempted updates as completed. Keep a target-null guard so current writer values are not overwritten. Numeric key ranges can have holes: a range with zero updated rows is not a completion signal. An id high-water mark misses later inserts and rows updated after the scan; prove the deployed writer invariant and finish with a reconciliation scan.

For parallel workers, document row ownership, lock order and retryable failures. SKIP LOCKED may leave skipped candidates, so a final independent scan is mandatory. Record measured duration, affected rows, unresolved rows, dead tuples, replication lag and query impact. Pause on declared budgets. Do not use a DO loop as evidence of separately committed batches. Batch size has no universal safe value. Sources: isolation and SELECT captures.

## 5. Validate the intended invariant

Count populated, legitimately unknown, rejected and mismatched rows separately. A zero-null target is valid only when the product meaning and complete population justify it. Historical unknowns prevent global NOT NULL; keep the column nullable or design a narrower truthful invariant and review its update behavior. Eligible CHECK/FK constraints may be added NOT VALID then validated in a separate step. Validation scans data and takes a lock; record both. Where using validated CHECK proof for SET NOT NULL, keep the proof during that command and remove it separately. Sources: ALTER TABLE capture.

## 6. Contract only with revision evidence

Retire old readers/writers only after the stated compatibility window, inventory and telemetry establish their retirement, including dormant jobs and offline clients. Review views, triggers, CDC, reporting, indexes and rollback users before dropping old shape. Record the destructive decision separately. Never promise zero downtime from row count alone. An index built concurrently needs transaction-boundary and pg_index validity proof before use; failed builds need documented recovery. Sources: CREATE INDEX and locking captures.

## 7. Rollback after writes, not just after DDL

Before any new writes, preserving expanded fields and rolling the app back can be straightforward, subject to tested compatibility. After new writes, show whether old clients can represent every new value and whether old fields were kept current. Never erase new columns as generic rollback. A committed batch cannot be undone by rolling back a later transaction. After contract, restoration needs a tested recovery/reconciliation procedure and a declared data-loss window; backup existence alone is insufficient. Forward repair may be the prepared recommendation when reverse conversion is lossy.

## 8. Report proof honestly

Attach actual revision pins, schema diff, authorized rehearsal outputs, constraint/index catalog results, representative query plans, contention tests, resume/retry tests and restore evidence. EXPLAIN ANALYZE executes SQL, including writes: obtain execution authorization and choose a safe environment. Security reviews tenant/RLS/PII consequences; Quality runs the approved verification after Security. Until these exist, report SOURCE REVIEW ONLY and list missing proof. No generated SQL or checklist automatically authorizes production changes.
