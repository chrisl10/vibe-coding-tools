# GitHub Repository Health Audit

**Repository:** `chrisl10/vibe-coding-tools`  
**Audit date:** 2026-09-01  
**Data collection mode:** Local clone + `gh` CLI + GitHub REST API (`repo`, `workflow`, `read:org`)  
**Coverage gaps:** Dependabot alert inventory was not enumerated; repository-level enablement was available. CODEOWNERS coverage is not applicable because no CODEOWNERS file exists.  
**Audited by:** orchestrator using `github-repo-health-stinger`

## Overall Score: 15/100

| Dimension | Raw | Weight | Weighted |
|---|---:|---:|---:|
| Branch protection / rulesets | 2/10 | 20% | 4.0 |
| Commit quality | 0/10 | 15% | 0.0 |
| CODEOWNERS | 0/10 | 15% | 0.0 |
| CI workflow density | 0/10 | 15% | 0.0 |
| Documentation presence | 4/10 | 10% | 4.0 |
| Repository settings | 4/10 | 10% | 4.0 |
| Issue / PR templates | 0/10 | 8% | 0.0 |
| `.gitignore` coverage | 4/10 | 7% | 2.8 |
| **Total** | | | **14.8 (15)** |

## Branching strategy

**Observed strategy:** Ad hoc GitHub Flow. `main` exists with three remote feature/restoration branches, mixed prefixes, no open pull requests, and no documented contribution workflow.  
**Branch inventory:** Four branches. None is older than 30 days; the oldest observed branch commit is dated 2026-08-15.  
**Assessment:** The branch count is small, but merge and naming policy are not enforced or documented.

## Branch protection / rulesets (2/10)

GitHub returned no repository rulesets, no active rules on `main`, and HTTP 404 for legacy branch protection. Pull-request review, status checks, non-fast-forward protection, stale-review dismissal, linear history, and signatures are therefore unenforced.

## Commit quality (0/10)

The repository has 33 commits in the available history. Two subjects (6.1%) match Conventional Commits; average subject length is 61.4 characters. Five subjects match the generic/noise prefix check. No commit-linting workflow is present.

## CODEOWNERS (0/10)

No `CODEOWNERS`, `.github/CODEOWNERS`, or `docs/CODEOWNERS` file exists. Security-sensitive paths such as `.github/`, `.claude/`, `.codex/`, `.agents/`, `learn/scripts/`, and `learn/packages/` therefore have no enforced owner review.

## CI workflow density (0/10)

No `.github/workflows/*.yml` or `.yaml` files exist. Pull requests have no repository-defined lint, test, build, archive-integrity, or security check. CI architecture is a handoff to `ci-release-worker-bee`.

## Documentation presence (4/10)

`README.md` and `LICENSE.md` are present. The README has a value proposition, quick start, usage examples, learning links, and license section. `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` are absent.

## Repository settings (4/10)

Secret scanning and push protection are enabled. Dependabot security updates are disabled. Merge commits, squash merges, and rebase merges are all allowed; auto-merge and automatic head-branch deletion are disabled. GitHub Issues are disabled.

## Issue and PR templates (0/10)

No bug-report, feature-request, or pull-request template exists under `.github/`. GitHub Issues are also disabled, so issue templates would not currently be usable.

## `.gitignore` coverage (4/10)

The file covers common Node and Python caches (`node_modules/`, coverage, `*.tsbuildinfo`, `__pycache__/`, `*.py[cod]`) and basic `.env` files. It does not cover the full `.env.*` family, common credential files (`*.pem`, `*.key`, `credentials.json`), Python virtual environments, general `dist/`, or common IDE/OS artifacts. No obviously ignored build/secret file was found tracked by the audit pattern.

## Prioritized remediation

| Priority | Finding | Impact | Effort | Recommended action |
|---:|---|---:|---:|---|
| 1 | `main` has no protection | 5 | 1 | Add a ruleset requiring pull requests, checks, and non-fast-forward protection in repository Rules settings. |
| 2 | No CI checks | 5 | 2 | Hand off to `ci-release-worker-bee` to add a PR workflow for generation idempotence, component validation, package checksums, archive integrity, and security scanning. |
| 3 | No CODEOWNERS | 4 | 1 | Add team ownership for harness sources, generated assets, release packages, and workflows. |
| 4 | Dependabot security updates disabled | 4 | 1 | Enable Dependabot security updates in Code security settings. |
| 5 | Auto-delete branches disabled | 3 | 1 | Enable automatic head-branch deletion in Pull Request settings. |
| 6 | Missing `SECURITY.md` | 3 | 1 | Add a responsible-disclosure policy. |
| 7 | No PR template | 3 | 1 | Add a template covering motivation, tests, generated artifacts, package checksums, and related issue. |
| 8 | `.gitignore` secret/build gaps | 3 | 1 | Extend ignore patterns for environment variants, credentials, virtualenvs, `dist/`, and IDE/OS artifacts. |
| 9 | Merge strategy is unconstrained | 3 | 1 | Disable merge commits and retain squash (optionally rebase) after branch rules are active. |
| 10 | Low Conventional Commit adherence | 3 | 2 | Add PR-title validation or commitlint as part of the CI handoff. |

These repository-wide hygiene gaps predate the Smoker patch. They are recorded separately and do not change the Security or Quality verdict for the exact release candidate.
