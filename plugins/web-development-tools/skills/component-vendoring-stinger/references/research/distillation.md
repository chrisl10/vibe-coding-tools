# Dated primary-source digest

Fetched 2026-10-08. The exact URLs, byte hashes and fetch timestamps are in source-index.json. Raw captures are unchanged bytes; each adjacent `.provenance.json` identifies its URL, time, hash and source type. Official website HTTP fetches failed with `HTTP Error 403: Forbidden`; versioned upstream Markdown is the working fallback. Fetch date is freshness of retrieval, not proof of recent publication. Pinned commits are snapshots, not a promise they remain latest.

| Finding | Evidence and consequence |
|---|---|
| shadcn-svelte distributes editable component code; Bits UI is a headless dependency | introduction. Distinguish copied top-layer files from installed dependency updates. |
| Theme uses CSS variables and foreground/background conventions | theming. Map to approved product tokens; defaults do not replace PRODUCT.md or DESIGN.md. |
| CLI init installs dependencies and may overwrite global CSS; add can overwrite files; no-deps-install still changes manifests | CLI. A dry copy plan must list each source, manifest and CSS mutation; no implied installation authority. |
| Registry item separately declares npm dependencies, registry dependencies and file targets | registry schema. Inspect closure before selecting a seemingly small component. |
| The pinned shadcn-svelte root LICENSE grants MIT permissions with retained copyright and permission notice conditions | actual LICENSE. This is exact artifact evidence, not a README label or complete file-level rights review. |
| Bits UI root LICENSE is MIT, but its actual NOTICE identifies modified Adobe Apache 2.0, Melt/Radix/cmdk MIT sources | LICENSE, NOTICE, Adobe utils LICENSE, Adobe stately LICENSE, Melt LICENSE. Blanket MIT-only whole-library claims are unsupported. Preserve notices and route subset/distribution obligations to Software Licensing and qualified counsel. |
| Bits UI package declares 2.19.5, Svelte peer ^5.33.0, Node >=20 and runtime dependencies including Floating UI, runed, svelte-toolbelt, tabbable | package manifest. These declarations are not a resolved target graph or shipped package inventory. Dependency Audit checks actual lockfile, transitives and bundle. |
| shadcn-svelte CLI package declares 1.7.0 | CLI package. A repository commit and CLI package version are different identifiers. |
| Bits UI documents mostly unstyled components and Dialog focus trap, focus return and keyboard behavior | introduction, styling, Dialog. These vendor assertions guide target tests, not an accessibility guarantee after adaptation. |
| Primitive changes have a dedicated upstream changelog | Bits changelog. Review candidate changes independently from local copied wrappers. |

The repository trees and Bits tree qualify inspected source paths and notice search. No shadcn root NOTICE was found in this tree; that does not prove a registry subset, generated output or package tarball has no additional obligations. The button source is archived for provenance research only. Its imports and local variant exports need closure review before copying. This archive does not resolve the actual target dependency graph, sublicense compatibility, contributor rights, screenshots, fonts, icons, trademarks or other assets.

Operational rules in the guides are authored workflow controls derived from these risks. They are not vendor promises. Runtime selection should first reuse existing primitives that already fit, then offer one evidence-backed recommendation. A new library is justified by a specific unmet contract, not novelty.
