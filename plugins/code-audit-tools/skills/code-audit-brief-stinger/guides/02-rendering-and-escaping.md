# 02. Rendering and escaping

How to run the renderer, and the rules that keep repo-derived text from becoming code in the reader's browser.

## Render

1. Run `python3 scripts/render_brief.py <workspace>` from this skill's folder (or with the full script path). It prints the output path, finding count after merge, merges, data checks, and the overall verdict.
2. If it exits with an error, read the message: a missing `intake.json` or an unknown tier means the run did not finish intake. Report it; do not hand-write an intake.
3. For a dark-theme preview, write to a scratch path: `--theme dark --out <scratch>/dark.html`. Never leave a preview inside the workspace's `brief/` folder; the contract allows one file there.
4. Run `python3 scripts/test_render_brief.py` after any edit to the script or to `brand.json`.

## Escaping rules (do not weaken them)

| Rule | Why | Source (source-repository research, not shipped) |
| --- | --- | --- |
| Every workspace string goes through `esc()` (`html.escape`, `quote=True`) | Encodes `& < > " '` for body text and quoted attributes | [../references/research/raw/escape--python-html-escape.md], [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| Attributes are always double-quoted | Unquoted attributes let data switch context | [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| The page carries no `<script>` | Untrusted data is never safe inside script; with no script there is no script context at all | [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| No repo text inside `<style>` except the footer strings, which go through `css_string()` hex escaping | `</style` would close the block; CSS needs hex escapes | [../references/research/raw/escape--whatwg-raw-text-restrictions.md], [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| `brand.json` values used in CSS must match a safe character set | A bad brand file cannot inject a rule or close the style block | [../references/research/raw/escape--whatwg-raw-text-restrictions.md (source-repository research, not shipped)] |
| Markdown links render as text plus the URL in plain text, never `href` | `javascript:` and look-alike links stay inert | [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| Inline `style` only carries numbers the renderer computed (bar widths, tick positions) | Repo data never reaches a CSS value | [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)] |
| Anchor ids are slugged to `[a-z0-9_-]` | Finding ids cannot break out of `href="#..."` | design choice |

## Accessibility rules the markup follows

- Every table has a `caption` as its first child (visually hidden when a heading already names it) and `th scope="col"` heads [../references/research/raw/a11y--mdn-caption-element.md] [../references/research/raw/a11y--w3c-wai-tables-tutorial.md (source-repository research, not shipped)].
- Every scroll frame is `role="region"`, `tabindex="0"`, with an `aria-label`, so keyboard users can scroll it [../references/research/raw/a11y--axe-scrollable-region-focusable.md (source-repository research, not shipped)].
- Pills, chart rows, and callouts always carry their word or value; color is never the only cue [../references/research/raw/a11y--wcag-use-of-color.md (source-repository research, not shipped)].
- The page reflows at 320 px; only tables scroll sideways, inside their frames [../references/research/raw/a11y--wcag-reflow.md (source-repository research, not shipped)].

## Changing the script

Keep `rollup_verdict` pure, small, and near the top. The next refinement replaces its body only; callers pass `{dimension: verdict}` and get one verdict back. Add a test in `test_render_brief.py` for any new rule.

## Sources

The notes listed below are source-repository research, not shipped.

- [../references/research/raw/escape--python-html-escape.md (source-repository research, not shipped)]
- [../references/research/raw/escape--owasp-xss-prevention.md (source-repository research, not shipped)]
- [../references/research/raw/escape--whatwg-raw-text-restrictions.md (source-repository research, not shipped)]
- [../references/research/raw/a11y--w3c-wai-tables-tutorial.md (source-repository research, not shipped)]
- [../references/research/raw/a11y--mdn-caption-element.md (source-repository research, not shipped)]
- [../references/research/raw/a11y--axe-scrollable-region-focusable.md (source-repository research, not shipped)]
- [../references/research/raw/a11y--wcag-reflow.md (source-repository research, not shipped)]
- [../references/research/raw/a11y--wcag-use-of-color.md (source-repository research, not shipped)]
