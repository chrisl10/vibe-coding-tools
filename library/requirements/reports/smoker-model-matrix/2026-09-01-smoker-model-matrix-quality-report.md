# QA Report: Smoker self-contained model matrix

**Plan document:** User-approved bugfix acceptance contract in the 2026-09-01 task context
**Audit date:** 2026-09-01
**Base branch:** `fork/main`
**Head:** `codex/smoker-self-contained-matrix` (uncommitted working-tree candidate)
**Auditor:** quality-worker-bee

## Summary

The working-tree generator and both generated Codex skill trees satisfy the fail-closed model-matrix contract, and repeated generation is byte-for-byte idempotent. The candidate is blocked by one Critical distribution gap: both tracked installable Codex archives still contain the old Smoker instructions, so installing from the repository's published package surface omits the new dispatch safeguards. Rebuild and validate the Codex archives and checksums, then rerun Security followed by Quality before merge.

## Scorecard

| Category      | Status | Notes |
|---------------|--------|-------|
| Completeness  | ❌ | Generated trees pass, but the two declared installable Codex archives do not contain the completed Smoker contract |
| Correctness   | ✅ | The canonical command, generated skills, bundled matrices, and generator behavior match the contract |
| Alignment     | ⚠️ | The release-package workflow at `learn/packages/README.md:14-21` was not completed |
| Gaps          | ⚠️ | The regression test checks source-tree skills only and cannot detect stale installable archives |
| Detrimental   | ❌ | A package-based install can reproduce the missing-safeguard behavior this change is intended to prevent |

## Critical Issues (must fix)

- [ ] **Installable Codex archives still ship the old Smoker contract**, `learn/packages/vibe-coding-tools-codex-1.0.0.zip:skills/the-smoker/SKILL.md:17`, `learn/packages/vibe-coding-tools-codex-project-1.0.0.zip:.agents/skills/the-smoker/SKILL.md:17`, `learn/packages/vibe-coding-tools-codex-project-1.0.0.zip:.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:17`

  `learn/packages/README.md:8-12` identifies these archives as the installable Codex distribution and project adapter. Inspection of both archives shows that each packaged Smoker still points at `../../model-comparison-matrix.md` and lacks the required stop-before-dispatch, no-ledger-reuse, no-silent-high-cost-default, and separate-reasoning-setting instructions. A user installing either tracked package therefore does not receive REQ-2 through REQ-4, even though the generated working-tree copies are correct.

  Suggested: rebuild the Codex plugin and project archives from the corrected generated trees, update `learn/packages/SHA256SUMS`, extract each archive into an empty temporary directory, and assert the packaged Smoker text and bundled matrix bytes before publishing. Prefer a new package version if the existing archive has already been distributed.

  ```markdown
  4. Route each task ... using the rubric in `../../model-comparison-matrix.md` ...
  ```

## Warnings (should fix)

- [ ] **Regression test does not inspect the installable Codex package surface**, `learn/scripts/test-smoker-model-matrix.py:11-29`

  `SMOKER_SKILLS` includes only the two checked-out generated directories. The assertions prove those trees are correct but never extract or inspect the installable archives declared in `learn/packages/README.md:8-12`, which allowed the stale packaged instructions to pass the current test. Extend the package validation step or this regression test to inspect each Codex archive's Smoker instructions and matrix bytes.

  ```python
  SMOKER_SKILLS = (
      ROOT / ".agents" / "skills" / "the-smoker",
      ROOT / ".codex" / "plugins" / "vibe-coding-tools" / "skills" / "the-smoker",
  )
  ```

## Suggestions (consider improving)

None.

## Plan Item Traceability

| # | Plan Requirement | Status | Implementation Location | Notes |
|---|---|---|---|---|
| REQ-1 | Every generated or installed Codex Smoker resolves and reads a bundled local model-comparison matrix | ⚠️ | `.agents/skills/the-smoker/SKILL.md:17-19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:17-19`; `learn/scripts/generate-harnesses.py:69-72,186-213` | Generated trees use skill-local, byte-identical matrices. Tracked archives retain the prior root-relative layout. |
| REQ-2 | Missing or unreadable matrix stops execution before Bee dispatch | ❌ | `.agents/skills/the-smoker/SKILL.md:19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:19` | Correct in generated trees, absent from all packaged Codex Smoker copies. |
| REQ-3 | No ledger-model reuse or silent expensive fallback | ❌ | `.agents/skills/the-smoker/SKILL.md:19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:19` | Correct in generated trees, absent from all packaged Codex Smoker copies. |
| REQ-4 | Model identifier and reasoning effort remain separate dispatch settings | ❌ | `.agents/skills/the-smoker/SKILL.md:19`; `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:19`; `.agents/skills/the-smoker/references/model-comparison-matrix.md:22-30` | Correct in generated trees and matrix, absent from all packaged Codex Smoker instructions. |
| REQ-5 | Generated outputs remain idempotent and validated | ⚠️ | `learn/scripts/test-smoker-model-matrix.py:17-31`; `learn/scripts/generate-harnesses.py:148-229` | Two generator reruns preserved digest `01616bcee11d5a48a90a24763a901ac110054ed2b5978125fe76dd8d0efc2144`; component validators returned zero findings. Installable packages are not covered. |

## Files Changed

- `.agents/skills/the-smoker/SKILL.md` (M), switches to the skill-local matrix and adds the fail-closed dispatch contract
- `.agents/skills/the-smoker/references/model-comparison-matrix.md` (A), bundles the canonical matrix with the generated project skill
- `.claude/commands/the-smoker.md` (M), adds the canonical fail-closed dispatch and separate-setting instructions
- `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md` (M), switches to the skill-local matrix and adds the fail-closed dispatch contract
- `.codex/plugins/vibe-coding-tools/skills/the-smoker/references/model-comparison-matrix.md` (A), bundles the canonical matrix with the generated plugin skill
- `.cursor/commands/the-smoker.md` (M), mirrors the canonical fail-closed instructions for Cursor
- `library/requirements/reports/smoker-model-matrix/2026-09-01-smoker-model-matrix-security-report.md` (A), records the preceding clean security gate for this candidate
- `learn/scripts/generate-harnesses.py` (M), copies the canonical matrix into each generated Codex skill that references it
- `learn/scripts/test-smoker-model-matrix.py` (A), validates checked-out Codex Smoker paths, matrix bytes, and fail-closed instructions
