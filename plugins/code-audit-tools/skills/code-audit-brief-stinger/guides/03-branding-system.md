# 03. Branding system (Legion Code Inc. Field Guide)

The brief reproduces the Field Guide's look. All brand values live in one file, `references/brand/brand.json`; the CSS in `render_brief.py` reads tokens from it and never hard-codes a brand color.

## Change the brand

1. Edit `references/brand/brand.json`: `palette.light` and `palette.dark` (brand tokens), `severity` and `bands` (meaning tokens), `fonts`, `logos`, `eyebrow`, `title_suffix`, `footer`.
2. Put any new logo SVG in `references/brand/` and point `logos.light` / `logos.dark` / `logos.favicon` at it. Logos are trusted files shipped with the skill and are inlined into the page.
3. Re-render a fixture and run the tests. A value with characters outside the safe CSS set stops the render with the key name.

## Palette (sampled from the Field Guide renders)

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `ink` | #0A0B0D | #F5F6F7 | headlines, body, part rule |
| `muted` | #4A5160 | #B3B9C4 | lead text, fixes |
| `faint` | #6B7280 | #8E95A1 | eyebrows, table heads, footer |
| `panel` | #F4F5F7 | #1A1E24 | cover |
| `box` | #FAFAFB | #171A1F | charts, timeline, neutral boxes |
| `rule`, `rule-strong` | #D8DCE2, #B5BAC2 | #2A2F37, #3D434D | hairlines |
| `brand-green`, `brand-green-ink`, `brand-mint` | #18A968, #0E6D43, #EBF6F0 | #3DDC97, #5FE3A8, #11291E | index number, REMEMBER, timeline |
| `brand-amber`, `brand-amber-soft` | #C77A00, #FAF2E8 | #E39A2D, #2A1F0E | cover bar, tool-limit box |

Light values come from pixel sampling [../references/research/raw/design--legion-field-guide-pdf.md]. Dark values are derived (the guide has only its closing dark band, #121212, and the dark logo's #3DDC97 cap); treat them as this skill's design.

Severity (`--sev-*`) and band (`--band-*`) tokens are separate from brand tokens on purpose. Never point a severity at a brand token: a rebrand must not change what "critical" looks like.

## Type

- Sans: Inter from Google Fonts with the `opsz` axis, so big headlines get the Inter Display cut automatically [../references/research/raw/fonts--google-fonts-inter-metadata.md] [../references/research/raw/fonts--mdn-font-optical-sizing.md]. Headlines weight 800 to 850, letter-spacing about -0.05em.
- Mono: JetBrains Mono for eyebrows (uppercase, 0.14em tracking), paths, numbers, and the footer [../references/research/raw/fonts--google-fonts-jetbrains-mono-metadata.md].
- Load string follows the CSS2 API rules (alphabetical axes, `..` ranges, `display=swap`) [../references/research/raw/fonts--google-fonts-css2-api.md]. Offline, system fonts take over.

## Components and where they appear

| Field Guide component | In the brief |
| --- | --- |
| Cover panel, eyebrow with green index and hairline, amber bar, heavy headline, meta strip, logo | Cover |
| "00 CONTENTS" rows and color key | Contents |
| Heavy black top rule, mono eyebrow, bold heading, muted lead | Every part; grey rule for Coverage and caps, green rule for the end |
| REMEMBER box (green border, mint fill) | One per dimension: its summary. One for the first Now work package |
| Definition box (amber border, amber soft fill) | "Tool limit, handled." per coverage cap |
| Lease diagram (square nodes, thick bars, dashed empty node) | Remediation Now, Next, Later timeline |
| Frameless tables, mono heads, hairline rows | All tables |
| Running mono footer | `@page` margin boxes on every printed page, plus a footer block at the end |

## Theme and print

Dark tokens apply under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` and under `:root[data-theme="dark"]` [../references/research/raw/theme--mdn-prefers-color-scheme.md]; `color-scheme` follows so scrollbars match [../references/research/raw/theme--mdn-color-scheme.md]. Print always uses the light set, keeps meaning colors with `print-color-adjust: exact` [../references/research/raw/print--mdn-print-color-adjust.md], starts each part on a new page, and keeps callouts, cards, and rows whole [../references/research/raw/print--mdn-break-after.md] [../references/research/raw/print--mdn-break-inside.md].

## Sources

- [../references/research/raw/design--legion-field-guide-pdf.md]
- [../references/research/raw/fonts--google-fonts-inter-metadata.md]
- [../references/research/raw/fonts--google-fonts-jetbrains-mono-metadata.md]
- [../references/research/raw/fonts--google-fonts-css2-api.md]
- [../references/research/raw/fonts--mdn-font-optical-sizing.md]
- [../references/research/raw/theme--mdn-prefers-color-scheme.md]
- [../references/research/raw/theme--mdn-color-scheme.md]
- [../references/research/raw/print--mdn-print-color-adjust.md]
- [../references/research/raw/print--mdn-break-after.md]
- [../references/research/raw/print--mdn-break-inside.md]
