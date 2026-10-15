# Actionable-alert worked cases

All services, traffic, releases and policies here are synthetic. These are manual decision exercises, not executed Sentry rules, notification tests or production recommendations. Read [guide 07](../../guides/07-qualify-actionable-alerts.md) and use the [worksheet](../templates/actionable-alert-worksheet.md). Product mechanics and sampling limits derive from the digest.

## A. Checkout failures have a usable denominator

Fictional Node checkout service, production, release fixture-r7. In a ten-minute fixture window, 40 failed eligible attempts out of 2,000 eligible attempts give `40 / 2,000 = 2%`. Both counters come from one complete synthetic request ledger with the same scope, excluding load-test traffic by the same rule. The ledger has 120 exception events because each failed attempt retried three times. `120 / 2,000 = 6%` is events per attempt, not failed-attempt rate. An adopted fixture policy pages checkout-oncall at greater than 1% failed attempts with at least 1,000 attempts in ten minutes during its staffed window. The fixture is above that policy's threshold; the action is justified in the exercise only.

Proposed mapping: an owning monitor that can express the adopted failed-attempt signal creates an issue; production-scoped Alert routes that issue to the supplied installed on-call destination. The current Sentry affected-session filter is not substituted for this custom counter. Verify monitor support before configuration. A runbook inspects the release and dependency status with read-only checks; rollback still needs the app's release authority. Same-issue throttling cannot deduplicate several downstream issues from the same checkout incident.

Recovery fixture: next ten minutes show 2 failures / 2,100 attempts = approximately 0.0952%. This satisfies the fixture's separately adopted recovery policy of below 0.2% for ten minutes, but still needs an authorized successful journey check and incident-owner confirmation. No actual receipt, acknowledgement or recovery has been observed.

## B. Sampled latency cannot support an all-user p95 claim

Search API, fixture-r8. Trace sampler keeps all checkout traces but 1% of search traces. Twelve search durations are retained in ten minutes; a dashboard reports a high sampled tail. The proposed wording says "95% of all users are slow." Reject it: p95 is a duration percentile, not that sentence's impact fraction; sampling scope, low sample size, timeout handling and eligible request denominator are unresolved. Preserve sampled diagnostic evidence and request the service's adopted latency SLI, minimum volume and tail calculation. No numerical population extrapolation or page threshold is manufactured. If the current monitor cannot represent the chosen percentile and operation, hand off measurement without claiming unsupported configuration.

## C. A fatal-looking event with no response owner

One browser extension exception has fatal level and unhandled metadata in a staging fixture. No journey failure is evidenced, no recipient or response-hours policy supplied. Output stays DRAFT: request service owner, destination and impact evidence. Severity metadata alone does not justify paging or prove process termination. If the owner identifies recurring harmless noise, propose a narrowly scoped triage/filter review; do not silently drop all browser errors. Current preferred-channel fallback can include recently active members, so never assume a particular on-caller receives it.

## D. Rule and privacy acceptance have distinct evidence

Synthetic event/activity trigger with production scope and an ALL count filter is reviewed against current trigger compatibility. Positive/negative events and two issue IDs exercise different branches on paper. A second proposal uses an escalation trigger with a frequency filter; reject the mapping because current docs restrict that filter to new-issue or event/activity triggers. A drafted same-issue throttle leaves the two-issue incident deduplication unresolved.

An event includes a fake token in its query string, fake customer text in a breadcrumb and an avatar rendered as a background image. Expected acceptance: notification metadata contains only approved environment, route template, release and aggregate counts; sensitive event fields are scrubbed by the applicable SDK hook; replay stays disabled pending synthetic masking checks including the avatar. Do not assume beforeSend handles every recording event, nor that hashing makes a private value anonymous. If a test notification is later authorized and arrives, only integration delivery is proven. Trigger evaluation, actual on-call schedule, human acknowledgement and escalation remain separate pending observations.

## E. Silence is inconclusive

Production errors vanish immediately after a release, but error sampling changed and quotas dropped incoming events. The numerator is no longer comparable to the prior window. Do not close the incident from silence or a resolved issue state. Record telemetry loss and seek an independently scoped request-success check under existing authority. Missing traffic with zero errors has no finite failure ratio when eligible attempts are zero; retain unknown, not 0% success or 100% reliability.
