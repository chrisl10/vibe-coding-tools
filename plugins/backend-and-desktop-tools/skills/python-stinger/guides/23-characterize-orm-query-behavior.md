# 23: Characterize and repair ORM query behavior

Use for O132, N+1 remediation or a serializer that keeps querying after the selector returns. Read [the research digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/python-stinger/references/research/orm-query-behavior/digest.md), [ORM patterns](03-django-orm.md) and [test discipline](10-pytest-discipline.md). Preserve existing behavior before reducing queries.

## Establish the boundary

1. Record the installed Django version, database engine and alias, selector, serializer/schema resolver, endpoint, permission policy, ordering and pagination. Do not infer these from this guide's Django 5.2 references.
2. Map every consumed field: FK attribute, reverse collection, filtered manager, computed property, count, deferred column and nested serializer. Include accesses inside __str__, template callables and validators.
3. Save a synthetic fixture with 0, 1 and many parent rows, multiple children, nullable single relations, filtered-out rows, another tenant and an unauthorized principal. Set the same data for before and after. Keep production data and SQL parameters out of reports.
4. Capture queries around queryset evaluation AND full response materialization. Record baseline counts separately for fixture setup, authentication, pagination count and consumer. Fresh queryset instances avoid an already-populated cache hiding work. Capture each used database alias.
5. Compare response values, shape, ordering, missing/null behavior and denied visibility. A permission failure blocks the optimization even when queries decrease.

Use [the characterization worksheet](../templates/orm-query-characterization.md). No migrations are needed for a loading-strategy repair. A proposed index or data migration leaves this scope and follows the DB owner and [migration guide](04-django-migrations.md).

## Choose the repair from the consumed relation

| Access pattern | Candidate repair | Failure to check |
|---|---|---|
| Forward FK / one-to-one | explicit select_related field paths | nullable values, connector fields, unauthorized related values |
| Reverse one-to-one | select_related using related_name | absent related instance exception and response semantics |
| Reverse FK / M2M collection | prefetch_related or explicit Prefetch | child fanout, ordering and consumer reuse of the prefetch cache |
| Filtered reverse collection | scoped Prefetch(queryset=..., to_attr=...) | consumer must read the list, not call manager.filter again |
| Nested child FK | select_related inside the prefetch queryset | tenant policy on both child and nested object |
| Only a count / existence | consider annotation or Exists under existing filters | join multiplication, distinct semantics and visibility parity |
| only/defer plus serializer access | remove unsuitable deferral or load consumed fields | hidden per-instance fetch, required relation connectors; async cannot lazy-load deferred fields |
| Large export | bounded pagination or measured iterator chunks | in Django 5.2 explicit chunk_size is required with prefetch; each chunk may query |

Reference: [QuerySet archive](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/python-stinger/references/research/orm-query-behavior/raw/querysets.html), select_related, prefetch_related, only, defer and iterator sections. Generic relations and multiple database routing have different counts; do not apply a universal two-query budget.

Keep the application's established permission predicate in the base queryset. Apply the existing child visibility policy to the prefetch queryset too. A join or cached related list does not check object permissions. Do not replace an established selector with Model.objects.all() to make the example fit.

## Measure the result

Run a characterization test with fixture creation outside the measured block. With the project's existing pytest-django dependency, django_assert_num_queries may wrap the selector plus serializer. Django's assertNumQueries is another supported measurement surface. Select the actual database alias. Write a budget only after observing the known fixture; do not copy hypothetical numbers from [the example](../examples/09-orm-query-characterization.md).

Then measure the complete request including authentication and pagination. Counts must not grow per parent for the repaired path. Account for empty pages, totals and batch chunks explicitly. Also compare elapsed time, peak memory, rows transferred and query plan on representative bounded data; one giant joined response can be worse than several small queries. Source: [optimization archive](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/python-stinger/references/research/orm-query-behavior/raw/optimization.html), Profile first.

Accept when response parity and visibility tests pass, observed counts match the documented fixture budget, measured performance meets the user's requirement, and the responsible Security then Quality checks finish. Keep a small selector/consumer patch that can be reverted under the user's Git policy. Never edit an applied migration as part of this fix.

## Report limits

Report source-reviewed, DB-measured and host-request-tested separately. A static heuristic finding is a candidate; it cannot prove a query was issued or eliminated. Missing Django/runtime/DB evidence leaves native qualification pending. No dependency installation or provider access is implicit in this guide.
