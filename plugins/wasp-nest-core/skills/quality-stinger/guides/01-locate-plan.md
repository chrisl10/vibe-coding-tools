# 01, Locate the Plan Document

The plan is the ground truth for the audit. Without a plan, there is no audit.

---

## Resolution order

Try each source in order. Stop at the first that yields a plan.

### 1. Explicit pointer from the invoker

If the user's message includes a path (e.g., "QA `library/requirements/<lifecycle>/prd-007-search/prd-007-search-index.md`"), use that file directly. Do not second-guess the choice. Verify the file exists and is readable.

### 2. Attached context

If the session has attached files or the message references a file that was just edited (like a PRD file), inspect those. A plan is typically the longest markdown document in the session that contains sections like "User Stories", "Acceptance Criteria", "Scope", or "Non-Goals".

### 3. `library/requirements/` directory

Scan the repo for plan documents in their canonical location. Typical patterns:

```bash
rg --files library/requirements library/issues | rg '/(backlog|in-work|completed)/(prd|ird)-[^/]+/.*\.md$'
```

The [Library Schema v2 framework](../../library-stinger/templates/documentation-framework.md) uses `backlog`, `in-work`, or `completed` as `<lifecycle>`:

- PRD index: `library/requirements/<lifecycle>/prd-<###>-<slug>/prd-<###>-<slug>-index.md`.
- Optional ClickUp index suffix: `prd-<###>-<slug>-index-ck-<clickupId>.md`; the folder has no suffix.
- Optional sub-PRD: `prd-<###><letter>-<slug>-<feature>.md` in the same PRD folder. Read the index and the relevant sub-PRD together.
- IRD index: `library/issues/<lifecycle>/ird-<###>-<slug>/ird-<###>-<slug>-index.md`.

A completed PRD is directly under `library/requirements/completed/`; a completed IRD is directly under `library/issues/completed/`.

**Existing repositories:** Use the user's supplied plan path and the receiving repository's documented conventions. Legacy `prd-feature-*.md`, `ird-issue-*.md`, `reports/` folders, `docs/prd/`, `docs/plans/`, `tasks/`, `.specify/specs/`, or `SPEC.md` remain valid when observed in that repository. Do not rename or move its plans or reports during QA. A migration requires a separate authorized Library task. If the plan or output destination is ambiguous, ask before writing.

### 4. Branch correlation

If the branch name encodes a plan reference (e.g., `feat/phase-3-search`), search for plans whose filename or header matches:

```bash
git branch --show-current           # get current branch
# then grep tasks/ for files whose name or heading matches
```

### 5. Last-modified PRD in git log

If nothing else works, look for the most recently modified plan-like file in git log:

```bash
git log --oneline --all -- 'library/requirements/**/prd-*.md' | head -20
git log --oneline --all -- 'library/issues/**/ird-*.md' | head -20
```

### 6. Ask the invoker

If no plan can be located after the above, stop and ask. Do not fabricate a plan from the diff. Example prompt:

> "I couldn't locate the plan document. Is it in `library/requirements/<lifecycle>/`, `library/issues/<lifecycle>/`, or somewhere else? If you don't have one, I need at least a short spec, the audit depends on comparing the implementation against stated requirements."

---

## Validate the plan before proceeding

Once you have a candidate plan:

1. It should contain at least one of: Goals, User Stories, Requirements, Acceptance Criteria, Non-Goals, Scope.
2. It should reference the feature/phase matching the branch or the user's request.
3. It should not itself be a QA report from a previous run (check for scorecards and "Critical Issues" sections, those mean you grabbed the wrong file).

If the candidate fails validation, escalate back to resolution step 3 or 6.

---

## Handling multi-plan situations

If the diff spans multiple plans (e.g., bug fixes from Plan A interleaved with feature work from Plan B):

- Produce **one report per plan**, each in that plan's own `qa/` subfolder as `<date>-qa-report.md` (or in `library/requirements/reports/<domain>/` for standalone audits).
- Each report's "Files Changed" section lists only files relevant to that plan.
- Note in each Summary that the audit was scoped to one plan and point at the sibling report.

Do not try to merge two plans into a single audit. The traceability table requires a single source of truth per report.

---

## Handling a missing plan that the invoker can't produce

If the user says "there's no plan, just audit what's there":

- This is not a plan audit. Decline politely and recommend either:
  - Having `library-wasp-drone` author a backwards-PRD from the diff first, then running QA against it, or
  - Running a plan-agnostic code review (which is not this Drone's job, suggest the `review` skill or a generic AI code reviewer like CodeRabbit).

Do not produce a report anyway. The value of the audit is the plan comparison.

---

## See also

- Example: `examples/01-happy-path-clean-audit.md` shows the plan location as `library/requirements/<lifecycle>/prd-007-result-mode-label/prd-007-result-mode-label-index.md` and the report reflects that in its heading.
- Research: plans and requirements traceability, `research/2026-04-24-traceability-matrix.md` (source-repository research, not shipped).
