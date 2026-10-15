# Forecast one person's AI-assisted project

Use for "How long and how much if I work N hours each day with you?" Runtime output is a worksheet and conditional scenarios. This does not configure a project or calculate team headcount.

## Diagnose and collect evidence

Read principles and diagnosis first. Classify happy-path-only effort as planning-fallacy optimism, a demanded fixed date as the commitment trap, and a vague full-product request as wrong granularity. Establish the minimum usable outcome and acceptance checks before estimating it. The existing [planning-fallacy guide](05-planning-fallacy.md) supplies the historical framework; the [fresh distillation](../references/ai-assisted-forecast/research/distillation.md) supports counting validation work when using AI.

Ask one compact batch for experience, unfamiliar work, first-version scope, daily hours, available weekdays, external prerequisites, completed comparable tasks and cash budget. Use [worksheet.md](../references/ai-assisted-forecast/worksheet.md). Identify whether the requested estimate will be treated as a promise. Do not commit to a date through this process.

Use completed comparable work to choose effort ranges when it exists. Otherwise label inputs hypothetical, retain unknowns explicitly, and forecast a small representative slice first. Record owner time spent engineering, learning, verification and rework through acceptance. Reforecast remaining scope after that slice. No fixed sample count establishes confidence by itself; representativeness and validation matter. No universal AI productivity factor is supplied or implied by the official sources. [Evidence and limits](../references/ai-assisted-forecast/research/distillation.md).

## Calculate conditional scenarios

For each bounded scenario, add engineering, learning, verification and rework hours. These categories must be mutually exclusive. Divide their total by the supplied usable fraction, then by N daily scheduled hours. Round required working days upward. A usable fraction describes interruptions and nonproject time, not review already counted in the numerator. Scheduled owner hours include the whole reserved project block; disclose that convention when valuing the owner's time.

Keep verification and rework explicit: generated suggestions and automated review need validation. A zero value requires an explanation rather than an assumption that AI removes the activity. Official inline guidance, official agent guidance.

Optional deterministic calculator, relative to this skill directory:

```bash
python3 scripts/forecast-ai-assisted.py references/ai-assisted-forecast/example-input.json
python3 scripts/test_forecast_ai_assisted.py
```

Its strict input accepts decimal strings, integers and JSON decimal numbers. Missing or extra fields, negative/nonfinite values, boolean numbers, invalid dates, duplicate JSON keys and impractical horizons fail with an explicit error. Numeric values have a maximum of one billion and bounded precision; the date horizon is 36,600 days. Hourly availability is greater than zero and at most 24; usable fraction is greater than zero and at most one. All cost inputs and all four effort fields are required. These are calculator support bounds, not estimation advice. Missing dates/rates stay unresolved in prose instead of being invented for the calculator.

Calendar scheduling uses the specified start date and working weekdays, Monday=0 to Sunday=6. The last scheduled day is completion day. A three-hour task started Monday with three daily hours finishes Monday; elapsed calendar days is zero, but its active calendar span is one day. Holidays and other unavailable dates are not modeled: adjust the worksheet or calculate them separately. Output gives dates and working days; do not label working days calendar days.

External prerequisites use ready-after-calendar-days offsets from the same start date. The calculator assumes they are independent release gates and engineering can continue while they are pending. Release readiness is the latest of build completion and prerequisite readiness, so overlapping waits do not add. A prerequisite blocking implementation, a chained dependency or a wait starting after build needs a separate schedule; do not insert its raw duration as though it starts on day zero. Unknown readiness makes the release forecast conditional. The calculator does not simulate a general dependency graph.

## Calculate cash separately

Supply one currency and a cost basis naming user-supplied assumptions or dated quotes. Direct cash equals one-time cash plus variable cash per scheduled owner hour plus recurring cash for each started 30-day block of the active calendar span. Started blocks are a conservative planning convention, not a vendor billing prediction; actual billing cycles and minimum commitments need a separate worksheet. Zero work and zero wait starts no recurring block, but one-time cash is still charged. Owner-time value equals scheduled owner hours times the owner's supplied hourly valuation and is displayed separately. These scenarios do not claim current vendor prices or forecast continuing postlaunch operating costs.

## Deliver and qualify

Return diagnosed cause, accepted scope, inputs and their evidence, lower/upper scenarios, working days and calendar dates, external readiness assumptions, cash and owner-time value, a calibration checkpoint and one recommendation. Without empirical calibration, call the result an assumption-based range and omit P50/P85/P95 or confidence percentages. Relative story-point sizing does not supply dated forecasts. Anti-pattern: multiplying AI generation time by a guessed productivity factor and treating the result as a contract.

Check that increased daily hours changes working days, verification remains represented, independent dependencies overlap, and cash never silently includes owner-time valuation. The [worked example](../examples/ai-assisted-forecast.md) and calculator tests exercise these requirements. Application implementation requires separate authorization and the relevant development owners. Parent registration and distribution must resolve this existing pair before invocation; an on-disk file alone is not installed-host proof.
