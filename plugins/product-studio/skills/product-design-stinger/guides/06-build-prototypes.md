# 06: Build clickable prototypes

Goal: real, clickable, single-file HTML prototypes of the key screens that look finished enough to judge, in light and dark, with every state reachable.

Grounding: [prototype fidelity](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-prototype-fidelity.md), [light-dark()](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/css--mdn-light-dark.md), [reduced motion](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/css--mdn-prefers-reduced-motion.md), [WCAG 2.2 new criteria](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/a11y--w3c-wai-new-in-22.md), [visual hierarchy](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-visual-hierarchy.md). Distilled: sections [5 and 9](../references/research/distilled-product-design.md).

Precondition: Gate A is recorded in `direction.md`. If it is not, stop and go back to guide 01.

## Rules every prototype follows

| Rule | Why |
|---|---|
| One `.html` file per screen, inline CSS and JS, no network requests, opens by double-click | Reviewable anywhere; the checker flags external `src` or `href` |
| Tokens as CSS custom properties on `:root`; no raw color, size or duration values in rules | Tokens are what design-system-stinger and Claude Design pick up later |
| `color-scheme: light dark` and colors through `light-dark()`; `[data-theme]` override for a manual toggle | Both themes from one set of tokens (Baseline 2024) |
| All four states reachable from a clearly labelled "Prototype controls" bar | States are part of the design, not an afterthought |
| `prefers-reduced-motion: reduce` removes animation and transition | Vestibular safety |
| Skip link, landmarks, one h1, labelled controls, polite live region for status | WCAG 2.2 AA baseline |
| Targets at least 24 by 24 CSS px (starter uses 44); `scroll-padding-top` equals the sticky header | 2.5.8 and 2.4.11 |
| Works at 320 CSS px wide with no horizontal page scroll | 1.4.10 |
| Every page is labelled "Prototype, not production" | Prevents premature launch decisions |
| Real copy from the screen spec, never lorem ipsum | Content fidelity is a fidelity dimension too |

## Procedure

1. Copy [prototype-starter.html](../references/templates/prototype-starter.html) to `design/prototypes/S-<area>-<nn>.html` for the first key screen.
2. Retune the tokens to the approved direction once, in the first prototype. Copy the final `:root` block into every other prototype unchanged; a token change happens in all files or none.
3. Replace the demo content with the screen spec: layout in reading order, components, the copy, and the four state views. Keep the state switcher and theme switcher.
4. Link screens the way the flows say they connect, so a reviewer can click through each `F-nn` end to end. Unbuilt screens link to `index.html` with a note, never to a dead `#`.
5. Write `design/prototypes/index.html`: a list of screens grouped by flow, each linking to its prototype. It must also meet the prototype rules (lang, viewport, tokens, both themes, reduced motion).
6. Pilot every prototype yourself before critique: click every link, switch every state and theme, check 1440 and 390 wide and 320 wide. If a browser tool is available, take the screenshots now; guide 07 uses them as evidence.
7. Run `python3 scripts/check-design-package.py package <design-dir>` and fix every prototype finding.

## Taste guardrails (they feed the anti-slop score)

- Neutrals carry the interface; the accent means something (primary action, selection, success) and is not decoration.
- No gradient text, glow halos, eyebrow chips above headings, numbered section labels, or decorative looping motion. These are Impeccable detector rules (repo: `impeccable-stinger/guides/06-detector-gate.md`).
- Weight and size create hierarchy before color does. At most three type sizes per screen.
- Tabular numbers for money and counts. Right-align numeric columns.
- System font stack unless the direction names a typeface; never load a web font from a CDN in a prototype.
