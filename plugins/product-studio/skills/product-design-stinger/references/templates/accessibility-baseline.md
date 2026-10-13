# Accessibility baseline: WCAG 2.2 AA

<!-- Design-time contract. It does not prove conformance; the built product is tested later by its implementation owners. Grounding: research/raw/a11y--w3c-wcag22-recommendation.md, a11y--w3c-wai-new-in-22.md, a11y--w3c-wcag22-quickref.md, css--mdn-prefers-reduced-motion.md, diagram--mermaid-accessibility.md -->

Target: WCAG 2.2 Level AA. Status: draft.

## Design-time requirements

| Area | Requirement | SC | How the package meets it |
|---|---|---|---|
| Text contrast | 4.5:1 body, 3:1 large, in light AND dark | 1.4.3 | {token pairs checked; list in table below} |
| UI contrast | 3:1 for borders of inputs, focus rings, state indicators | 1.4.11 | |
| Color alone | Errors, status and links also use text, icon or underline | 1.4.1 | |
| Reflow | Every key screen works at 320 CSS px wide | 1.4.10 | prototypes tested at 320 |
| Focus visible | Clear focus ring on every interactive element | 2.4.7 | `--focus-ring` token |
| Focus not obscured | Sticky headers, toasts and drawers never fully hide focus | 2.4.11 | scroll-padding equals sticky header height |
| Target size | 24 by 24 CSS px minimum (44 preferred for primary touch) | 2.5.8 | `--target-min` token |
| Dragging | Single-pointer alternative for every drag | 2.5.7 | {list drags and alternatives} |
| Consistent help | Help in the same relative place on every screen | 3.2.6 | IA navigation model |
| Redundant entry | Never re-ask data entered earlier in a flow | 3.3.7 | flows checked |
| Authentication | No puzzles or transcription at sign-in; allow paste and password managers | 3.3.8 | S-auth specs |
| Structure | One h1, ordered headings, landmarks, labelled controls | 1.3.1, 2.4.6, 4.1.2 | screen specs |
| Status messages | Loading, success and error announced without moving focus | 4.1.3 | polite live regions |
| Motion | Honor reduced motion: remove scale and pan, keep opacity | 2.3.3 (AAA, adopted as house rule) | prototype CSS |
| Diagrams | Mermaid diagrams carry accTitle and accDescr | n/a | flows |

## Contrast record

| Pair | Light ratio | Dark ratio | Pass |
|---|---|---|---|
| `--text` on `--surface` | | | |
| `--text-muted` on `--surface` | | | |
| `--on-accent` on `--accent` | | | |
| `--border-strong` on `--surface` (UI 3:1) | | | |

## Known exceptions

| Screen | Criterion | Why | Plan |
|---|---|---|---|
| | | | |
