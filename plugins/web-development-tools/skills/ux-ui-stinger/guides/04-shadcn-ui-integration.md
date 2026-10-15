# 04 — shadcn/ui Integration

shadcn/ui distributes editable component source. Copied components may still import package dependencies. Inspect the actual source family, imports and pinned versions before adopting Radix-specific composition instructions; current official documentation includes Radix and Base UI dialog families. Product wrappers and tokens are this skill's policy, not an upstream requirement. Record source provenance and upgrade deltas using `guides/14-react-primitive-contracts.md`.

Research: `research/2026-04-24-shadcn-ui-wrapping.md` (source-repository research, not shipped).

## Decision tree

When a UI need arises:

```
Does an existing product wrapper cover it?
├── Yes → use the product wrapper. Done.
└── No
    ├── Is shadcn's primitive a close fit?
    │   ├── Yes → inspect selected source/provenance, then prepare the product contract; copy/install only within authorized scope
    │   └── No → is Mantine a close fit?
    │       ├── Yes → see `guides/05-mantine-integration.md`
    │       └── No → build system-native. Cite the brief section that declares the aesthetic.
```

**Never** pick a library primitive because "it's there" — pick it because the product needs an accessible primitive with behavior the team will not re-implement well (dialog, dropdown, popover, tabs, combobox, date picker, etc.).

## Folder discipline

```
components/
├── ui/                         <- shadcn CLI-generated. Treat as read-mostly.
│   ├── button.tsx
│   ├── dialog.tsx
│   └── ...
└── <product>/                  <- your wrappers live here.
    ├── Button.tsx              <- wraps ui/button with product variants + tokens
    ├── Dialog.tsx              <- wraps ui/dialog with product motion + shadow
    └── ...
```

Feature code imports `@/components/<product>/Button`, never `@/components/ui/button`. Enforce via code review or an ESLint `no-restricted-imports` rule.

## Wrapping rules

1. **Preserve ref and props behavior.** Radix composition requires the underlying node to receive its ref and passed props/event handlers. React 19 can accept ref as a prop; older-compatible wrappers may use `forwardRef`. Choose syntax from the installed React/primitive/types, and test behavior rather than mandate one syntax. See current C03-C04.

2. **Use CVA for variants.** Export a `<component>Variants` CVA factory. Match shadcn's convention so upstream updates re-merge cleanly. See `research/2026-04-24-cva-variant-architecture.md` (source-repository research, not shipped).

3. **Map to product tokens via Tailwind v4 `@theme`.** shadcn's default Tailwind config uses CSS variables for every color — point those at product tokens in `globals.css`:

   ```css
   @theme {
     --color-primary: var(--color-brand);
     --color-primary-foreground: var(--color-brand-ink);
     --color-secondary: var(--color-surface-secondary);
     /* ... */
   }
   ```

   The shadcn primitive keeps its `bg-primary text-primary-foreground` classes; the tokens resolve to product values. See `research/2026-04-24-tailwind-v4-theme-tokens.md` (source-repository research, not shipped).

4. **For selected Radix parts supporting `asChild`, compose with it** when placing a product button inside a Radix Trigger, Menu Item, or similar:

   ```tsx
   <DropdownMenu.Trigger asChild>
     <Button variant="secondary">Open</Button>
   </DropdownMenu.Trigger>
   ```

   This requires `<Button>` to preserve ref and passed props on the correct semantic node. It is not a universal recipe for every shadcn source family. See `guides/14-react-primitive-contracts.md`.

5. **Product variants, not shadcn variants.** shadcn's `variant="destructive"` is shadcn's opinion; your product's opinion might be `tone="danger"` or simply "don't expose a destructive variant". The wrapper translates: accept product-shaped props, emit shadcn-shaped classes.

6. **Keep `components/ui/*` edit-minimal.** Re-running the CLI must not blow up the wrappers. If you need a behavior change that requires editing `components/ui/button.tsx`, ask: could the wrapper express it? Usually yes.

## When to wrap vs. edit the primitive

- **Wrap** when the change is about variants, tokens, motion, composed behavior, or product-specific props. This is 90% of cases.
- **Edit the primitive** when the shadcn source has an upstream bug you're fixing for the product, or when a product-wide contract (like "every button must track analytics") is cleaner inline than in every wrapper.
- **Reject the primitive** when the product aesthetic materially conflicts with shadcn's composition model. Build system-native.

## Common violations

- Feature code imports `@/components/ui/*` directly. → Fix: import from `@/components/<product>/*`.
- Wrapper drops the ref contract. → Fix: restore compatible ref propagation to the underlying node and exercise selected primitive composition.
- Wrapper hard-codes Tailwind colors instead of referencing product token variables. → Fix: map in `@theme`.
- Product exposes shadcn's `destructive` variant when the brief doesn't authorize it. → Fix: remove variant from the wrapper's CVA.

---

*Worked example:* `examples/wrapper-spec-example.md` — a Button wrapper over a shadcn primitive.

*Template:* `templates/component-wrapper.tsx`.
