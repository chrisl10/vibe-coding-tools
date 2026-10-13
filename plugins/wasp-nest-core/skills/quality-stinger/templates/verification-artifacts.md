# Verification artifacts: {{audit_id}}

Companion to `qa-report.md`, not a second audit engine. Fill actual observations; unresolved fields remain UNKNOWN. Do not leave placeholder PASS verdicts. Local format, not a signed attestation.

## Candidate identity

- Plan path and SHA-256: {{path, digest}}
- Repository/worktree and resolved base/head IDs: {{values}}
- Dirty state and included/excluded paths: {{values}}
- Candidate manifest path and SHA-256: {{values}}
- Manifest rules: {{sorted relative paths, exact-byte digest, additions/deletions, symlink target and mode policy; excluded logs, evidence and secrets}}
- Freeze timestamp; before/after consistency check: {{actual values}}
- Previous candidate and superseded evidence: {{values or None}}

## Producers and chronology

| Artifact or report | Producer and role | Start/end UTC | Candidate manifest digest | Output path and digest | Basis and limits |
|---|---|---|---|---|---|
| Security | {{identity}} | {{timestamps}} | {{digest}} | {{path, digest}} | {{actual review}} |
| Quality | {{identity}} | {{timestamps}} | {{digest}} | {{path, digest}} | {{actual review after Security}} |
| Generated output | {{builder/version}} | {{timestamps}} | {{digest}} | {{path, digest}} | {{inputs and build receipt}} |

## Check receipts

| ID and requirement | Command/runner, cwd, versions and nonsecret inputs | Candidate digest | Start/end UTC | Exit and signal | Observed outcomes | Log/output digest | Result and limitation |
|---|---|---|---|---|---|---|---|
| {{check}} | {{exact invocation}} | {{digest}} | {{times}} | {{values, or UNKNOWN}} | {{pass/fail/skip/xfail/xpass counts or N/A}} | {{path, digest}} | {{PASS/FAIL/NOT_RUN/SKIPPED/CANCELLED/INCOMPLETE/STALE/UNKNOWN}} |

## Trust and claim boundary

- Collection type: {{observed execution, imported vendor result, manual inspection, hypothetical example}}
- Artifact producer and evidence collector: {{identities; self-authored if applicable}}
- Signature/attestation: {{NOT_PRESENT or actual verification result, signer, policy and artifact subject digest}}
- Inputs/dependencies/platform omitted from manifest: {{limits}}
- Permitted conclusion: {{exact claim supported}}
- Runtime/provider/other-host proof not supplied: {{requirements}}
- Sensitive fields excluded or redacted: {{names/categories, never values; restricted original location only if authorized}}
- Reviewer decision and open findings: {{actual result; author draft is not approval}}
