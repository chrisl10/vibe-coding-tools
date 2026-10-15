# Measure emitted bundle weight

Treat before/after output as the result, not dependency declarations or filename guesses. Grounding

1. Record commit/tree identity, lockfile, build command, mode, target, relevant env names without values and runtime versions. Run the existing production build with its normal configuration. No install or configuration change is implied by this skill.
2. Obtain the actual Vite manifest when already emitted. The standard enabled manifest is `.vite/manifest.json`; a custom manifest path can differ. Map the selected manifest entry and static imports, deduplicate shared assets, and list dynamic entries separately. If missing, request a reviewed manifest configuration change or inspect an existing analyzer; do not infer routes from hashes.
3. Reuse [bundle-budget-check.ts](../scripts/bundle-budget-check.ts): `node <skill>/scripts/bundle-budget-check.ts <build-dir> <manifest-path> <entry-key> [budget-KiB]` on a Node version with native TypeScript stripping, or an already installed TS runner. It measures only emitted static JavaScript. It rejects unsupported/malformed inputs; exit2 is UNVERIFIED, exit1 means measured budget exceeded, exit0 without a budget means measured without a budget verdict.
4. Save per-asset raw bytes and fixed gzip level9 bytes, static total, dynamic-entry list and scope exclusions. Compare same build conditions. Count CSS/fonts/media/runtime requests separately. Gzip estimates are not observed CDN transfer or browser timing.
5. Choose one measured contributor, make an authorized targeted change, rebuild once and compare the same entry. A split can reduce initial JS while increasing later requests. Record feature-load cost and interaction latency if relevant. Package metadata, source file count and synthetic byte compression cannot prove an application gain.

The helper supports explicit Vite JavaScript entry graphs. Next.js manifests and framework-specific first-load accounting require that framework's actual analyzer; coverage is reduced here. [Synthetic measurement](../examples/outcome-modernization.md#bundle-measurement) exercises graph accounting only.
