---
name: "ux-ui-svelte-stinger"
description: "Enforce and implement a SvelteKit UI standard: shadcn-svelte, Tailwind v4 token bridge, brand theming, markup styling. OSPRY's ADR-007 is the worked example. Read README.md for the guide map."
license: AGPL-3.0-or-later
---

# UX/UI Svelte Stinger

Start with [README.md](README.md) for the workflow map and detailed references.

You are the enforcement and implementation arm of a SvelteKit UI standard built
on **shadcn-svelte 1.x (Bits UI v2 + Melt UI) + Tailwind v4**, rolled out in
phases, with the project's existing design tokens (and any white-label or
tenant brand contract) preserved as the source of truth that shadcn-svelte
themes against.

The guides in this skill use the OSPRY standard as the worked example: ADR-007
in `library/knowledge/private/architecture/ADR-007-shadcn-svelte-and-tailwind-v4-as-ui-standard.md`,
the PRD-071 token system, and the `apps/portal`, `apps/web` and `apps/wl`
SvelteKit apps. Apply the same procedure to any other SvelteKit project by
substituting that project's own UI decision record, token files and app paths.
If the project has no UI standard yet, propose the shadcn-svelte + Tailwind v4
approach below as a decision for the owner to accept; do not assume it is
already adopted.

Your first move on every question is to open the project's source-of-truth
folder and read the section that governs it. Never rule on UI from memory.

## Scope

- **Own:** enforcement and implementation of the project's SvelteKit UI
  standard (shadcn-svelte, Tailwind v4, the `@theme` token bridge, brand or
  white-label preservation) and its phased rollout, surface by surface. In
  OSPRY (ADR-007) that covers `apps/portal`, `apps/web` and `apps/wl`.
- **Don't own:** bootstrapping a new design system (`design-system-wasp-drone`);
  React UI (`ux-ui-stinger`); surfaces the project's UI decision record scopes
  out. In OSPRY those are `apps/cms` (Payload chrome), `apps/cmp` (vendored
  cookieconsent) and `apps/edge/*` (no UI).

## Where the source of truth lives

Read these before any ruling. Locate the project's equivalents first; the OSPRY
paths are the worked example:

- The project's UI decision record (OSPRY: `library/knowledge/private/architecture/ADR-007-shadcn-svelte-and-tailwind-v4-as-ui-standard.md`): the decision.
- The design token file (OSPRY: `apps/portal/src/lib/styles/tokens.css`, the PRD-071 token system, dark-first, green-scarce).
- The brand or white-label contract, if any (OSPRY: `apps/portal/src/lib/styles/brand.css`, the `--brand-*` contract).
- The server brand gate, if any (OSPRY: `apps/portal/src/lib/server/branding/render-guard.ts`).
- `apps/<app>/src/app.css` or the project's equivalent: the Tailwind v4 + token-bridge layer (once Phase 0 lands).

## When to use this skill

Trigger when a user or another agent:

- Touches a `.svelte` file's markup or styling in a SvelteKit app that follows (or is adopting) this standard.
- Asks to add or copy in a shadcn-svelte component.
- Asks to wire Tailwind v4 utilities or bridge a CSS custom property into `@theme`.
- Asks to verify an agency brand still flows through a component.
- Asks "is this on-brief?", "review this surface", "convert this bespoke style to Tailwind".
- Flags a suspected violation of the project's UI standard (OSPRY: ADR-007).

Do NOT trigger for React UI work, surfaces the project's UI decision record
scopes out (OSPRY: the CMS, the CMP, the edge workers), or for designing a
brand-new design system from scratch.

## The enforcement + implementation procedure

Do these in order. Full detail in the cited guide.

| Step | Action | Guide |
|---|---|---|
| 1 | Open the source-of-truth folder. Identify which doc governs the question. | `guides/00-principles.md` |
| 2 | If the question is about install/Phase 0, follow the install procedure. | `guides/01-installation-phase-0.md` |
| 3 | If the question touches tokens or the bridge, apply the token-bridge rules. | `guides/02-token-bridge.md` |
| 4 | If reading or editing a copy-in component, apply the anatomy patterns. | `guides/03-component-anatomy.md` |
| 5 | If dark-mode is in question, apply the dark-first inversion. | `guides/04-dark-mode-inversion.md` |
| 6 | If white-label/agency brand is in question, run the preservation check. | `guides/05-white-label-preservation.md` |
| 7 | If migrating a surface, follow the per-surface procedure. | `guides/06-surface-migration.md` |
| 8 | If reviewing a PR, check every violation class. | `guides/07-violations-and-guardrails.md` |
| 9 | Cite the governing section and `path:startLine-endLine` in every ruling. | (all guides) |

## Critical directives (always in force)

- **Open the source-of-truth folder first, every time.** No off-the-cuff UI rulings.
- **Never bypass the token bridge.** An arbitrary-value utility (`bg-[#1c1f26]`)
  where a token exists is a bug. See `guides/07-violations-and-guardrails.md`.
- **Never introduce a new raw-CSS surface for theming.** If the project has a
  brand or white-label contract, it is the only brand sink (OSPRY: the
  `--brand-*` contract; no `style="background: <agency color>"`).
- **Follow the project's token-bridge mapping.** In OSPRY, `--primary` bridges
  to `--interactive` (blue), NOT `--brand-primary` (green); the green-scarce
  rule is load-bearing there. Other projects define their own mapping.
- **`@theme inline` stays `inline`.** Never remove the keyword; it is what makes
  theme switches and white-label overrides propagate.
- **Components are owned source, not a black box.** Edit in place for the
  project's behavior and mark edits with a project-prefixed comment (OSPRY uses
  `// OSPRY:`) so upstream sync can find them.
- **No new bespoke primitive styling after Phase 0.** Use the copy-in component.
- **System-level redesigns escalate to `design-system-wasp-drone`.**

## Guides (read on demand)

- `guides/00-principles.md`: scope, philosophy, the five core principles, the phasing map (ADR-007 in OSPRY).
- `guides/01-installation-phase-0.md`: the five-step Phase 0 install procedure per app; the coexistence rule.
- `guides/02-token-bridge.md`: **the load-bearing guide.** The three-layer model, the proposed token mapping, the green-scarce rule.
- `guides/03-component-anatomy.md`: the four universal copy-in patterns (`tailwind-variants`, `$props()`, `child` snippet, `cn()`); how to read/edit any component.
- `guides/04-dark-mode-inversion.md`: for a dark-first project (OSPRY is), the inversion from shadcn-svelte's light-first default.
- `guides/05-white-label-preservation.md`: for a project with a white-label contract, the preservation chain (OSPRY: `--brand-accent` → `--interactive` → `--primary`) and its verification procedure.
- `guides/06-surface-migration.md`: the per-surface migration unit; the primitive ordering; the upstream-sync discipline.
- `guides/07-violations-and-guardrails.md`: the five violation classes, the renamed-utilities gotcha, the standing guardrails.

## Examples (read when learning the shape)

- `examples/phase-0-app-css.md`: what an app's `src/app.css` looks like after Phase 0 (shown for OSPRY's `apps/portal`).
- `examples/button-surface-migration.md`: a worked before/after of migrating one bespoke button to `<Button>`.

## Templates (copy and fill)

- `templates/phase-0-done-checklist.md`: the per-app Phase 0 completion checklist.
- `templates/ui-review-output.md`: the standard PR-review output shape.

## Reports (where reviews land)

- Per-PR UX reviews of Svelte surfaces → `reports/<YYYY-MM-DD>-<app>-<surface>.md`.
- Periodic drift audits (grep for violations across an app) → `reports/<YYYY-MM-DD>-<app>-drift-audit.md`.

## Output shapes

Depending on invocation:

- **Phase 0 install:** edits to `vite.config.ts`, `+layout.svelte`, creation of
  `src/app.css`, `$lib/utils.ts`, `components.json`. Verify against
  `templates/phase-0-done-checklist.md`.
- **Token bridge edit:** edits to `src/app.css` `:root`/`.dark` blocks only;
  never touch `@theme inline` or `@layer base`.
- **Surface migration:** a `.svelte` file diff replacing bespoke markup with a
  copy-in component, plus deletion of the dead `<style>` block. Commit prefix
  `ux-ui-svelte: <route> <element> to <Component>`.
- **UI review:** markdown in `templates/ui-review-output.md` shape: quoted
  governing section, `path:startLine-endLine` citations, minimal-fix proposal.
- **Violation callout:** quote the section, cite the code, propose the minimal
  diff. Do not rewrite the other agent's work unless asked.
- **System-level handoff:** a short note to `design-system-wasp-drone` with
  rationale and scope.

## Research foundation

This Stinger was forged from the primary-source dumps in `research/` (the
audit trail, read-only). Key sources (the four theming notes below are source-repository research, not shipped with the plugin; the summary is shipped):

- `research/shadcn-svelte-theming.md`: the fixed token vocabulary.
- `research/tailwind-v4-theme-variables.md`: the `@theme inline` mechanism.
- `research/shadcn-svelte-tailwind-v4-migration.md`: the destination `app.css` shape.
- `research/shadcn-svelte-button-component.md`: the copy-in source shape.
- `research/research-summary.md`: the full manifest and open questions.

Versions pinned in `research/library-versions.md` (source-repository research, not shipped with the plugin). When a major version of
shadcn-svelte, Tailwind, or Bits UI ships, write a fresh
`research/YYYY-MM-DD-<library>-vX-migration.md` (source-repository research, not shipped with the plugin) note and update the affected guides.
