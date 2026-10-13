# Guide 02: Map the features into PRDs

Goal: a PRD Map that lists every PRD to write, one row each, with a one-line scope, a size, and its dependencies. You do not write the PRDs. `library-stinger` does that.

Template: [../references/templates/prd-map.md](../references/templates/prd-map.md). Example: [../references/examples/example-prd-map.md](../references/examples/example-prd-map.md).

## Steps

1. **List the slices.** Walk the journeys step by step. For each step, ask "what has to exist so a user can do this?" Group the answers into slices that can be built, checked and finished on their own. Name each slice by what it delivers ("Book a slot"), not by a layer or a team ("Backend work"). [Shape Up scopes](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/shape-up-map-the-scopes.md)
2. **Give each slice a key** (`F01`, `F02`, ...). Keys never change once the map is approved. Library adds the real `PRD-###` numbers later.
3. **Write the one-line scope.** One sentence: who can do what, and the limit. If you need "and also" twice, it is probably two PRDs.
4. **Set a size budget.** S (a few days), M (about a week), L (about two weeks). Anything larger gets split or narrowed. A size is a budget the PRD must fit, not a promise. [Shape Up appetite](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/shape-up-setting-boundaries.md) For a real time forecast, hand off to `estimation-stinger`.
5. **Split bad slices.** Split a slice when its "done" is hard to say, its name is generic ("misc", "improvements"), or one side (screen or server) is much bigger than the other. [Shape Up scopes](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/shape-up-map-the-scopes.md)
6. **Write dependencies.** In "Depends on", list the keys this PRD cannot finish without. Only real end-to-start needs count: "needs F01's data to exist". Wanting to build things in a nice order is not a dependency. [GitHub](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/github-issue-dependencies.md) [Linear](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/linear-project-dependencies.md)
7. **Rate risk.** High means big unknowns (new tech, unclear rules, outside services). Risk decides order later.
8. **Flag nice-to-haves.** `Yes` only if the main journey still works without it. [Shape Up](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-planning-stinger/references/research/raw/shape-up-show-progress.md)
9. **Fill the journey coverage table.** Every journey step must point to at least one key. Any step with no key is a gap: add a PRD or list it under Gaps.
10. **List shared boundaries** using [Guide 03](03-flag-boundaries.md).

## Checks before you show the owner

- [ ] Every row has a key, title, scope, size, depends on, risk and nice-to-have.
- [ ] No row is larger than L.
- [ ] Every journey step is covered or listed as a gap.
- [ ] Nothing from "out of scope" in the strategy sneaked back in.
- [ ] No two PRDs depend on each other (that is a cycle; merge them or pull out a shared boundary).

Then follow [Guide 07](07-approve-and-revise.md) to get approval.
