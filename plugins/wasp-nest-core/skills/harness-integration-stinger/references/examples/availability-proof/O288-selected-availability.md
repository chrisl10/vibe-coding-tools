# O288 rendered cases

## Cached docs pack, Core-only selection

Synthetic setup: a documentation package exists beside Core, but the explicit registry selects only Core. Request `library-packets-stinger`.
Expected existing resolver refusal: `required plugin is not installed: documentation-tools`.
Conclusion: source/catalog coverage exists; installed optional selection is refused. No scan or activation of the cached sibling occurs. Native discovery and execution: UNEXECUTED.

## Selected owner, missing workflow prerequisite

Synthetic registry includes Core and documentation. `library-packets-stinger` resolves to documentation. Request `kb-refresh-stinger` with workflow `kb-refresh full repository discovery`; code-audit owner is missing.
Expected refusal: `required plugin is not installed: code-audit-tools`.
After selecting the synthetic dependency, checked owners include code-audit. Conclusion: helper accepts explicit selection; native availability still UNKNOWN. Source of scenario: existing InstalledRegistryTests, not a real account/host probe.

## Manifest version mismatch

Synthetic documentation manifest says `wrong` instead of the catalog version.
Expected refusal: `installed plugin version differs from Core: documentation-tools`.
Do not substitute a current cached version or auto-update. Record refusal and prepare source-only work if authorized.
