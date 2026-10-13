# Three migration decisions

These are synthetic review cases, not executed migrations. PostgreSQL behavior traces to the [distillation](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/data-and-ai-tools/skills/db-stinger/references/research/live-schema-migration/distillation.md); the product invariants are declared scenario inputs.

## A. Introduce an observed timestamp

Before: orders(id, created_at, status); no reliable historical paid event exists. After: nullable paid_at records only the confirmed paid event going forward. Historical created_at is not proof of payment time. Expand adds nullable paid_at with no default. Existing rows remain null. New payment writer revision persists the observed timestamp atomically with its state change; old revisions and reconciliation require explicit retirement. No bulk backfill and no global NOT NULL. Report historical unknown count, new known count and writer coverage. Rollback preserves paid_at data; reverting the app does not justify dropping recorded facts.

## B. Copy an equivalent representation

Declared invariant: display_name_v2 is exactly the same text as display_name while old and new clients coexist. Source rows may already have null display_name. Expand adds nullable display_name_v2. Atomic mixed writers keep both equal, including updates. Batches copy only non-null source into still-null target and commit individually. Sparse IDs 1, 90000, 200000 defeat a driver that exits after the first empty numeric range. Empty candidate batches also require writer and skip-lock reconciliation. Validation compares both with IS DISTINCT FROM; inherited nulls remain legitimate, so zero-null is not the exit gate. Rollback uses the preserved old representation only after proving every new write stayed representable and synchronized.

## C. Tighten a truly total field

Declared invariant: a supplied source of truth can establish every required code, every writer has been upgraded, and no legitimate unknown exists. Unknown source or writer breaks this case and returns it to nullable. Backfill and reconcile the full population. Add CHECK (required_code IS NOT NULL) NOT VALID only after writer coverage; validate separately. SET NOT NULL keeps the validated proof, then proof removal is a later action. Lock waits, validation scans and actual latency remain measured rehearsal requirements. Do not infer safety from total row count or a generated SQL file.
