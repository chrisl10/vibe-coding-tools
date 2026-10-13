# Supplied-input quotation model

One scenario uses one currency and one period (`project` or `month`). Inputs: name, basis (dated user inputs or quote sources), owner_hours, owner_cost_per_hour, subcontractor_cost, fixed_cost, contingency_fraction, pricing_mode (`markup` or `margin`), pricing_fraction, pass_through_cost.

Owner labour L = owner_hours × owner_cost_per_hour. This cost/valuation is counted once. A selling hourly rate is not a labour cost input; do not also add owner opportunity cost. Cash baseline D = subcontractor_cost + fixed_cost. Reserve R = (L + D) × contingency_fraction. Cost basis C = L + D + R. Pass-through T is excluded from reserve and profit uplift by this declared convention.

Markup on cost: service price P = C × (1 + pricing_fraction). Target margin on service revenue: P = C ÷ (1 − pricing_fraction). Proposed total = P + T. Planned surplus = P − C. Effective service margin = (P − C) ÷ P, undefined when P=0. A 25% markup yields 20% margin; a 25% margin needs one-third markup. Contingency reserves uncertainty; markup/margin supplies planned surplus. They are not interchangeable.

This is a proposed pre-tax worksheet price, not acceptance, audited profit or vendor billing. Reserve is a planning allowance, not proof of a cash expense. Tax, FX, collection/payment fees, financing, insurance and warranty liability are excluded unless explicitly allocated into the supplied fixed/subcontract cost with evidence. Clients paying vendors directly should not also be billed pass-through amounts here.

Every amount is finite and nonnegative. Hours/rates/costs capped at 1 billion; decimal exponents −12 through 12 and 30 significant digits. Fractions: contingency 0..1; markup 0..10; margin 0..<1. No guessed percentages. Missing costs and unbounded integration effort stay unresolved, not zero.

The script uses Decimal at precision 60 and reports currency amounts to two decimal places, half up. This display convention is not appropriate for all currencies; keep unrounded values for reconciliation and specify minor-unit requirements before an actual quote. The bundled examples use USD. Project/month separation requires separate scenarios, not adding their totals.
