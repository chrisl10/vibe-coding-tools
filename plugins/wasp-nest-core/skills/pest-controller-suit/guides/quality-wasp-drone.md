# quality-wasp-drone

**Plugin owner:** `wasp-nest-core`. **Required selection:** Core itself. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain
This Drone is the final checkpoint in the plan-implement-security-QA loop. It audits implementation against the selected PRD in `library/requirements/` or IRD in `library/issues/`, checks requirements and acceptance criteria against code, and reports Critical / Warning / Suggestion findings. It does not implement fixes or replace the plan's decisions. Security always precedes Quality on the candidate.

## Paired Stinger
[quality-stinger](../../quality-stinger) - the five-axis evaluation model, severity decision tree, and report-writing templates.

## Trigger phrases
- "QA this implementation against the PRD"
- "audit the implementation"
- "check the plan against the code"
- "run quality-wasp-drone on this branch"
- "verify the PRD was actually built"
- "did we miss anything from the issue spec"

## Do NOT route when
- Security has not yet run for this cycle: this Drone must not be invoked before `security-wasp-drone`; if invoked out of order, flag the violation and halt rather than proceeding.
- The task is general code quality, testing strategy, or linting review with no source plan to audit against: that broader "is this code good" question, disconnected from a specific PRD/IRD, sits closer to a code-review pass than this Drone's plan-vs-implementation audit; this Drone needs a plan document as ground truth, not a general quality opinion.
- The task is judging whether the plan itself is well-formed: that belongs to `library-wasp-drone`, the plan's author, not this Drone.
- The task is fixing the gaps found: this Drone reports with coordinates and recommended remediation, it never implements fixes itself.
- The task is a security-specific vulnerability or hardening question: that is `security-wasp-drone`'s domain and must close out before this Drone's pass is valid.

## Inputs the Drone needs
- The matching PRD or IRD path under `library/requirements/<lifecycle>/` or `library/issues/<lifecycle>/`
- A `git diff`/`git status` capturing every file added, modified, or deleted for the branch
- Confirmation that `security-wasp-drone` has already run for this cycle
- Access to the plan's User Stories and Acceptance Criteria to seed the traceability table

## Verification artifacts (O293)

Route exact-candidate evidence packets through the existing Quality pair after matching Security review. Its [verification guide](../../quality-stinger/guides/08-verification-artifacts.md) binds plan/content manifests, actual check receipts, generated outputs and producer limits. Preserve NOT_RUN, skip, cancellation and stale results. Draft authorship does not create independent approval; source checks do not establish native/provider behavior.

## Outputs
- A report in the selected v2 PRD/IRD folder's `qa/<date>-qa-report.md`, or `library/requirements/reports/<domain>/` for a standalone audit. Preserve a receiving repository's documented legacy report destination when auditing its existing plans.
- A traceability table mapping every plan item to code (or marking it a gap)
- Findings classified Critical / Warning / Suggestion, each with file:line + snippet

## Commonly sequenced with
- `security-wasp-drone` always before: security fixes can invalidate a QA snapshot taken too early
- `library-wasp-drone` for ambiguity: any ambiguous requirement in the plan is deferred back to the plan's author, not reinterpreted here
- Any implementing Drone (react/python/payments/etc.) before: this Drone audits their completed work against the plan
