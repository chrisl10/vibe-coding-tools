# 01: Read the strategy and set the direction (Gate A)

Goal: turn the Product Strategy into design inputs and get the owner to pick one direction before any high-fidelity work.

Grounding: [prototype fidelity](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-prototype-fidelity.md), [critique needs agreed objectives](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-design-critiques.md), Impeccable context contract (repo: `packs/web-development-tools/skills/impeccable-stinger/guides/01-context-contract.md`).

## 1. Preconditions

1. Open `library/knowledge/private/product/product-strategy.md`. If it is missing, stop. Tell the owner the strategy stage comes first (`product-strategy-stinger`). Do not invent one.
2. Look for existing design authority, in this order, and read what exists:
   - repo-root `PRODUCT.md` and `DESIGN.md` (Impeccable context contract)
   - a design-system folder (`library/knowledge/private/<product>-ux-ui/` or `library/knowledge-base/<product>-ux-ui/`)
   - a running app's webapp-capture inventory (`library/design/` or the capture config's output)
   - an existing `library/knowledge/private/product/design/` package (resume it; never start over silently)
3. A coherent existing UI is authority even without `DESIGN.md`. Record its invariants instead of redesigning by accident (Impeccable rule, repo guide 01).

## 2. Extract design inputs

Write these into the top of `design/direction.md`, quoting the strategy section for each:

| Input | Where it usually lives in the strategy |
|---|---|
| Primary actor and secondary actors | target customer or ICP section |
| Core job and the moment of first value | problem, value proposition |
| Top 3 to 5 tasks | jobs, use cases, scope |
| Platforms and contexts (desktop, mobile, field use) | constraints |
| Brand commitments and tone | positioning |
| Non-goals | scope |
| Success metrics the design must move | metrics |

Anything the strategy does not say becomes an open question `Q-nn`, not an assumption. Ask the owner only the questions that block direction; batch them.

## 3. Draft direction options

Use [direction-options.md](../references/templates/direction-options.md). Write 2 or 3 options that differ in substance (density, pace, type character, how color carries meaning, depth), not three shades of the same idea. Each option gets a rough static frame: a low-fidelity HTML sketch or a single screen from the prototype starter with placeholder content. Keep frames rough on purpose so the owner judges the idea, not the polish (fidelity source above).

If Impeccable is installed, write the recommended option as an Impeccable direction contract (repo: `impeccable-stinger/templates/direction-contract.md`) so the later implementation reads the same words.

## 4. Gate A: owner approval

Present the options with a recommendation tied to strategy evidence. Ask for one decision. Record it in the decision table of `direction.md` and in the README approvals log (template: [design-package-readme.md](../references/templates/design-package-readme.md)).

No prototypes are built until Gate A is recorded. If the owner says "you choose", record that delegation verbatim with the date; that counts as approval of the recommendation.

## Output

- `design/README.md` created from the template, status `draft`
- `design/direction.md` with inputs, options, recommendation and the recorded decision
