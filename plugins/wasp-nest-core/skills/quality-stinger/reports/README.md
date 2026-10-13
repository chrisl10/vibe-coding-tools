> **DEPRECATED**, per-stinger `reports/` folders have been retired. QA reports now live in the host repo's `library/` tree:
>
> - **Feature-tied:** `library/requirements/<lifecycle>/prd-<###>-<title>/qa/<date>-qa-report.md`
> - **Issue-tied:** `library/issues/<lifecycle>/ird-<###>-<title>/qa/<date>-qa-report.md`
> - **Standalone audits:** `library/requirements/reports/quality-audits/<date>-<plan-name>-qa-report.md`
>
> Use the receiving repository's documented legacy report location when applicable; see [report placement](../guides/06-report-writing.md). Do not move old evidence during QA.
>
> The canonical QA report template lives at [`../templates/qa-report.md`](../templates/qa-report.md). The teaching set (happy-path, blocker-heavy, ordering-violation) lives in [`../examples/`](../examples). This stub remains so existing references don't 404, it can be removed via `git rm` when convenient.
