This pair has no deterministic capture script. Screenshots are taken with the harness's own browser tool per `guides/03-capture-checkpoint-screenshots.md`. The planned shared `shared/scripts/visual-capture.py` was never implemented; it exits with status 2 and points back to that guide.

One reference snippet is kept local to this Stinger instead of the shared folder, because it is not a deterministic script this Drone invokes but a copy-ready configuration block for whatever browser-automation surface the harness provides:

| File | Purpose |
|---|---|
| `playwright-viewport-config.js` | Copy-ready Playwright device-emulation config for the two required checkpoint viewports (1440x900 desktop, 390x844 mobile). Grounded in `references/research/raw/playwright-dev-docs-emulation.md`; see `distilled-visual-funnel.md` section 5 for why these are custom profiles rather than named registry devices. |
