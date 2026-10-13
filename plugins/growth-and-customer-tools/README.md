# Growth and Customer Tools

Research buyers, acquire leads, follow up, support customers and grow accounts.

Acquire, serve and retain is a coherent business journey. These generic methods must not acquire mandatory Littlebird or HighLevel dependencies.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 15 skills, 15 agents and 2 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [affiliate-referral-program-stinger](skills/affiliate-referral-program-stinger/SKILL.md) | Design SaaS affiliate and referral programs. Use for platform choice, attribution, commissions, fraud, or program economics. |
| [alt-ads-platforms-stinger](skills/alt-ads-platforms-stinger/SKILL.md) | Plan paid acquisition beyond Meta and Google Search. Use for LinkedIn, TikTok, Reddit, Bing, Pinterest, Quora, YouTube, or podcasts. |
| [blogging-content-strategy-stinger](skills/blogging-content-strategy-stinger/SKILL.md) | Plan search-led blog content. Use for topic clusters, titles, post structure, cadence, AEO formatting, or calls to action. |
| [cold-outreach-stinger](skills/cold-outreach-stinger/SKILL.md) | Build founder cold-email programs. Use for deliverability, list hygiene, outreach tools, personalization, or sequences. |
| [competitive-research-stinger](skills/competitive-research-stinger/SKILL.md) | Build competitor workbooks and reports. Use for market mapping, feature gaps, or sales battlecards. |
| [customer-support-tooling-stinger](skills/customer-support-tooling-stinger/SKILL.md) | Choose and configure a SaaS support stack. Use for inboxes, AI deflection, SLAs, routing, or founder triage. |
| [go-to-market-stinger](skills/go-to-market-stinger/SKILL.md) | Choose one acquisition channel from dated buyer evidence and team constraints, then draft a falsifiable experiment. Use before paid, organic, outbound or partner execution. |
| [icp-research-stinger](skills/icp-research-stinger/SKILL.md) | Ideal Customer Profile research from a company domain: seed from its site, fan out with Exa or Firecrawl, grade stated vs revealed evidence, and deliver an ICP dossier. Account and role level only. |
| [knowledge-base-help-center-stinger](skills/knowledge-base-help-center-stinger/SKILL.md) | Select and improve customer help centers. Use for KB platforms, search, AI deflection, localization, versioning, or content gaps. |
| [lifecycle-email-stinger](skills/lifecycle-email-stinger/SKILL.md) | Writes evidence-grounded hot and warm lead follow-up emails. Use for lead classification, sequences, cadence, suppression, QA, and measurement. |
| [live-chat-support-stinger](skills/live-chat-support-stinger/SKILL.md) | Choose and wire SaaS live chat. Use for widget identity checks, support routing, AI deflection, or data export. |
| [newsletter-platform-stinger](skills/newsletter-platform-stinger/SKILL.md) | Choose and integrate a newsletter platform. Use for Beehiiv vs Kit, signup forms, deliverability, monetization, or migration. |
| [review-funnels-stinger](skills/review-funnels-stinger/SKILL.md) | Build SaaS review collection. Use for G2, Capterra, Trustpilot, Product Hunt, request timing, incentives, or negative reviews. |
| [social-media-marketing-organic-stinger](skills/social-media-marketing-organic-stinger/SKILL.md) | Plan authentic organic social growth. Use for platform focus, founder voice, build-in-public, calendars, or AI-slop avoidance. |
| [tawk-to-api-stinger](skills/tawk-to-api-stinger/SKILL.md) | Integrate the tawk.to REST API. Use for contacts, chats, tickets, webhooks, metrics, widgets, or knowledge-base articles. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install growth-and-customer-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use lifecycle-email-stinger to prepare a follow-up sequence from [approved lead context]. Keep the messages as drafts for review.
```

Expected result: The requested customer/growth analysis or reviewed drafts. Sending and customer-data access are separate actions.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/growth-and-customer-tools:choose-acquisition-channel` ([procedure](commands/choose-acquisition-channel.md)) | Choose one acquisition channel from dated buyer evidence, operating constraints and a falsifiable experiment draft. |
| `/growth-and-customer-tools:launch-product` ([procedure](commands/launch-product.md)) | Prepare an evidence-based product launch with customer fit, channel focus, review readiness, and measurable follow-up. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [affiliate-referral-program-wasp-drone](agents/affiliate-referral-program-wasp-drone.md) | Affiliate and referral program specialist for SaaS products -- platform selection (Rewardful, FirstPromoter, Tolt, PartnerStack, Impact, Refersion), the affiliate-vs-referral distinction, cookie-based and server-side attribution (post-ITP, post-3PC era), payout automation, fraud detection (self-referral, cookie stuffing, velocity fraud), and EPC/LTV program economics. | [affiliate-referral-program-stinger](skills/affiliate-referral-program-stinger/SKILL.md) |
| [alt-ads-platforms-wasp-drone](agents/alt-ads-platforms-wasp-drone.md) | Paid acquisition specialist for alternative ad platforms beyond Meta and Google Search - LinkedIn Ads (B2B Lead Gen Forms, Thought Leader Ads, ABM), TikTok Ads (Smart+ 2026 default, CAPI), Reddit Ads (community targeting, AI citation compound value), Microsoft/Bing Ads (LinkedIn Profile Targeting layer), Pinterest Ads (Shopping Catalogs, 70-90 day attribution), Quora Ads (comparison-intent B2B), YouTube standalone video, Spotify Ad Studio + podcast advertising, and the channel-fit-by-ICP heuristic that selects among them. | [alt-ads-platforms-stinger](skills/alt-ads-platforms-stinger/SKILL.md) |
| [blogging-content-strategy-wasp-drone](agents/blogging-content-strategy-wasp-drone.md) | Editorial blogging strategy specialist - cluster + pillar topical authority architecture, post-length decisions by search intent, title + H1 + meta description craft, keyword research scoping without obsession, AEO/answer-engine formatting for AI Overviews and chatbot citations, CTA copy that converts without begging, the 12-point pre-publish review checklist, and realistic publishing-cadence planning for solo founders and small teams. | [blogging-content-strategy-stinger](skills/blogging-content-strategy-stinger/SKILL.md) |
| [cold-outreach-wasp-drone](agents/cold-outreach-wasp-drone.md) | Outbound sales specialist for founders running cold email. | [cold-outreach-stinger](skills/cold-outreach-stinger/SKILL.md) |
| [competitive-research-wasp-drone](agents/competitive-research-wasp-drone.md) | Builds competitor-landscape XLSX workbooks and brand-matched PDF competitive reports: research sweep, category taxonomy, feature-gap analysis, computed market-pattern insights, sales battlecards. | [competitive-research-stinger](skills/competitive-research-stinger/SKILL.md) |
| [customer-support-tooling-wasp-drone](agents/customer-support-tooling-wasp-drone.md) | Support stack specialist for SaaS products. | [customer-support-tooling-stinger](skills/customer-support-tooling-stinger/SKILL.md) |
| [go-to-market-wasp-drone](agents/go-to-market-wasp-drone.md) | Choose one acquisition channel for a specific buyer from evidence and constraints. | [go-to-market-stinger](skills/go-to-market-stinger/SKILL.md) |
| [icp-research-wasp-drone](agents/icp-research-wasp-drone.md) | Ideal Customer Profile researcher: starts from a company domain, seeds from its site, fans out with Exa or Firecrawl across customers, market, hiring, reviews, news, and technographic lanes, grades stated vs revealed evidence in a validated ledger, and delivers an ICP dossier. | [icp-research-stinger](skills/icp-research-stinger/SKILL.md) |
| [knowledge-base-help-center-wasp-drone](agents/knowledge-base-help-center-wasp-drone.md) | Customer-facing knowledge base specialist - platform selection (Intercom Articles, Help Scout Docs, ReadMe.com, Document360, HelpJuice, Zendesk Guide), search-first architecture, AI deflection (chat-with-your-docs, Fin standalone, Eddy AI, llms.txt), versioning (Document360 branch versioning, ReadMe git-backed), multi-language (50+ language auto-translate, RTL, TMS), and the analytics-driven content-gap loop (CRAVA framework, no-result triage). | [knowledge-base-help-center-stinger](skills/knowledge-base-help-center-stinger/SKILL.md) |
| [lifecycle-email-wasp-drone](agents/lifecycle-email-wasp-drone.md) | Lifecycle lead email specialist. | [lifecycle-email-stinger](skills/lifecycle-email-stinger/SKILL.md) |
| [live-chat-support-wasp-drone](agents/live-chat-support-wasp-drone.md) | Customer support surface specialist - Intercom, Crisp, Plain, Pylon, Help Scout - widget integration, HMAC/JWT identity verification, conversation routing, AI deflection (Fin 2.0, Ari, Crisp Bot), and the data-export discipline. | [live-chat-support-stinger](skills/live-chat-support-stinger/SKILL.md) |
| [newsletter-platform-wasp-drone](agents/newsletter-platform-wasp-drone.md) | Newsletter-as-channel specialist for product builders and founders - platform selection (Beehiiv, ConvertKit/Kit, Loops, Substack, Resend Audiences, Ghost), embedded newsletter signup integration for Next.js, deliverability tradeoffs (managed SaaS vs self-hosted), monetization options (ad network, paid subscriptions, sponsorships, referral programs), and platform migration (Substack to Beehiiv). | [newsletter-platform-stinger](skills/newsletter-platform-stinger/SKILL.md) |
| [review-funnels-wasp-drone](agents/review-funnels-wasp-drone.md) | Review collection and online-reputation specialist for SaaS products. | [review-funnels-stinger](skills/review-funnels-stinger/SKILL.md) |
| [social-media-marketing-organic-wasp-drone](agents/social-media-marketing-organic-wasp-drone.md) | Genuine organic social media strategy for solo developers, founders, and small product teams (up to ~10 people). | [social-media-marketing-organic-stinger](skills/social-media-marketing-organic-stinger/SKILL.md) |
| [tawk-to-api-wasp-drone](agents/tawk-to-api-wasp-drone.md) | tawk.to REST API v1.1.0 integration specialist: API key Basic Auth and OAuth2, Property/Widgets/Members/Chats/Tickets/Tabs, both webhook directions, Metrics, Contacts, and the Knowledge-Base content-block model (header, paragraph, image, code, video, divider, table) plus the markdown-to-KB workflow (host images on Cloudflare R2 or DigitalOcean Spaces, then reference by URL). | [tawk-to-api-stinger](skills/tawk-to-api-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `CRM/account sync implementation` also needs `platform-and-release-tools`.
- `branded report packets` also needs `documentation-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
