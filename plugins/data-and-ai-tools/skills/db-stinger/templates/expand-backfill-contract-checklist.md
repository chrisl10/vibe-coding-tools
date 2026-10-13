# Expand-Backfill-Contract Checklist

A gating checklist for any migration touching a table > 1M rows. Tick every box before advancing to the next phase.

---

## Pre-flight

- [ ] Postgres major version captured.
- [ ] Affected table sizes captured (`pg_relation_size`, `reltuples`).
- [ ] Lock-class table consulted for every DDL: `guides/03-migrations.md`.
- [ ] Worst-case lock duration estimated.
- [ ] Backup / PITR confirmed available for the affected window.
- [ ] Rollback plan documented.

## Phase 1: Expand

- [ ] Every Phase 1 DDL lock and acquisition/hold budget is stated and measured; metadata-only or CONCURRENTLY is not lock-free.
- [ ] Default expression classified by volatility, version and product meaning; no invented historical fact or unqualified rewrite.
- [ ] No `ADD COLUMN ... NOT NULL` on a large table.
- [ ] No `ALTER COLUMN ... TYPE` requiring rewrite.
- [ ] All new indexes built `CONCURRENTLY`.
- [ ] App code dual-writes (or reads from both shapes): verified in staging.
- [ ] Phase 1 PR merged, deployed, observed green for {{N}} hours.
- [ ] `\d <table>` confirms new shape.
- [ ] Exact schema/index query joining pg_index/pg_class/pg_namespace confirms intended index validity/readiness; see migration-plan.md.

## Phase 2: Backfill

- [ ] Driver commits each bounded batch and records selected cursor after commit; sparse IDs and zero changed rows do not end correctness checks.
- [ ] Throttled by autovacuum lag and replication slot lag.
- [ ] No single `UPDATE` covering the whole table.
- [ ] Backfill driver (script / job) is idempotent and resumable.
- [ ] For NOT NULL transitions: `CHECK ... NOT VALID`, `VALIDATE CONSTRAINT`, `SET NOT NULL`, `DROP CONSTRAINT` sequence followed.
- [ ] Backfill populations reconcile: eligible, already present, unknown, rejected and mismatched; NOT NULL only when meaning and every writer justify it.
- [ ] Bloat check after backfill (`scripts/bloat-check.sql`).
- [ ] Autovacuum tuning revised on the affected table if necessary.

## Phase 3: Contract

- [ ] Phase 1 + 2 deployed and observed for at least one full deploy cycle.
- [ ] Logs / metrics confirm zero traffic to the old shape.
- [ ] App code reads/writes only the new shape: verified in staging.
- [ ] Phase 3 lock acquisition/hold budgets and reader/writer compatibility are proven; metadata-only is not a no-blocking promise.
- [ ] Rollback plan revisited: Phase 3 is destructive; only proceed at high confidence.

## Post-deploy

- [ ] Verification queries run by `quality-wasp-drone`: all green.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` on critical queries: no unexpected plan changes.
- [ ] Bloat check; reindex if necessary.
- [ ] Migration plan archived in the host repo's `library/requirements/reports/db/<date>-migration-plan.md` (standalone) or `library/requirements/<lifecycle>/prd-<###>-<title>/reports/<date>-migration-plan.md` (feature-tied).

## References

- `guides/03-migrations.md`