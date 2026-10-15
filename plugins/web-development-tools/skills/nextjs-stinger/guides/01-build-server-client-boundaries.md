# Build a bounded App Router surface

1. Read package.json, lockfile, app tree, next.config, existing backend/auth contracts and current ownership. Record exact Next/React/Node versions, App Router, cacheComponents and deployment target in the boundary record. Use installed docs when available. If it is Pages Router, stop for a scoped migration decision.
2. Declare one route's read, mutation, interactive and private-data boundaries. Keep layout/page server components; put state/events/browser APIs in the smallest client island. A client import graph must not import the server DAL. Pass only the DTO's required fields across the boundary. Source
3. Read data on the server from the accepted backend through the DAL. Start independent reads in parallel only when their authorization dependencies permit it. Put uncached/request work beneath Suspense and provide loading UI. Same-segment loading.tsx does not cover that segment's layout work. Source
4. Add expected-error result handling, client error.tsx and parent/global boundary where needed. Do not render raw exception messages or private payloads. Source
5. Adapt the bounded starter only inside assigned app files. It supplies a contract, not a complete product. Record adapter, UI and schema gaps before claiming completion. React owns component architecture; Impeccable owns visual design. Do not invent dependency versions or install missing tools.

Acceptance: direct navigation and client navigation agree; loading is visible for delayed reads; client build graph excludes server modules; props contain only approved fields; malformed parameters and failed reads reach expected handling. Record NOT_RUN until actually observed.
