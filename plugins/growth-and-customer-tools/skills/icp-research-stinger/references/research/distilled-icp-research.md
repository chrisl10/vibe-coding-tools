# Distilled research: domain-seeded ICP research with Exa and Firecrawl

Stage 3 of the forge for `icp-research-stinger`. Every factual row ends with the ID of the source it derives from; the Source index at the end maps each ID to its URL, fetch date, and source type. Raw page captures were removed from this skill at the owner's request on 2026-09-23 after the grounding, security, and quality audits; re-fetch a URL to re-verify a claim. Research window 2026-03-23 through 2026-09-23; retrieval on 2026-09-23. Documentation pages are living baseline references. Vendor tool names, parameters, prices, and limits are dated observations; verify them against the live tool list before relying on them. Vendor methodology sources carry commercial bias, noted where it matters.

## D1. What an ICP is

| Fact | Detail | Source |
|---|---|---|
| ICP is account-level | A description of the organization (not a person) that gets the most value from the product and can buy it; characteristics include size or budget, industry, geography, technical infrastructure, and pain urgency | [icp--method--icp-vs-buyer-persona] |
| Persona is individual-level | Role, responsibilities, goals, authority, and objections inside an already-qualified account. ICP answers "is this company worth pursuing"; persona answers "who inside it, and how". Collapsing them targets the right person at the wrong company | [icp--method--icp-vs-buyer-persona] |
| Firmographic core | Employee count, industry, revenue, geography, growth trajectory; built iteratively from best-fit customers and refined as accounts close or churn | [icp--method--icp-definition] |
| Technographics belong in the ICP | Detected tools are compounded with firmographics in one rule (example: uses HubSpot, 50 to 1,000 employees, $10M+ raised); a complementary tool signals compatibility, a competitor's tool signals displacement | [icp--signals--technographic-signals] |
| Signal taxonomy | Fit (firmographic), readiness (technographic, headcount and hiring growth as timing), interest (third-party intent), behavioral (first-party engagement). Interest and behavioral data are proprietary and not observable from public research | [icp--signals--intent-trigger-signals] |
| Buying committee | Economic buyer (budget, ROI), champion (feels the problem, drives the deal), technical buyer (integration, security; the vendor cites it as the largest objection source), end user, legal and procurement, executive sponsor. Committees of 10 or more appear only at companies over 1,000 employees | [icp--method--buying-committee-roles] |
| Tiering | Three tiers by fit plus potential: Tier 1 dedicated treatment, Tier 2 scaled, Tier 3 programmatic. Composite scores mix static fit with dynamic signals and should be recalculated on a rolling basis | [icp--method--tiering-fit-scoring] |
| Negative ICP | Hard disqualifiers (jurisdiction or regulation, economic floor, technical incompatibility, unsupported use case) are evaluated before prioritization and cannot be overridden by engagement; soft penalties only lower fit. Disqualifiers require verified data: "unknown" is not "below minimum" | [icp--signals--negative-icp-disqualifiers] |

## D2. Evidence a company's public footprint reveals

| Source | What it reveals | Source |
|---|---|---|
| Pricing page | Plan-name and tagline copy signal the intended buyer; SSO, SCIM, audit logs, dedicated account management on the top tier signal buyers large enough for security and procurement review; gated "contact sales" pricing signals an enterprise-leaning motion, transparent per-seat pricing a self-serve one | [icp--signals--pricing-page-signals] |
| Case studies and logos | Vendors pick case studies to attract more of the same buyer, so the library approximates the realized ICP: logo scale, regulated or regional verticals, and the kind of featured person. The pattern across the library matters, not any single story | [icp--template--case-studies-customer-logos] |
| Job postings | Sales titles segmented by account size (Enterprise AE, Mid-Market AE, SMB AE, territory language) reveal internal tiering; posting volume per segment shows current investment; new-logo versus expansion language shows GTM priority | [icp--signals--job-postings-sales-titles] |
| Hiring shifts | A shift toward enterprise titles often precedes public upmarket moves; technology named in engineering posts reveals stack and roadmap; hiring bursts correlate with funding. Single practitioner account, anecdotal | [icp--method--reverse-engineer-competitor-icp-jobs] |
| Review-site segments | G2 tags verified reviewers with company size, industry, and region and exposes these as filters, a public proxy for who actually adopts a product. Exact size thresholds were not confirmed on the official page | [icp--signals--g2-reviewer-segments] |

## D3. Exa

| Fact | Detail | Source |
|---|---|---|
| Search types | `type`: `instant`, `fast`, `auto` (default), `deep-lite`, `deep`, `deep-reasoning`. No `neural`/`keyword` values in the current enum | [exa--api--search] |
| Search params | `numResults` default 10, max 100; `includeDomains`/`excludeDomains` up to 1,200 each (hostnames, paths, wildcard subdomains); `startPublishedDate`/`endPublishedDate`; `userLocation`; inline `contents` | [exa--api--search] |
| Categories | `company`, `publication`, `news`, `personal site`, `financial report`, `people`. `company` and `people` do not support date filters or `excludeDomains` | [exa--api--search] |
| Category renames | `research paper` became `publication` (2026-07-23); `pdf`, `github`, `tweet` being phased out; `startCrawlDate`/`endCrawlDate` ignored | [exa--changelog--2026] |
| Deprecated params | `includeText`/`excludeText` on search (use highlights or text); `livecrawl`, `context`, `crawledBeforeDate` on contents | [exa--api--search], [exa--api--contents] |
| Contents | `urls` or `ids` (1 to 100); `text` with `maxCharacters`, `verbosity`, include or exclude sections; `highlights` with `query`, `maxCharacters`; `summary` with `query` and JSON `schema`; `maxAgeHours` (-1 cache only, 0 fresh, N hours); `subpages` 0 to 100 with `subpageTarget`; `extras.links` | [exa--api--contents] |
| Highlights | Primary token-efficiency lever versus full text; Dynamic Highlights beta (2026-08-28) needs a beta header | [exa--docs--highlights], [exa--changelog--2026] |
| Deep search | `deep-lite`, `deep`, `deep-reasoning` are search types, not a separate endpoint; up to 10 `additionalQueries`; `outputSchema` returns structured content with per-field `grounding` citations and confidence | [exa--api--deep-search] |
| Answer | `/answer` returns an answer with citations; `model` `exa`, `exa-pro`, `exa-research`, `exa-fast`; optional `outputSchema` | [exa--api--answer] |
| Agent | `POST /agent/runs` (2026-06-16): `query`, `effort` (`minimal` to `max`, default `auto`), `output_schema`, `input.data`, `input.exclusion`, `budget.maxCostDollars`; returns structured output with grounding and `cost_dollars` | [exa--api--agent], [exa--changelog--2026] |
| Agent guidance | Treat the query as a task spec (what, scope, evidence, completeness); bound arrays with `maxItems`; fixed effort gives predictable cost; `auto` or `max` needs `budget.maxCostDollars` | [exa--docs--agent-best-practices] |
| Websets | Search plus criteria verification plus enrichments into a verified dataset (`/websets/v0/websets/`); async results by polling or webhook. The quickstart's example enrichment is a person's LinkedIn profile | [exa--api--websets] |
| findSimilar | Absent from the current docs index, quickstart, and SDK examples; reported deprecated in favor of search (secondary source, no dated notice) | [exa--api--findsimilar], [exa--docs--llms-index], [exa--docs--api-surface-quickstart], [exa--docs--sdk-exa-py-readme] |
| MCP tools | Default: `web_search_exa`, `web_fetch_exa`. Optional: `web_search_advanced_exa`, `agent_run`. Enable with `https://mcp.exa.ai/mcp?tools=...`; an explicit list replaces the defaults. Auth: OAuth, API key, or anonymous with rate limits. Local: `npx -y exa-mcp-server` with `EXA_API_KEY` | [exa--mcp--github-readme], [exa--mcp--docs-page] |
| Legacy MCP names | `company_research_exa`, `linkedin_search_exa`, `crawling_exa`, `deep_researcher_*`, `find_similar_exa` do not appear in either official source | [exa--mcp--github-readme] |
| SDKs | `exa-py` (`search`, `get_contents`, `answer`, `stream_answer`, `stream_search`, `AsyncExa`), `exa-js` (`search`, `getContents`, `answer`) | [exa--docs--sdks-quickstart], [exa--docs--sdk-exa-py-readme] |
| Query guidance | Describe the pages you want, not keywords; put retrieval preferences in the query; record `requestId` and `costDollars` | [exa--docs--best-practices] |
| Prices (2026-09) | Search $7 per 1,000 (up to 10 results), deep types $12 to $15 per 1,000; contents $1 per 1,000 pages per content type; answer $5 per 1,000; agent fixed effort $0.012 to $1.00 per request, metered at $0.10 per ACU; agent email and phone enrichment priced per item; $10 monthly free credit | [exa--pricing--rates] |
| Rate limits | Search and answer 10 QPS; deep types 5 QPS; contents 100 QPS; agent 5 QPS plus 50 active runs (a start counts as two); websets 20 QPS; 429 rate limit, 402 credits exhausted | [exa--pricing--rate-limits] |
| Query privacy | Exa says query fields "are not intended for the submission of personal information" and query data is used to improve and train its models | [exa--legal--privacy-policy] |

## D4. Firecrawl

| Fact | Detail | Source |
|---|---|---|
| Scrape | `POST /v2/scrape`; `formats` default markdown; also `summary`, `links`, `json` (schema and/or prompt), `highlights` (query), `question`, `branding`, `screenshot`, `changeTracking`; `onlyMainContent` default true; `maxAge` default 2 days; `redactPII`; `location`; `proxy` default auto | [firecrawl--api--scrape-v2] |
| Map | Discovers URLs without scraping; `search` orders links by relevance; `sitemap` skip, include (default), or only; `limit` default 5,000, max 100,000; returns url, title, description | [firecrawl--api--map] |
| Crawl | `POST /v2/crawl`; `limit` default 10,000 pages; `includePaths`/`excludePaths` regex; `maxDiscoveryDepth`; `prompt` generates options; async job with status polling and webhooks; `ignoreRobotsTxt` enterprise-only | [firecrawl--api--crawl-post], [firecrawl--api--crawl-status] |
| Search | `POST /v2/search`; `limit` default 10, max 100 per source; `sources` web, news, images; `categories` research, pdf, developer; `tbs` time filters; `includeDomains`/`excludeDomains`; inline `scrapeOptions`. Research category moves to `data.research` on 2026-11-16 | [firecrawl--api--search] |
| Extract | `urls` in glob form, `schema`, `prompt`, `enableWebSearch`; returns a job id | [firecrawl--api--extract] |
| Agent | `/agent` "builds on" extract: `prompt` (max 10,000 chars), optional `urls`, `schema`, `effort`, `maxCredits` default 2,500, `strictConstrainToURLs`; Spark 1 deprecated, routes to `spark-2`; FIRE-1 branding retired | [firecrawl--api--agent], [firecrawl--changelog--deep-research-deprecation] |
| Deep research | Original deep-research endpoint unmaintained after 2025-06-30; use search plus agent | [firecrawl--changelog--deep-research-deprecation] |
| Batch scrape | Same scrape options and webhook contract as crawl, for a known URL list | [firecrawl--api--batch-scrape] |
| MCP tools | `firecrawl_scrape`, `firecrawl_map`, `firecrawl_crawl`, `firecrawl_check_crawl_status`, `firecrawl_search`, `firecrawl_agent`, `firecrawl_agent_status`, `firecrawl_parse`, `firecrawl_interact`, `firecrawl_credit_usage`, plus research, developer, and monitor families. No `firecrawl_extract` or `firecrawl_deep_research` in the current list. `FIRECRAWL_API_KEY` required for cloud | [firecrawl--mcp--server-github-readme] |
| Hosted MCP | `https://mcp.firecrawl.dev/v2/mcp` (API key) and `/v2/mcp-oauth`; keyless mode exposes only scrape, search, parse with daily limits | [firecrawl--mcp--hosted-remote], [firecrawl--mcp--server-github-readme] |
| SDKs | `firecrawl-py` and unscoped `firecrawl` on npm; scrape, crawl, map, search, batch scrape, agent | [firecrawl--docs--github-main-repo-readme], [firecrawl--sdk--python-methods], [firecrawl--sdk--node-methods] |
| Credits | Scrape 1 per page; JSON format +4; PDF +1; PII redaction +4; crawl 1 per page plus surcharges; map 1 per call; search 2 per 10 results plus scraped pages | [firecrawl--pricing--billing-credits], [firecrawl--pricing--plans] |
| Rate limits | Free: 10 per minute for scrape, map, search; 2 per minute for crawl and agent; 2 concurrent browsers. Hobby 100 and 20; Standard 500 and 100 | [firecrawl--pricing--rate-limits], [firecrawl--pricing--billing-credits] |
| Robots | The crawler honors robots.txt and crawl-delay; single-URL scrapes are "treated like direct visits"; responsibility for site policies and personal data rests with the user | [firecrawl--legal--robots-and-ethical-scraping] |
| Docs for agents | `llms.txt` and `llms-full.txt` published; a v1-to-v2 migration guide was not retrievable | [firecrawl--docs--introduction-and-defaults] |
| Recent changes | Highlights and Question formats (May 2026), keyless core endpoints and automatic PII redaction (v2.11, 2026-06-24), improved search relevance (2026-07-22) | [firecrawl--changelog--2026-releases] |

## D5. Legal and ethical limits

| Fact | Detail | Source |
|---|---|---|
| Minimisation | GDPR Art 5(1)(b) purpose limitation and 5(1)(c) minimisation make account- and role-level research the minimising design; named-person profiles exceed an ICP purpose | [icp--ethics--gdpr-data-minimisation-role-level] |
| Legitimate interest | Art 6(1)(f) permits processing on legitimate interest subject to balancing; Recital 47 names direct marketing as a possible legitimate interest; never self-executing | [icp--legal--gdpr-article-6-legitimate-interest] |
| Indirect collection | Art 14 requires informing people whose data was obtained indirectly; the disproportionate-effort exemption needs compensating public notice | [icp--legal--gdpr-article-14-information-duties] |
| UK ICO | Written for web scraping to train generative AI, applied here by analogy: legitimate interest is the only workable basis for scraping personal data; a generic interest is unlikely to pass the purpose test; purpose, necessity, and balancing tests; scraping is "high-risk" and "invisible" processing, so transparency is a precondition | [icp--legal--ico-web-scraping-lawful-basis] |
| EDPB | Draft, not yet binding: Guidelines 03/2026 (2026-07-14, consultation to October 2026), written for generative-AI scraping, mirror the ICO test and require public privacy information even when individual notice is excused | [icp--legal--edpb-web-scraping-guidelines] |
| Dutch AP | Commercial scraping generally cannot rely on legitimate interest; the European Commission asked for revision; the AP maintains its position pending the Court of Justice | [icp--legal--dutch-ap-scraping-guidance] |
| CCPA | B2B and employee exemptions expired 2023-01-01; California business contact data carries full consumer rights | [icp--legal--ccpa-b2b-exemption-expired] |
| Terms of service | hiQ v. LinkedIn (US, Ninth Circuit and N.D. Cal.): the Ninth Circuit held that scraping public pages likely does not violate the CFAA, but LinkedIn won on its user agreement; hiQ paid $500,000 and was enjoined | [icp--legal--hiq-v-linkedin] |
| robots.txt | Not binding by itself, but strong good-faith evidence in contract and trespass disputes; honor it by default, throttle, identify the crawler, read the terms | [icp--legal--robots-txt-signal] |

## D6. Conflicts and gaps

| ID | Conflict or gap | Readings | Preferred |
|---|---|---|---|
| C1 | Commercial scraping of personal data under GDPR | ICO and draft EDPB: legitimate interest can work with a three-part test [icp--legal--ico-web-scraping-lawful-basis], [icp--legal--edpb-web-scraping-guidelines]. Dutch AP: generally cannot [icp--legal--dutch-ap-scraping-guidance] | Avoid the question by design: collect no personal data. Account- and role-level evidence only |
| C2 | Exa MCP tool roster | Older integrations reference many named tools; both official sources list four [exa--mcp--github-readme], [exa--mcp--docs-page] | Discover tools at run time; map capabilities, not names |
| C3 | findSimilar status | Absent from current docs; deprecation stated only by a secondary source [exa--api--findsimilar] | Use search with a descriptive query for lookalikes; with `category: "company"`, filter the company's own domain out of results afterward, because that category does not support `excludeDomains` |
| C4 | Firecrawl map credit wording | "1 per page" on pricing summary versus "1 per call" on billing [firecrawl--pricing--plans], [firecrawl--pricing--billing-credits] | Budget as one call; verify with `firecrawl_credit_usage` |
| C5 | Stated versus revealed ICP | Vendor ICP guides build from existing best-fit customers [icp--method--icp-definition]; public research sees marketing claims and partial customer evidence | Grade revealed evidence (customers, reviews, hiring, pricing structure) above stated copy |
| G1 | No official Exa acceptable-use text | Terms PDF did not parse | Apply the privacy-policy query rule and GDPR minimisation |
| G2 | G2 segment thresholds | Only secondary figures (up to 50, 51 to 1,000, 1,001+) | Report bands as read from the page, not normalized thresholds |
| G3 | Websets criteria and enrichment formats | Reference page returned 404 | Use Websets only for company lists with company-level enrichments |
| G4 | Firecrawl extract status path and v1-to-v2 guide | Not captured | Prefer scrape with `json` format or agent with `maxCredits` |
| G5 | Intent data | Third-party intent and first-party engagement are proprietary [icp--signals--intent-trigger-signals] | Report fit and public timing signals only; never claim intent |
| G6 | No primary JTBD methodology source | Buying-committee source covers roles | Frame pains and jobs from customer evidence; label as synthesis |

## Source index

| ID | Title | URL | Fetched | Source type |
|---|---|---|---|---|
| exa--api--agent | Exa Agent API (async research, list-building, enrichment) | https://exa.ai/docs/agent/quickstart.md | 2026-09-23 | official-docs |
| exa--api--answer | Exa Answer API Reference | https://exa.ai/docs/reference/answer | 2026-09-23 | official-docs |
| exa--api--contents | Exa Contents API Reference | https://exa.ai/docs/reference/get-contents | 2026-09-23 | official-docs |
| exa--api--deep-search | Exa Deep Search (deep / deep-reasoning search types) | https://exa.ai/docs/search/deep-search.md | 2026-09-23 | official-docs |
| exa--api--findsimilar | Exa findSimilar Endpoint (deprecated in favor of Search) | https://exa.ai/docs/reference/find-similar-links | 2026-09-23 | official-docs |
| exa--api--search | Exa Search API Reference | https://exa.ai/docs/reference/search | 2026-09-23 | official-docs |
| exa--api--websets | Exa Websets (verified, enriched web datasets) | https://exa.ai/docs/websets/quickstart.md | 2026-09-23 | official-docs |
| exa--changelog--2026 | Exa Changelog (in-window entries, March-September 2026) | https://exa.ai/docs/changelog.md | 2026-09-23 | official-docs |
| exa--docs--agent-best-practices | Exa Agent Best Practices | https://exa.ai/docs/agent/best-practices.md | 2026-09-23 | official-docs |
| exa--docs--api-surface-quickstart | Exa API Surface Overview (Quickstart) | https://exa.ai/docs/reference/quickstart | 2026-09-23 | official-docs |
| exa--docs--best-practices | Exa Search Best Practices | https://exa.ai/docs/search/best-practices.md | 2026-09-23 | official-docs |
| exa--docs--highlights | Exa Highlights Feature | https://exa.ai/docs/search/highlights.md | 2026-09-23 | official-docs |
| exa--docs--llms-index | Exa Documentation Index (llms.txt) | https://exa.ai/docs/llms.txt | 2026-09-23 | official-docs |
| exa--docs--sdk-exa-py-readme | exa-py GitHub README (SDK method examples) | https://raw.githubusercontent.com/exa-labs/exa-py/master/README.md | 2026-09-23 | official-docs |
| exa--docs--sdks-quickstart | Exa SDKs (exa-py / exa-js) Quickstart | https://exa.ai/docs/sdks/quickstart.md | 2026-09-23 | official-docs |
| exa--legal--privacy-policy | Exa Labs Privacy Policy (personal data / people-search relevant clauses) | https://exa.ai/privacy-policy | 2026-09-23 | official-docs |
| exa--mcp--docs-page | Exa MCP - Official Docs Page | https://exa.ai/docs/get-started/exa-mcp.md | 2026-09-23 | official-docs |
| exa--mcp--github-readme | Exa MCP Server - GitHub README (exa-labs/exa-mcp-server) | https://raw.githubusercontent.com/exa-labs/exa-mcp-server/master/README.md | 2026-09-23 | official-docs |
| exa--pricing--rate-limits | Exa Rate Limits | https://exa.ai/docs/admin/rate-limits | 2026-09-23 | official-docs |
| exa--pricing--rates | Exa Pricing | https://exa.ai/docs/admin/pricing.md | 2026-09-23 | official-docs |
| firecrawl--api--agent | Agent - Firecrawl Docs | https://docs.firecrawl.dev/features/agent | 2026-09-23 | official-docs |
| firecrawl--api--batch-scrape | Batch Scrape - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/batch-scrape | 2026-09-23 | official-docs |
| firecrawl--api--crawl-post | Crawl - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/crawl-post | 2026-09-23 | official-docs |
| firecrawl--api--crawl-status | Get Crawl Status - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/crawl-get | 2026-09-23 | official-docs |
| firecrawl--api--extract | Extract - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/extract | 2026-09-23 | official-docs |
| firecrawl--api--map | Map - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/map | 2026-09-23 | official-docs |
| firecrawl--api--scrape-v2 | Scrape - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/scrape | 2026-09-23 | official-docs |
| firecrawl--api--search | Search - Firecrawl Docs | https://docs.firecrawl.dev/api-reference/endpoint/search | 2026-09-23 | official-docs |
| firecrawl--changelog--2026-releases | Changelog - Firecrawl | https://www.firecrawl.dev/changelog | 2026-09-23 | official-docs |
| firecrawl--changelog--deep-research-deprecation | Deep Research (Alpha, Legacy v1) - Firecrawl Docs | https://docs.firecrawl.dev/features/alpha/deep-research | 2026-09-23 | official-docs |
| firecrawl--docs--github-main-repo-readme | Firecrawl (main repo README) | https://github.com/firecrawl/firecrawl | 2026-09-23 | official-docs |
| firecrawl--docs--introduction-and-defaults | Introduction - Firecrawl Docs | https://docs.firecrawl.dev/introduction | 2026-09-23 | official-docs |
| firecrawl--legal--robots-and-ethical-scraping | Firecrawl and robots.txt / ethical scraping (glossary pages) | https://www.firecrawl.dev/glossary/web-crawling-apis/what-is-robots-txt-protocol | 2026-09-23 | official-docs |
| firecrawl--mcp--hosted-remote | MCP Server - Firecrawl Docs | https://docs.firecrawl.dev/mcp-server | 2026-09-23 | official-docs |
| firecrawl--mcp--server-github-readme | Firecrawl MCP Server (GitHub README) | https://github.com/mendableai/firecrawl-mcp-server/ | 2026-09-23 | official-docs |
| firecrawl--pricing--billing-credits | Billing - Firecrawl Docs | https://docs.firecrawl.dev/billing | 2026-09-23 | official-docs |
| firecrawl--pricing--plans | Pricing - Firecrawl | https://www.firecrawl.dev/pricing | 2026-09-23 | official-docs |
| firecrawl--pricing--rate-limits | Rate Limits - Firecrawl Docs | https://docs.firecrawl.dev/rate-limits | 2026-09-23 | official-docs |
| firecrawl--sdk--node-methods | Node SDK - Firecrawl Docs | https://docs.firecrawl.dev/sdks/node | 2026-09-23 | official-docs |
| firecrawl--sdk--python-methods | Python SDK - Firecrawl Docs | https://docs.firecrawl.dev/sdks/python | 2026-09-23 | official-docs |
| icp--ethics--gdpr-data-minimisation-role-level | GDPR Article 5(1) - Principles Relating to Processing of Personal Data (Purpose Limitation, Data Minimisation) | https://gdpr-info.eu/art-5-gdpr/ | 2026-09-23 | official-docs |
| icp--legal--ccpa-b2b-exemption-expired | California Consumer Privacy Act: Employee and B2B Exemptions Expire January 1, 2023 | https://www.morganlewis.com/pubs/2022/10/california-consumer-privacy-act-employee-and-b2b-exemptions-expire-january-1-2023 | 2026-09-23 | vendor-blog |
| icp--legal--dutch-ap-scraping-guidance | Dutch DPA Issues Guidelines on Data Scraping | https://www.hlc.com/en/publications/dutch-dpa-issues-guidelines-on-data-scraping_1 | 2026-09-23 | vendor-blog |
| icp--legal--edpb-web-scraping-guidelines | EDPB Guidelines 03/2026 on Web Scraping in the Context of Generative AI (via Reed Smith commentary) | https://www.reedsmith.com/our-insights/blogs/technology-law-dispatch/102nbqu/edpb-web-scraping-guidelines-for-ai-making-the-impossible-possible/ | 2026-09-23 | vendor-blog |
| icp--legal--gdpr-article-14-information-duties | GDPR Article 14 - Information to be Provided Where Personal Data Have Not Been Obtained From the Data Subject | https://gdpr-info.eu/art-14-gdpr/ | 2026-09-23 | official-docs |
| icp--legal--gdpr-article-6-legitimate-interest | GDPR Article 6(1)(f) - Lawfulness of Processing (Legitimate Interests) | https://gdpr-info.eu/art-6-gdpr/ | 2026-09-23 | official-docs |
| icp--legal--hiq-v-linkedin | hiQ Labs v. LinkedIn | https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn | 2026-09-23 | community |
| icp--legal--ico-web-scraping-lawful-basis | The Lawful Basis for Web Scraping to Train Generative AI Models | https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/the-lawful-basis-for-web-scraping-to-train-generative-ai-models/ | 2026-09-23 | regulator |
| icp--legal--robots-txt-signal | Robots.txt Scraping: Rules, Ethics, and Policy Explained | https://www.promptcloud.com/blog/robots-txt-scraping-compliance-guide/ | 2026-09-23 | vendor-blog |
| icp--method--buying-committee-roles | B2B Buying Committees: How to Target Decision Makers | https://www.influ2.com/academy/buying-committees | 2026-09-23 | vendor-blog |
| icp--method--icp-definition | Ideal Customer Profiles (ICPs): Benefits & How to Create | https://www.salesforce.com/sales/ideal-customer-profile/ | 2026-09-23 | vendor-blog |
| icp--method--icp-vs-buyer-persona | Ideal Customer Profiles and Buyer Personas: How Are They Different? | https://blog.hubspot.com/customers/ideal-customer-profiles-and-buyer-personas-are-they-different | 2026-09-23 | vendor-blog |
| icp--method--reverse-engineer-competitor-icp-jobs | I've Been Tracking Competitor Job Postings for 6 Months. Here's What I Learned. | https://dev.to/vhub_systems_ed5641f65d59/ive-been-tracking-competitor-job-postings-for-6-months-heres-what-i-learned-46i9 | 2026-09-23 | community |
| icp--method--tiering-fit-scoring | How to Segment & Tier Accounts for Effective ABM Programs | https://hginsights.com/blog/account-segmentation-tiering | 2026-09-23 | vendor-blog |
| icp--signals--g2-reviewer-segments | G2 Market Intelligence: Firmographic Filters and Reviewer Segments | https://documentation.g2.com/docs/market-intelligence | 2026-09-23 | official-docs |
| icp--signals--intent-trigger-signals | What are Intent Signals? B2B Buying Signals Glossary | https://6sense.com/glossary/b2b-buying-signals/ | 2026-09-23 | vendor-blog |
| icp--signals--job-postings-sales-titles | Sales Careers at Salesforce (Territory Account Executive - SMB / Enterprise AE listings) | https://careers.salesforce.com/en/jobs/jr274177/territory-account-executive-smb/ | 2026-09-23 | vendor-blog |
| icp--signals--negative-icp-disqualifiers | ICP Scoring Criteria for B2B Sales: Framework and Template | https://www.searcle.ai/insights/icp-scoring-criteria-b2b-sales | 2026-09-23 | vendor-blog |
| icp--signals--pricing-page-signals | The SaaS Pricing Page Playbook: Practices and Real Examples | https://www.webstacks.com/blog/saas-pricing-page-design | 2026-09-23 | vendor-blog |
| icp--signals--technographic-signals | Setting Up Your Martech Stack and Activating Your ICP | https://clearbit.com/resources/books/b2b-data/setting-up-your-martech-stack | 2026-09-23 | vendor-blog |
| icp--template--case-studies-customer-logos | Using Case Studies to Infer a Vendor's Ideal Customer Profile | https://breadcrumbs.io/blog/case-study-examples/ | 2026-09-23 | vendor-blog |
