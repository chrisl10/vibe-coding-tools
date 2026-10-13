# Account recovery implementation evidence

Status: DRAFT. No account action authorized by this document.

## Pinned target and authority

- Source SHA / environment / framework-version / SDK-version / provider:
- Stable account subject and tenant enforcement (synthetic references only):
- Session consumers / caches / callback / API / RLS locations:
- Incident type: password reset / factor replacement / suspected compromise:
- Required assurance, original identity proofing and owner-accepted recovery policy:
- Accepted evidence / independent return channel / operator authorization / separate approval:
- Provider feature/document snapshot and gaps:

## Decisions before implementation

| Requirement | Approved value and source | File:line or provider reference | Actual proof / unresolved gap |
|---|---|---|---|
| Enrollment and usable alternate method | | | |
| Generic responses and timing envelope | | | |
| Per-account/source/channel abuse controls | | | |
| Purpose, subject binding and callback allowlist | | | |
| Token storage, expiry and atomic single use | | | |
| Recovery-only access and restored-factor authentication | | | |
| Compromised factors/channels review | | | |
| Session/refresh/access-token/cache revocation windows | | | |
| Safe notifications and unauthorized-recovery escalation | | | |
| Support operator scope and required approval | | | |

## Required native cases

Each row needs source SHA, SDK/version, exact command, expected result, sanitized actual result and status. “Pending” never means pass.

| Case | Expected property | Actual / status |
|---|---|---|
| Existing vs missing account requests | Indistinguishable public envelope; measured timing | Pending |
| Repeated per-account and multi-source requests | Approved abuse policy applied without account-disable bypass | Pending |
| Expired, replayed, wrong-purpose and wrong-account proofs | Rejected; no mutation | Pending |
| Concurrent duplicate redemption | At most one successful consumption | Pending |
| Preview/GET and hostile redirects | No mutation; unsafe redirect denied | Pending |
| Fresh, stolen/stale and recovery-only sessions | Only approved recovery operations; MFA not silently bypassed | Pending |
| Cross-user/tenant direct API and RLS operations | Denied without scope change | Pending |
| Changed recovery address or missing proof | Safe escalation; no unsupported ownership shortcut | Pending |
| Old sessions/access tokens/refresh tokens/caches after compromise recovery | Approved revocation window observed for every consumer | Pending |
| Notification failure and unauthorized-recovery report | Recorded failure/escalation without credential logging | Pending |

Security report / source manifest:
Quality report after Security / source manifest:
Unknowns and owner decisions:
