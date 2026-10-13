# Measures and bands

Every measure in `metrics.json` uses the shared bands: `healthy`, `moderate`, `at-risk`, `critical`, `not-run`. `foundation_scan.py` fills all of them except `tests_passing`, which the Drone fills from `run_in_copy.py` (pass `--measures-extra` to `assemble_foundation.py`). Measure values may be numbers or short strings ("yes", "no", "green").

| Key | What it answers | Healthy | Moderate | At-risk | Critical | Basis |
| --- | --- | --- | --- | --- | --- | --- |
| `checklist_pass_rate` | How many applicable file and API checks pass (n/a, judgment and capped checks are left out) | 85% and up | 70 to 84.9 | 50 to 69.9 | under 50 | Wasp Nest banding, same cut points as the Scorecard-aligned and agent-readiness rates |
| `agent_readiness` | Can an AI agent work here safely (agent file, size, commands, real paths, file size) | 85% and up | 70 to 84.9 | 50 to 69.9 | under 50 | claude-code--memory-claude-md; agents--agents-md-spec |
| `tests_present` | Are there tests | any test file | n/a | none when 3+ source files | n/a | openssf--best-practices-criteria (test) |
| `tests_passing` | Do the tests pass when run in the scratch copy | 100% | 95 to 99.9 | 80 to 94.9 | under 80 | openssf--best-practices-criteria; `not-run` plus a cap if they could not run (no network, missing service, timeout) |
| `ci_present` | Is CI configured | present | n/a | absent | n/a | openssf--best-practices-criteria (test_continuous_integration) |
| `ci_green_default_branch` | Result of recent completed runs on the default branch | latest and last 5 succeed | latest ok, earlier failures | latest failed | 5 straight failures | github-api--workflow-runs; `not-run` when gh is unavailable |
| `library_initialized` | Is the Wasp Nest Library set up (value yes, partial, no) | yes: valid lock, full tree, knowledge docs when code exists | partial | no | n/a | wasp-nest--get-started-assess-map |
| `lockfile_consistent` | Lockfile committed, not ignored, names match manifest | yes | n/a | no | n/a | npm--ci; pnpm--frozen-lockfile |
| `dependency_automation` | Dependabot or Renovate configured | yes | no | n/a | n/a | scorecard--checks-reference (High risk, but Dependabot alerts may still be on, so no worse than moderate) |
| `committed_secret_files` | Tracked env or credential files | 0 | n/a | 1 or more | set by Drone only when a live secret is confirmed | git--gitignore |
| `branch_protection` | Default branch protection (protected, partial, none, unknown) | protected | partial | none | n/a | github-api--branch-protection; `not-run` when unreadable |
| `oversized_source_files` | Source files over 1,000 lines | 0 to 2 | 3 to 10 | over 10 | n/a | Wasp Nest heuristic |
| `scorecard_aligned_pass_rate` | Pass rate of the file-assessable Scorecard-style checks (CI-002, CI-003, CI-004, DEPS-006, DOCS-004, DOCS-006, REPO-020, REPO-003) | 85% and up | 70 to 84.9 | 50 to 69.9 | under 50 | scorecard--checks-reference; an approximation, never an official Scorecard score |

Optional measure the Drone may add: `official_scorecard_score` only if a `scorecard` binary was already on the machine and ran against the scratch copy; record which checks returned a score. Never install it.

## Verdict (contract section 8, with Foundation guard)

Default rule: `critical` for a critical finding at confirmed or likely confidence; `at-risk` for any high finding or two measures in `critical`; `moderate` for any medium finding or any measure at `moderate` or `at-risk`; else `healthy`. `assemble_foundation.py` computes it. No extra Foundation rule is needed: a repository with no tests has `tests_present` at `at-risk`, which already keeps the verdict at `moderate` or worse.

## Summary sentence

Answer the user's real question: "Is this repository set up so humans and AI agents can work in it safely?" Name the one or two biggest gaps in plain words. Example: "Builds are red on main and nothing documents how to run the tests; fix those two before letting agents loose."
