# estimation-stinger

The paired Stinger for `estimation-wasp-drone`. Encodes the full software estimation and probabilistic forecasting knowledge base: relative-sizing frameworks (Fibonacci story points, T-shirt sizing), the NoEstimates movement, the planning-fallacy literature, and Monte Carlo simulation for delivery forecasting.

**Procedure:** [skill procedure](SKILL.md)
**Research summary:** [`research/research-summary.md`](research/research-summary.md)

## Quick-start for estimation-wasp-drone

1. Read `SKILL.md` (master index).
2. Read `guides/01-diagnosis.md` to classify the team's dysfunction before recommending any technique.
3. Navigate to the relevant technique guide (`guides/02-*` through `guides/05-*`).
4. Use `templates/estimation-advisory.md` to structure the output.

## AI-assisted individual-project forecasts

For a build at N hours daily, use [guide 06](guides/06-ai-assisted-forecast.md), the [input worksheet](references/ai-assisted-forecast/worksheet.md), and [worked example](examples/ai-assisted-forecast.md). The optional [stdlib Decimal calculator](scripts/forecast-ai-assisted.py) separates engineering, learning, verification and rework, scheduled weekdays, overlapping independent release gates, direct cash and owner-time valuation. [Tests](scripts/test_forecast_ai_assisted.py) exercise boundaries and accounting behavior. [Fresh research](references/ai-assisted-forecast/research/distillation.md) supports retaining review work; no universal AI speed gain or confidence percentage is inferred.

Owning-pack workflow: [estimate-build](../../commands/estimate-build.md). It produces a conditional range and calibration checkpoint, with no app implementation or provider actions.

## Total build budget including AI tools

For O037, read [guide 07](guides/07-total-build-budget.md), the [cash/time/credit worksheet](references/build-budget/worksheet.md), [fictional examples](references/build-budget/fictional-examples.md) and [fresh source digest](references/build-budget/research/distillation.md). Reuse the current forecast helper and resolve Operating Cost for applicable monthly mechanics. Actual invoice periods, subscription quotas, API token/tool meters, contractors/assets and the first operating period are reconciled once. Unknowns remain gaps; owner-time valuation stays separate; no vendor-rate or AI-productivity default is supplied.
