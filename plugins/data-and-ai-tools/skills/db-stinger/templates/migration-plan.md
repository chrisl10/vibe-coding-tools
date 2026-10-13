# Migration Plan: {{slug}}

**Date:** {{YYYY-MM-DD}}
**Author:** db-wasp-drone
**Postgres version:** {{exact major/minor}}
**Tooling:** {{drizzle-kit / prisma migrate / raw SQL + pgroll}}
**Affected tables:** {{table-1 (~N rows), table-2 (~N rows)}}

---

## Goal

{{One paragraph: what is changing, why, and what's the user-visible behavior change.}}

## Risk classification

- **Largest affected table:** {{N}} rows
- **Expand-backfill-contract required?** {{yes / no, and why}}
- **Estimated worst-case lock duration:** {{seconds}}
- **Replication impact:** {{e.g., slot lag, downstream consumers, logical replication}}

## Phase 1: Expand

| DDL | Lock class | Duration estimate | Notes |
|---|---|---|---|
| `ALTER TABLE x ADD COLUMN y text;` | `ACCESS EXCLUSIVE` (brief) | {{measured acquisition/hold budgets}} | metadata-only still acquires lock |
| `CREATE INDEX CONCURRENTLY ...` | `SHARE UPDATE EXCLUSIVE` | {{minutes}} | does not block writes |

**App code change:**
- {{Describe dual-write or read-from-both pattern.}}

**Verification:**
- [ ] `\d {{table}}` shows new column / index.
- [ ] Exact schema/index catalog lookup below returns one intended index, `indisvalid = true` and `indisready = true`.

## Phase 2: Backfill

Use the [live-schema packet](live-schema-migration-packet.md) and [single-batch SQL sketch](../examples/migration-review.sql). Driver commits each bounded batch, persists selected cursor after commit, keeps target-null guards and independently reconciles sparse IDs, unknown source data and concurrent writers. No DO loop or zero-update termination proof.


**Throttle / pause criteria:**
- Autovacuum lag > {{threshold}}.
- Replication slot lag > {{threshold}}.

**For NOT NULL transitions:**
1. `ALTER TABLE x ADD CONSTRAINT y_nn CHECK (y IS NOT NULL) NOT VALID;`
2. `ALTER TABLE x VALIDATE CONSTRAINT y_nn;` (SHARE UPDATE EXCLUSIVE; data scan and conflicts remain)
3. `ALTER TABLE x ALTER COLUMN y SET NOT NULL;` (validated CHECK may avoid scan; ACCESS EXCLUSIVE still acquired)
4. `ALTER TABLE x DROP CONSTRAINT y_nn;`

**Verification:**
- [ ] Row count of `{{new_col}} IS NOT NULL` matches expected.
- [ ] Constraint validated.

## Phase 3: Contract

| DDL | Lock class | Notes |
|---|---|---|
| `ALTER TABLE x DROP COLUMN old_col;` | `ACCESS EXCLUSIVE` (brief) | metadata-only |
| `DROP INDEX ...` | `ACCESS EXCLUSIVE` (brief) | brief |

**App code change:**
- {{Stop dual-writing; new column / shape is source of truth.}}

**Pre-conditions:**
- [ ] Phase 1 + 2 fully deployed; observed for at least one full deploy cycle.
- [ ] No traffic to the old shape (logs / metrics).

## Rollback

- **Before new writes:** preserve expanded fields; test app rollback and writer compatibility.
- **After committed backfill/new writes:** retain new values and prove inverse conversion, old-client representability and reconciliation. A later ROLLBACK cannot undo prior commits. Do not truncate or drop-and-readd.
- **After contract:** require tested recovery and declared data-loss window; choose forward repair when reverse conversion is lossy.

## Verification queries (handed to `quality-wasp-drone`)

```sql
-- 1. Row counts match
SELECT count(*) FROM {{table}} WHERE {{new_col}} IS NULL;  -- classify eligible, unknown, rejected and mismatched populations; zero only if justified

-- 2. Indexes valid
SELECT n.nspname, t.relname AS table_name, i.relname AS index_name,
       x.indisvalid, x.indisready
FROM pg_catalog.pg_index x
JOIN pg_catalog.pg_class i ON i.oid = x.indexrelid
JOIN pg_catalog.pg_class t ON t.oid = x.indrelid
JOIN pg_catalog.pg_namespace n ON n.oid = t.relnamespace
WHERE n.nspname = '{{schema}}' AND t.relname = '{{table}}'
  AND i.relname = '{{index}}';
-- Zero/multiple rows fail the named-index check; sketch requires native revision proof.

-- 3. Plan check on critical query
EXPLAIN (ANALYZE, BUFFERS) {{representative query}};
```

## Handoffs

- **`quality-wasp-drone`**: runs authorized verification after Security; distinguishes source review from native/provider proof.
- **`security-wasp-drone`**: review any new PII columns or RLS impact.
- **`react-wasp-drone`**: flag any data-layer changes the UI must adopt.

## References

- `guides/03-migrations.md`
- `templates/expand-backfill-contract-checklist.md`
- {{external URLs}}

---

*Template from `db-stinger/templates/migration-plan.md`. See `examples/zero-downtime-not-null.md` for a filled example.*
