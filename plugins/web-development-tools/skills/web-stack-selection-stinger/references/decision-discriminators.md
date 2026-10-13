# Framework discriminators in plain language

Primary capabilities are cited in the [digest](research/distilled-web-stack.md). The recommendations below apply the approved workload-selection contract; they are not popularity or speed claims.

| Need | Decision discriminator | Avoid |
|---|---|---|
| Public content should arrive as HTML | Prerender stable content; SSR dynamic content where needed | Claiming any framework guarantees SEO or needs a permanent server for static output |
| Signed-in app with browser-heavy interactions and separate API | SPA composition can fit existing React/Vue expertise | Treating Vite alone as routing/auth/backend design |
| Mixed public content and dynamic routes | Evaluate integrated app frameworks and per-route delivery | Applying one rendering choice to every route automatically |
| Existing React team plus accepted Next server needs | Next may fit, with explicit server/client/deployment owner | Assuming a React component reviewer also owns Next server behavior |
| Existing Vue team and public dynamic HTML | Nuxt may fit; record implementation owner availability | Rewriting to another framework only because a local agent is missing |
| Small static website | Smallest qualified static/prerender track, no forced DB/CMS | Adding auth, payments or full admin because a stack supports them |
| Native mobile reuse | Separate actual business logic/data contracts from UI/runtime reuse | Promising React DOM components automatically become native mobile UI |
| Existing backend with specific libraries/workers | Preserve API contract; frontend choice need not replace backend | Labeling Go/Python/Rust universally superior to JS |
| Host adapter/runtime constraints | Verify exact framework version and deployment feature support | Assuming static export supports all server mutations |

## Plain terms

CSR builds the visible page in the browser. SSR prepares HTML when a request arrives. Prerendering prepares HTML during a build. Hydration adds browser behavior to prepared HTML. An SPA changes views in the browser, with routing/data conventions selected by the application. These explanations reflect the official rendering descriptions; they do not prescribe one mode for all products.

## Backend is a separate decision

Choose a separate backend only when integration/library/worker/runtime/scaling/security/team needs justify the boundary. Go/Python/Rust owners qualify their own service and deployment details. A familiar Python integration may favor retaining Python; a host-control requirement may favor a container/VM decision; Rust systems needs may matter. None is implied by choosing React, Svelte or Vue. Record identity, tenancy, API/event contracts, storage, secrets and failure/retry ownership independently.

## Component and license handoffs

Visual direction and component selection belong to actual selected UI/design-system and library owners. Tailwind/shadcn mechanics belong to their actual framework-specific specialists. Component vendoring needs exact revision/license/notices/patch ownership and an actual owner; Software Licensing handles the rights/obligations explanation. Never select an unreviewed MIT-labeled repository as though the label clears fonts/assets/transitive content. This workflow returns a handoff request, not a vendor-tree change.
