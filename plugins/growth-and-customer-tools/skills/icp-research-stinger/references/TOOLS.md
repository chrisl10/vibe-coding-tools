# Tool capability map: Exa, Firecrawl, and fallback

Load this before the first research call. Tool names, parameters, prices, and limits are observations dated 2026-09-23 from [research/distilled-icp-research.md](research/distilled-icp-research.md) (sections in brackets). Harnesses expose tools differently, so map **capabilities**, then bind each to whatever the session actually has. Never call a tool name from memory; list the session's tools first ([guides/02-discover-tools.md](../guides/02-discover-tools.md)).

## Capabilities the pipeline needs

| Capability | Used for | Exa | Firecrawl | Degraded fallback |
|---|---|---|---|---|
| Discover a site's URLs | Seed lane page inventory | none (use search with the domain in `includeDomains`) | `map` with `search`, `limit` [D4] | fetch `/sitemap.xml`, then the homepage links |
| Fetch clean page text | Reading pages | `/contents` or MCP `web_fetch_exa` [D3] | `scrape` markdown or MCP `firecrawl_scrape` [D4] | generic web fetch |
| Query-focused excerpts | Cheap evidence quotes | `/contents` `highlights` with `query` [D3] | `scrape` `highlights` format with `query` [D4] | fetch plus manual excerpt |
| Structured extraction | Pricing tiers, customer lists | `/contents` `summary` with `schema`; deep search `outputSchema` [D3] | `scrape` `json` format with `schema` (+4 credits per page) [D4] | fetch plus manual extraction |
| Web search | Off-site lanes | `/search` or MCP `web_search_exa` / `web_search_advanced_exa` [D3] | `search` or MCP `firecrawl_search` [D4] | generic web search |
| Company-type results | Customer firmographics, lookalikes | `/search` `category: "company"` [D3] | none | web search with descriptive query |
| News with dates | Triggers, funding, launches | `/search` `category: "news"` plus published dates [D3] | `search` with `sources: ["news"]`; the `tbs` time filter is documented on the `web` source [D4] | web search with date words |
| Multi-step research | Optional deep pass | `/agent/runs` or MCP `agent_run` with `budget.maxCostDollars` [D3] | `/agent` or MCP `firecrawl_agent` with `maxCredits` [D4] | run the lanes manually |
| Credit check | Budget guard | response `costDollars` / `cost_dollars` [D3] | MCP `firecrawl_credit_usage`, response `creditsUsed` [D4] | none |

Prefer the cheapest capability that answers the question: map and highlights before full scrapes; full scrapes before structured extraction; structured extraction before agents.

## Exa specifics [D3]

| Topic | Rule |
|---|---|
| MCP tools | Defaults `web_search_exa`, `web_fetch_exa`; optional `web_search_advanced_exa`, `agent_run`, enabled by `https://mcp.exa.ai/mcp?tools=...` (an explicit list replaces the defaults) |
| Names absent from current docs | Do not call `company_research_exa`, `linkedin_search_exa`, `crawling_exa`, `deep_researcher_*`, `find_similar_exa` unless the session lists them; neither official source mentions them (C2) |
| Search type | `fast` or `auto` for lane queries; `deep` or `deep-reasoning` only for the optional synthesis pass (5 QPS, higher price) |
| Categories | `company` for firmographics and lookalikes; `news` for triggers. **Never `people`** (privacy rule below) |
| Filters | `excludeDomains: [<company domain>]` for off-site lanes, but never with `category: "company"` or `"people"`, which do not support it or date filters; filter those results afterward. `includeDomains` to pin review sites, job boards, or a customer's own site |
| Deprecated | `includeText`/`excludeText`, `livecrawl`, `context`, `research paper` category, findSimilar endpoint (absent from current docs; deprecation reported only by a secondary source, C3) |
| Queries | Describe the page you want ("case study of a mid-market logistics company using <product>"), not keyword bags |
| Freshness | `maxAgeHours: 0` only when freshness matters (pricing, careers); otherwise accept cache |
| Cost (2026-09) | Search $7 per 1,000; deep $12 to $15 per 1,000; contents $1 per 1,000 pages per content type; agent fixed effort $0.012 to $1.00 per request |
| Limits | Search 10 QPS, deep 5 QPS, contents 100 QPS, agent 5 QPS and 50 active runs; 429 means slow down, 402 means stop and report |

## Firecrawl specifics [D4]

| Topic | Rule |
|---|---|
| MCP tools | `firecrawl_map`, `firecrawl_scrape`, `firecrawl_search`, `firecrawl_crawl` + `firecrawl_check_crawl_status`, `firecrawl_agent` + `firecrawl_agent_status`, `firecrawl_credit_usage` |
| Names absent from current docs | No `firecrawl_extract` or `firecrawl_deep_research` in the current MCP list (not formally listed as deprecated); deep research is unmaintained; FIRE-1 is now `/agent` on `spark-2` |
| Map first | `map` with `search: "pricing"`, `"customers"`, `"careers"` and so on costs one call and ranks URLs |
| Scrape defaults | `formats: ["markdown"]`, `onlyMainContent: true`; add `highlights` with a query for long pages |
| JSON extraction | +4 credits per page; reserve for pricing and customer-list pages |
| Crawl | Avoid; if needed, always set `limit` (default is 10,000 pages) and `includePaths` |
| Agent | Always set `maxCredits` (default 2,500) and `urls` with `strictConstrainToURLs` when possible |
| Credits (2026-09) | Scrape 1 per page; JSON +4; PDF +1; PII redaction +4; map 1 per call (C4); search 2 per 10 results plus scraped pages |
| Limits (Free) | 10 per minute for scrape, map, search; 2 per minute for crawl and agent; 2 concurrent browsers |
| Robots | Crawls honor robots.txt; single scrapes do not check it for you, so this Stinger checks it ([guides/03-seed-from-domain.md](../guides/03-seed-from-domain.md)) |

## Privacy rules that bind every tool

1. Queries, schemas, and enrichments name **companies and roles**, never people. Exa states its query fields are not for personal information and query data trains its models [D3].
2. Never use Exa `category: "people"`, Websets person enrichments, agent email or phone enrichment, or personal profile URLs [D3, D5].
3. Never request contact details. If a fetched page contains them, do not copy them into notes or the ledger; `scripts/icp_ledger.py` rejects emails, common phone formats, and LinkedIn, Facebook, and Instagram personal profile URLs; it cannot detect names, so these rules remain the main control.
4. Honor robots.txt and site terms by default; skip platforms whose terms prohibit automated collection (D5, hiQ v. LinkedIn).

## Degraded mode

With neither Exa nor Firecrawl available, run the same lanes with the session's generic search and fetch tools, cap each lane at its page budget, and set `tool: "websearch"` or `"webfetch"` in the ledger. State "degraded mode" in the dossier header; confidence ceilings do not change, but coverage usually drops.
