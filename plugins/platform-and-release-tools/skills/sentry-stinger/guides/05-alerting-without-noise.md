# 05. Alerting without noise

## The model: trigger + filter + action

- **Trigger** (WHEN): an issue-state event - created, resolved, escalates, resolved-issue-reopens. Multiple triggers in one alert run under `ANY`.
- **Filter** (IF): a condition narrowing which matching issues actually fire the alert - severity, assignment, team. Group multiple filters under `ANY` or `ALL`.
- **Action** (THEN): Slack/Teams/Discord, email, PagerDuty/Opsgenie, Jira/Linear/Azure DevOps ticket, webhook.

Newer terminology: a **Monitor** defines what to track and when to create an issue; an **Alert** defines who gets notified when that issue is created. One Alert can serve many Monitors - configure routing once, reuse it [raw/sentry--alerts--issue-alert-rules-noise.md].

## Inspect the actual default and recipient fallback

The August archive describes older all-project-members behavior. Current official documentation says the preferred-channel action's suggested-assignee fallback defaults to Recently Active Members, with All Project Members and No One also available. Inspect the actual rule and every recipient fallback before claiming who receives it. Available actions depend on installed integrations. Current source

For a measured impact signal, adopted urgency policy and acceptance record, follow [guide 07](07-qualify-actionable-alerts.md) before proposing configuration.

## Three concrete levers, in priority order

1. **Define "new" by threshold, not by first occurrence.** Alert once an issue crosses N events or M affected users, not on the very first single occurrence - a single occurrence of a rare edge case is not the same signal as a fast-climbing issue.
2. **Route unassigned-issue noise deliberately.** Inspect issue assignment, installed action and current recipient fallback. Propose the owner-approved triage destination instead of assuming a historical default supplies the right recipient. Current source
3. **Filter by severity or exception type.** `level:fatal` is one of the highest-signal single filters available. If that's too blunt (some `fatal`-level exceptions genuinely aren't actionable, e.g. transient `ReadTimeout`), filter out the specific exception type rather than loosening the level filter for everything.

[raw/sentry--alerts--issue-alert-rules-noise.md]

## Throttling - per-issue, not global

The Throttling option sets a minimum re-trigger interval **for the same issue**. It stops one bursting issue from spamming repeatedly, but does not suppress simultaneous alerts from *different* issues that all match the same rule at the same time - don't rely on it as a global rate limiter [raw/sentry--alerts--issue-alert-rules-noise.md].

## Prepare an approved response shape

Use [guide 07](07-qualify-actionable-alerts.md) to distinguish a page from a triage ticket or feed using measured impact and the team's existing response policy. A fatal level, new issue or unassigned issue does not supply an owner, hours, threshold or paging authorization. Keep those decisions draft when absent.

Current frequency and event-attribute filters only work with new-issue and event/activity triggers. Check the exact selected trigger/filter combination; adding a count condition to an unsupported trigger does not establish a working threshold. Current source

Expand filters and add rules only as specific observed noise patterns justify it - don't pre-build an elaborate rule taxonomy speculatively before the project has real alert traffic to tune against [raw/sentry--alerts--issue-alert-rules-noise.md].

## ML Priority Alerts - treat as directional, not guaranteed-available

An ML-classifier-driven default alert rule and Escalating Issues detection exist per a 2024 Sentry blog post, claimed to average a 35% alert-volume reduction for adopters, gated to a Business-tier plan at time of writing. This was not re-confirmed against current pricing/feature availability in this research - mention it as a possibility worth checking in the Sentry dashboard directly, not as a feature to assume is active or included in the current plan [raw/sentry--alerts--issue-alert-rules-noise.md].

## Next

`06-cost-control-and-triage.md` covers the two remaining topics that tie everything above together: keeping the event bill under control, and correctly triaging handled vs. unhandled errors so alerts fire on the right things.
