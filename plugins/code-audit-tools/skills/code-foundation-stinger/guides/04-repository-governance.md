# 04. Repository governance

README, license, contribution and security documents, CODEOWNERS, branch protection and the OpenSSF Scorecard view. File checks run from the clone; protection and settings need `gh` (read-only).

## Procedure

1. **README (DOCS-001, 002).** Open it. A good README for this audit answers four things: what the project is, the prerequisites (runtime version), the install command, and how to run and test it. The scanner only matches headings and command lines (`possible`). Resolve it: if the steps are there and name scripts that exist (compare each `npm run <x>` to package.json `scripts`, each `make <x>` to the Makefile), drop the finding. If a command names something that does not exist or a version the pin contradicts, write FND-DOCS-050 with both lines as evidence. A stub README is `medium` (DOCS-001 family); missing steps are `low`.
2. **License (DOCS-004).** Missing license is `medium` for a repository others may use, `low` if private (package.json `private: true` or `UNLICENSED`). Never suggest a license; get-started lists the license choice as a human decision. Check that the `license` field in package.json or pyproject, if present, matches the file name you can see.
3. **CONTRIBUTING, SECURITY, CHANGELOG, templates (DOCS-005 to 008).** These mirror the get-started templates (steps 3.2 and 3.4). SECURITY.md also feeds the Scorecard Security-Policy check. All are `low` or `info`.
4. **CODEOWNERS (REPO-001, 002, 011).** Valid locations are `.github/`, the root and `docs/`, first found wins; the file must be under 3 MB; negation, `\#` escapes and `[ ]` ranges do not work; owning `.github/` stops someone quietly removing the review rule. A CODEOWNERS file does nothing at merge time unless review by code owners is required (REPO-011). Open the file; confirm the scanner's line-level complaints.
5. **Branch protection and settings (REPO-003 to 010).** With `--gh`, the scanner combines the classic protection call and the active rules for the default branch (rulesets). Interpret:
   - Classic 404 "Branch not protected" and an empty rules list: unprotected (`medium`, confirmed).
   - Classic 403: you are not admin. If the rules list is non-empty, protection exists; otherwise write a cap and no finding.
   - Protected but force pushes allowed: `medium`. No PR required or no status checks required: `low` each. A solo-maintainer repo may legitimately push to main; say so in `why_it_matters` rather than lowering severity silently.
   - `security_and_analysis` missing from the response means the caller is not admin; write a cap. Secret scanning disabled is `medium`; push protection disabled `low`. These are Settings actions: remediation says "a human with admin rights enables it under Settings, Advanced Security".
   - Community profile below 100 percent is `info`; list the missing files.
6. **Scorecard view.** Read [scorecard-mapping](../references/scorecard-mapping.md). The `scorecard_aligned_pass_rate` measure is an approximation of the checks that can be judged from files plus branch protection. Never call it an official score. If a `scorecard` binary is already installed, run it in local mode against the scratch copy and archive the JSON in `raw/`; report only checks that returned a score. Do not install it.
7. **Commit convention (REPO-023, info).** Only a note: under 50 percent Conventional Commits in the last 50 non-merge commits. Skip it if the project clearly uses another documented convention.

## Severity calibration

| Situation | Severity |
| --- | --- |
| No README | medium |
| No license on a public repo | medium |
| Default branch unprotected | medium |
| Force pushes allowed on default branch | medium |
| Secret scanning off (visible) | medium |
| No CODEOWNERS, SECURITY.md, CONTRIBUTING.md | low |
| Missing templates, changelog, community profile gaps | info |

## References loaded by this guide

- [scorecard-mapping](../references/scorecard-mapping.md), [gh-readonly-calls](../references/gh-readonly-calls.md), [get-started-assess-map](../references/get-started-assess-map.md), [foundation-checklist](../references/foundation-checklist.md) (DOCS, REPO)

## Sources

- [research/raw/github--codeowners.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/github--codeowners.md)
- [research/raw/github-api--branch-protection.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/github-api--branch-protection.md)
- [research/raw/github-api--rulesets-rules.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/github-api--rulesets-rules.md)
- [research/raw/github-api--community-profile.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/github-api--community-profile.md)
- [research/raw/github-api--get-repository.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/github-api--get-repository.md)
- [research/raw/scorecard--checks-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--checks-reference.md)
- [research/raw/scorecard--cli-local-mode.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--cli-local-mode.md)
- [research/raw/wasp-nest--github-repo-health-checks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/wasp-nest--github-repo-health-checks.md)
- [research/raw/openssf--best-practices-criteria.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/openssf--best-practices-criteria.md)
