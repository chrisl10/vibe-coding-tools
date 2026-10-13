# Worked Example: Zero-Downtime NOT NULL Column Add

Source-only hypothetical: add a NOT NULL `preferred_name` column to a 100M-row `users` table. No native lock/latency or zero-downtime result is claimed. For current live procedure use [guide 11](../guides/11-live-schema-migration.md); the historical pgroll/config examples below are unexecuted and require exact version qualification. Source: `guides/03-migrations.md`, `templates/migration-plan.md`, `templates/expand-backfill-contract-checklist.md`.

---

## Context

- **Postgres version:** 16.
- **Table:** `users`, ~100M rows, hot (writes ~500/s, reads ~5000/s).
- **Goal:** add `preferred_name text NOT NULL`, default to current `name`, remain editable independently going forward.
- **Tooling:** raw SQL + `pgroll` (could also do this manually).
- **Naive single-step that would fail:**
  ```sql
  -- 🚫 DO NOT DO THIS ON A 100M-ROW TABLE
  ALTER TABLE users ADD COLUMN preferred_name text NOT NULL DEFAULT name;
  ```
  This is invalid PostgreSQL SQL: a default cannot reference another column. It is not evidence of a table rewrite or measured lock duration. The staged nullable field plus an explicitly justified driver backfill is the reviewed pattern. Source: `guides/03-migrations.md` §DDL-lock-class-table.

## Plan

### Phase 1: Expand (Deploy 1)

```sql
-- Metadata-only: nullable column with no default
ALTER TABLE users ADD COLUMN preferred_name text;
```

| DDL | Lock | Duration | Notes |
|---|---|---|---|
| `ADD COLUMN ... text` (nullable, no default) | `ACCESS EXCLUSIVE` (brief) | measured acquisition/hold | metadata-only on PG 11+ |

**App code change:**
- Reads: prefer `preferred_name`, fall back to `name`.
- Writes: when writing `name`, also write `preferred_name`. Dual-write.

**Verification:**
- [ ] `\d users` shows the new column.
- [ ] App logs show dual-writes happening.
- [ ] No regression in p99 write latency.

**Observe** through the declared compatibility window and writer inventory. No universal 24-hour window establishes retirement.

### Phase 2: Backfill (Background job)

Use [guide 11](../guides/11-live-schema-migration.md) and the [single-batch SQL sketch](migration-review.sql). Commit each batch separately, resume only from committed selected cursors, handle sparse IDs and null source values, and reconcile concurrent writes. Do not infer completion from zero updates. Duration and safe size require native measured proof.

**Then consider NOT NULL only if complete derivation, zero legitimate unknowns and every writer are proven.** NOT VALID constrains subsequent writes, including updated existing rows. The following source sketch still needs native revision/lock rehearsal:

```sql
-- Add CHECK constraint NOT VALID — metadata-only, brief lock
ALTER TABLE users
  ADD CONSTRAINT preferred_name_nn CHECK (preferred_name IS NOT NULL) NOT VALID;

-- Validate it — data scan with SHARE UPDATE EXCLUSIVE; ordinary DML can continue but waits/conflicts remain
ALTER TABLE users VALIDATE CONSTRAINT preferred_name_nn;

-- Now SET NOT NULL is metadata-only (because the constraint already proves it)
ALTER TABLE users ALTER COLUMN preferred_name SET NOT NULL;

-- Drop the redundant CHECK constraint
ALTER TABLE users DROP CONSTRAINT preferred_name_nn;
```

| DDL | Lock | Duration | Notes |
|---|---|---|---|
| `ADD CONSTRAINT ... NOT VALID` | `ACCESS EXCLUSIVE` (brief) | measured acquisition/hold | metadata-only |
| `VALIDATE CONSTRAINT` | `SHARE UPDATE EXCLUSIVE` | minutes | permits ordinary DML; waits and other lock conflicts remain |
| `SET NOT NULL` (after VALIDATE) | `ACCESS EXCLUSIVE` (brief) | measured acquisition/hold | metadata-only because constraint validated |
| `DROP CONSTRAINT` | `ACCESS EXCLUSIVE` (brief) | measured acquisition/hold | metadata-only |

**Verification:**
- [ ] `SELECT count(*) FROM users WHERE preferred_name IS NULL;` returns 0.
- [ ] `\d users` shows `preferred_name text not null`.
- [ ] Bloat check after backfill: large `UPDATE`s create dead tuples.

**Tune autovacuum on `users`** before this phase if not already:
```sql
ALTER TABLE users SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_vacuum_threshold = 1000,
  autovacuum_vacuum_cost_limit = 2000
);
```

### Phase 3: Contract (Deploy 2)

**App code change:**
- Reads: only `preferred_name`.
- Writes: only `preferred_name`. Stop dual-writing.

There is no DDL change in Phase 3 for this migration: the column already has the right shape. The contract is purely an app-code change that retires the dual-write code path.

For migrations that add a *replacement* column (renaming `name` → `preferred_name`), Phase 3 would also `DROP COLUMN name` after observing no writes.

**Pre-conditions:**
- [ ] Phase 1 + 2 deployed and observed for at least one full deploy cycle.
- [ ] Logs / metrics confirm no writes touching the old code path.

## Rollback

- **Phase 1:** preserve expanded fields and test app rollback; do not drop newly written values.
- **Phase 2:** preserve new writes; prove old representation and inverse conversion or use forward repair. PITR existence does not prove recovery without data loss.
- **Phase 3:** the app-code path is the rollback target. Re-deploy the dual-write code if reading-from-only-`preferred_name` causes regression.

## Verification queries (handed to `quality-wasp-drone`)

```sql
-- 1. Backfill complete
SELECT count(*) AS null_rows FROM users WHERE preferred_name IS NULL;
-- expect 0

-- 2. Constraint enforced
SELECT conname, convalidated FROM pg_constraint
WHERE conrelid = 'users'::regclass AND contype = 'c';

-- 3. Plan check on critical query
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, preferred_name FROM users WHERE id = 12345;

-- 4. Bloat check
\i bloat-check.sql
```

## Why `pgroll` could replace most of this

The same migration in `pgroll`:

```yaml
operations:
  - add_column:
      table: users
      column:
        name: preferred_name
        type: text
        nullable: false
      up: name
      down: NULL
```

`pgroll start` runs Phase 1 + Phase 2; `pgroll complete` runs Phase 3. The virtual schemas mediate dual reads/writes during the migration. Trade-off: less control over throttling and ordering than the manual approach above.

## References

- `guides/03-migrations.md` §DDL-lock-class-table.
- `templates/migration-plan.md`.
- `templates/expand-backfill-contract-checklist.md`.
- `research/2026-04-25-expand-backfill-contract-pgroll.md`.
- https://github.com/xataio/pgroll

---

*Forged 2026-04-25.*
