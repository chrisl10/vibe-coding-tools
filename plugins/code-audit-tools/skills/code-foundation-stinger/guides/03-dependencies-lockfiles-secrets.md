# 03. Dependencies, lockfiles and secrets hygiene

Check that installs are reproducible, that updates are proposed automatically, that the runtime is pinned and supported, and that no secrets or env files are committed. This guide never judges what a leaked secret means; that is `security-wasp-drone`'s job.

## Procedure

1. **Read the scan.** Findings FND-DEPS-001 to 008 and FND-ENV-001 to 010, `facts.dependency_automation`, `facts.package_manager`, `facts.lock_check` (how the lockfile names were compared).
2. **Lockfiles (DEPS-001 to 005).** Confirm one lockfile per manifest, one package manager at the root, not git-ignored, and `packageManager` matching. A library meant to be published to npm may deliberately not ship its lock, but should still commit it; keep the finding at `medium` for apps and say `low` only if the README states a reason.
3. **Prove consistency in the scratch copy when you can.** `npm ci --ignore-scripts` exits non-zero when package.json and the lock disagree and never rewrites the lock; `pnpm install --frozen-lockfile` fails when the lock is out of date (it is on by default in CI). Only when `intake.json.execution.allowed` is true: run it in the consented mode (guide 02, `run_in_copy.py --execution-allowed` on the host). When it is false, keep the scanner's name-presence result and record the cap. A mismatch error is a confirmed FND-DEPS-050 with the first lines of the error as evidence. The scanner's name-presence check (FND-DEPS-005) is `confirmed` for package-lock.json (parsed) and `likely` for other lockfiles (text search); the install is the full test.
4. **Update automation (DEPS-006).** The scanner finds a Dependabot file or any of the 14 Renovate config locations. Remember what files cannot show: Dependabot alerts and security updates are repository settings, and the Renovate app may or may not be installed. Say "no routine update PRs are configured" in plain words and keep `medium`. When a Dependabot file exists, read it: version 2, each ecosystem the repo uses (npm, pip, gomod, cargo, bundler, github-actions) has an entry, schedule present. Partial coverage is `low`.
5. **Runtime pin and support (DEPS-007, 008).** `.nvmrc`, `.node-version`, `.tool-versions`, `engines`, Volta, `.python-version`, `requires-python`. `engines` and `requires-python` are floors, not pins. EOL status comes from [runtime-eol-table](../references/runtime-eol-table.md); only flag what the table flags, and re-read the source page first if the run is after 2026-09-30.
6. **Env files and ignore rules (ENV-001 to 005).**
   - Tracked `.env` files: `high` when any key has a non-placeholder value, `low` when all values are placeholders. Evidence lists key names only. If a value looks like a live credential (confirmed by reading the line locally; never copy it), say so in `verified_by`, tag `handoff:security-wasp-drone`, and raise the `committed_secret_files` measure to `critical` through `measures-extra.json`.
   - `.gitignore` coverage uses `git check-ignore --no-index` with global excludes disabled, so a personal ignore file cannot hide the gap. Missing `.env` rules are `medium`; missing generated-folder rules are `low`.
   - Tracked `node_modules`, `.venv`, `dist` and similar: `medium` for dependency folders, `low` for build output. A tracked `dist/` can be deliberate (some libraries commit it); read the README before keeping it.
   - Remediation text is always "git rm --cached, then ignore, then rotate"; you never run it. `.gitignore` does not untrack files already committed (this is the usual surprise).
7. **Secret-shaped strings and key files (ENV-009, 010).** Every hit is `possible` until you read it. Open each location. Real credential: update to `likely` or `confirmed`, raise severity (`critical` only if confirmed live, usable and exposed), tag the handoff. Regex literal, test fixture, documentation sample or the detector's own pattern list: drop it and list it under "Not confirmed" in notes.md with the reason. Redact in every field.
8. **.env.example (ENV-007, 008).** If code reads env vars and no example exists, it is `low`. The name-diff finding is `possible`; read the example and the code before keeping it (platform-provided variables are not gaps).

## Severity calibration

| Situation | Severity |
| --- | --- |
| Live credential committed (confirmed) | critical (handoff) |
| Env file with populated values committed | high |
| No lockfile, or lock out of sync with manifest | medium |
| No update automation | medium |
| Runtime pinned to an unsupported version | medium |
| Runtime not pinned | low |
| `.env.example` missing | low |

## References loaded by this guide

- [detection-patterns](../references/detection-patterns.md), [runtime-eol-table](../references/runtime-eol-table.md), [foundation-checklist](../references/foundation-checklist.md) (DEPS, ENV), [finding-templates](../references/finding-templates.md)

## Sources

The notes listed below are source-repository research, not shipped.

- research/raw/npm--ci.md (source-repository research, not shipped)
- research/raw/pnpm--frozen-lockfile.md (source-repository research, not shipped)
- research/raw/uv--project-layout-lockfile.md (source-repository research, not shipped)
- research/raw/dependabot--options-reference.md (source-repository research, not shipped)
- research/raw/dependabot--features-overview.md (source-repository research, not shipped)
- research/raw/renovate--config-file-locations.md (source-repository research, not shipped)
- research/raw/nvm--nvmrc.md (source-repository research, not shipped)
- research/raw/nodejs--release-status.md (source-repository research, not shipped)
- research/raw/python--version-status.md (source-repository research, not shipped)
- research/raw/python-packaging--pyproject-toml.md (source-repository research, not shipped)
- research/raw/git--gitignore.md (source-repository research, not shipped)
- research/raw/github-api--secret-scanning-overview.md (source-repository research, not shipped)
