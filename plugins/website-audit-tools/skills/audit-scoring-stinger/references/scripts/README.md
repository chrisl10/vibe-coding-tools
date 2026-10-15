Deterministic scripts for this pair.

| Script | Purpose |
|---|---|
| `generate-scorecard-xlsx.py` | Generates `references/templates/website-audit-scorecard-template.xlsx` from scratch via `openpyxl`. Real, working generator, not a spec document - run it and it produces an openable workbook with live formulas. Re-run this after any change to the category/sub-audit weighting design instead of hand-editing the `.xlsx`. See the module docstring for exactly which design choices are sourced from `plan/website-auditor-build-plan.md` / `prd-020-audit-scoring-index.md` versus this Stinger's own engineering design (the leaf-to-sub-audit-to-category nesting structure). Usage: `python3 generate-scorecard-xlsx.py [output_path]`. |

Run-time helpers live in the plugin-root `shared/scripts/` folder:

- `score-rollup.py` computes the sub-audit, category and final percentages, the security override and the letter grade from validated leaf JSON, and lists rejected leaves. It reads the default weights from `generate-scorecard-xlsx.py`; pass `--rubric <json>` when the engagement retuned the `Rubric` sheet. Use it in procedure step 6 to cross-check the recalculated workbook: `python3 <pack>/shared/scripts/score-rollup.py --findings <leaf-json-dir> --out scoring/rollup-check.json`. It masks N/A at every level, exactly like the workbook: the sub-audit, category and final formulas all exclude an N/A child from both the numerator and the denominator, so the two agree number for number. An entry it lists under `na_subaudits` or `na_categories` shows as "N/A" in the workbook's rollup cell, and an all-N/A engagement shows "N/A" for the final score and grade. Any other difference is a transcription error; record it in the verification log.
- `xlsx-populate.py` was never implemented and exits with status 2. Transcribe leaves into the workbook copy by hand (procedure steps 1 and 4).
