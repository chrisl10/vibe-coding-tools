# Worked source example: scoped order summaries

This is a hypothetical synchronous Django 5.2 model contract, not executed DB evidence. Assume Order has tenant_id, owner_id, customer (FK), items (reverse FK); LineItem has tenant_id, order, product (FK), visible and status. The established policy in this example permits only the owner's tenant orders and visible children. A real application must retain its own policy, including nested Product/Customer visibility if required. Authorization is not furnished by eager loading.

## Before: repeated relation access

```python
from django.db.models import Prefetch


def before(Order, principal):
    orders = Order.objects.filter(
        tenant_id=principal.tenant_id, owner_id=principal.id
    ).order_by("id")[:20]
    return [
        {"id": order.id, "customer": order.customer.name,
         "items": [{"product": item.product.name, "quantity": item.quantity}
                   for item in order.items.filter(
                       tenant_id=principal.tenant_id, visible=True, status="open"
                   ).order_by("id")]}
        for order in orders
    ]
```

## After: same filters, shape and ordering

```python
def after(Order, LineItem, principal):
    children = LineItem.objects.filter(
        tenant_id=principal.tenant_id, visible=True, status="open"
    ).select_related("product").order_by("id")
    orders = (Order.objects.filter(
        tenant_id=principal.tenant_id, owner_id=principal.id
    ).select_related("customer").prefetch_related(
        Prefetch("items", queryset=children, to_attr="open_visible_items")
    ).order_by("id")[:20])
    return [
        {"id": order.id, "customer": order.customer.name,
         "items": [{"product": item.product.name, "quantity": item.quantity}
                   for item in order.open_visible_items]}
        for order in orders
    ]
```

The consuming serializer must use open_visible_items; retaining order.items.filter(...) defeats the filtered prefetch. If customer is nullable, both implementations need the same explicit null handling. If product has additional access restrictions, use the existing authorized selector for children and verify excluded products rather than broaden visibility.

## Query hypotheses to test

Let N be returned orders and M be returned visible open items. Assuming fresh QuerySets, non-null customer/product FKs, one database, no hidden properties and no request middleware queries, the before code is expected to issue 1 + 2N + M queries. The after code is expected to issue 2 on a nonempty page and 1 on an empty page. These are explanatory expectations, not observations or application budgets.

| Scenario | Hypothetical before | Hypothetical after | Additional acceptance |
|---|---|---|---|
| Empty page | 1 | 1 | Same empty response |
| 1 order, 2 qualifying items | 5 | 2 | Same customer and item ordering |
| 10 orders, 20 qualifying items | 41 | 2 | Other-tenant and hidden items excluded |
| Consumer calls filtered manager after prefetch | Depends on fields consumed | 2 plus N filtered queries before nested lazy access | Fails intended consumption contract |
| only("id") then reads deferred field per order | 1 + N for that field under fresh synchronous instances | Pending repair measurement | Avoid a second N+1 via serialization |
| Chunked iterator/export | Depends on chunk count and lookup structure | Measure per chunk | Do not reuse the page's two-query expectation |

Prepare fixtures outside the query assertion. Compare before and after materialized dictionaries on the same fixture, then assert observed query budgets on fresh instances. Include unauthorized principal, other tenant, filtered rows, null relation, totals/pagination and nested-field cases. Native DB proof is pending because the forge runtime has no Django installed.

Sources: QuerySet API digest, [official query APIs](https://docs.djangoproject.com/en/5.2/ref/models/querysets/), [official measurement API](https://docs.djangoproject.com/en/5.2/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries).
