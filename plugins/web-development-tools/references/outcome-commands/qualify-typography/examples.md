# Acceptance scenarios: qualify-typography

Mode: reference. These are source-workflow qualification scenarios. They do not claim native dispatch, application execution or provider/device proof.

## Case 1
Request: A Svelte site has approved variable fonts and source token drift.
Expected: Separate typography tokens from loading mechanics and use actual frontend owner for fixes.
Source review: PASS. Located instructions: `typography-font-wasp-drone`, `font-loading-wasp-drone`, `actual frontend/component owner`.
Native/runtime outcome: UNPROVEN.

## Case 2
Request: Browser tooling is unavailable but CSS passes inspection.
Expected: Return bounded source review and explicitly unproven runtime; do not claim completed qualification.
Source review: PASS. Located instructions: `runtime checks explicitly unproven`, `never call that qualification complete`.
Native/runtime outcome: UNPROVEN.

## Case 3
Request: Latin subsetting removes required Arabic glyphs.
Expected: Preserve scripts and ask before dropping required language coverage.
Source review: PASS. Located instructions: `languages/scripts`, `dropping language coverage`, `required glyphs`.
Native/runtime outcome: UNPROVEN.

## Case 4
Request: Cold-cache and blocked-font text clips at 200 percent zoom.
Expected: Capture browser/viewport/network state and report concrete type/loading failures against baseline.
Source review: PASS. Located instructions: `200 percent`, `blocked-font states`, `clipping`.
Native/runtime outcome: UNPROVEN.

## Case 5
Request: A paid font or new font tool is required for a proposed repair.
Expected: Do not purchase, download paid assets or install implicitly; record gap.
Source review: PASS. Located instructions: `Do not install font tools`, `paid font assets`.
Native/runtime outcome: UNPROVEN.
