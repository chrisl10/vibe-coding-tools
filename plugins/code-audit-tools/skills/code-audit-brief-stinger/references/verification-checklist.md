# Verification checklist: before the brief goes to the user

Tick every line. A line that cannot be ticked is reported to the orchestrator, not skipped. Derived from `research/distilled-brief-rendering.md`.

## Completeness

- [ ] The brief covers exactly the tier's dimensions (foundation; vibe adds bloat; basic adds security; full adds quality; mario adds the remediation roadmap). No other dimension heading appears.
- [ ] Every dimension that did not produce `metrics.json` shows "Not run" with a reason, and the reason is true.
- [ ] Finding count in the brief equals the line count of every tier `findings.jsonl` minus merges minus unparsed lines (both listed under Data checks).
- [ ] Every `coverage.caps` entry appears twice: as an amber "Tool limit" box in its section and in the Coverage and caps table. A dimension with no `caps` key is flagged "Not reported".
- [ ] Top 10 "Fix these first" is ordered severity, confidence, effort.
- [ ] Mario tier: the Now, Next, Later timeline matches `plan.json` waves, and `uncovered_finding_ids` is empty or flagged.

## Safety

- [ ] `grep -ci '<script' brief.html` prints 0.
- [ ] No `href="javascript` and no raw `<img`, `<iframe`, or `on...=` from repo text (search for a hostile string you know is in the findings and confirm it appears escaped as `&lt;`).
- [ ] No unredacted secret: search for `sk_live_`, `ghp_`, `AKIA`, `-----BEGIN`. If the renderer masked one, a "Evidence masked" data check is present; send the finding back to its Drone.
- [ ] No absolute home path or personal data beyond `requested_by` and repo metadata.

## Layout and print

- [ ] At 360 px wide there is no horizontal page scroll; wide tables scroll inside their frame (`scripts/` has no browser, so check in a browser or a headless one).
- [ ] Light and dark both read well (render once with `--theme dark` to a preview path to check).
- [ ] Print preview ("Save as PDF"): cover fills page 1, each part starts a new page, callouts and table rows are not split, footer line shows on each page in Chromium browsers.

## Truthfulness

- [ ] Spot-check three numbers in the brief against `metrics.json` and three findings against `findings.jsonl`. They match character for character (apart from escaping).
- [ ] The overall verdict equals `rollup_verdict` of the dimension verdicts shown in the scorecard.

Sources: [research/raw/a11y--wcag-reflow.md], [research/raw/print--mdn-break-inside.md], [research/raw/print--mdn-print-color-adjust.md], [research/raw/escape--owasp-xss-prevention.md].
