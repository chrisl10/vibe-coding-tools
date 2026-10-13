# Inputs Checklist: website-stinger

Collect missing inputs that change work in one batched question before scaffolding. Read [quick scope](../guides/14-scope-a-quick-website.md) or [CMS contract](../guides/15-build-an-independent-payload-cms.md) first. Existing answers remain valid; ask later only when new evidence creates a material unresolved decision. The checklist below describes the full-template branch; mark unrelated providers N/A, do not ask for accounts or identifiers merely to complete a form.

---

## Stack confirmation

- Confirm actual framework/version, runtime and hosting requirements. Website implements the SvelteKit public branch; another required framework needs a selected implementer. Add Payload, database and tracking only from accepted requirements.

## CMS mode

- **Does this site need a managed content admin panel with blog/pages management by non-developer editors?**
  - YES → **Payload mode**: scaffold `apps/cms` (Next.js + Payload), use Payload Collections for blog
  - NO → **TypeScript-as-CMS fallback**: no `apps/cms`, blog posts are TypeScript data objects

---

## Site identity

- Site name
- Target audience (1 to 2 sentences)
- Primary conversion action (e.g. "Book a consultation", "Start free trial", "Contact us")
- Industry / vertical (for generic schema.org selection)

## URLs and environment

- Primary domain (or "not yet decided")
- Vercel project for `apps/web` (linked / create new)
- Vercel project for `apps/cms` (Payload mode only: linked / create new / N/A)
- Supabase project ref (`abcdefgh12` format, or "create new")
- Payload URL (e.g. `https://cms.example.com`, or "same domain at /cms", or "TBD")
- `PUBLIC_SITE_URL` value

## Analytics

- GA4 measurement ID (G-XXXXXXXXXX, or "skip")
- Microsoft Clarity project ID (or "skip")
- Facebook Pixel ID (or "skip")

## Brand

- Primary brand color (HEX or HSL)
- Secondary / accent color (HEX or HSL)
- Display font (Google Fonts name, or "default Inter")
- Body font (Google Fonts name, or "default Inter")
- Dark mode: enabled by default / light only / system preference

## Content

- Blog/content needed: yes / no (drives CMS mode confirmation above)
- Lead capture form: yes / no
- Estimated number of pages at launch
- Any existing content to migrate

## Phase opt-outs

- List any phases to skip and why (e.g. "skip Phase 10: no webhook integrations needed")
- No opt-outs → proceed with all 12 phases in canonical order

---

## Architectural consequences of common opt-outs

| Opt-out | Consequence |
|---|---|
| Skip Payload (TypeScript-as-CMS fallback) | No `apps/cms` scaffold. Blog content requires code deploys to publish. No visual editor. |
| Skip Supabase (Phase 5) | No leads table, no RLS, no app_settings. Phase 8 needs an email-relay fallback. |
| Skip auth (Phase 6) | No protected admin routes. Phase 7 is automatically skipped. |
| Skip blog (Phase 9) | No blog routes. If Payload mode: Posts collection still recommended for future use. |
| Skip webhooks (Phase 10) | No outbound integrations. Lead notifications must be handled by Supabase email or alternative. |
