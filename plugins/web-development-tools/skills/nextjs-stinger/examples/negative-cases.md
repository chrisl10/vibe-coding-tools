# Required negative cases

All application cases below are NOT_RUN. A parser exercise cannot satisfy them.

| Case | Required observable result |
| --- | --- |
| Client imports server DAL | Existing app build rejects server-only boundary violation. |
| Forged user/tenant form fields | Trusted identity comes from adapter; foreign resource read/write denied. |
| Direct action/handler invocation without session | No private read or write; explicit authentication failure. |
| Session valid but resource belongs to another tenant | No DTO and zero affected rows; denial follows app's enumeration policy. |
| Permission revoked between read and write | Atomic write predicate rejects; cached UI cannot grant permission. |
| Invalid route ID, non-string FormData value or oversize title | Validation failure before write. |
| Runtime cookies helper inside normal use cache | Production request rejects; no build-only success claim. |
| Shared private cache without tenant/permission contract | Do not introduce it; obtain scoped cache design and audit. |
| Logout, back navigation and account switch after warm private page | Previous identity's private data absent; inspect browser/RSC evidence. |
| Action mutates then router refresh without tag invalidation | Declared freshness test detects stale cached data. |
| updateTag called from handler | Reject implementation; use supported invalidation semantics. |
| Static export proposed with private server action | Provider handoff rejects output mode as incompatible. |
| Missing Next/dependencies | Report NOT_RUN and dependency blocker; do not install implicitly. |
