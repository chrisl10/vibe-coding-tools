# PWA implementation digest

Captured 2026-10-08 UTC from official MDN and Chrome web.dev documentation. Rolling docs establish API guidance, not target-browser support or installed-app behavior.

| ID | Implementation consequence | Source |
|---|---|---|
| P1 | Service workers require a secure context, with localhost development exceptions. Registration and control scope need actual browser proof. | service-worker |
| P2 | Install/activate work uses event.waitUntil; activation and client control are separate lifecycle states. | service-worker |
| P3 | Cache API does not honor HTTP cache headers. A private/no-store header cannot alone prevent a custom service worker from persisting a response. | cache |
| P4 | Cache entries do not automatically expire; application cache lifecycle and browser storage limits need explicit handling. | cache |
| P5 | Installability depends on manifest, secure serving and browser criteria. An available manifest or service worker does not prove installation. | installable |
| P6 | Manifest describes application metadata and entry URL; its scope is distinct from service-worker registration scope. | manifest |
| P7 | skipWaiting can activate a new worker while clients remain open; forced update/control changes need a tested application update contract. | lifecycle |
| P8 | Background sync can retry a task but availability and scheduling vary; retries do not provide application idempotency or conflict resolution. | offline |
| P9 | Browser storage can be evicted; offline cache availability is not a durability guarantee. | storage |

## Derived security and product policy

The public static allowlist, omission of credentials during precache, fail-closed response validation, no private/session/tenant/API cache default, and no mutation queue without an accepted idempotency/sync/conflict contract are application policy derived with Core Security ownership. Offline revocation cannot reliably erase bytes already held by a disconnected device. Logout purge is bounded best effort and does not establish remote erasure. No browser cache, installation, performance, privacy or security guarantee is claimed.
