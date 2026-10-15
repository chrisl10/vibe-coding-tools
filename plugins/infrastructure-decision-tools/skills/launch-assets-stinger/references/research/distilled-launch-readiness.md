# Launch readiness research digest

Fresh official-source retrieval: October 7, 2026. Prices below are observations of public documentation in USD, not quotes for a specific user or region. Refresh rates and requirements at the actual preparation date. No account was opened and no provider state inspected.

| Primary finding | Preparation implication | Source |
|---|---|---|
| Apple enrollment distinguishes individual and organization requirements; organization enrollment includes authority, legal entity and generally a D-U-N-S number. | Capture intended seller identity and enrollment owner without collecting identity documents. | Apple enrollment |
| Apple lists 99 USD per membership year, with regional currency variation and possible eligible waivers. | Record the observed annual unit and regional caveat; never treat this as approved spend. | Apple enrollment |
| Google Play lists personal/organization accounts, verification, a 25 USD one-time registration fee and additional testing/device conditions for applicable new personal accounts. | Account existence alone cannot clear production distribution. Capture account type and required release evidence. | Play Console |
| Developer ID supports signing Mac apps distributed outside the Mac App Store and Apple notarization. | Treat developer membership, signing identity and notarization preparation as distinct assets. | Developer ID |
| Windows executable signing verifies contents/publisher; signing and download reputation are separate. EV no longer grants automatic SmartScreen reputation. | Plan signing and a clean-device distribution check; do not promise a certificate eliminates warnings. Smart App Control is a separate feature. | Signing, SmartScreen |
| Hosting providers may manage Let's Encrypt certificates; otherwise an ACME client operates issuance. | Ask who owns HTTPS renewal before recommending a manual certificate workflow. This concerns network TLS, not executable signing. | TLS readiness |
| Google OAuth production policies require separate testing/production projects, relevant contacts, necessary scopes and additional verification for sensitive/restricted scopes. | Plan project/callback/brand/contact/scopes by environment. Do not infer approval from a working test login. | Google OAuth |
| GitHub authorization callback and installation setup URL serve different flows. | Keep callback, installation setup and webhook assets distinct. Review current callback match settings rather than assuming every provider uses the same rule. | GitHub callbacks |
| Supabase's production checklist covers security, capacity, availability and auth-email concerns. | A database project's existence is separate from production readiness, backup evidence and email capacity. | Supabase |
| WorkOS stages and production scope identities and endpoints independently; some project-level settings are shared. | Record actual environment and product scope; staging objects do not establish production preparation. | WorkOS environments |
| Doppler configs follow environments and hold environment-specific values. | Track config references and responsible owners; do not collect secret contents. | Doppler configs |
| Exa exposes search; Firecrawl exposes web search/scrape capabilities. | Research/crawl assets are conditional on a real workflow need. Presence on a vendor list is not a prerequisite. | Exa, Firecrawl |
| Neon documents Postgres/backend services; Qdrant documents vector search production concerns. | Resolve the chosen data architecture before making separate database/vector accounts a requirement. | Neon, Qdrant |
| Tailscale provides private connectivity; Sentry supports application error monitoring; UptimeRobot offers external uptime monitoring. | Record operational responsibilities first, then selected tools and alert recipients. | Tailscale, Sentry, UptimeRobot official product page |

## Scope and limits

The ledger's statuses, evidence classes, blocking/dependency rules and exclusion recipes are the approved topic contract, not vendor statements. Account ownership, secret provisioning, spending authority and release approval require actual task authority and evidence. Public docs do not establish any user's account state.

No universal approval duration is supported here. Record lead time as unknown unless the provider publishes an applicable duration or the user supplies a dated measured record. Vendor estimates are not guarantees. No full cloud cost model or market comparison is attempted. The current sources carry varying publication dates; a fresh capture is not a claim every page was published in 2026.

The guessed WorkOS `/authkit/production` URL returned `HTTP Error 404: Not Found`. Official search identified `/authkit/environments`, captured successfully. Do not cite the failed URL as supporting evidence. Browser opening Sentry/Neon failed, while direct public-document capture succeeded. Raw archive/HTTP evidence is recorded in the source ledger.
