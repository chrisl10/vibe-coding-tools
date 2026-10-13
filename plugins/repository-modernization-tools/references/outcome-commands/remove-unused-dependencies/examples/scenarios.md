# Synthetic workflow cases

These are authored decision exercises, not scanner runs or real application build evidence. Names beginning `fixture-` are invented.

## Dynamic and build usage refuses removal

A synthetic scanner report flags `fixture-adapter` and `fixture-build-cli`. A loader computes `await import(adapterName)` and a workspace build script invokes `fixture-build-cli`. The operator's full search reads the loader mapping and package scripts. Both remain. The report records configuration coverage and entry gaps; it does not treat no static import as absence. Removing either requires a separately approved replacement feature and is outside this behavior-preserving command.

## Scope refusal

User approval covers `fixture-unused` in `apps/site/package.json` and its shared lockfile. A proposed `pnpm remove -r fixture-unused` would affect additional workspaces. Stop before execution and prepare the bounded workspace proposal. Approval of an audit or a package name without exact mutation scope is insufficient; no package is removed.

## Narrow before/after proposal, proof still required

Synthetic before declaration: `{"dependencies":{"fixture-used":"1.0.0","fixture-unused":"1.0.0"}}`. Proposed after: `{"dependencies":{"fixture-used":"1.0.0"}}`. Only the approved package declaration and manager-generated lockfile closure are in scope. The worksheet requires baseline and candidate import resolution, consumer entrypoints, tests and build outputs under matched environments. Their status here is **not run**. A frozen install could prove manifest/lockfile consistency but would not prove the imports, build or public package contract. Do not close the outcome for an application until the selected implementer produces these observations and the final gates pass.

## Published peer contract

A peer appears unused by private source imports but forms a public consumer contract. Retain it until actual exported types/runtime adapters and supported consumer combinations are checked. If removal breaks the accepted contract, stop and request a separately approved compatibility/version decision; no automatic major release or publication.
