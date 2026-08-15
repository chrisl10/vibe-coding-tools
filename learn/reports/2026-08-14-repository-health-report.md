# GitHub Repository Health Audit Report

**Repository:** `legioncodeinc/vibe-coding-tools`
**Audit date:** 2026-08-14
**Data collection mode:** Local clone plus authenticated `gh` CLI with `repo`, `workflow`, and `read:org` scopes
**Coverage gaps:** None for public repository metadata. GitHub returned no active ruleset and confirmed the default branch is not protected.
**Audited by:** github-repo-health-worker-bee

## Overall Score: 14/100

| # | Dimension | Raw Score | Weight | Weighted points |
|---|---|---|---|---|
| 1 | Branch protection and rulesets | 2/10 | 20% | 4.0 |
| 2 | Commit quality | 0/10 | 15% | 0.0 |
| 3 | CODEOWNERS coverage | 0/10 | 15% | 0.0 |
| 4 | CI workflow density | 0/10 | 15% | 0.0 |
| 5 | Docs presence | 4/10 | 10% | 4.0 |
| 6 | Repository settings | 3/10 | 10% | 3.0 |
| 7 | Issue and PR templates | 0/10 | 8% | 0.0 |
| 8 | `.gitignore` coverage | 4/10 | 7% | 2.8 |
| | **Total** | | | **13.8, rounded to 14** |

## Branching Strategy

**Observed strategy:** Partly GitHub Flow, with feature branches and pull requests targeting `main`, but no written contributor workflow or enforcement.

**Documented:** No `CONTRIBUTING.md` or branching guide exists in the remote baseline.

**Branch inventory:** The repository API returns only `main` as a repository branch. Two pull requests remain open: `feat/rust-worker-bee-stinger` from 2026-08-07 and `agent/global-codex-bee-army` from 2026-07-12. PR #4 is more than 30 days old and should be reviewed for closure or revival.

**Assessment:** The feature-branch pattern is sensible, but the absence of protection, CI, templates, and documented conventions makes the actual strategy ad hoc.

## Branch Protection and Rulesets (Score: 2/10)

**Enforcement mechanism:** None. `GET /rulesets` returned no ruleset, and `GET /branches/main/protection` returned `404 Branch not protected`.

| Rule | Status |
|---|---|
| Pull request required | ❌ |
| Required status checks | ❌ |
| Force push blocked | ❌ |
| Stale reviews dismissed | ❌ |
| Linear history required | ❌ |
| Signed commits required | ❌ |

Recommendation: Create an active ruleset for `main` in [Settings, Rules, Rulesets](https://github.com/legioncodeinc/vibe-coding-tools/settings/rules). Require pull requests, at least one review, dismissal of stale approvals, and required checks after CI exists. Block force pushes and deletion.

## Commit Quality (Score: 0/10)

| Metric | Value |
|---|---|
| Sample | 22 commits |
| Conventional Commit subjects | 0 of 22, 0% |
| Average subject length | 69.6 characters |
| Exact one-word generic subjects | 0 |
| Commit linting | Not configured |

Recommendation: Document Conventional Commits in a new contribution guide and validate pull request titles. This can be introduced without rewriting existing public history.

## CODEOWNERS (Score: 0/10)

No `CODEOWNERS`, `.github/CODEOWNERS`, or `docs/CODEOWNERS` file exists.

Recommendation: Add `.github/CODEOWNERS` with a team or durable organization owner for the default catch-all and explicit ownership for `.github/`, `.claude/`, `.codex/`, `.cursor/`, `learn/scripts/`, and `learn/packages/`.

## CI Workflow Density (Score: 0/10)

No `.github/workflows/` directory or GitHub Actions workflow exists. There is no automated link check, component validation, plugin validation, package verification, or secret scan on pull requests.

Handoff: `ci-release-worker-bee` should design a pull request workflow that runs the existing deterministic checks and makes them eligible for required status checks.

## Docs Presence (Score: 4/10)

| File | Present | Notes |
|---|---|---|
| `README.md` | ✅ | New WIFM, quickstart, harness setup, learning links, and license statement |
| `LICENSE.md` | ✅ | MIT |
| `CONTRIBUTING.md` | ❌ | Missing |
| `SECURITY.md` | ❌ | Missing responsible disclosure instructions |
| `CODE_OF_CONDUCT.md` | ❌ | Missing |
| `CHANGELOG.md` | ❌ | Missing |

Recommendation: Add community health files in a follow-up repository-health change. The user's root-layout request intentionally limits human-facing root Markdown, so `.github/` is the better location for contribution, security, and conduct files.

## Repository Settings (Score: 3/10)

Authenticated API results:

| Setting | Status |
|---|---|
| Delete head branches after merge | ❌ Disabled |
| Merge commits | ⚠️ Enabled |
| Squash merge | ✅ Enabled |
| Rebase merge | ✅ Enabled |
| Auto-merge | ❌ Disabled |
| Suggest updating branches | ❌ Disabled |
| Secret scanning | ❌ Disabled |
| Push protection | ❌ Disabled |
| Dependabot security updates | ❌ Disabled |

Recommendation: In [General settings](https://github.com/legioncodeinc/vibe-coding-tools/settings), enable automatic branch deletion and branch updates, prefer squash or rebase, and consider auto-merge after CI is required. In [Code security settings](https://github.com/legioncodeinc/vibe-coding-tools/settings/security_analysis), enable secret scanning, push protection, validity checks, and Dependabot security updates. The security settings are the highest-priority external fix because this task began with a push-protection-style finding.

## Issue and Pull Request Templates (Score: 0/10)

No `.github/ISSUE_TEMPLATE/`, issue forms, or pull request template exists.

Recommendation: Add a bug form, feature request form, template configuration, and substantive pull request template under `.github/`. Include testing, documentation, security, breaking-change, and acceptance-ledger checks.

## `.gitignore` Coverage (Score: 4/10)

The root `.gitignore` covers Node logs, dependencies, caches, common build output, Python validation caches, and exact `.env` and `.env.test` files. It does not cover the broader `.env.*` family, private keys, credentials files, or common operating-system and IDE files.

Recommendation: Add `.env.*` with explicit exceptions for `.env.example`, credential and key patterns, `.venv/`, `.DS_Store`, and `Thumbs.db`. Review before adding broad patterns so intentional project configuration remains tracked.

## Prioritized Remediation Plan

| Priority | Finding | Impact | Effort | Action |
|---|---|---|---|---|
| 1 | Secret scanning and push protection disabled | 5 | 1 | Enable in repository code-security settings; hand secret details to `security-worker-bee` |
| 2 | No branch protection or ruleset | 5 | 1 | Add an active `main` ruleset after CI check names exist |
| 3 | No CI | 5 | 2 | Hand workflow design to `ci-release-worker-bee`; run link, plugin, component, archive, and secret gates |
| 4 | No CODEOWNERS | 4 | 1 | Add team-based ownership for distribution and workflow paths |
| 5 | Auto-delete and update-branch settings disabled | 3 | 1 | Enable both in General settings |
| 6 | Missing security and contribution docs | 3 | 1 | Add `.github/SECURITY.md` and `.github/CONTRIBUTING.md` |
| 7 | Missing issue and PR templates | 3 | 2 | Add issue forms and a substantive PR template |
| 8 | No conventional-commit enforcement | 3 | 2 | Document the convention and validate PR titles |
| 9 | `.gitignore` misses common secret and operating-system patterns | 3 | 1 | Extend the ignore file in a separate reviewed change |

## Handoffs

- `ci-release-worker-bee`: Create the CI workflow and status-check architecture.
- `security-worker-bee`: Confirm repository secret-scanning configuration after a human enables it.
- `readme-writing-worker-bee`: No follow-up needed for the README in this migration.
- Human repository administrator: Change GitHub settings and decide the fate of stale PR #4.

This audit is read-only with respect to GitHub. No repository setting, branch, workflow, or pull request was changed by the health audit.
