# 03: Migrations

The expand-backfill-contract pattern is the discipline that keeps migrations from blocking production.

Source: `research/2026-04-25-expand-backfill-contract-pgroll.md`. For live changes, use [guide 11](11-live-schema-migration.md) and its [current PostgreSQL 18 evidence](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/data-and-ai-tools/skills/db-stinger/references/research/live-schema-migration/distillation.md). Historical examples require exact server/tool revision review.

## The pattern

Split a single logical change into three deployments:

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│ EXPAND   │  →   │ BACKFILL │  →   │ CONTRACT │
└──────────┘      └──────────┘      └──────────┘
   add new        populate new       remove old
   alongside        from old           shape
   old
```

App code reads/writes both shapes during expand+backfill, then only the new shape after contract.

### Phase 1: Expand
- Add new column / table / index: non-destructive.
- `CREATE INDEX CONCURRENTLY` takes `SHARE UPDATE EXCLUSIVE`, permits ordinary DML but can wait or fail. It cannot run inside a transaction block; inspect `pg_index.indisvalid` and `indisready`, and prepare failed-build recovery.
- Add as `NULL`able with no default (metadata-only).
- App code dual-writes to old and new.

### Phase 2: Backfill
- Populate the new column from the old one.
- **Use separately committed bounded driver batches:** choose size from measured workload budgets; persist the selected-row cursor after commit. Empty numeric ranges or zero changed rows do not prove completion.
- Throttle by autovacuum lag: heavy backfill creates bloat fast.
- For NOT NULL transitions: add `CHECK (col IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT` separately (SHARE UPDATE EXCLUSIVE plus a data scan), then `SET NOT NULL` (now metadata-only, since the constraint already proves it).

### Phase 3: Contract
- App code reads/writes only the new shape.
- Drop old column / index / constraint.
- Do this after observing zero traffic to the old path for a full deploy cycle.

## DDL lock-class table (Postgres 16+)

| DDL | Lock class | Blocks reads? | Blocks writes? | Safe on large table? |
|---|---|---|---|---|
| `CREATE INDEX` | `SHARE` | no | yes | no: use `CONCURRENTLY` |
| `CREATE INDEX CONCURRENTLY` | `SHARE UPDATE EXCLUSIVE` | no | no | yes (slower; can fail invalid) |
| `ADD COLUMN` (nullable, no default) | `ACCESS EXCLUSIVE` (brief) | brief | brief | yes: metadata-only |
| `ADD COLUMN ... DEFAULT <const>` (PG 11+) | `ACCESS EXCLUSIVE` (brief) | brief | brief | yes: metadata-only |
| `ADD COLUMN ... DEFAULT <expr>` | `ACCESS EXCLUSIVE` | acquisition/hold depends on workload | acquisition/hold depends on workload | volatile defaults can rewrite; classify expression and server version |
| `ADD COLUMN ... NOT NULL` | `ACCESS EXCLUSIVE` | depends on operation | depends on operation | truth of existing values, default and writer compatibility must be proven |
| `ALTER COLUMN ... TYPE` (compatible) | `ACCESS EXCLUSIVE` | brief | brief | maybe |
| `ALTER COLUMN ... TYPE` (incompatible) | `ACCESS EXCLUSIVE` | yes | yes | **NO: table rewrite** |
| `ALTER COLUMN ... SET NOT NULL` | `ACCESS EXCLUSIVE` | brief | brief | maybe: full scan unless `CHECK NOT NULL` validated first |
| `DROP COLUMN` | `ACCESS EXCLUSIVE` (brief) | brief | brief | yes: metadata-only |
| `ADD CONSTRAINT ... CHECK NOT VALID` | `ACCESS EXCLUSIVE` (brief) | brief | brief | yes: metadata-only |
| `VALIDATE CONSTRAINT` | `SHARE UPDATE EXCLUSIVE` | no | no | yes |
| `ADD FOREIGN KEY ... NOT VALID` | `SHARE ROW EXCLUSIVE` (brief) | brief | brief | yes |

**Budget lock acquisition and hold time separately.** ACCESS EXCLUSIVE conflicts with reads and writes; metadata-only is not non-blocking. Use measured invocation-specific limits rather than a universal duration promise.

## Common patterns

### Add a NOT NULL column on a large table

```sql
-- Phase 1 — Expand (one deploy)
ALTER TABLE users ADD COLUMN preferred_name text;  -- nullable, metadata-only

-- App: dual-write preferred_name when name is set.

-- Phase 2: run separately committed driver batches.
-- See examples/migration-review.sql and guide 11 for selected-row cursors,
-- sparse keys, null-source handling and independent reconciliation.
-- This source sketch does not prove live migration behavior.

ALTER TABLE users ADD CONSTRAINT preferred_name_nn CHECK (preferred_name IS NOT NULL) NOT VALID;
ALTER TABLE users VALIDATE CONSTRAINT preferred_name_nn;
ALTER TABLE users ALTER COLUMN preferred_name SET NOT NULL;  -- now metadata-only
ALTER TABLE users DROP CONSTRAINT preferred_name_nn;

-- Phase 3 — Contract (later deploy)
-- App: stop dual-writing; preferred_name is the source of truth.
```

See `examples/zero-downtime-not-null.md` for the full worked example.

### Change a column type

Don't `ALTER COLUMN ... TYPE` on a large table. Instead:

1. Add a new column with the target type.
2. Backfill (with conversion).
3. Swap reads/writes incrementally.
4. Drop the old column.

### Rename a column

Single-step `ALTER TABLE ... RENAME COLUMN` is metadata-only and fast, but it requires every reader to pick up the new name simultaneously. In a multi-deploy world, instead:

1. Add a new column; trigger to keep it synced.
2. App code reads new, writes old.
3. App code reads new, writes both.
4. App code reads new, writes new.
5. Drop trigger and old column.

Or use `pgroll`, which automates this with views.

## `pgroll`

`pgroll` (Xata) automates expand-backfill-contract using virtual schemas:

```yaml
operations:
  - add_column:
      table: users
      column:
        name: preferred_name
        type: text
        nullable: false
      up: name              # how to compute new from old
      down: preferred_name  # how to compute old from new
```

During the migration, `pgroll` exposes both `migration_<n>_old` and `migration_<n>_new` schemas; app instances on either version read and write through views that hide the change. `pgroll complete` removes the old schema.

**Strengths:** codifies the pattern. Exact version support and rollback after new writes require tested representation/recovery evidence; one command is not data-preservation proof.
**Weaknesses:** not every Postgres feature is supported; partitioned tables and exotic constraints sometimes need manual work.

## Migration tooling per ORM

| ORM | Tool | Diff or declarative? | Plays nice with `pgroll`? |
|---|---|---|---|
| Drizzle | `drizzle-kit` | Diff-based | Yes: `drizzle-kit` writes raw SQL files |
| Prisma | `prisma migrate` | Declarative + shadow DB | Partial: Prisma owns the migration history |
| Raw SQL | hand-rolled | n/a | Yes: `pgroll` IS the migration tool |

For zero-downtime requirements at scale, raw SQL + `pgroll` is the most flexible. Prisma + `pgroll` requires extra coordination because Prisma wants to own the migration history.

## Checklist

Use `templates/migration-plan.md` and `templates/expand-backfill-contract-checklist.md`. Every migration plan must:

- [ ] State the Postgres major version.
- [ ] State the lock class of every DDL.
- [ ] Identify any DDL that takes `ACCESS EXCLUSIVE`: these need expand-backfill-contract on tables > 1M rows.
- [ ] Specify the rollback path.
- [ ] Specify verification queries (handed to `quality-wasp-drone`).

## Cross-references

- `04-partitioning.md`: partition `ATTACH` / `DETACH` lock behavior.
- `05-performance-pooling.md`: bloat after backfill; autovacuum tuning.
- `templates/migration-plan.md`, `templates/expand-backfill-contract-checklist.md`.
