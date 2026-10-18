# 00. Scoping and read-only rules

Start here on every run. This guide fixes what the Foundation audit may touch, where output goes, and how to record what you could not see. The Foundation audit answers one question: is this repository set up so humans and AI agents can work in it safely?

## Hard rules

1. **Never modify the audited repository.** No file writes, no `git add`, `commit`, `checkout`, `stash`, `reset`, `clean`, no `git worktree add` against the audited repo, no `npm install` there, no running its scripts there. Reading files and read-only git (`ls-files`, `log`, `check-ignore`, `remote get-url`, `archive`) is fine.
2. **Never run a get-started write step.** `get-started-stinger` is the source of the baseline (see [get-started-assess-map](../references/get-started-assess-map.md)). Where it would create something, record a finding that names the step. Do not run `mark-repo-started.py`, `install-global-instructions.py`, or copy a template.
3. **Nothing that executes project code runs without consent.** Read `intake.json.execution` first. When `allowed` is false, run no project command at all and record the cap. When it is true, everything that executes project code runs in the throwaway copy `<workspace>/.scratch/repo-copy/`, in the consented mode: a no-network container, or on the host through `scripts/run_in_copy.py --execution-allowed` (allowlisted command shapes, timeout, no global installs, secrets stripped from the environment, not a sandbox). Never install a global tool. Never run `npx` or download-and-run commands. If the orchestrator did not make the copy, make it from `HEAD` with `python3 <audit-my-code-stinger>/scripts/make_scratch_copy.py <repo> <workspace>/.scratch/repo-copy` (read-only against the repo, portable to Windows) and note "audited HEAD, not uncommitted work" as a cap.
4. **Write only inside the workspace** `<workspace>/00-foundation/` (and `raw/` under it). Never write to `library/` (that is the `mario` tier's remediation step, not this Drone's).
5. **GitHub access is read-only.** Only the allowlist in [gh-readonly-calls](../references/gh-readonly-calls.md), only `--method GET`, only after `gh auth status` succeeds. If it fails, write a cap and continue with file checks. Never authenticate, never ask for a token.
6. **Secrets.** Never print a secret value. In evidence keep the first 4 characters and write `****`. For env files list key names only. A confirmed live secret is handed to `security-wasp-drone`; your finding records presence and location.
7. **No finding without evidence.** A suspicion you could not show goes in `notes.md` under "Not confirmed".

## Steps

1. Read `<workspace>/intake.json`: repo path, branch, sha, `stacks[].paths`, `scope.include` and `scope.exclude`, `workspace`. If it is missing, ask the orchestrator; do not guess the workspace.
2. Confirm the repo root (the directory with `.git`). If the repo is a monorepo, run the scan at the root and treat `stacks[].paths` as the areas to read for tests, lint and typecheck.
3. Record the tooling you can use: `python3 --version` (3.11 or newer needed for the scripts), `git --version`, `gh auth status`, and whether `scorecard` is already on PATH. Missing tools become caps, not failures.
4. Make or find the scratch copy (rule 3). Confirm the repo is clean enough to compare: `git status --porcelain` read-only; if dirty, add the cap "uncommitted changes exist and were not audited".
5. Continue with the guides in order: [01](01-wasp-nest-readiness.md), [02](02-ci-tests-lint-typecheck.md), [03](03-dependencies-lockfiles-secrets.md), [04](04-repository-governance.md), then [05](05-writing-metrics-and-findings.md). The scan in step 1 of guide 01 produces most findings for all of them.

## Caps (what you could not see)

A cap is a silent limit that you lifted or hit. Record each in `metrics.json` `coverage.caps` (`assemble_foundation.py --cap "text"`) and under "Coverage caps" in `notes.md`. An empty list claims no limit applied, so be honest. Typical caps:

| Situation | Cap text |
| --- | --- |
| gh missing or not authenticated | gh unavailable: branch protection, repository settings, community profile and CI status were not assessed |
| HTTP 403 on protection | token lacks admin; protection detail not assessed |
| No network in sandbox | dependency install skipped; tests not run; lockfile consistency judged by name only |
| Install run with `--ignore-scripts` | lifecycle scripts skipped; tests that need native builds may fail for that reason |
| Test timeout | tests did not finish in N seconds; pass rate not available |
| Monorepo | only root scripts were run; workspace packages not run individually |
| Uncommitted work | audited HEAD only |
| Not a GitHub remote | GitHub checks not applicable |

## Output files

`findings.jsonl`, `metrics.json`, `notes.md` (contract sections 5 and 6) in `00-foundation/`, plus `raw/` for scan JSON and command logs. Guide 05 explains how to write them.

## Handoffs

| Topic | Hand to |
| --- | --- |
| What a leaked secret means, rotation, exploitability | `security-wasp-drone` |
| CI architecture depth beyond presence and green | `ci-release-wasp-drone` |
| Duplicate, dead or oversized code | `code-bloat-wasp-drone` |
| Whether the implementation matches a plan | `quality-wasp-drone` |
| History rewrite after a committed secret | `git-wasp-drone` |

## Sources

The notes listed below are source-repository research, not shipped.

- research/raw/wasp-nest--get-started-assess-map.md (source-repository research, not shipped)
- research/raw/wasp-nest--github-repo-health-checks.md (source-repository research, not shipped)
- research/raw/gh-cli--api-manual.md (source-repository research, not shipped)
- research/raw/github-api--get-repository.md (source-repository research, not shipped)
- research/raw/git--gitignore.md (source-repository research, not shipped)
