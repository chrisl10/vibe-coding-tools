# 02: Map journeys and information architecture

Goal: one journey map per primary actor and goal, then an IA and screen map that every later artifact references by ID.

Grounding: [journey mapping](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-journey-mapping-101.md), [journeys vs flows](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-journeys-vs-flows.md), [IA vs navigation](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/ux--nngroup-ia-vs-navigation.md), [Mermaid flowchart](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/diagram--mermaid-flowchart.md), [Mermaid accessibility](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/diagram--mermaid-accessibility.md). Distilled: [section 2](../references/research/distilled-product-design.md).

## Journeys

1. List actor and goal pairs from the strategy. Usually 2 to 4 journeys cover a first release. One actor per map, always.
2. For each pair copy [journey-map.md](../references/templates/journey-map.md) to `design/journeys/<actor>-<goal>.md` and assign `J-nn`.
3. Fill phases with narrative actions, mindsets in the actor's words and a single emotion line. Do not log screen clicks here; those belong in flows.
4. Mark evidence honestly. If no research backs a pain point, label it "assumption" and add a `Q-nn` with how to verify it (for example a `discovery-research-stinger` interview).
5. End every journey with opportunities that name an owner and a metric, and point each to the flow or screen that will deliver it.

## Information architecture

Copy [ia-screen-map.md](../references/templates/ia-screen-map.md) to `design/information-architecture.md`.

1. Inventory the objects and functions the journeys touch. Record frequency; it drives navigation priority.
2. Group by the user's mental model, not the org chart or the database schema.
3. Write the controlled vocabulary: one term per concept, with the words to avoid. Every later file must use these terms.
4. Draw the screen map in Mermaid with `accTitle` and `accDescr`. Give every screen a stable `S-<area>-<nn>` ID.
5. Only then choose navigation patterns (global, local, utility), each justified by the inventory. Help goes in the same relative place on every screen (WCAG 3.2.6).
6. Select the key screens to prototype: the ones on the critical path of the highest-value journeys, usually 4 to 8.

## Checks before moving on

- Every journey touchpoint points at a screen ID that exists in the screen map.
- No screen exists in the map that no journey or flow needs; if one does, it is a proposal and says so.
- Vocabulary table has no synonyms left unresolved.
