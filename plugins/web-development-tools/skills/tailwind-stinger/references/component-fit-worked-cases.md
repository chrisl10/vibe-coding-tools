# Worked fit cases

These are declared hypothetical intake cases. No app was built and no accessibility result is asserted. Use [the worksheet](component-fit-intake.md) to replace assumptions with repository evidence.

## Svelte 5 dashboard with dialogs

Inputs: existing SvelteKit/Vite app, Tailwind v4 already present, copied shadcn-svelte dialog, user theme preference. Recommendation: retain Tailwind and the Svelte component variant, with selected Svelte and shadcn-svelte owners implementing behavior. Impeccable handles the actual UI surface. Acceptance remains pending: production CSS, SSR/hydration, theme first render and dialog keyboard/focus tests. React component source is not interchangeable with a Svelte component.

## React app with runtime badge colors

Inputs: React/Vite, class expression `bg-${color}-600`, finite red/green badge states. Recommendation: use a literal map (`red: "bg-red-600", green: "bg-green-600"`) in scanned source. Keep React component work with the React owner; modal and icon work use their owners. Inspect generated CSS and visible error/success contrast in the actual app. Do not claim an application test from the corrected example text.

## Shared package classes missing in production

Inputs: monorepo app importing component code from an ignored dependency. Recommendation: identify the package source path and explicitly register that path relative to the CSS entry with `@source`. Record scan-base evidence; check production output for representative literal classes. A local dev screen alone cannot prove production class coverage.

## Content site with ordinary CSS and no complex controls

Inputs: existing maintainable CSS, plain navigation and content, no requested redesign. Recommendation: retain the existing CSS. Introducing Tailwind or copied primitives needs a requirement and migration justification; framework popularity does not supply one. Impeccable becomes relevant when actual UI changes are requested.

## Vue or Next-specific component request

Inputs: framework-specific rendering requirement and proposed component package. Recommendation: first verify framework compatibility and selected implementation coverage. Tailwind mechanics can be explained here, but this source enhancement supplies no new Vue or Next-specific implementer. Keep implementation unresolved when the required owner is absent.

These judgments derive from source detection, Svelte components, React components, and Bits dialog.
