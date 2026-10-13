# Synthetic recovery reviews

These are source walkthroughs, not tests of an application, provider or account. No credentials are included. Review against [guide 12](../guides/12-account-recovery.md) and its archived sources.

| Case | Given | Decision | Evidence still needed |
|---|---|---|---|
| Lost phone, enrolled alternate factor | A synthetic user has a previously bound alternate authenticator and an owner-defined assurance policy | Follow provider verification and factor-binding path; password reset alone cannot disable MFA | Pin SDK, alternate-factor challenge, old-factor revocation and notification |
| Support pressure from a new address | Requester knows public company details and says the founder approved | Deny the shortcut; independently use accepted evidence and authorized approval path | Policy, operator roles and legitimate-owner return-channel proof |
| Mailbox takeover | Reset address was changed during the incident | Do not treat that address as independent evidence or blindly restore its predecessor | Safe earlier evidence, compromise review and assurance-specific recovery |
| Concurrent saved-code replay | Two requests attempt the same synthetic code | Require at most one atomic redemption; regenerated evidence invalidates replaced codes | Native concurrency test plus approved storage/provider semantics |
| Stolen token after signout | A synthetic Supabase session is terminated while a stateless API holds an unexpired JWT | Do not claim immediate revocation from signout alone; inspect sensitive-action session checking | Actual API/RLS denial or accepted residual window on pinned deployment |
| Recovery event with admin request | Client observes PASSWORD_RECOVERY then attempts tenant-admin export | Event is not authority; deny export until normal accepted authentication and tenant enforcement | Direct API, web and RLS negative cases |
| No alternate evidence, no original proofing | Lost device and caller offers a newly photographed ID | Do not invent reproofing; keep account unchanged and escalate under policy | Owner-approved alternative permitted by assurance requirements |
| Link-preview request | Mail scanner GETs the synthetic reset page | Rendering must not consume mutation authority or change password | Native browser/API preview and actual SDK flow test |

Human support rehearsal and provider test evidence remain pending. A worksheet with completed fields cannot certify takeover resistance.
