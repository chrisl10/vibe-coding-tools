# react-stinger

Cursor skill that equips **react-wasp-drone** to be the Wasp Nest's authority on bleeding-edge React architecture, patterns, and code quality for 2025-2026. Encodes the bulletproof-react architectural pillars, the awesome-react curated ecosystem, and React 19/Compiler idioms into guides, examples, templates, and scanning scripts.

Entry point: `SKILL.md`.

## Scope

- **Owns:** project structure, component composition, state management, data layer, error boundaries + Suspense, forms, performance, testing strategy, TypeScript patterns, React 19 idioms, Server Components, anti-patterns, ecosystem selection.
- **Does not own:** visual design (ux-ui-svelte-wasp-drone), SEO / Next.js metadata (seo-aeo-wasp-drone), security audits (security-wasp-drone), PRD authoring (library-wasp-drone), post-refactor QA (quality-wasp-drone).

## Layout

```
react-stinger/
  SKILL.md              Navigation + hard rules
  guides/               14 numbered guides (principles -> ecosystem catalog)
  examples/             ADR, code review, refactor proposal
  templates/            ADR, project-structure, provider-stack, error-boundary, test-setup, eslint config, review-output template
  scripts/              scan-anti-patterns, bundle-budget-check, react-version-audit
  research/ (source-repository research, not shipped with the plugin)             Dated research notes + react-version-log
```

## Output convention

Reports are written into the host repo's `library/` tree, never into this Stinger:

- **Standalone reviews** → `library/requirements/reports/react/<date>-<topic>.md`
- **Feature-tied** → `library/requirements/<lifecycle>/fea-<###>-<title>/reports/<date>-<type>-report.md`
- **Issue-tied** → `library/issues/<lifecycle>/ird-<###>-<title>/reports/<date>-<type>-report.md`

## Outcome procedures

- [React/Vite with a separate backend](guides/21-react-vite-separate-backend.md)
- [Split a component and preserve behavior](guides/22-split-a-component-preserve-behavior.md)
- [Measure emitted bundle weight](guides/23-measure-bundle-weight.md)
- [Simplify state without races](guides/24-simplify-state-without-races.md)

[Worked records](examples/outcome-modernization.md), official-source archive and digest.
