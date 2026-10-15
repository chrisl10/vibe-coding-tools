# 05: Write content, voice and the accessibility baseline

Goal: two cross-cutting files every screen and every later PRD obeys.

Grounding: ten heuristics, error messages, empty states, WCAG 2.2 Recommendation, new in 2.2, quick reference, reduced motion. Distilled: [section 6](../references/research/distilled-product-design.md).

## Content and voice

1. Copy [content-voice.md](../references/templates/content-voice.md) to `design/content-voice.md`.
2. Derive three voice traits from the strategy's positioning. Each trait gets a "sounds like" and a "never sounds like" example drawn from this product, not generic SaaS.
3. Fill the message patterns with real examples from the screen specs. When a spec's copy breaks a pattern, fix the spec.
4. List banned words: product-specific false friends plus generic AI marketing words. No em or en dashes in product copy.

## Accessibility baseline

1. Copy [accessibility-baseline.md](../references/templates/accessibility-baseline.md) to `design/accessibility-baseline.md`. Target WCAG 2.2 AA.
2. For each row, say how this package meets it (a token, a layout rule, a flow rule) or list it under known exceptions with a plan.
3. Fill the contrast record from the prototype tokens in BOTH themes once prototypes exist (guide 06). Ratios: 4.5:1 text, 3:1 large text and UI boundaries.
4. State plainly at the top: this is a design-time baseline; conformance needs testing of the built product by its implementation owners.

## Checks

- Every screen spec's accessibility notes are consistent with the baseline.
- No AAA criterion is claimed as required except the reduced-motion house rule, which is labelled as such.
