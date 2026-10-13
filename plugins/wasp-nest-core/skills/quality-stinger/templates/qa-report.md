<!-- For Library Schema v2, save inside the source plan's qa/ folder.
Standalone audits use library/requirements/reports/<domain>/.
Honor receiving-repository legacy conventions; do not overwrite prior evidence. -->

# QA Report: {{plan_name}}

**Plan document:** `{{plan_path}}`
**Audit date:** {{YYYY-MM-DD}}
**Base branch:** `{{base_branch}}`
**Head:** `{{head_branch_or_sha}}`
**Auditor:** quality-wasp-drone
**Candidate scope and manifest:** `{{reviewed scope, manifest path and SHA-256; resolved HEAD alone does not pin dirty contents}}`
**Plan digest:** `{{SHA-256}}`
**Security evidence:** `{{report path, digest, completion time and matching candidate pin}}`
**Verification packet:** `{{companion packet path and digest; use templates/verification-artifacts.md}}`
**Claim boundary:** {{source/static/local/native/provider/manual; missing proof and imported/self-authored evidence limits}}

<!-- Bind actual checks and generated artifacts to this candidate. Preserve NOT_RUN,
skips, expected failures, cancellation, unknown and stale results. An author draft
is not independent QA approval. See guides/08-verification-artifacts.md. -->

## Summary

{{2-3 sentence verdict. Lead with the overall call (pass / pass-with-warnings / blocked), then the headline findings, then the recommendation.}}

## Scorecard

| Category      | Status         | Notes |
|---------------|----------------|-------|
| Completeness  | {{✅ / ⚠️ / ❌}} | {{one-line}} |
| Correctness   | {{✅ / ⚠️ / ❌}} | {{one-line}} |
| Alignment     | {{✅ / ⚠️ / ❌}} | {{one-line}} |
| Gaps          | {{✅ / ⚠️ / ❌}} | {{one-line}} |
| Detrimental   | {{✅ / ⚠️ / ❌}} | {{one-line}} |

## Critical Issues (must fix)

- [ ] **{{short title}}**, `{{path/to/file.ts:LN-LN}}`

  {{2-4 sentence explanation: what's wrong, why it matters, suggested remediation.}}

  ```{{lang}}
  {{1-6 lines of offending or missing code}}
  ```

<!-- Repeat. If none, write: "None." -->

## Warnings (should fix)

- [ ] **{{short title}}**, `{{path/to/file.ts:LN-LN}}`

  {{explanation}}

  ```{{lang}}
  {{snippet}}
  ```

<!-- Repeat. If none, write: "None." -->

## Suggestions (consider improving)

- [ ] **{{short title}}**, `{{path/to/file.ts:LN-LN}}`

  {{explanation}}

<!-- Repeat. If none, write: "None." -->

## Plan Item Traceability

| #      | Plan Requirement                          | Status | Implementation Location          | Notes |
|--------|-------------------------------------------|--------|----------------------------------|-------|
| {{ID}} | {{short description}}                     | {{✅ / ⚠️ / ❌ / 🟦}} | `{{path:LN-LN}}`                 | {{optional}} |

<!-- Include every plan requirement and every Non-Goal (NG-*) row. No silent omissions. -->

## Files Changed

- `{{path/to/file.ext}}` ({{A/M/D/R}}), {{one-line summary of the change}}

<!-- Sort alphabetically by path. One line per file. -->
