-- REVIEW SKETCH ONLY. Not executed, not an authorized production migration.
-- PostgreSQL 18 facts; hypothetical public.orders schema declared in case A.
-- Example timeouts are deliberately omitted: named invocation must supply budgets.
-- Existing table assumed: public.orders(id bigint PRIMARY KEY, created_at timestamptz, status text).

-- Expand: ACCESS EXCLUSIVE acquisition still required. No historical fact invented.
ALTER TABLE public.orders ADD COLUMN paid_at timestamptz;
-- Historical paid_at values stay NULL; future writer must persist real observed events.
-- No UPDATE paid_at = created_at. No DEFAULT now(). No NOT NULL.

-- Read-only population evidence sketch, exact semantics require the scenario packet.
SELECT count(*) AS historical_unknown FROM public.orders WHERE paid_at IS NULL;

-- Separate hypothetical case B, declared pre-existing public.profiles schema:
-- (id bigint PRIMARY KEY, display_name text); no triggers assumed.
ALTER TABLE public.profiles ADD COLUMN display_name_v2 text;

-- ONE BATCH, not a DO loop. Driver supplies numeric :after_id and :batch_size.
-- Driver commits transaction and saves max selected id only after successful commit.
-- Requires deployed atomic mixed writers and final independent reconciliation.
BEGIN;
WITH candidates AS (
  SELECT id FROM public.profiles
  WHERE id > :after_id
  ORDER BY id LIMIT :batch_size
), changed AS (
  UPDATE public.profiles p SET display_name_v2 = p.display_name
  FROM candidates c
  WHERE p.id = c.id AND p.display_name_v2 IS NULL AND p.display_name IS NOT NULL
  RETURNING p.id
)
SELECT (SELECT max(id) FROM candidates) AS selected_high_water,
       (SELECT count(*) FROM candidates) AS selected_rows,
       (SELECT count(*) FROM changed) AS changed_rows;
COMMIT;
-- selected_rows = 0 closes this scan only, not the migration correctness gate.
SELECT count(*) AS mismatches FROM public.profiles
WHERE display_name_v2 IS DISTINCT FROM display_name;

-- Separate hypothetical case C: public.items(required_code text), complete
-- source derivation and upgraded writers MUST be established outside this sketch.
ALTER TABLE public.items ADD CONSTRAINT items_required_code_nn
  CHECK (required_code IS NOT NULL) NOT VALID;
ALTER TABLE public.items VALIDATE CONSTRAINT items_required_code_nn;
ALTER TABLE public.items ALTER COLUMN required_code SET NOT NULL;
ALTER TABLE public.items DROP CONSTRAINT items_required_code_nn;
-- Each statement's invocation has explicit boundaries/budgets in the packet.
-- No generic rollback DROP COLUMN is supplied: preserve new writes and prove recovery.
