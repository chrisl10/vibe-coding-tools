# Offline acceptance contract

Status: TEMPLATE, real app/browser NOT_RUN.
Record revision, authorized files, framework owner, design direction, current registration/manifest, approved scope, worker/cache namespace and actual browser/device list.

| Task/route | Public/private | Online behavior | Offline behavior | Allowed persisted bytes | Revocation/update limit | Actual proof |
|---|---|---|---|---|---|---|
| Fill target | Fill | Fill | Public static fallback or unavailable | Exact reviewed assets | Fill | NOT_RUN |

Record asset path/MIME/SHA-256 from reviewed build output; no private HTML/API/tenant/session caching. First-visit offline has no installed cache. Quota/eviction can remove public assets. Manifest metadata and worker scope must be qualified separately. No POST queue until accepted idempotency, auth freshness, sync and conflict contracts exist. Logout/device erasure cannot be guaranteed while disconnected.
