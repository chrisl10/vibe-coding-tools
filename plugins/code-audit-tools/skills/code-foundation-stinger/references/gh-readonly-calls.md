# Read-only GitHub calls

`foundation_scan.py --gh` calls only these paths, always as `gh api --method GET`, and refuses any other path. The Drone follows the same allowlist when it calls `gh` itself. Sources: research/raw/gh-cli--api-manual.md and the github-api raw files.

| Path | Used for | Failure meaning |
| --- | --- | --- |
| `repos/{owner}/{repo}` | default branch, archived, pushed_at, visibility, security_and_analysis | 404: no access or wrong remote; `security_and_analysis` absent: caller is not admin (cap, not a finding) |
| `repos/{owner}/{repo}/branches/{branch}/protection` | classic branch protection | 404 "Branch not protected": no classic rule (check rules too); 403: not admin (cap) |
| `repos/{owner}/{repo}/rules/branches/{branch}` | active rules from rulesets | empty list plus 404 on classic = unprotected |
| `repos/{owner}/{repo}/rulesets` | ruleset list (recorded for the notes) | |
| `repos/{owner}/{repo}/community/profile` | health_percentage and missing files | |
| `repos/{owner}/{repo}/actions/runs?branch=<b>&status=completed&exclude_pull_requests=true&per_page=10` | CI result on the default branch | |

Before any call: `gh auth status`. If gh is missing or unauthenticated, write a cap (see guide 00) and carry on with file checks. Never run `gh auth login`, never pass `--method` other than GET, never use `gh pr`, `gh issue` or `gh repo edit`, never call secret-scanning alert endpoints (their roles and payloads were not confirmed in this research; secret values could appear).

A cap is not a finding. "The audit could not see branch protection" goes in `coverage.caps` and `notes.md`, never in `findings.jsonl`.
