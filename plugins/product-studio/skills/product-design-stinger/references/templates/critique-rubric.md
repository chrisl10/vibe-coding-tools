# Design critique: round {n}, {YYYY-MM-DD}

<!-- Score BEFORE the owner sees anything. Score against the approved direction and the screen's purpose, never against taste. Anchors synthesize research/raw/ux--nngroup-visual-hierarchy.md, ux--nngroup-design-critiques.md, ux--nngroup-empty-states.md, ux--nngroup-error-messages.md, css--mdn-prefers-reduced-motion.md and Impeccable's detector (repo: impeccable-stinger/guides/06-detector-gate.md). The pass bar is a house decision, not an external standard. -->

| Field | Value |
|---|---|
| Scope | {prototype files and screen IDs reviewed} |
| Objectives | {approved direction from direction.md, quoted} |
| Reviewer | {who scored; the author never gives the final score alone when a second reader exists} |
| Viewports checked | 1440 wide desktop and 390 wide mobile, light and dark |
| Detector | `npx impeccable detect design/prototypes/` exit {0, 2, 1, or "not available"} |

## Scale

0 absent or broken. 1 present but works against the user. 2 acceptable with clear problems. 3 good, minor issues. 4 excellent, nothing to fix.

## Scores

| # | Dimension | Score | Evidence (file, element, what you saw) | Fix |
|---|---|---|---|---|
| 1 | Hierarchy | | | |
| 2 | Spacing rhythm | | | |
| 3 | Typography | | | |
| 4 | Color and contrast | | | |
| 5 | Motion restraint | | | |
| 6 | States completeness | | | |
| 7 | Anti-slop | | | |

## Anchors for 2 vs 4

| Dimension | Scores 2 when | Scores 4 when |
|---|---|---|
| Hierarchy | Two or more elements compete in the blur test; more than three type sizes | One clear focal point per screen survives a 10 px blur; reading order matches the spec |
| Spacing rhythm | Ad-hoc gaps; related items not closer than unrelated ones | Every gap is a spacing token; proximity alone explains grouping; containers rare |
| Typography | Long lines over about 80 characters, tight leading, tiny UI text | Comfortable measure, clear scale steps, weights do the work instead of color |
| Color and contrast | Any text under 4.5:1 or UI boundary under 3:1 in either theme; color is the only signal | Both themes pass; accent used for meaning only; states use shape or text as well as color |
| Motion restraint | Decorative or looping motion; nothing changes under reduced motion | Motion only explains a change; under 300 ms for UI; reduced motion removes scale and pan |
| States completeness | One or more of empty, loading, error, success missing or generic | Every key screen shows all four with specific copy, preserved input and a next step |
| Anti-slop | Detector findings unresolved, or visible AI tells (gradient text, eyebrow chips, glow halos, generic "Unlock your potential" copy) | Detector exit 0 or every finding waived with a narrow written reason; copy sounds like this product |

## Accessibility blockers (pass or fail, not scored)

| Check | Result | Evidence |
|---|---|---|
| Text contrast 4.5:1, large text 3:1, both themes (1.4.3) | | |
| UI boundary and state contrast 3:1 (1.4.11) | | |
| Visible focus that nothing covers (2.4.7, 2.4.11) | | |
| Targets at least 24 by 24 CSS px (2.5.8) | | |
| Works at 320 CSS px wide (1.4.10) | | |
| Every drag has a single-pointer alternative (2.5.7) | | |
| Reduced motion honored | | |

## Gate

Show the owner only when all are true:

- Every dimension scores 3 or 4.
- No accessibility blocker fails.
- Detector exit 0, or each finding has a narrow written waiver, or the detector is unavailable and that is stated.

Bounded rounds: at most two fix rounds. If round 2 still misses the bar, show the owner anyway with the honest scores and the open fixes listed. Never inflate a score to pass.

## Owner-facing summary

{Three sentences: what changed since last round, the weakest dimension and why, what we want the owner to decide.}
