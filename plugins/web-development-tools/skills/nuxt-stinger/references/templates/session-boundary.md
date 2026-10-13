# Session integration boundary

NOT_RUN. Preserve the accepted provider and session model.
Fill: adapter path; validation of signature/expiry/revocation; approved minimal session DTO; principal/tenant derivation; per-resource permission; CSRF/origin policy for mutations; logout invalidation and client state clearing; cookie flags and server proxy policy; tests and actual outputs.

The official nuxt-auth-utils recipe demonstrates requireUserSession with sealed-cookie sessions, but module adoption and credential/configuration changes require explicit authorization. Never replace WorkOS, Supabase, or another accepted provider with this recipe automatically. Page middleware can redirect for UX; direct server requests still require enforcement.
