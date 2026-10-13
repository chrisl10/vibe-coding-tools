# Foundation checklist

Every check the audit makes. `Script` checks are done by `scripts/foundation_scan.py` and need no judgment beyond what the guide says. `Drone` checks need reading or running. IDs 001 to 049 in each area belong to the script; the Drone numbers its own findings from 050 up so ids never collide.

Severity shown is the default. Raise or lower with the rules in the area's guide, and always keep contract rule 3 (possible cannot exceed medium). "get-started step" names the Wasp Nest fix; the audit only names it, never runs it. Sources are raw files under `research/raw/`.

## LIB (guide 01)

| ID | Check | Who | Default severity | get-started step | Sources |
| --- | --- | --- | --- | --- | --- |
| FND-LIB-001 | `wasp-nest.lock` tracked | Script | medium | step 7, `mark-repo-started.py` | wasp-nest--get-started-assess-map |
| FND-LIB-002 | `library/` exists | Script | medium | stage 5 copy `library/` | wasp-nest--library-schema-v2 |
| FND-LIB-003 | All Library Schema v2 folders exist | Script | low | stage 5 | wasp-nest--library-schema-v2 |
| FND-LIB-004 | `library/README.md` states schema version | Script | low | stage 5 | wasp-nest--library-schema-v2 |
| FND-LIB-005 | `knowledge/private` has architecture, standards, contracts, and `documentation-framework.md` | Script | low | stage 5 | wasp-nest--library-schema-v2 |
| FND-LIB-006 | Existing code has knowledge docs | Script | medium | step 6, knowledge-stinger | wasp-nest--get-started-assess-map |
| FND-LIB-007 | Lock file valid (schema 1, playbook `get-started-stinger`) | Script | low | step 7 | wasp-nest--get-started-assess-map |
| FND-LIB-008 | Lock says knowledge pass completed when code exists | Script | medium | step 6 | wasp-nest--get-started-assess-map |
| FND-LIB-009 | No unfilled template tokens in baseline files | Script | low, medium in workflows | guide 01 rule 4 | wasp-nest--get-started-assess-map |
| FND-LIB-050+ | Knowledge docs are thin, stale or contradict the code (read three) | Drone | low to medium | step 6 | wasp-nest--library-schema-v2 |

## AGENT (guide 01)

get-started creates no repository agent file, so there is no get-started step to name for AGENT findings. Say so in the remediation.

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-AGENT-001 | AGENTS.md or CLAUDE.md present | Script | medium (low if another tool's rules file exists) | agents--agents-md-spec, claude-code--memory-claude-md |
| FND-AGENT-002 | Both present and CLAUDE.md imports AGENTS.md | Script | low | claude-code--memory-claude-md |
| FND-AGENT-003 | Instruction file at most 200 lines | Script | low | claude-code--memory-claude-md |
| FND-AGENT-004 | Names build or test commands | Script (possible, Drone reads) | low | agents--agents-md-spec |
| FND-AGENT-005 | Backticked paths exist | Script | low | claude-code--memory-claude-md |
| FND-AGENT-006 | Source files over 1,000 lines | Script | low | Wasp Nest heuristic |
| FND-AGENT-050+ | Instructions contradict the repo (says pnpm, lockfile is npm; says Jest, repo has Vitest) | Drone | low to medium | claude-code--memory-claude-md |

## CI (guide 02)

| ID | Check | Who | Default severity | get-started step | Sources |
| --- | --- | --- | --- | --- | --- |
| FND-CI-001 | CI config present | Script | medium | step 3.2 `ci.yml` | wasp-nest--get-started-assess-map |
| FND-CI-002 | Workflow token permissions read-only by default | Script | medium | step 3.2 | actions--secure-use, scorecard--checks-reference |
| FND-CI-003 | Actions pinned to 40-character SHAs | Script | medium third-party, low first-party only | step 3.2 | actions--secure-use |
| FND-CI-004 | No dangerous workflow patterns | Script (likely, Drone reads) | high | step 3.2 | actions--secure-use |
| FND-CI-005 | CI runs the tests | Script | medium | step 3.2 | openssf--best-practices-criteria |
| FND-CI-006 | Latest completed run on default branch is green | Script `--gh` | medium, high after 5 straight failures | n/a | github-api--workflow-runs |
| FND-CI-007 | Workflows have run on default branch | Script `--gh` | low | n/a | github-api--workflow-runs |
| FND-CI-009 | CI runs lint or typecheck | Script (possible) | low | step 3.2 | wasp-nest--get-started-assess-map |
| FND-CI-010 | Static analysis in CI or CodeQL default setup | Script (possible) | low | step 3.2, guide 06 | scorecard--checks-reference |
| FND-CI-050+ | Failures swallowed (`continue-on-error: true`, `|| true` after test, test job gated off) | Drone | medium | n/a | detection-patterns.md |

## TEST (guide 02)

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-TEST-001 | Tests present when 3+ source files | Script | medium | openssf--best-practices-criteria |
| FND-TEST-002 | `npm test` exists and is not the npm placeholder | Script | medium | npm--package-json-fields (heuristic) |
| FND-TEST-004 | Test files at least 3 percent of source files when 100+ source | Script (possible) | low | heuristic |
| FND-TEST-050 | Tests run in the scratch copy and fail | Drone (run_in_copy.py) | medium; high if half fail | openssf--best-practices-criteria |
| FND-TEST-051 | Tests run but do not test anything (no assertions, all skipped) | Drone | medium | openssf--best-practices-criteria |

## LINT (guide 02)

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-LINT-001 | Linter configured | Script | low | openssf--best-practices-criteria |
| FND-LINT-002 | tsconfig exists when TypeScript files exist | Script | medium | n/a |
| FND-LINT-003 | `strict` on in root tsconfig | Script | low | n/a |
| FND-LINT-004 | package.json has lint and typecheck scripts when configs exist | Script | low | get-started step 3.2 |
| FND-LINT-005 | Pre-commit hooks | Script | info | wasp-nest--get-started-assess-map |
| FND-LINT-007 | `.editorconfig` | Script | info | get-started step 3.1 |
| FND-LINT-050 | Lint command fails in scratch copy | Drone | low (medium when more than 50 errors) | n/a |
| FND-LINT-051 | Typecheck fails in scratch copy | Drone | medium | n/a |

## DEPS (guide 03)

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-DEPS-001 | Lockfile committed for each manifest | Script | medium | npm--ci, pnpm--frozen-lockfile, uv--project-layout-lockfile |
| FND-DEPS-002 | One package manager at the root | Script | medium | n/a |
| FND-DEPS-003 | Lockfile not git-ignored | Script | medium | git--gitignore |
| FND-DEPS-004 | `packageManager` matches lockfile | Script | medium | n/a |
| FND-DEPS-005 | Declared dependencies present in lockfile | Script | medium | npm--ci |
| FND-DEPS-006 | Dependabot or Renovate configured and covering ecosystems | Script | medium missing, low partial | dependabot--options-reference, renovate--config-file-locations |
| FND-DEPS-007 | Node or Python version pinned | Script | low | nvm--nvmrc, python-packaging--pyproject-toml |
| FND-DEPS-008 | Pinned runtime still supported | Script | medium | nodejs--release-status, python--version-status |
| FND-DEPS-050 | `npm ci` or `pnpm install --frozen-lockfile` fails in scratch copy | Drone | medium | npm--ci, pnpm--frozen-lockfile |

## ENV (guide 03)

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-ENV-001 | No `.env` files tracked | Script | high with populated keys, low if all placeholders | git--gitignore |
| FND-ENV-002 | `.gitignore` exists | Script | medium | get-started step 3.1 |
| FND-ENV-003 | `.gitignore` ignores `.env`, `.env.local` | Script | medium | git--gitignore |
| FND-ENV-004 | `.gitignore` covers generated folders for detected stacks | Script | low | get-started step 3.1 |
| FND-ENV-005 | No `node_modules`, `.venv`, `dist` and similar tracked | Script | medium or low | git--gitignore |
| FND-ENV-007 | `.env.example` exists when code reads env vars | Script | low | get-started step 3.1 |
| FND-ENV-008 | `.env.example` lists the variables code reads | Script (possible) | low | get-started guide 03 rule |
| FND-ENV-009 | Secret-shaped strings in tracked files | Script (possible, Drone reads) | high after reading, medium if unread | github-api--secret-scanning-overview |
| FND-ENV-010 | Key and credential files tracked | Script (possible, Drone reads) | high after reading | n/a |

## DOCS (guide 04)

| ID | Check | Who | Default severity | get-started step |
| --- | --- | --- | --- | --- |
| FND-DOCS-001 | README present | Script | medium | step 3.3 |
| FND-DOCS-002 | README has install and run steps | Script (possible, Drone reads) | low | step 3.3 |
| FND-DOCS-004 | LICENSE present | Script | medium (low if private) | human decision |
| FND-DOCS-005 | CONTRIBUTING.md | Script | low | step 3.4 |
| FND-DOCS-006 | SECURITY.md | Script | low | step 3.4 |
| FND-DOCS-007 | CHANGELOG.md | Script | info | step 3.4 |
| FND-DOCS-008 | Issue and PR templates | Script | info | step 3.2 |
| FND-DOCS-050 | README commands do not work (names a script or file that does not exist, wrong version) | Drone | low to medium | step 3.3 |

## REPO (guide 04)

| ID | Check | Who | Default severity | Sources |
| --- | --- | --- | --- | --- |
| FND-REPO-001 | CODEOWNERS present | Script | low | github--codeowners |
| FND-REPO-002 | CODEOWNERS lines valid, `.github/` owned | Script | low | github--codeowners |
| FND-REPO-003 | Default branch protected (classic or rules) | Script `--gh` | medium | github-api--branch-protection, github-api--rulesets-rules |
| FND-REPO-004 | Force pushes blocked | Script `--gh` | medium | scorecard--checks-reference |
| FND-REPO-005 | Pull request required | Script `--gh` | low | wasp-nest--github-repo-health-checks |
| FND-REPO-006 | Status checks required | Script `--gh` | low | wasp-nest--github-repo-health-checks |
| FND-REPO-007 | Secret scanning and push protection on (when visible) | Script `--gh` | medium off, low push protection off | github-api--get-repository |
| FND-REPO-008 | Repository not archived | Script `--gh` | info | github-api--get-repository |
| FND-REPO-009 | Community profile 100 percent | Script `--gh` | info | github-api--community-profile |
| FND-REPO-010 | Push in last 365 days | Script `--gh` | info | scorecard--checks-reference |
| FND-REPO-011 | Code Owner review required when CODEOWNERS exists | Script `--gh` | low | github--codeowners |
| FND-REPO-020 | No committed binaries | Script (possible) | low | scorecard--checks-reference |
| FND-REPO-023 | Commit convention (under 50 percent conventional in last 50) | Script | info | wasp-nest--get-started-assess-map |
