# QA Report: Smoker self-contained model matrix final candidate

**Plan document:** User-approved bugfix acceptance contract in the 2026-09-01 task context
**Audit date:** 2026-09-01
**Base branch:** `fork/main`
**Head:** `codex/smoker-self-contained-matrix` (final uncommitted working-tree candidate)
**Auditor:** quality-worker-bee

## Summary

The final 1.0.1 candidate passes all five acceptance requirements across the canonical command, generated Codex trees, installable Codex archives, package versions, and checksums. The earlier Critical package-distribution gap is resolved: all four archives match their source trees, every installed Codex Smoker carries the fail-closed contract and byte-identical matrix, and two generator reruns produced no change. No Critical or Warning finding blocks merge; one non-blocking test-hardening Suggestion remains.

## Scorecard

| Category      | Status | Notes |
|---------------|--------|-------|
| Completeness  | ✅ | All five requirements pass in source, generated trees, and current installable artifacts |
| Correctness   | ✅ | Matrix resolution, fail-closed behavior, routing safeguards, and dispatch-setting separation match the contract |
| Alignment     | ✅ | Canonical-source generation, versioned packages, manifests, README references, and checksums are synchronized |
| Gaps          | ✅ | Regression coverage includes checked-out skills plus the Codex plugin and project archives |
| Detrimental   | ✅ | No stale active package, broken path, archive mismatch, or generated-output drift remains |

## Critical Issues (must fix)

None.

## Warnings (should fix)

None.

## Suggestions (consider improving)

- [ ] **Inspect both Smoker copies inside the Codex project archive in the regression test**, `learn/scripts/test-smoker-model-matrix.py:16-25`

  The current test validates the standalone Codex plugin archive and the `.agents/skills/the-smoker` copy inside the project archive. The project archive also contains `.codex/plugins/vibe-coding-tools/skills/the-smoker`; it is correct in this candidate and the full archive-to-source comparison passed, but adding that third archive entry to `SMOKER_ARCHIVES` would make the focused regression test independently cover every packaged Smoker copy.

## Plan Item Traceability

| # | Plan Requirement | Status | Implementation Location | Notes |
|---|---|---|---|---|
| REQ-1 | Every generated or installed Codex Smoker resolves and reads a bundled local model-comparison matrix | ✅ | `.agents/skills/the-smoker/SKILL.md:17-19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:17-19`; `learn/scripts/generate-harnesses.py:69-72,186-213`; `learn/packages/vibe-coding-tools-codex-1.0.1.zip:skills/the-smoker/references/model-comparison-matrix.md`; `learn/packages/vibe-coding-tools-codex-project-1.0.1.zip:.agents/skills/the-smoker/references/model-comparison-matrix.md` | All source and packaged matrix copies have SHA-256 `48743442d7a082db1eb421b807e3a88747080a517c55592b51176ad12e4ec7db`. Full project-archive comparison also proves its plugin copy matches source. |
| REQ-2 | Missing or unreadable matrix stops execution before Bee dispatch | ✅ | `.claude/commands/the-smoker.md:16-18`; `.agents/skills/the-smoker/SKILL.md:17-19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:17-19`; `learn/scripts/test-smoker-model-matrix.py:28-34` | Canonical, generated, and packaged instructions all require stop-before-dispatch and report the exact path. |
| REQ-3 | No ledger-model reuse or silent expensive fallback | ✅ | `.claude/commands/the-smoker.md:18`; `.agents/skills/the-smoker/SKILL.md:19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:19`; `learn/scripts/test-smoker-model-matrix.py:31-34` | Both prohibitions are present and asserted for checked-out and archive surfaces. |
| REQ-4 | Model identifier and reasoning effort remain separate dispatch settings | ✅ | `.claude/commands/the-smoker.md:18`; `.agents/skills/the-smoker/SKILL.md:19`; `.agents/skills/the-smoker/references/model-comparison-matrix.md:22-30`; `learn/scripts/test-smoker-model-matrix.py:34` | Instruction and matrix agree, and the test rejects a missing separation statement. |
| REQ-5 | Generated outputs remain idempotent and validated | ✅ | `learn/scripts/generate-harnesses.py:148-229`; `learn/scripts/test-smoker-model-matrix.py:37-56`; `learn/packages/README.md:14-22`; `learn/packages/SHA256SUMS:1-4` | Two reruns preserved tracked diff digest `43d590059c5ee2bd983f82b4974a710a9189cbf5c939192e4e0142797fcc2df8` and generated/package digest `8599a851b376e8fd4bd4e2763f1140091d7189beed2554d6f8d537fb7981ebfe`. Focused test, command and skill validators, archive integrity, source comparison, JSON parsing, and all four checksums passed. |

## Files Changed

- `.agents/skills/the-smoker/SKILL.md` (M), switches to the skill-local matrix and adds the fail-closed dispatch contract
- `.agents/skills/the-smoker/references/model-comparison-matrix.md` (A), bundles the canonical matrix with the generated project skill
- `.claude/.claude-plugin/plugin.json` (M), advances the Claude plugin package version to 1.0.1
- `.claude/commands/the-smoker.md` (M), adds the canonical fail-closed dispatch and separate-setting instructions
- `.codex/plugins/vibe-coding-tools/.codex-plugin/plugin.json` (M), advances the Codex plugin package version to the 1.0.1 release identity
- `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md` (M), switches to the skill-local matrix and adds the fail-closed dispatch contract
- `.codex/plugins/vibe-coding-tools/skills/the-smoker/references/model-comparison-matrix.md` (A), bundles the canonical matrix with the generated plugin skill
- `.cursor/.cursor-plugin/plugin.json` (M), advances the Cursor plugin package version to 1.0.1
- `.cursor/commands/the-smoker.md` (M), mirrors the canonical fail-closed instructions for Cursor
- `README.md` (M), points the Cowork package example at 1.0.1
- `learn/packages/README.md` (M), catalogs all four 1.0.1 archives and the four-archive release checklist
- `learn/packages/SHA256SUMS` (M), records the four current 1.0.1 archive digests
- `learn/packages/vibe-coding-tools-claude-code-1.0.0.zip` (D), removes the superseded Claude package
- `learn/packages/vibe-coding-tools-claude-code-1.0.1.zip` (A), rebuilt Claude package matching `.claude`
- `learn/packages/vibe-coding-tools-codex-1.0.0.zip` (D), removes the superseded Codex plugin package
- `learn/packages/vibe-coding-tools-codex-1.0.1.zip` (A), rebuilt Codex plugin package with the corrected Smoker and bundled matrix
- `learn/packages/vibe-coding-tools-codex-project-1.0.0.zip` (D), removes the superseded Codex project package
- `learn/packages/vibe-coding-tools-codex-project-1.0.1.zip` (A), rebuilt Codex project package with both corrected Smoker surfaces
- `learn/packages/vibe-coding-tools-cursor-1.0.0.zip` (D), removes the superseded Cursor package
- `learn/packages/vibe-coding-tools-cursor-1.0.1.zip` (A), rebuilt Cursor package matching `.cursor`
- `library/requirements/reports/smoker-model-matrix/2026-09-01-smoker-model-matrix-quality-report.md` (A), preserves the first Quality pass and its now-remediated package blocker
- `library/requirements/reports/smoker-model-matrix/2026-09-01-smoker-model-matrix-security-report-final.md` (A), records the clean Security review of this final 1.0.1 candidate
- `library/requirements/reports/smoker-model-matrix/2026-09-01-smoker-model-matrix-security-report-rerun.md` (A), preserves the intermediate Security rerun and release-version finding
- `library/requirements/reports/smoker-model-matrix/2026-09-01-smoker-model-matrix-security-report.md` (A), preserves the initial Security pass for the pre-package candidate
- `learn/scripts/generate-harnesses.py` (M), copies the canonical matrix into each generated Codex skill that references it
- `learn/scripts/test-smoker-model-matrix.py` (A), validates checked-out and packaged Codex Smoker paths, matrix bytes, and dispatch safeguards
