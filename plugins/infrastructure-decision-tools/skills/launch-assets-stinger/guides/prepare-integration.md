# Prepare an integration or plugin

1. Lock host platform, customer-facing versus internal use, distribution method, required events/actions and acting identity. No provider account is needed merely because it appears in a broad asset list.
2. Resolve the selected platform/API/MCP/extension specialist. Record provider application/project reference, exact requested scopes/permissions, accountable owner and environment. Do not let an integration borrow a user's authority implicitly.
3. Separate authorization callback, installation setup URL and inbound webhook endpoint. Capture app brand/privacy/support contact and domain ownership as applicable. Google production policies and GitHub callback rules are provider-specific; do not impose them universally.
4. Record secret custodian/reference, event delivery/retry/recovery owner and approved test fixtures. Never request secret values. Identify verification/review/rate-plan unknowns with the current official source needed to resolve them.
5. Prepare ledger rows and concrete handoffs. Hosted callbacks/webhooks need their selected hosting/HTTPS preparation; purely local plugins do not automatically need a server, database, OAuth or store account. No registration, permission settings, installations or external test events are performed here.

Grounding: Google OAuth, GitHub callbacks, Doppler configs, TLS. Authorization/status boundaries are topic contracts.
