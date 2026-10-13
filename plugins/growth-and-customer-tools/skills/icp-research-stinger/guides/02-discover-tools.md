# 02: Discover and bind tools

Vendor tool rosters change fast: Exa's MCP server now exposes two default tools where older integrations listed many, and Firecrawl's MCP server no longer lists extract or deep-research tools (D3, D4, C2). Bind by capability, never by remembered name.

## Procedure

1. List the tools this session actually exposes. Look for Exa (`web_search_exa`, `web_fetch_exa`, optionally `web_search_advanced_exa`, `agent_run`), Firecrawl (`firecrawl_*`), and generic web search and fetch.
2. For each capability in [references/TOOLS.md](../references/TOOLS.md), record which tool provides it in the research brief. Read each chosen tool's input schema; map the documented API fields in [examples/01-tool-call-recipes.md](../examples/01-tool-call-recipes.md) onto it.
3. If an MCP server is connected but a needed optional tool is not enabled (for example Exa's `web_search_advanced_exa` for domain filters), use the default tools and note the limitation. Enabling tools or adding API keys changes the user's configuration: ask first.
4. If a direct API is available (API key present in the environment, network allowed), it may replace an MCP tool, but never print, log, or write the key, and never put it in a URL (Exa's hosted MCP accepts `?exaApiKey=`; prefer OAuth or a header).
5. With neither Exa nor Firecrawl, choose degraded mode: generic search and fetch, same lanes, `tool` set to `websearch` or `webfetch` in the ledger, and "degraded mode" stated in the dossier.
6. Make one cheap test call (a single search or a single fetch of the homepage) and confirm the response shape before starting lanes.

## Cost and rate guards

- Record `costDollars` (Exa) or `creditsUsed` (Firecrawl) from every response in the lane notes when present; check `firecrawl_credit_usage` between lanes if available.
- On 429, back off and slow down; on 402 or credit exhaustion, stop the lane and report (D3, D4).
- Never start a Firecrawl crawl without `limit`, or an agent run without `maxCredits` or `budget.maxCostDollars` (D3, D4).
