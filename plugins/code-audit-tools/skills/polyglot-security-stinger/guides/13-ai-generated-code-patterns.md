# 13 AI-generated code failure patterns

Loads [../references/cross-cutting/ai-failure-patterns.md](../references/cross-cutting/ai-failure-patterns.md).

Run on every audit, whether or not the user says the code was AI-written. Research found risky flaws in 45 percent of AI-generated samples, with newer models no better [raw/ai--veracode-genai-code-security-2025.md], and about one in five generated samples naming a package that does not exist [raw/ai--csa-slopsquatting-2026.md].

## Steps

1. **Run the sweep** in ai-failure-patterns.md from each stack path. Many hits overlap the ecosystem checklists; that is fine, the point is a second net tuned to how generated code fails.
2. **Walk the pattern table AI1 to AI14.** For each pattern write "found (finding ids)", "not found", or "not applicable" in notes.
3. **Tutorial secrets (AI1).** Compare literal keys with well-known tutorial values (for example the FastAPI tutorial's hard-coded `SECRET_KEY`) and generic placeholders. A tutorial key used in production config is a real secret leak: anyone can forge sessions or tokens [raw/python--fastapi-oauth2-jwt.md].
4. **Package names (AI2).** For each direct dependency you do not recognize, follow the registry-metadata check in ai-failure-patterns.md (metadata only, never install). Record the network cap if offline [raw/ai--csa-slopsquatting-2026.md].
5. **Coverage gaps (AI3, AI4, AI6).** Revisit the route tables from guides 01 to 08 and look for the routes added "around" the main flow: exports, admin, bulk operations, webhooks, internal tools. These are where generated code most often skips auth and ownership checks.
6. **Switched-off protections (AI7) and debug (AI9).** Every hit is read; each real one is a finding in its ecosystem's class.
7. **Placeholder checks (AI14).** `TODO: add auth` next to a live route is a finding about the route (missing auth), with the TODO as evidence.
8. **Write findings** per guide 14 with an extra `ai-pattern` tag and the pattern number (for example `["python", "ai-pattern", "AI1"]`). Do not claim the code was AI-generated; describe the weakness.

## Done when

Every pattern AI1 to AI14 has a result in notes, and every real hit is a finding or is listed under "Not confirmed" with the reason.

## Sources

[raw/ai--veracode-genai-code-security-2025.md], [raw/ai--csa-slopsquatting-2026.md], [raw/python--fastapi-oauth2-jwt.md], [raw/ci--github-actions-secure-use.md]
