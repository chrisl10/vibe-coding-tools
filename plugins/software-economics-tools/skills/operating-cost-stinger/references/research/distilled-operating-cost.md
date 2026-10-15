# Operating-cost distillation

Observed 2026-10-07. Five current official vendor documentation bodies were retrieved and archived with provenance headers and body hashes. Maintained pages may lack publication dates; fresh retrieval is not claimed as fresh publication. No numerical vendor rate from these pages is adopted as a default.

| Domain claim | Grounding and modeling implication |
|---|---|
| Railway describes a subscription amount that goes toward resource usage. | Railway raw. A floor covered by usage must not be added to that same usage as an independent fee. Confirm the actual plan's invoice semantics. |
| Vercel distinguishes included quantities from a monetary usage credit, with usage charging after the applicable inclusion. Regional pricing is explicit. | Vercel raw. A unit allowance and a cash credit are different fields; regional/unit evidence accompanies each rate. |
| Supabase anchors billing cycles to organization creation, has fixed fees and usage fees, and applies compute credits at the billing level while additional projects add cost. | Supabase raw. Keep plan fees and per-project compute separate and allocate a shared credit once across eligible costs. Calendar-month estimates may differ from invoice timing. |
| Neon describes distinct compute, storage, branch and transfer metrics; workload/configuration affect the bill. Current docs describe usage-based paid plans with no minimum monthly fee. | Neon raw. Measure each billed unit rather than guessing a per-user infrastructure constant. No generic minimum is invented. |
| AWS Pricing Calculator supports pre-build solution modeling and inspecting estimate calculations. | AWS raw. Use workload-specific estimates and evidence rather than claiming AWS is universally expensive. |

## Bounded model decisions

The local tool accepts supplied provider-neutral rate inputs. It does not infer a provider plan from a brand or apply the archived vendors' numerical rate tables. For each provider group, quantity allowances are consumed first, usage-scoped credit allocations second, minimum-usage floor or additive fee third, and total-invoice credit allocations last. This order is an explicit model contract; use it only when it matches the actual provider agreement. A different credit/floor order requires a worksheet extension. Sources motivate the distinction but do not claim every provider implements this exact generic order.

Credit budgets are scenario-local. Each pool declares its available currency amount, eligible provider IDs and scope. Allocations cannot exceed the shared budget, eligible charge or available usage. Unused credit is reported, never treated as income. Alternatives low/base/high are independent, not three invoices sharing a pool. Operator paid labor is cash cost; unpaid hours multiplied by a user-supplied value are separate opportunity cost. These are modeling decisions, not tax/accounting conclusions.

Linear meters only: no tiered pricing, annual-contract proration, currency conversion, taxes, reserved commitments, late invoices or autoscaling inference. Platforms supply the actual constraints and rates. Unknown charges remain evidence gaps instead of zero.
