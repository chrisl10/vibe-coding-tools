Most deterministic scripts for this plugin live in the shared `shared/scripts/` folder at the plugin root, per the build plan's "shared where the use case is genuinely shared" instruction. See that folder's README for the full centrally-planned list.

Core Web Vitals collection is a Drone step, not a script: follow `guides/01-audit-procedure.md` step 3. The planned shared `shared/scripts/cwv-collect.py` was never implemented; it exits with status 2 and points back to that step.

This folder carries one local script specific to this pair's own scope, the caching and CDN half of this Stinger's audit:

| Script | Purpose |
|---|---|
| `cdn-header-scan.py` | Read-only HTTP header capture (`Cache-Control`, `CDN-Cache-Control`, `Server`, and other CDN-identifying headers) against a sampled page set. Mechanical capture only, it does not judge caching-strategy adequacy, that judgment is out of scope pending a dedicated research pass, per `references/research/distilled-performance-cwv.md` section 7 and `references/templates/cdn-header-checklist.md`. |

Do not extend `cdn-header-scan.py` to render a "good vs bad caching strategy" verdict from general knowledge. Per this Stinger's own research gap note, no primary source in this archive documents caching-strategy audit methodology; a dedicated research pass is required first.
