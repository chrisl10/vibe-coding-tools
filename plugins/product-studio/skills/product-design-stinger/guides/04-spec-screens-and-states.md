# 04: Specify screens and their states

Goal: one spec per screen that a designer, Claude Design, or an engineer can build from without guessing, including empty, loading, error and success.

Grounding: empty states, error messages, ten heuristics, visual hierarchy, WCAG 2.2 quick reference. Distilled: [section 3](../references/research/distilled-product-design.md).

## Procedure

1. For each screen in the screen map copy [screen-spec.md](../references/templates/screen-spec.md) to `design/screens/S-<area>-<nn>.md`. Spec every screen in the map; prototype only the key ones.
2. Name the one job and exactly one primary action. A screen with two primary actions is two screens or a hierarchy problem.
3. Set the mode (Operate, Persuade, Read, Experience). Mode comes from the surface, not the product (Impeccable rule, repo guide 01). Most product screens are Operate: scanability beats expression.
4. Write the reading order. Apply the hierarchy limits: no more than three type sizes, at most two large elements, grouping by proximity before borders. Write what should still dominate in a blur test.
5. Write the four states. These rules come from the sources above:
   - **Empty**: say whether it is truly empty (not loading, not failed), teach what the area is for, give the direct action. Never show "no results" before loading finishes.
   - **Loading**: a skeleton that matches the final layout for regions, an inline indicator for actions; mark the region busy and announce through a polite live region (WCAG 4.1.3).
   - **Error**: one row per error kind (validation, network, permission, conflict). Message next to the source, plain and precise, includes the fix, input preserved, no humor, not color alone (WCAG 1.4.1).
   - **Success**: visible confirmation and the next step.
6. Copy uses the IA vocabulary and the patterns in `content-voice.md`.
7. Fill the accessibility notes: heading order, landmarks, focus order, 24 by 24 CSS px targets, contrast, reflow at 320 CSS px, what moves under reduced motion.

## Checks

- Every state named by a flow branch exists in the spec.
- `scripts/check-design-package.py package` reports no missing state headings.
