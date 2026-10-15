# 03. Quality without a single plan document

Load this guide for `full` and `mario`. `quality-stinger` normally audits an implementation against its PRD or IRD. An Audit My Code run usually has no single plan document, and `quality-stinger` defines no separate mode for that case. The arming line therefore states the constraints directly (report only, fix nothing, write only to `03-quality/`) and points it at the yardstick below.

References: [arming-lines.md](../references/arming-lines.md) (the quality line); [audit-contract.md](../references/audit-contract.md) sections 5 and 6.

## The yardstick, in priority order

1. **PRDs and IRDs in `library/requirements/` and `library/issues/`**, when the repository has them. Audit the shipped ones: does the code do what the accepted criteria say? This is the strongest signal and the reason the Foundation tier checks for a Library.
2. **The repository's own claims**: README features and setup steps, documented commands, CI configuration. A README that says `npm test` runs a suite which does not exist is a finding.
3. **Behavior evidence**: when `intake.json.execution.allowed` is true, run the test, lint, and typecheck commands in the throwaway copy in the consented mode (with a timeout, no global installs) and record pass, fail, or could-not-run. When it is false, record "not run: user declined code execution" as a cap and judge from CI history (read-only) instead. Failing tests on the default branch are a `high` quality finding.
4. **Engineering quality signals**: error handling on I/O boundaries, input validation, logging of failures, dead feature flags, TODO and FIXME density in critical paths, test coverage of the riskiest modules (from the bloat Drone's largest-files list and the security Drone's hot spots).

## Steps

1. Wait until W1 is verified. Pass the quality Drone the paths of `01-bloat/metrics.json` and `02-security/findings.jsonl` (when they exist) so it can weight its review toward the riskiest, largest code.
2. Arm `quality-wasp-drone` with the standalone line from [arming-lines.md](../references/arming-lines.md). It writes `03-quality/` per the contract instead of a report under `library/`.
3. Verify per [05-verify-and-deliver.md](05-verify-and-deliver.md).
