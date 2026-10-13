# Synthetic store readiness cases

These are constructed bookkeeping examples, not a real app, store build, privacy declaration or policy approval. Apply [the evidence procedure](../guides/06-prepare-artifact-privacy-and-entitlement-evidence.md).

## A. Android update with stale billing dependency

Supplied synthetic facts: package `example.notes`, old versionCode 41, proposed versionCode 42, matching distribution signing fingerprint, release build report provided, bundled Billing Library 7, no app-specific extension evidence. Privacy SDK inventory and new crash destination supplied; runtime trace missing. Subscription purchase-button test says success; refund/restore/server verification tests absent.

Decision: build identity READY FOR OWNER REVIEW; billing eligibility NOT READY because the [dated deprecation table](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/app-store-submission-stinger/references/research/store-readiness-20261007/raw/play-billing-deprecation.html) requires 8+ for new submissions/updates after August31,2026 without an applicable granted extension. Privacy and entitlements UNRESOLVED. Overall NOT READY. Assign native billing upgrade and server lifecycle proof to their implementation owners. Do not infer grandfathering from an already-live version.

## B. iOS subscription with a US link and mixed storefront list

Supplied synthetic facts: iOS native artifact identity absent, US and Germany planned, digital premium subscription, web-checkout link visible in both regions, no selected entitlement/agreement evidence for Germany. Analytics SDK transmits a user identifier and diagnostic payload; partner retention unknown.

Decision: build NOT READY; US external-link treatment is considered under Apple3.1.1(a), but it cannot qualify the Germany path. Germany payment applicability UNRESOLVED; privacy UNRESOLVED until processor/retention and actual flow evidence exist. No universal free-checkout exception and no blanket EU no-mix verdict. Overall NOT READY. [Apple3.1.1(a),3.1.2,3.1.3](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/app-store-submission-stinger/references/research/store-readiness-20261007/raw/apple-review.html).

## C. On-device feature plus ephemeral server call

Supplied synthetic facts: notes remain on device, weather feature transmits location to a server; app vendor claims memory-only processing but actual logging configuration is absent. No analytics SDK claimed; dependency inventory unprovided.

Decision: do not label the entire app no-data. Apple on-device note handling and off-device collection are evaluated separately. Play main ephemeral definition and later FAQ have a documented tension; record both and conservatively include the flow for review until the concrete Console answer is clarified. No-runtime-proof is UNRESOLVED, not no collection. [Apple definitions](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/app-store-submission-stinger/references/research/store-readiness-20261007/raw/apple-privacy.html), [Play definitions and FAQ](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/app-store-submission-stinger/references/research/store-readiness-20261007/raw/play-data-safety.html).

## D. Source-ready worksheet with absent native specialists

Every source worksheet is filled and its links resolve, but no Swift/Kotlin engineer, native compiler proof or transaction tests are available. Decision: source preparation complete; release NOT READY. React/Python agent presence is not native StoreKit/Billing expertise. Keep the implementer gap visible rather than routing to a fictional specialist or claiming store acceptance.
