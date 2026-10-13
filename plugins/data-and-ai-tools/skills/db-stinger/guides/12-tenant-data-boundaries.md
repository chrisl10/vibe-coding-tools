# 12: design tenant data boundaries and prepare denial proof

Use the [boundary worksheet](../templates/tenant-boundary-proof.md), [source cases](../examples/tenant-boundary-cases.md) and [captured facts](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/data-and-ai-tools/skills/db-stinger/references/research/tenant-boundaries/distillation.md). This is architecture and verification preparation. Security accepts the control design and conducts the security audit; Quality executes the approved proof after Security.

## 1. Name identity and every access path

Record exact server, ORM/client revision, provider endpoint, pooler mode and deployment revision. Enumerate ordinary request handlers, raw SQL, ORM relations, joins, aggregations, bulk updates, imports/exports, jobs, migrations, privileged support, reporting, CDC, cache and search. Identify which principal authenticates each path, how membership is checked, and who can choose tenant context. A tenant_id supplied in a URL, job payload or JSON body is not membership evidence. Background workers must revalidate the authority appropriate to their operation; cancellation, membership revocation and retry semantics belong in the packet.

## 2. Declare the database role boundary

List connection role, effective role, memberships, table owner, superuser/BYPASSRLS flags, RLS enable/FORCE flags, grants and applicable policies per table. Record views, security-definer functions and privileged escape paths for Security review. A green query under the owner is not proof that an ordinary app identity is constrained. FORCE does not constrain a superuser or BYPASSRLS role. TRUNCATE and REFERENCES need grant review. Source: row-security capture.

## 3. Choose the enforcement design with its actual trust model

For application enforcement, centralize authorization and tenant predicates at the server data boundary; require those predicates on nested relations, counts, mutations and exports. Inspect generated ORM SQL. An unfiltered fallback, admin credential or raw query can defeat this architecture. For RLS, define USING and WITH CHECK for each action and evaluate all applicable policies together. An additional permissive policy can widen access. Include tenant-changing writes, missing context, invalid context and role inheritance. Combining application controls with RLS can add defenses but does not remove either proof requirement. Do not infer RLS from selecting Supabase, Neon or another provider. Sources: row-security and policy captures.

Tenant-scoped relationships need an explicit invariant. A projects row in tenant A must not reference a tenant B account merely because account_id exists. A reviewed composite relationship such as (tenant_id, account_id) can enforce matching scope where the referenced pair is unique; capture actual generated constraints and mutation outcomes. Have Security assess error/existence disclosure through integrity checks.

## 4. Make pooled context atomic with the query

If the design uses transaction-local context, authenticate and authorize before deriving it, establish it inside the same transaction as every relevant query, and fail closed when absent or invalid. Inspect driver transaction callbacks and pooler compatibility. Do not set tenant context on one pooled connection then execute on another. SET LOCAL ends at commit/rollback; session SET is not safe request identity in transaction pooling. A custom setting is a trusted app assertion, not independent database authentication: assess arbitrary-SQL authority and injection with Security. Test missing context after both successful and failed transactions, and A-to-B reuse under concurrency. Sources: SET and PgBouncer captures.

## 5. Carry the boundary across derived data

Caches, CDN responses, object keys, search/embedding indexes and materialized exports require tenant and permission scope. Specify key construction, invalidation, membership changes, retention and index update lag. Apply authorized filters before retrieval results can become candidates; never fetch all tenants then filter only rendered output. Recheck authority before serving cached/exported artifacts. Jobs need explicit scope and narrowly granted principals; retries cannot inherit a preceding job's tenant. These are derived architecture policies, not claims about a provider's defaults.

## 6. Prepare native proof and report gaps

In an authorized disposable representative environment, seed clearly synthetic tenants A/B plus privileged and ordinary identities. Run same request/query as each principal; prove own-tenant allowed controls, cross-tenant read invisibility, mutation denial/no effects, tenant-changing writes denied, relation/aggregate/export restrictions, pool reuse and background/cache/search cases. Check database side effects independently; an HTTP 403 alone is insufficient. Record exact revisions, role/policy/catalog snapshots, expected result, actual result and sanitized evidence. Use a privileged harness identity only for fixture/setup and independent effect checks, never as the actor under test. Do not run production probes without authorization. Until actual evidence exists, report SOURCE REVIEW ONLY and list each missing path.
