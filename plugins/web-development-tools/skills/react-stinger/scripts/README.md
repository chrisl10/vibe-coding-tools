# Scripts

Three TypeScript tools react-stinger can invoke on a codebase. The anti-pattern and version tools retain their documented stub scope. The bundle helper now measures explicit Vite manifests. Use a compatible existing runtime; no installation is implied.

## `scan-anti-patterns.ts`

AST scan for the first 8 anti-patterns in `guides/12-anti-patterns.md`. Emits a markdown report; exit code = number of must-fix findings.

```bash
pnpm tsx .claude/skills/react-stinger/scripts/scan-anti-patterns.ts src/
```

Dependencies: `ts-morph`.

## `bundle-budget-check.ts`

Measures an explicit Vite manifest entry's deduplicated static JavaScript graph. Dynamic entries are listed separately. It no longer assigns routes from filenames.

```bash
node <skill>/scripts/bundle-budget-check.ts dist dist/.vite/manifest.json src/main.tsx 180
```

Requires a Node version with native TypeScript stripping or an already installed TS runner. Positional BUILD_DIR remains; MANIFEST and ENTRY now distinguish verified measurement. Old BUILD_DIR-only use exits2 UNVERIFIED. Optional positive budget is KiB gzip, level9; no budget reports MEASURED_NO_BUDGET. Next.js output, CSS/media and transfer/timing evidence require separate tools. See [measurement procedure](../guides/23-measure-bundle-weight.md).

## `react-version-audit.ts`

Reads `package.json` and reports React version, Compiler readiness, deprecated dependencies, and which version-specific idioms apply.

```bash
pnpm tsx .claude/skills/react-stinger/scripts/react-version-audit.ts
```

Run this **first** on any invocation: the output tells you which guides are relevant for the stack.

## Adapting

These are stubs. Expected to be extended per project:

- Add detectors for anti-patterns #4-12 in `scan-anti-patterns.ts`.
- Next.js first-load accounting is outside the Vite manifest measurement mode.
- Extend `react-version-audit.ts` with framework-specific checks (Next.js pages-vs-app, Remix loader presence).
