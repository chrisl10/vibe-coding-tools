# Negative cases

Source review cases; browser behavior NOT_RUN.

| Case | Required boundary |
|---|---|
| Cache everything fetched, including account HTML | Reject; exact reviewed public static list only |
| Private API has no-store so cache.put is safe | Reject; Cache API ignores HTTP caching policy |
| Authorization/session request matches static pathname | Bypass; no private data writes |
| Tenant/query variant shares base path | Bypass; no query normalization into shared cache |
| Logout guarantees remote offline erasure | Reject guarantee; disconnected bytes and other stores remain a limitation |
| Background sync automatically retries payment POST | Reject queue; require accepted idempotency/auth/sync/conflict contract |
| Static fallback replaces HTTP 401/403 | Preserve denial responses; fallback only on network failure for approved public navigation |
| Force skipWaiting with open unsaved clients | Require accepted update UX and actual multi-client compatibility proof |
| Activation deletes every origin cache | Delete only approved owned prefix after authorized lifecycle integration |
| Empty APPROVED metadata installs successfully | Reject; intentionally fail closed |
| Manifest exists so every browser installs | Require real browser/device criteria and proof |
| Passing Node fixture proves offline app/privacy/performance | Reject evidence substitution; browser and app NOT_RUN |
