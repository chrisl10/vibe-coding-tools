# Distilled research: rendering the Audit My Code brief

Fetched 2026-09-30. Research window 2026-03-30 to 2026-09-30; standing standards (WCAG, WHATWG HTML, W3C WAI tutorials) are labeled as timeless where older. Every claim cites its raw file. Two internal design sources set the content structure and the visual system; the web sources set print, accessibility, escaping, and font loading.

## 1. Content structure (from the WHIPT model brief)

| Element | Rule | Source |
| --- | --- | --- |
| Header | Mono eyebrow with branch and sha, title, one framing paragraph naming who asked and what question, meta line with run time, tool versions, and "Repo changes: none" | [raw/design--whipt-bloat-audit-html.md] |
| Verdict | One big verdict word, a bold one-line answer, then a measures table: Measure, Result (right aligned, tabular numbers), Band pill, Threshold | [raw/design--whipt-bloat-audit-html.md] |
| Sections | Eyebrow "N · tool", h2, a scope paragraph stating what was scanned and excluded | [raw/design--whipt-bloat-audit-html.md] |
| Tool gotcha | A callout for every silent tool limit that was lifted or hit (jscpd's 1,000-line default skip is the example) | [raw/design--whipt-bloat-audit-html.md] |
| Charts | To-scale bars with a stated scale, dashed threshold ticks, labeled values, and a legend saying what color means | [raw/design--whipt-bloat-audit-html.md] |
| Spot checks | A table that says how each flagged item was confirmed or dismissed | [raw/design--whipt-bloat-audit-html.md] |
| Close | "Where the real savings are" ordered list, then a footer on method and "Nothing in the repo changed" | [raw/design--whipt-bloat-audit-html.md] |

## 2. Visual system (from the Legion Code Inc. Field Guide)

Palette sampled from the page renders, sRGB hex [raw/design--legion-field-guide-pdf.md]:

| Token | Light | Role |
| --- | --- | --- |
| ink | #0A0B0D | Headlines, body, heavy top rule |
| muted | #4A5160 | Subtitles, lead text |
| faint | #6B7280 | Eyebrows, mono footer, table heads |
| panel | #F4F5F7 | Cover panel |
| box | #FAFAFB | Diagram and neutral boxes |
| rule / rule-strong | #D8DCE2 / #B5BAC2 | Hairlines / table top rules |
| brand-green / ink / mint | #18A968 / #0E6D43 / #EBF6F0 | Index numbers, REMEMBER box |
| brand-amber / soft | #C77A00 / #FAF2E8 | Cover bar, definition box |
| brand-red, brand-blue | #DC2839, #1273D6 | Expired, human gate |

Components to reproduce: cover panel with mono eyebrow, green index, hairline rule; short amber bar over a very heavy tight headline; muted subtitle; three-cell meta strip; logo bottom left; heavy black top rule per part (grey for "fair" parts, green for the end); mono uppercase eyebrows; frameless tables with mono heads and hairline rows; green-bordered mint REMEMBER callout; amber definition box; lease diagram with square nodes and thick bars; mono running footer with company, person, context, date left and title right [raw/design--legion-field-guide-pdf.md].

Severity and band colors are separate tokens from brand colors. They are a design decision of this skill (not sampled), kept apart so a brand change never changes what "critical" looks like. Thin spot: no external source rules on severity color choice; WCAG 1.4.1 only requires that color is not the sole cue [raw/a11y--wcag-use-of-color.md].

## 3. Fonts

| Fact | Source |
| --- | --- |
| Google Fonts Inter has axes `opsz` 14 to 32 and `wght` 100 to 900; designer Rasmus Andersson; OFL | [raw/fonts--google-fonts-inter-metadata.md] |
| JetBrains Mono on Google Fonts is a variable `wght` font; OFL | [raw/fonts--google-fonts-jetbrains-mono-metadata.md] |
| CSS2 API ranges use `..`; axes must be listed alphabetically; `display=swap` is usually appropriate | [raw/fonts--google-fonts-css2-api.md] |
| `font-optical-sizing: auto` is the default and drives `opsz` from font size, so big headlines get the display cut | [raw/fonts--mdn-font-optical-sizing.md] |

Request used: `family=Inter:opsz,wght@14..32,400..900&family=JetBrains+Mono:wght@400..700&display=swap`, verified against the live endpoint on 2026-09-30 [raw/fonts--google-fonts-css2-api.md]. Visual match of Inter Display and JetBrains Mono to the PDF is a judgment from the page renders, not a font-file extraction [raw/design--legion-field-guide-pdf.md].

## 4. Theming

| Fact | Source |
| --- | --- |
| `prefers-color-scheme` has `light` and `dark`; baseline since January 2020 | [raw/theme--mdn-prefers-color-scheme.md] |
| `color-scheme` makes scrollbars and form controls follow the theme; inherited | [raw/theme--mdn-color-scheme.md] |

Pattern: light tokens on `:root`; dark tokens under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` and again under `:root[data-theme="dark"]`; print forces the light set.

## 5. Print ("Save as PDF")

| Fact | Source |
| --- | --- |
| `break-inside: avoid` keeps a block on one page; `page-break-inside` is a legacy alias | [raw/print--mdn-break-inside.md] |
| `break-before/after: page` forces a page break; `page-break-after: always` maps to `page` | [raw/print--mdn-break-after.md] |
| `@page` sets size and margins; MDN warns many page-box properties are unsupported; Baseline 2024 | [raw/print--mdn-page-at-rule.md] |
| Print rules go in `@media print`; hide screen-only chrome there | [raw/print--mdn-printing-guide.md] |
| Browsers may drop backgrounds in print (`economy`); `print-color-adjust: exact` keeps authored colors; user settings still win | [raw/print--mdn-print-color-adjust.md] |

Running footer: emitted twice, as `@page` `@bottom-left` and `@bottom-right` margin boxes (CSS-escaped strings) and as a normal footer block at the end. Verified on 2026-09-30 in the local Chrome build: margin boxes printed on every page. Conflict: MDN says margin-box support is uneven [raw/print--mdn-page-at-rule.md]; the end-of-document footer is the fallback for browsers without it.

Observed during verification (not from a source): wide tables with `overflow: visible` in print make Chrome shrink the whole page to fit, so print rules also let header cells and paths wrap.

## 6. Accessible tables and scroll frames

| Fact | Source |
| --- | --- |
| Header cells `th` with `scope="col"`; captions name a table's topic | [raw/a11y--w3c-wai-tables-tutorial.md] |
| `caption` must be the first child of `table` | [raw/a11y--mdn-caption-element.md] |
| Scrollable regions need keyboard access: `tabindex="0"` on the container | [raw/a11y--axe-scrollable-region-focusable.md] |
| Reflow at 320 CSS px without two-dimensional scrolling; data tables are excepted, only for that section | [raw/a11y--wcag-reflow.md] |
| Color must not be the only cue | [raw/a11y--wcag-use-of-color.md] |

## 7. Escaping untrusted text

| Fact | Source |
| --- | --- |
| Body context: encode `& < > " '`; quote every attribute | [raw/escape--owasp-xss-prevention.md] |
| Never put untrusted data in script blocks or handlers; CSS values only, hex-escaped | [raw/escape--owasp-xss-prevention.md] |
| `html.escape(s, quote=True)` converts `& < >` and both quotes | [raw/escape--python-html-escape.md] |
| `script` and `style` must not contain `</` plus their tag name | [raw/escape--whatwg-raw-text-restrictions.md] |
| `findings.jsonl` is JSON Lines: UTF-8, one value per line, blank lines invalid | [raw/data--jsonlines-format.md] |

## Thin spots

- No primary source states which browsers support `@page` margin boxes by version; support was tested locally only.
- The Field Guide fonts were identified visually, not extracted from the PDF.
- The brief carries no script, so there is no theme toggle in the page; `--theme` pins a theme at render time instead. This is a security choice, not a sourced rule.
