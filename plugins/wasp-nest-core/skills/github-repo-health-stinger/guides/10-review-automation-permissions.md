# Review automation and permission hygiene

Use for O114: “Can this repository's automation run changed code with too much authority, or show green checks without the intended proof?” Start with [principles](00-principles.md). This is a scoped hygiene review, not an exploit assessment or workflow repair. Read the current evidence digest, complete the [worksheet](../templates/automation-permission-review.md), then compare the [synthetic cases](../examples/automation-permission-cases.md).

## Collect evidence without running automation

Declare local clone, owner-supplied settings/run evidence, or already-authorized read-only API scope. Read the supplied workflows at a recorded revision. Follow local referenced action/workflow files as data; do not run scripts, install packages, execute a downloaded artifact, start a workflow or query credentials. Record exact path and lines, revision, product/version and review date. Do not publish secret values or token payloads. Unknown settings stay unknown; a missing evidence packet is not evidence of disabled controls.

## Trace event to execution

Record each event and filter, which revision supplies the workflow, and the actual checkout repository/ref/SHA. Also trace fetch commands, reusable workflows, local actions, build scripts, dependency install hooks and tool configuration. Describe who can change each executable input. A trusted workflow file can execute untrusted code or configuration. For pull_request_target, distinguish current documented defaults from explicit checkout/cache overrides and fetching outside checkout. Do not conclude an event name alone proves vulnerability or safety. Current action protections require version-specific evidence. Sources: secure use and PR target

## Trace job authority and boundaries

For each job, inventory workflow/job permissions, effective repository/organization defaults and fork/event reductions. Record secret names/scopes and availability only, environment references and observed protections, reusable-call inheritance and credential persistence. The action can use github.token even without an explicit token input. An omitted permissions key does not establish least privilege. Escalate uncertain effective grants to Security. Sources: token and syntax

For OIDC, record the requesting job and supplied evidence for issuer, audience, subject/claim restrictions and provider role. id-token: write enables token requests; cloud access depends on the provider trust and role. Record actual subject format without requesting a token. For environments, compare the YAML name with supplied configured protections, branch/tag restrictions, bypass behavior and plan/visibility availability. A name is not an approval policy. Provider/settings inspection beyond authorized evidence is a coverage gap. Sources: OIDC and environments

For artifacts, cache and runners, record producer repository/revision/run, consumer authority, selection by run/digest, whether data becomes executable, cache scope/restore keys/access mode, and runner isolation/reuse/network reach. Artifact names and cache keys alone do not establish origin or trust. workflow_run may cross into a privileged context. Refer boundary findings to Security; CI Release owns pipeline/runner redesign. Sources: events, cache and secure use

## Distinguish merge eligibility from evidence

Record exact candidate SHA/ref, run ID/attempt, workflow revision, required check names and expected source App, conclusion, skip reason and actual completed stages. Consider PR merge commits, head commits and merge-group candidates separately. Current required-check documentation distinguishes filtered workflow skips (pending checks) from conditional job skips (success) and describes merge_group requirements. A platform-accepted skip is not task proof. Cancelled, queued, timed-out or older-candidate runs do not prove the candidate passed; identify incomplete stages without rerunning anything. Concurrency cancellation and aggregate-job conditions belong in the evidence packet. CI Release designs any fix. Sources: required checks, status and syntax

## Report and hand off

Every finding needs observable evidence, boundary crossed, practical implication, confidence, missing evidence, impact 1–5, effort 1–5, priority = impact divided by effort, and named owner. Label source observations, supplied live evidence and inference separately. Rank findings; do not assign an exploit severity or claim remediation from this review. Security owns vulnerability/secret implications; CI Release owns CI/release architecture; the human owns settings changes and authorization.

Keep the eight-dimension model. This supplemental review contributes observations to CI density, settings and required-check findings without creating a ninth score. In a full audit report every dimension; unavailable ones are N/A with missing evidence, not 0 or 10. Report assessed weight and known-dimension score separately. Full coverage score is 10 × sum(score × decimal weight). Partial coverage score is 10 × sum(known score × weight) / sum(known weights), explicitly labeled partial and never a full-repository score. Avoid double deductions for one missing-control finding. A scoped review may remain unscored.
