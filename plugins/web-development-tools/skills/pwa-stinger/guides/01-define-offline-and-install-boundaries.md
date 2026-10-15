# Define offline and install boundaries

1. Read the accepted product/stack and Impeccable design contracts. Identify a concrete offline task, supported browser/device matrix and honest disconnected UX. An installable site does not imply offline support, and a worker does not prove installability.
2. Inventory current workers, registration URL/scope, manifest link/metadata/scope/start_url/icons, framework/PWA modules and storage ownership. Do not install a new framework/module, replace an active worker or broaden origin scope without authorization.
3. Choose the narrow public scope and exact static assets that are safe for every account. Never include server-rendered account HTML, session/tenant DTOs, auth endpoints or private API responses by default. Framework and design owners retain the app and UX; PWA owns worker/manifest/offline integration only.
4. Fill the offline contract, including browser fallback with no worker, secure-context requirement, installation criteria per browser, cache quota/eviction, first-visit offline limits and updates. Inspect app-generated asset metadata rather than guessing hashes or file names.

Grounding: service worker, installability, manifest, storage. Owner/scope policy is derived from existing Web Stack Selection, Impeccable and Core Security boundaries.
