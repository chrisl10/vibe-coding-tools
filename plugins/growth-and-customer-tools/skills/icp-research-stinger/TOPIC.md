# ICP Research Stinger Topic Record

- Component type: Stinger, paired with `icp-research-wasp-drone`
- Domain: evidence-backed Ideal Customer Profile (ICP) identification for one company, starting from its domain and fanning out across the public web with Exa and Firecrawl
- Question answered: "Given `example.com`, who are this company's ideal customers, and how sure are we?" The output describes the accounts and buying roles the company sells to best, with every claim graded by independent evidence
- Trigger boundary: use for ICP discovery, account targeting research, reverse-engineering a company's or competitor's customer base, segment and persona definition, and go-to-market research seeded by a domain
- Exclusions: ICP inside a website-audit engagement (`icp-positioning-stinger` in the website-auditor pack owns wave W2 and its hard gate); competitor workbooks and battlecards (`competitive-research-stinger`); outbound sequences (`cold-outreach-stinger`); CRM sync and enrichment pipelines (`crm-integration-stinger`); ICP built from a company's own CRM or closed-won data (internal analytics, not web research); person-level lead lists or dossiers on named individuals (never in scope)
- Harness targets: Claude Code, Cursor, ChatGPT Codex, and Claude Cowork
- Focus: research-only. The Stinger produces a dossier and an evidence ledger, not code committed to a product repository, so it carries no Ship Gate. The forge's own changes to this repository still pass the Ship Gate
- Research window: 2026-03-23 through 2026-09-23, retrieval at the cutoff
- Source policy: official Exa and Firecrawl documentation and repositories for tool facts; regulators and official guidance for legal limits; established vendor and practitioner sources for ICP methodology, labeled for bias
- Tool policy: Exa and Firecrawl through MCP or API, whichever the harness exposes; a labeled degraded mode with generic web search and fetch when neither is available. Tool names and parameters are dated observations; verify against the live tool list at run time
- Privacy policy: account-level and role-level only. No personal contact data, no personal profile pages, no compilation of information about named individuals

## Outcomes

The Stinger must equip its paired Drone to:

1. Normalize a domain into a research brief with a purpose, budget, and stop conditions.
2. Discover and prioritize the company's own pages (map, then scrape pricing, customers, industries, integrations, careers, security, docs).
3. Fan out off-site in parallel lanes: customers, market and competitors, hiring, voice of customer, news and funding, technographic.
4. Separate what the company says (stated) from who actually buys (revealed) and weigh revealed evidence higher.
5. Record every signal in a validated evidence ledger and grade each ICP claim by independent sources.
6. Synthesize firmographics, segments and tiers, buying committee roles, pains and jobs, triggers, and disqualifiers.
7. Report confidence honestly, including contested claims and missing lanes.
8. Control cost and rate limits for Exa and Firecrawl and degrade gracefully without them.
9. Stay inside legal and ethical limits for web research on companies and people.
10. Hand results to outreach, CRM, competitive, and positioning peers in a reusable format.
