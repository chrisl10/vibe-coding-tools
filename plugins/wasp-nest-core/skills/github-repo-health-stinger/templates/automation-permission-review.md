# Automation and permission review worksheet

Data collection mode: local clone / supplied evidence / authorized read-only API.
Review date, repository/product/version, source revision:
Coverage gaps (live rules, organization policy, environment, provider, runners):
No workflows/scripts/artifacts executed; no settings changed:

| Job and exact source path:lines | Event and filters | Workflow source revision | Checkout/fetch repository and SHA | Who controls executable code/config/dependencies? |
|---|---|---|---|---|
| | | | | |

| Job | Workflow/job token grants and effective-default evidence | Secret names/scopes only | Environment protections/bypass evidence | OIDC request and provider trust evidence |
|---|---|---|---|---|
| | | | | |

| Boundary | Producer repository/ref/SHA/run | Consumer authority | Artifact selection/digest and execution | Cache scope/restore/access | Runner reuse/isolation/network evidence |
|---|---|---|---|---|---|
| | | | | | |

| Candidate SHA/ref | Run ID/attempt and workflow revision | Required name/expected App | Conclusion and skip/cancellation reason | Executed stages | Missing candidate proof |
|---|---|---|---|---|---|
| | | | | | |

| Finding | Evidence and archive/settings URL | Observed / supplied / inferred | Boundary and implication | Confidence/gaps | Impact | Effort | Impact/effort | Owner |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Eight-dimension score if full audit: each dimension scored or N/A; assessed weight; full or partial formula; scoped review may be unscored. Never claim passing tests from skipped success, verified cloud policy from id-token permission, or safe automation from event name alone.
