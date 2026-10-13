# 05. Verify and deliver

Load this guide every time a Drone returns, and again before rendering the brief.

References: [audit-contract.md](../references/audit-contract.md) sections 5 to 9; `scripts/check_workspace.py` (deterministic checks).

## After each Drone

Run `python3 <this-skill>/scripts/check_workspace.py <workspace> --dimension <name>`. It checks, and prints every failure:

- `metrics.json` exists, parses, and has `verdict`, `summary`, `measures`, and `coverage`.
- Every `findings.jsonl` line parses and has every required field with a legal enum value.
- `possible` confidence never carries a severity above `medium`.
- No finding has empty `evidence` or `verified_by`.
- No line contains an unredacted secret-looking string.

Then read three findings at random yourself and check the evidence against the code at the cited lines. A citation that does not match the code is a failed check.

## Before the brief

1. Build `evidence-index.md` with `python3 <this-skill>/scripts/build_evidence_index.py <workspace>` (contract section 9). It collects every Drone's `## Evidence` section and lists any raw file nobody described.
2. Run `check_workspace.py <workspace>` with no dimension, which also checks that every dimension the tier needs has output, that `intake.json` is complete, and that the evidence index exists.
3. Remove `<workspace>/.scratch/` (the throwaway copy). Leave the raw tool reports.
4. Arm `code-audit-brief-wasp-drone`. It renders `brief/brief.html` and returns the overall verdict.

## Deliver

Tell the user, in this order and briefly: the overall verdict and one-sentence answer, the top five findings (id, severity, one line each), the brief path, every coverage cap, and for `mario` the roadmap path plus the list of files written to `library/`. Offer, in one line, to publish the brief as a private page when the session can do that; never publish without a yes.
