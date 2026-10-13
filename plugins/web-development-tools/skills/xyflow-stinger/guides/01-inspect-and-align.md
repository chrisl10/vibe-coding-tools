# 01: Inspect and align

Inspect before editing. The goal is an accurate picture of the kit, generation, state model, and risky patterns.

## Run the inspector

Resolve `scripts/inspect-xyflow-project.py` relative to this Stinger's `SKILL.md`, then run it with your tools (it is read-only, uses no network, and writes nothing):

```text
python <stinger-dir>/scripts/inspect-xyflow-project.py <project-root> --pretty
```

Exit 0 means no error or manual-review finding; exit 1 means review is required; exit 2 is a usage error. Every finding carries a `basis` pointing at the distillation row it depends on. After changing the script, run it with `--self-test`.

The inspector is regex-based. Treat its output as leads, then confirm by reading the code.

## Manual checks

| Check | Look for | Source |
|---|---|---|
| Generation | `@xyflow/react` 12 vs `reactflow` 11; `@xyflow/svelte` 1.x vs 0.x | D1, D9 |
| Mixed generations | Old and new packages both installed | D1 |
| Framework floor | React 17 or newer; Svelte 5.25 or newer for Svelte Flow 1.x | D2, D3 |
| Stylesheet | `style.css` or `base.css` imported once, in a global location | D3, D11 |
| Container | Parent of the flow has explicit height | D3 |
| Types registries | `nodeTypes`/`edgeTypes` stable | D7 |
| State | Immutable updates; `$state.raw` in Svelte; narrow subscriptions | D5, D13 |
| Providers | Hooks used outside the flow are under a provider; one provider per flow | D6 |
| Deprecated APIs | `useHandleConnections`, `parentNode`, `onEdgeUpdate`, Svelte stores | D6, D9 |
| SSR | Next.js client boundary; SvelteKit sizes and handles | D12 |
| Attribution | `hideAttribution` usage | D14 |
| Layout libraries | unscoped `dagre`; `elkjs` license | D10 |

## Align versions

1. Keep one xyflow generation per app. Do not add `@xyflow/system` directly; the framework package pins it exactly (D1).
2. Match the framework peer range (D2). If Svelte is below 5.25, upgrade Svelte first (coordinate with `svelte-wasp-drone`).
3. Never adopt `2.0.0-next` or `1.0.0-next` prereleases without an explicit owner decision (D2, G5).
4. Record findings in [templates/inspection-report.md](../templates/inspection-report.md) under the consumer repository's `library/` path.
