# Synthetic automation review cases

These cases exercise interpretation. They are invented descriptions, not repository findings, runnable workflows or exploit demonstrations. Apply the [guide](../guides/10-review-automation-permissions.md) and record missing evidence rather than manufacturing a clean bill of health.

| Case | Supplied facts | Expected review result | Owner |
|---|---|---|---|
| A: fork build in privileged context | pull_request_target job overrides checkout to fork head, installs its dependencies, secret reference exists; action version omitted | Cite the input-to-execution boundary and potential privileged exposure. Inspect version-specific guards/effective grants before confirming behavior. No execution to prove exploit. | Security; CI Release for design |
| B: label-only event | pull_request_target uses base source and treats PR labels as data; job issues:write and contents:read | Narrow task-compatible grant is observable. Runner and default policy remain unknown; event alone is no vulnerability finding. Review interpolation/data handling if supplied. | Security for unresolved input handling |
| C: privileged artifact consumer | workflow_run downloads a named artifact from a fork PR and runs its script; producer run identity/digest absent | Artifact became executable across privilege boundary; name does not prove origin. No download/execution. | Security and CI Release |
| D: named environment | deploy job says environment:production; no settings packet | Environment protections unverified. Do not assert required reviewers or cloud permission. No create/configure action. | Human evidence request; CI Release |
| E: OIDC permission | id-token:write and contents:read; no provider trust policy | Can request a token under documented rules, but no proof of role access or least privilege. Subject/audience/product specifics remain unknown. | Security/provider owner |
| F: workflow filter | required build workflow filtered to src changes, current PR only changes docs | If workflow skipped, associated check may remain pending. Do not claim tests passed or silently exempt requirement. | CI Release |
| G: conditional skipped job | test job if evaluates false; recorded success, no executed tests | Platform success does not prove test execution. Mark task proof incomplete; no speculative vulnerability verdict. | CI Release |
| H: old green / new cancelled | old SHA passed; current candidate cancelled; build completed but integration tests not run | Current candidate unproven. Report completed stages and cancellation, never substitute old SHA or green aggregate. | CI Release |
| I: cache override | low-trust job explicitly enables cache writes; consumer later restores same scope; versions and runner lifecycle missing | Review observed override and provenance. Do not claim all low-trust caches are writable by default or a hash key prevents poisoning. | Security; CI Release |
| J: merge queue gap | supplied settings require build; source workflow only pull_request, queue configured | Missing merge_group coverage is a required-check alignment finding; live policy supplied, no API mutation. | CI Release |

Qualification: manual table exercises, source review and archive hashes. No native runs, ruleset enforcement, credentials, provider policy or exploit proof.
