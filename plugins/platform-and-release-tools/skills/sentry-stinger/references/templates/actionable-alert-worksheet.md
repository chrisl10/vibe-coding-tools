# Actionable-alert worksheet

Status: DRAFT. Complete fields with evidence or mark unknown. Values below are blank placeholders, not accepted policy. Procedure: [guide 07](../../guides/07-qualify-actionable-alerts.md).

| Field | Recorded value and evidence |
|---|---|
| User journey and expected result | |
| Service / Sentry organization-project scope | |
| Environment emitted by SDK / deployment environment | |
| Release and active older-release population | |
| Observed failure or latency impact / UTC timestamp | |
| Numerator definition, unit and query | |
| Denominator definition, unit and query | |
| UTC window / baseline window / ingestion delay | |
| Sample size / volume floor / timeout treatment | |
| Error/trace/replay sample rates / inherited sampling | |
| Filters, quotas, drops and unknown coverage | |
| Adopted SLI/SLO and policy version, or unknown | |
| Threshold / comparison / window / approval source | |
| Page, triage or feed / reason / staffed hours | |
| Primary owner / destination / backup | |
| Acknowledgement / escalation policy and evidence | |
| Runbook / permitted diagnosis / mitigation authority | |
| Issue source or connected monitor | |
| WHEN / IF qualifier and exact filters / THEN | |
| Current trigger/filter compatibility confirmed | |
| Installed integration / recipient fallback | |
| Per-issue throttle / incident deduplication boundary | |
| Security policy / notification field allowlist | |
| Replay and sensitive-data evidence or disabled/pending | |
| Recovery threshold / duration / same-population check | |
| Change authorization / reviewer / unresolved fields | |

## Acceptance record

| Case | Expected result | Observed evidence / pending |
|---|---|---|
| Impacting failure above adopted threshold | Intended owner/action | |
| Non-impacting or handled noise | Defined triage/feed or none | |
| Below threshold with normal denominator | No urgent action | |
| Low volume / absent / stale telemetry | Inconclusive branch per policy | |
| Wrong environment or excluded release | Scoped behavior, explicit coverage gap | |
| Same issue repeated inside throttle | Per-issue behavior | |
| Two different issues from one incident | Dedup boundary explicitly checked | |
| Wrong/missing integration, owner or fallback | Draft, unresolved recipient | |
| Synthetic sensitive values | Required fields absent from every output | |
| Recovery followed by recurrence | Recovery and regression branches | |
| Test notification receipt | Separate from trigger evaluation | |
| Acknowledgement and backup escalation | Separate from delivery | |

Evidence levels: worksheet complete; source reasoning checked; configuration observed; trigger exercised; delivery observed; response observed; recovery observed. Record each independently with UTC time and exact artifact. A blank field or hypothetical case supplies no live evidence.
