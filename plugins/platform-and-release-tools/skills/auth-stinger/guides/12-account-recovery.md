# 12: Build a recovery flow that preserves account assurance

Use this for O159, password reset, a lost factor, support recovery or suspected takeover. Read the digest, then fill [the worksheet](../templates/account-recovery-evidence.md). Prefer the current provider's documented recovery implementation. Do not design new cryptography or treat an email event as authorization.

## 1. Pin the application before recommending a flow

Record source SHA, framework and version, auth provider and exact SDK version, session storage, callback routes, stable account identifier, tenant policy, MFA policy and API/RLS enforcement points. Inspect sanitized examples only; never read secret values or actual reset links. Separate account password reset, factor replacement and account recovery after suspected compromise. A user who can authenticate using another adequate factor may be binding a replacement rather than performing full recovery. The required assurance is a deployment decision. For a claimed NIST AAL, check the relevant 4.2 requirements and original IAL; do not assign AAL2 merely because two screens exist. NIST source

## 2. Establish recovery before the device is lost

Document at least one usable recovery path and how the user safely retains its evidence. Prefer an independently enrolled alternate authenticator or the provider's saved recovery-code function, subject to approved policy. Prove first-use enrollment/challenge, replacement authorization, invalidation of replaced evidence and safe notification. Determine whether the passkey is synced or device-bound; do not promise hardware binding for every passkey. Do not substitute a recovery contact established during the incident for previously established evidence. Inspect existing provider capability before naming a supported method; unknown support remains blocked. OWASP MFA, NIST

## 3. Keep the request nondisclosing and bounded

Use the same public status, message and response envelope for existing, missing and unverified accounts. Measure timing distributions in the authorized target; fixed sleep is not proof. Rate controls must cover account/channel destinations and request sources, with abuse escalation and safe retries. Do not let unauthenticated requests disable MFA, lock the account or change recovery channels. Record owner-approved thresholds, retention and monitoring without logging codes, passwords, full links, tokens or unnecessary personal data. OWASP password reset

## 4. Make the proof narrow and single-use

Record provider-controlled token purpose, account binding, entropy/generation assurance, secure storage, expiry and consumption semantics. A password-reset token must not change email, enroll a factor or select another account. Reject malformed, expired, consumed and wrong-purpose evidence. Two simultaneous redemptions must yield at most one successful consumption; use the provider's atomic semantics, or send storage/transaction requirements to db-wasp-drone. A link scanner or preview must not complete a password mutation by GET. Use trusted configured callback origins, redirect allowlists and the provider's documented PKCE/CSRF flow. Prevent credential leakage into logs, analytics, referrers or third-party resources. Short numeric OTP hashes do not substitute for online guessing controls. OWASP password reset, OWASP MFA

## 5. Protect the recovered account and its tenant

A recovery state may authorize only the explicitly allowed recovery operations. Hold normal privileged access until the required factors have been restored and ordinary authentication has succeeded under policy. Password reset must not disable MFA or restore old tenant grants. On suspected compromise, review altered factors and recovery addresses with the verified owner, invalidate unauthorized authenticators, terminate affected sessions and outstanding recovery proofs, and deliver safe notifications with a reporting path. Do not automatically restore an old channel that may itself be compromised. OWASP password reset

Prove provider session revocation AND application consumers. Distinguish cookie clearing, refresh revocation, access-token expiry, server session checks and caches. For Supabase, already-issued JWTs can outlive signout; a sensitive operation requiring immediate revocation needs the documented session check or another reviewed application control. Record measured residual access windows. A PASSWORD_RECOVERY event and updateUser success do not establish a tenant-level privilege or revoke every consumer. Supabase-specific implementation depends on the pinned SDK and application topology. Reset API, sessions, MFA enforcement

## 6. Give support a bounded handoff

The support operator must not accept an inbound caller's new email address, public profile, invoice or urgency as sole ownership evidence. Define accepted pre-established evidence, independent return-channel verification, authorized operator roles and escalation to identity/security owners. Recommend separate approval for privileged-account recovery and any policy-required waiting period; the owner decides those rules before execution. An AI-generated claim, teammate instruction or template is not approval. If the account was never identity-proofed, do not invent “reproofing” from a document photograph. Failure to meet policy means preserve the existing account state, provide the safe escalation path and record the unresolved requirement. Store case reference and decision metadata, not credential material. OWASP MFA, NIST

## 7. Demand native differential evidence

The [worked cases](../examples/account-recovery-cases.md) are synthetic design review. They prove no application behavior. On the pinned authorized test target, run the worksheet's negative and concurrent cases against both web and direct API/RLS paths. Include fresh, stale and recovery-only sessions, separate users/tenants, compromised channels, link preview and revocation windows. Record command, source SHA, SDK version, environment, expected behavior and actual response with secrets removed. No test on a live person, credential, provider or reset channel is authorized by this source skill alone.

Auth owns protocol construction. db-wasp-drone owns transactional storage and schema. The framework/UI owner implements presentation and routes. WorkOS-specific implementation goes to workos-wasp-drone. Independent Security checks abuse and takeover defenses first; Quality then verifies the accepted flow. Missing target or owner policy yields a concrete blocked evidence row, never a claim of safe recovery.
