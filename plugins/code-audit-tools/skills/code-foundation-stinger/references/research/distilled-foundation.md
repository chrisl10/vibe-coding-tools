# Distilled research: code-foundation-stinger

Research window 2026-03-30 to 2026-09-30. All sources fetched 2026-09-30. Each claim ends with its raw file. The first three raw files marked "internal" describe The Wasp Nest's own get-started and repo-health skills, which define the baseline this audit measures against.

## 1. What a correctly set up repository has (the Wasp Nest baseline)

| Item | Detail | Source |
| --- | --- | --- |
| Copy order | foundational files, then .github, README, CONTRIBUTING/SECURITY/CHANGELOG, then library/ | [raw/wasp-nest--get-started-assess-map.md] |
| Library Schema v2 | knowledge (public, private), requirements (backlog, in-work, completed, reports), issues (backlog, in-work, completed), notes; lifecycle is the folder | [raw/wasp-nest--library-schema-v2.md] |
| Lock | `wasp-nest.lock` is written last, only after verification and, for existing code, the knowledge pass | [raw/wasp-nest--get-started-assess-map.md] |
| Settings-only items | branch protection or ruleset, secret protection and push protection, CodeQL default setup, license choice | [raw/wasp-nest--get-started-assess-map.md] |
| Gap in the baseline | get-started installs home-level agent instructions only; it never creates a repository AGENTS.md or CLAUDE.md | [raw/wasp-nest--get-started-assess-map.md] |
| Read-only repo-health calls | protection, rules for branch, rulesets; declare API scope; local-only mode cannot see branch protection | [raw/wasp-nest--github-repo-health-checks.md] |

An audit built on get-started must never repair: get-started itself never overwrites a maintainer's file and reports "differs, not touched" [raw/wasp-nest--get-started-assess-map.md].

## 2. OpenSSF Scorecard: what a local clone can and cannot assess

| Check | Risk | From a clone? | Notes | Source |
| --- | --- | --- | --- | --- |
| Binary-Artifacts | High | Yes | generated executables in source | [raw/scorecard--checks-reference.md] |
| License | Low | Yes | LICENSE, LICENCE, COPYING, COPYRIGHT or LICENSES/ | [raw/scorecard--checks-reference.md] |
| Security-Policy | Medium | Yes | SECURITY.md with contact or text | [raw/scorecard--checks-reference.md] |
| Token-Permissions | High | Approximate from workflow files | top-level read-only plus per-job write | [raw/scorecard--checks-reference.md] |
| Pinned-Dependencies | Medium | Approximate from workflow, Docker, scripts | | [raw/scorecard--checks-reference.md] |
| Dangerous-Workflow | Critical | Approximate from workflow files | pull_request_target or workflow_run with untrusted checkout; script injection | [raw/scorecard--checks-reference.md] |
| Dependency-Update-Tool | High | Config file only | detects Dependabot or Renovate; does not prove it runs | [raw/scorecard--checks-reference.md] |
| Branch-Protection | High | No, needs API | tiered 3 to 10 | [raw/scorecard--checks-reference.md] |
| Code-Review, Maintained, Vulnerabilities, Signed-Releases, Contributors, CII-Best-Practices, SAST, Fuzzing, Packaging, SBOM, CI-Tests, Webhooks | mixed | No (history, API or release data) | out of scope for local file checks; SAST and CI-Tests can be hinted from workflow files | [raw/scorecard--checks-reference.md] |

The Scorecard CLI has a `--local` mode that skips checks needing the host API but the README does not list which, so any official local run must be read check by check [raw/scorecard--cli-local-mode.md]. A GitHub token is needed for `--repo` mode to avoid rate limits [raw/scorecard--cli-local-mode.md]. The Wasp Nest "Scorecard aligned" measure is an approximation built from file checks and is never reported as an official score.

## 3. Read-only GitHub API facts the audit relies on

- Branch protection endpoint needs admin; 404 means no classic rule (or no branch), so pair it with the rules-for-branch endpoint before saying "unprotected"; 403 is a cap [raw/github-api--branch-protection.md][raw/github-api--rulesets-rules.md].
- Rules for a branch lists active rules from every source; evaluate or disabled rules are excluded [raw/github-api--rulesets-rules.md].
- Workflow runs can be filtered by branch, status and excluding pull requests; conclusion is on each run [raw/github-api--workflow-runs.md].
- Repository response carries default_branch, archived, pushed_at; security_and_analysis only shows to admins, owners or security managers [raw/github-api--get-repository.md].
- Community profile gives health_percentage and per-file presence [raw/github-api--community-profile.md].
- Public repos get secret scanning free; private need Secret Protection; the alerts API was not confirmed in the fetched page so it is not called [raw/github-api--secret-scanning-overview.md].
- `gh api` defaults to GET; pass `--method GET` explicitly; 4xx and 5xx exit non-zero (read the message, do not assume) [raw/gh-cli--api-manual.md].

## 4. CI, tests, lint

- Pin actions to a full commit SHA; set GITHUB_TOKEN read-only by default and raise per job; keep untrusted expressions out of `run:`; avoid untrusted checkout under pull_request_target or workflow_run [raw/actions--secure-use.md].
- Token-Permissions rewards read-only top-level with job-level writes; one point lost when top-level is undefined [raw/scorecard--checks-reference.md].
- OpenSSF passing criteria: a working build; an automated test suite invoked in a standard way; tests run in CI; a policy that new functionality gets tests; compiler or linter warnings enabled and fixed [raw/openssf--best-practices-criteria.md].
- Thin spot: the exact npm init placeholder test script ("Error: no test specified") is not in the fetched npm page, so the check is labeled a Wasp Nest heuristic [raw/npm--package-json-fields.md].

## 5. Dependencies, lockfiles, runtime pins

- `npm ci` errors when package.json and the lock disagree and never writes the lock; so it is a consistency test [raw/npm--ci.md]. pnpm `--frozen-lockfile` fails when the lock is missing or out of date and defaults on in CI [raw/pnpm--frozen-lockfile.md]. uv says uv.lock should be committed [raw/uv--project-layout-lockfile.md].
- Dependabot file lives at .github/dependabot.yml or .yaml and needs version 2, updates, package-ecosystem, directory and schedule.interval [raw/dependabot--options-reference.md]. Alerts and security updates are repository settings, so no file does not mean no alerts [raw/dependabot--features-overview.md]. Renovate config can be in 14 places; Renovate stops at the first match and package.json config is deprecated [raw/renovate--config-file-locations.md].
- Node: v20 and older are EOL; v22 and v24 are LTS lines; v26 is Current [raw/nodejs--release-status.md]. Conflict: the fetch summary printed EOL dates of September 2026 next to v22 and v24, which looks like a summarizer error; only v20 and older are flagged, and the Drone must re-read the page before flagging v22 or v24 [raw/nodejs--release-status.md].
- Python: 3.9 and older EOL; 3.10 security-only until October 2026; 3.11 to 3.14 supported [raw/python--version-status.md]. `requires-python` is a floor, not a pin; `.python-version` is a pin [raw/python-packaging--pyproject-toml.md]. The uv excerpt did not document `.python-version`, so it is not cited for uv.
- `.nvmrc` holds exactly one version; accepts versions and `lts/*` [raw/nvm--nvmrc.md]. package.json `engines` is advisory unless engine-strict [raw/npm--package-json-fields.md].

## 6. Secrets hygiene

- `.gitignore` never untracks already-tracked files; `git rm --cached` does; `git check-ignore --no-index` tests paths that do not exist [raw/git--gitignore.md].
- Get-started's `.gitignore` template ends the `.env` block as `.env`, `.env.*`, `!.env.example`, in that order [raw/wasp-nest--get-started-assess-map.md].
- Secret pattern formats in the scanner (AWS AKIA, GitHub ghp_, Stripe live keys, private-key blocks and so on) are widely documented vendor token shapes but were not archived from a primary page; they are Wasp Nest heuristics and every hit must be read before it is trusted.

## 7. Agent readiness

- AGENTS.md: plain Markdown, build and test commands, style, tests, security, nested files with closest-wins; supported by 25+ tools [raw/agents--agents-md-spec.md].
- Claude Code: reads both file families but if CLAUDE.md exists it reads CLAUDE.md only unless the setting is changed; `@AGENTS.md` import keeps one shared file; target under 200 lines; stale paths and contradictions are what its prompt audit hunts [raw/claude-code--memory-claude-md.md].
- Evidence of value: one small study (10 repos, 124 PRs) associated AGENTS.md with about 28.6 percent lower runtime and 16.6 percent fewer output tokens at similar completion [raw/research--agents-md-efficiency-arxiv-2601-20404.md]. Small sample; used only to justify checking for presence.
- The 1,000-line oversized-file threshold is a Wasp Nest heuristic with no published source.

## 8. Governance

- CODEOWNERS: three locations in order; 3 MB limit; `!`, `\#` and `[ ]` do not work; only gates merges when review by owners is required; own `/.github/CODEOWNERS` [raw/github--codeowners.md].
- Branch protection floor per the Wasp Nest repo-health skill: PR with review, required status checks, block force push; nice to have stale-review dismissal, linear history, signatures [raw/wasp-nest--github-repo-health-checks.md]. Scorecard tiers go from 3/10 for blocking force push to 10/10 with stale-review dismissal and admin review [raw/scorecard--checks-reference.md].

## Conflicts and thin spots

1. Node EOL dates (section 5), unresolved.
2. No primary source archived for token regexes, npm placeholder script text, or the 1,000-line threshold; all three are labeled heuristics.
3. Scorecard `--local` skipped-check list is not documented in the fetched README.
4. Scorecard 2026 release notes: a search found no confirmed new checks in the window; the 20-check table is the current reference.
5. Secret scanning alerts API was not confirmed from a fetched page; the audit does not call it.
