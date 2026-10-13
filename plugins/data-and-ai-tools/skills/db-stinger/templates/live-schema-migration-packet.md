# Live-schema migration packet

Status: SOURCE REVIEW ONLY / REHEARSED / QUALIFIED FOR NAMED ACTION. Approval scope and evidence links: ___.

## Revision and workload pins

- Source commit, migration file hashes, schema before/after hash: ___.
- Actual PostgreSQL major/minor and matching documentation: ___.
- Provider, environment, pooler mode; ORM/client/runner exact versions: ___.
- Runner transaction boundaries; concurrent-index handling: ___.
- All writer/reader/client revisions, dormant jobs and retirement evidence: ___.
- Row counts/distribution, hot paths, representative workload and measurement timestamp: ___.

## Field meaning

| Field | Source of truth | Permitted derivation/provenance | Unknown population | Null meaning | Overwrite/conflict rule |
|---|---|---|---|---|---|
| ___ | ___ | ___ | ___ | ___ | ___ |

No guessed backfill or invented default. If source evidence is absent, keep historical values null.

## Phase gates

| Phase | Exact SQL hash/client revision | Lock class and possible scan/rewrite | Lock/statement budget with reason | Permission | Actual proof | Exit gate |
|---|---|---|---|---|---|---|
| Expand | ___ | ___ | ___ | ___ | ___ | Mixed-client insert/update/retry/delete verified |
| Backfill | ___ | ROW EXCLUSIVE plus row locks for UPDATE | ___ | ___ | ___ | Committed batches, cursor durability and reconciliation |
| Validate | ___ | ___ | ___ | ___ | ___ | Truthful invariant; unknown/rejected rows reported |
| Contract | ___ | ___ | ___ | ___ | ___ | Every old reader/writer retired; recovery qualified |

## Batch and race proof

Derivation source, transaction per batch, chosen/observed batch size, isolation, row guard, cursor semantics, sparse-key behavior, concurrent writes, skipped-row reconciliation, retry/idempotency, crash-before/after-commit cases: ___. Pause thresholds and measured query/replication/bloat impact: ___.

## Rollback matrix

| State | Old shape still current? | New writes representable in old clients? | Restore/reconcile procedure | Data-loss window | Evidence |
|---|---|---|---|---|---|
| Expand before new writes | ___ | ___ | ___ | ___ | ___ |
| Backfill committed plus new writes | ___ | ___ | ___ | ___ | ___ |
| New-only writes | ___ | ___ | ___ | ___ | ___ |
| Old shape removed | ___ | ___ | ___ | ___ | ___ |

## Verification and handoff

Approved SELECT counts for derived/unknown/rejected/mismatch populations; pg_constraint validation; pg_index validity; actual representative query plan; lock contention; mixed-client tests; resume/retry; recovery rehearsal: ___. Mutating EXPLAIN ANALYZE authorization and safe environment: ___. Security findings/evidence: ___. Quality results after Security: ___. Missing native/provider proof: ___.
