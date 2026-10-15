# 04. Verification before handing the brief to the user

The brief is the only thing most readers will see. Check it before the orchestrator shows it.

## Steps

1. **Render** (guide 02) and keep the printed summary line: finding count, merges, data checks, overall verdict.
2. **Work the checklist** in [../references/verification-checklist.md](../references/verification-checklist.md) top to bottom. Use `grep` for the safety lines; they are fast and exact.
3. **Read the Data checks table in the brief.** Each row is a problem in a Drone's output. Do not fix the workspace yourself. Send the list to the orchestrator with the owning Drone named (the folder tells you which).
4. **Open the page.** Read the cover, the one-paragraph summary, the verdict, and one dimension end to end. If the summary paragraph is confusing, the fix belongs in that Drone's `metrics.summary`, not in the brief.
5. **Check phone width and print.** In a browser at 360 px there must be no sideways page scroll. Print preview must start each part on a new page and keep callouts whole [../references/research/raw/a11y--wcag-reflow.md] [../references/research/raw/print--mdn-break-inside.md (source-repository research, not shipped)].
6. **Report** to the orchestrator: the brief path, the overall verdict, counts by severity, the data checks, and anything from the checklist you could not tick.

## Done when

- Every checklist line is ticked or reported.
- `grep -ci '<script' brief.html` prints 0.
- The overall verdict in the brief equals the worst dimension verdict shown in its own scorecard.

## Sources

The notes listed below are source-repository research, not shipped.

- [../references/research/raw/a11y--wcag-reflow.md (source-repository research, not shipped)]
- [../references/research/raw/print--mdn-break-inside.md (source-repository research, not shipped)]
- [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)]
