# 10: Hand off to planning, the design system and enforcement

Goal: close the package so sibling and downstream owners can act on it without re-reading the whole folder.

Grounding: repo owners named in the locked topic ([topic.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/topic.md)); design-system bootstrap scope (repo: `packs/web-development-tools/skills/design-system-stinger/SKILL.md`); enforcement scope (repo: `packs/web-development-tools/skills/ux-ui-stinger/SKILL.md`); Impeccable implementation routing (repo: `src/skills/pest-controller-suit/SKILL.md`, "Frontend design / UI implementation").

Precondition: Gate B is recorded, or the owner explicitly asked for a handoff of a draft (record that).

## 1. Planning handoff (product-planning-stinger)

Copy [planning-handoff.md](../references/templates/planning-handoff.md) to `design/planning-handoff.md`.

- One row per screen and per flow, by ID, with states specified, prototype yes or no, a rough size (S, M, L) and dependencies.
- Suggest PRD groupings by shared data and journey phase. Do not write PRDs; product-planning-stinger builds the PRD map and wave plan, and `library-stinger` writes PRDs.
- List the open questions that block planning.

## 2. Design system (design-system-stinger)

Hand off when no design system exists and the product will be built:

- the approved direction (`direction.md`), the prototype `:root` token block, any accepted Claude Design token or DESIGN.md proposals, the screen specs, and the accessibility baseline.
- design-system-stinger interviews and bootstraps the durable system. The prototype tokens are input evidence, not the system.

## 3. Enforcement (ux-ui-stinger or ux-ui-svelte-stinger)

Hand off when a design system exists: screen specs and any token change requests. Use `ux-ui-stinger` for React products and `ux-ui-svelte-stinger` for SvelteKit products. System-level changes they escalate back to design-system-stinger.

## 4. Implementation (impeccable-stinger)

Impeccable is the single router for UI implementation. Give it the approved direction (as a direction contract when possible), the screen specs as surface briefs, and the prototypes as visual references. This skill does not write production components.

## 5. Close the package

- README status table updated; status `owner-approved` only with a Gate B record.
- `python3 scripts/check-design-package.py package <design-dir>` exits 0.
- Report to the orchestrator: files written, Gate A and B records, critique scores, detector result, open questions, and the handoffs made. Then the Ship Gate applies before any commit.
