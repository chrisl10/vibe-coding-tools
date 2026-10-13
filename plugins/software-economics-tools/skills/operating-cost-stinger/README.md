# Operating cost

Estimate low/base/high monthly operating costs from a supplied workload and dated provider rate inputs. Distinguish cash from operator time valuation, additive fees from usage floors, and unit allowances from shared monetary credits.

| Load | Purpose |
|---|---|
| [Intake](guides/01-intake.md) | Workload, rates, units, regions and invoice semantics |
| [Calculate and report](guides/02-calculate-and-report.md) | Scenario reconciliation and evidence-backed recommendation |
| [Model](references/model.md) | Exact JSON fields, generic credit/floor order, formulas and limits |
| [Input](references/templates/input.json) / [worksheet](references/templates/worksheet.md) | Explicit assumptions and reviewable output |
| [Fictional example](examples/fictional-monthly-cost.md) | Worked low/base/high arithmetic |
| [Source distillation](references/research/distilled-operating-cost.md) | Official provider semantics, with original raw archive |
| [Calculator](scripts/README.md) | Offline stdlib Python CLI and meaningful tests |

No rate is inferred from a vendor name. This component does not select architecture, set a SaaS price, deploy, or configure live cost controls. The model's credit/floor ordering must fit the actual provider agreement before it can represent that invoice. Resolve selected platform owners through trusted Core for constraints this model does not cover.
