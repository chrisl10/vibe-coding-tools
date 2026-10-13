# OpenSSF Scorecard mapping

Which Scorecard checks the Foundation audit approximates, and how. Source: [research/raw/scorecard--checks-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--checks-reference.md), [research/raw/scorecard--cli-local-mode.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--cli-local-mode.md).

| Scorecard check (risk) | Foundation check | Mode | Limit |
| --- | --- | --- | --- |
| Binary-Artifacts (High) | FND-REPO-020 | clone | extension match only; Scorecard allows generated source and docs |
| License (Low) | FND-DOCS-004 | clone | does not test for an FSF or OSI license id |
| Security-Policy (Medium) | FND-DOCS-006 | clone | existence only; Scorecard also scores contact and text |
| Token-Permissions (High) | FND-CI-002 | clone, workflow files | no check of which write scopes a job really needs |
| Pinned-Dependencies (Medium) | FND-CI-003 (workflows), FND-DEPS-001 (lockfiles) | clone | Docker and shell downloads are not parsed |
| Dangerous-Workflow (Critical) | FND-CI-004 | clone, workflow files | heuristic; Drone must read |
| Dependency-Update-Tool (High) | FND-DEPS-006 | clone | detects config only; app installation invisible |
| Branch-Protection (High) | FND-REPO-003 to 006 | API | needs admin for classic detail; rules endpoint works with read |
| SAST (Medium) | FND-CI-010 | clone hint | default-setup CodeQL leaves no file |
| CI-Tests (Low) | FND-CI-005, FND-CI-006 | clone plus API | Scorecard samples recent commits; this audit reads workflows and recent runs |
| Maintained (High) | FND-REPO-010 | API | Scorecard wants a commit a week over 90 days; this check is only a year-long staleness flag |
| Code-Review, Contributors, Vulnerabilities, Signed-Releases, Packaging, SBOM, Fuzzing, CII-Best-Practices, Webhooks | not assessed | n/a | need commit history, release data, OSV or host settings; out of scope for Foundation. Vulnerabilities belongs to the security dimension |

The `scorecard_aligned_pass_rate` measure averages the pass or fail of CI-002, CI-003, CI-004, DEPS-006, DOCS-004, DOCS-006, REPO-020 and REPO-003. Label it "Scorecard aligned" and never "Scorecard score".

If a `scorecard` binary is already installed, the Drone may run it against the scratch copy with `scorecard --local <copy> --format json` under `run_in_copy.py`-style limits (timeout, no network assumptions) and archive the output in `raw/`. Only report checks that returned a score. Do not install it, and do not pass a token.
