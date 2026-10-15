# 06, Report Writing

How to produce the findings-report markdown. Use `templates/qa-report.md` as the skeleton and fill each section in order.

---

## File name and location

Pick the path that matches the source plan. Reports are dated, so multiple audits can coexist without overwriting.

`<lifecycle>` is `backlog`, `in-work`, or `completed`. These defaults describe Library Schema v2. First read the receiving repository's README and report conventions. For a legacy repository that uses another plan filename or a plan-local `reports/` folder, keep that documented location. Record the actual plan and report paths in the audit; do not migrate existing files or replace earlier reports. Ask when the repository gives conflicting destinations.

- **Feature PRD audit:** `library/requirements/<lifecycle>/prd-<###>-<title>/qa/<YYYY-MM-DD>-qa-report.md`
- **Issue IRD audit:** `library/issues/<lifecycle>/ird-<###>-<title>/qa/<YYYY-MM-DD>-qa-report.md`
- **Standalone audit (no source plan):** `library/requirements/reports/<domain>/<YYYY-MM-DD>-qa-report.md`

Examples:

- Plan `library/requirements/<lifecycle>/prd-007-search/prd-007-search-index.md` -> report at `library/requirements/<lifecycle>/prd-007-search/qa/2026-04-26-qa-report.md`.
- Plan `library/issues/<lifecycle>/ird-042-stale-cache/ird-042-stale-cache-index.md` → report at `library/issues/<lifecycle>/ird-042-stale-cache/qa/2026-04-26-qa-report.md`.
- Standalone audit of the auth surface → `library/requirements/reports/auth/2026-04-26-qa-report.md`.

If two audits run on the same date, suffix the second one with a slug (e.g., `2026-04-26-qa-report-post-security-fixes.md`) rather than overwriting.

For Library Schema v2, create the plan's `qa/` folder or the standalone `library/requirements/reports/<domain>/` folder if it does not exist.

---

## Writing each section

### Summary (2-3 sentences)

Open with the verdict, then the headline findings, then the recommendation. Voice: calm, factual, no hedging.

Good:

> The phase-3 library-search implementation is largely complete with one Critical gap (missing BM25 fallback, US-3) and three Warnings. Recommend addressing the fallback logic before merge; the Warnings can be deferred to a follow-up.

Bad:

> Overall the PR seems to be in good shape! There are a few things to look at but nothing too serious. I think maybe the fallback stuff should be revisited.

### Scorecard

A five-row table, one row per axis. Use ✅ / ⚠️ / ❌ exclusively, no yellow-light ambiguity.

```markdown
| Category       | Status | Notes |
|---------------|--------|-------|
| Completeness  | ⚠️ | 1 of 7 plan items missing (US-3 BM25 fallback) |
| Correctness   | ✅ | Implementations match plan behavior |
| Alignment     | ✅ | Naming and structure match `library/requirements/<lifecycle>/prd-007-search/prd-007-search-index.md` |
| Gaps          | ⚠️ | Missing empty-result message; no degraded-mode label |
| Detrimental   | ⚠️ | N+1 dataset read in `search-service.ts:search` |
```

### Findings sections

Three sections in this order: Critical, Warnings, Suggestions. Each is a checkbox list so PR authors can tick items as they fix.

Each finding follows this shape:

```markdown
- [ ] **<one-line title>**, `path/to/file.ts:LN-LN`

  <2-4 sentences explaining what's wrong, why it matters, and a suggested remediation.>

  ```ts
  <1-6 lines of offending or missing code>
  ```
```

Example:

```markdown
- [ ] **Missing BM25 fallback when embeddings off (US-3)**, `src/search/search-service.ts:88-104`

  The plan §3.3 specifies that when embeddings are disabled, search must fall back to a BM25 lexical ranker and label the result mode. The current handler logs the unavailability and returns, no fallback runs. This leaves search returning nothing offline, which the plan explicitly prohibits.

  Suggested: call the BM25 ranker over the library corpus and tag the result mode `bm25-fallback`.

  ```ts
  if (!embeddingsAvailable) {
    logger.warn("embeddings unavailable");
    return;  // <- missing BM25 fallback
  }
  ```
```

If a section has no findings, include an empty list with "None" below:

```markdown
## Suggestions (consider improving)

None.
```

Do not omit empty sections, the reader needs to see that each tier was considered.

### Plan Item Traceability

Full table from step 3. Don't abbreviate. If a plan has 40 requirements, the table has 40 rows. Use horizontal scroll or wrap, do not cut rows.

Include non-goals as rows (prefix `NG-`) so the reader sees scope was audited.

### Files Changed

One-line summary per file. Derived from the inventory in step 2.

```markdown
- `src/retrieval/rank.ts` (M), added cursor-capped ranking per US-1
- `src/search/search-service.ts` (A), new service; contains the fallback gap (US-3)
- `src/dataset/schema.ts` (M), added the search index tensor to the Deep Lake schema
- `docs/SUMMARIES.md` (M), architecture note per §2.1
```

Group by file path (alphabetical within the group) rather than by status.

---

## Voice and tone

- **Direct.** "The handler does not retry." Not "Looks like there might be no retry here, maybe?"
- **Cite evidence.** Every finding has a file, line, and (usually) a snippet.
- **Suggest, don't mandate.** "Suggested:" rather than "You must:". The author owns the fix.
- **No adjectives.** "Appalling", "terrible", "lovely", none of these. Severity lives in the tier, not the prose.
- **No apologies or softeners.** "I think maybe", "just a thought", "probably", cut all of these.

---

## Metadata block at the top

Before the Summary, include:

```markdown
# QA Report: <Plan Name>

**Plan document:** <path>
**Audit date:** <YYYY-MM-DD>
**Base branch:** <base branch, e.g., `main`>
**Head:** <current branch or SHA>
**Auditor:** quality-wasp-drone
```

This lets a future reader reproduce the audit.

---

## Verification receipts alongside the report

Use [verification artifacts](08-verification-artifacts.md) and the [companion template](../templates/verification-artifacts.md) to bind candidate, plan, Security review, actual checks and outputs. Record unresolved execution as NOT_RUN, SKIPPED, CANCELLED, INCOMPLETE, STALE or UNKNOWN, retaining runner-specific outcomes. A source/docs pass cannot satisfy a runtime acceptance criterion. Metadata links extend the existing report; preserve its section order.

## Final check before saving

Run through this list:

- [ ] Every finding has `file:line` coordinates.
- [ ] Every finding has a severity matching `guides/05-severity-classification.md`.
- [ ] The Scorecard has exactly five rows.
- [ ] The traceability table includes every plan requirement, no silent omissions.
- [ ] The Files Changed list matches the inventory from step 2 exactly.
- [ ] No findings appear in more than one severity section.
- [ ] No section is missing (write "None" if empty).
- [ ] The file is saved at the correct path: feature audits in `library/requirements/<lifecycle>/prd-<###>-<title>/qa/`, issue audits in `library/issues/<lifecycle>/ird-<###>-<title>/qa/`, standalone audits in `library/requirements/reports/<domain>/`.

Then write the file. Then stop.

---

## See also

- Templates: `templates/qa-report.md`, `templates/traceability-table.md`.
- Examples: `examples/01-happy-path-clean-audit.md`, `examples/02-blocker-heavy-audit.md`, `examples/03-ordering-violation-escalation.md`.
- Research on AI-reviewer output shape: `research/2026-04-24-ai-code-review-tools.md` (source-repository research, not shipped).
