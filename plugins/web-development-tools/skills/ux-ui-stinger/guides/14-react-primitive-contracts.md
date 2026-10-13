# 14 - Qualify React primitives inside the product system

Grounding: [C01-C05 and conflicts](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/web-development-tools/skills/ux-ui-stinger/references/research/2026-10-07-flow-contracts/digest.md). This is component-contract guidance. Actual UI implementation, redesign or refinement uses the selected Impeccable owner and its PRODUCT.md, DESIGN.md and surface brief.

## Intake before prescribing a primitive

Read the supplied design-system folder and its governing section. Also read PRODUCT.md, DESIGN.md and the affected surface brief when present. Record exact paths, dates/revisions and unresolved conflicts in [the intake worksheet](../templates/product-system-intake.md). A missing folder is an unknown, not permission to create a brand. Coherent existing code can provide observed invariants for owner confirmation; framework defaults alone do not supply product direction. An uncovered minor contract can be proposed within the current system; foundational changes route to design-system-wasp-drone and actual design work to Impeccable.

Identify user task, success state, surrounding layout, framework/runtime, current copied component source and installed versions. Resolve the selected owner and availability before handoff. Do not silently substitute Base UI for Radix, React for Svelte, or a newly generated component for maintained source.

## Record three distinct contracts

1. **Product system:** token/utility names, approved variants, existing wrapper imports, motion/reduced-motion policy, dark/tenant/RTL behavior and governing sections. Unknown values stay unknown.
2. **Primitive behavior:** actual family and imports, semantic root, focus/ref/event propagation, controlled/uncontrolled contract, default state, keyboard model and overlay composition. Radix asChild applies only to Radix parts that support it. React19 ref props and legacy forwardRef can both preserve the ref contract depending on installed source and types.
3. **Copied-source maintenance:** upstream URL/ref, captured source hash, local file hash, retained license/notice, local delta and reason, dependency versions, last reviewed upstream changes, maintainer and upgrade characterization. Never re-run a generator over modified files as an assumed safe update. Prepare a reviewable diff; installation/update needs the task's authorization.

Use [primitive acceptance](../templates/primitive-acceptance-contract.md). A wrapper earns its place by mapping the product vocabulary, tokens or behavior. Product-owned copied source may itself be the designated wrapper seam when the system says so; this still preserves the feature-import contract. Upstream defaults do not establish the product's aesthetic.

## Review behavior, then the product delta

Inspect default, hover, keyboard focus, disabled, loading, empty, error, success and overflow states that apply. Use explicit N/A reasons, not missing rows. Confirm accessible name, label/error relationships, semantic button/link choice, focus-visible style, event composition and ref access. Ensure loading prevents duplicate work without concealing status. Document how errors recover and whether input survives dismissal/navigation.

For modal dialogs, review initial focus, tab containment, Escape, visible close/cancel, accessible name, outside inertness and return to the invoker or a documented logical successor. Avoid nested interactive controls produced by incorrect composition. Match the actual APG pattern, not a generic checklist imposed on every widget. Source: [APG](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/web-development-tools/skills/ux-ui-stinger/references/research/2026-10-07-flow-contracts/raw/wai-modal-dialog.html), [Radix](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/web-development-tools/skills/ux-ui-stinger/references/research/2026-10-07-flow-contracts/raw/radix-composition.html).

## Acceptance and handoff

Report code path/line, governing section, token-named delta and evidence status. Require existing build/type checks plus relevant interaction tests and manual keyboard/assistive-technology/device review for changed behavior. Record actual command, version, source revision, result and artifact path. Automated name/role checks do not prove focus order, task usability or all accessibility criteria. Never mark passing from a filled worksheet or from the library's reputation.

[Worked source cases](../examples/primitive-and-mobile-flow-cases.md) show missing context and known review failures without inventing a product surface. Parent Security, Quality and repository gates remain separate.
