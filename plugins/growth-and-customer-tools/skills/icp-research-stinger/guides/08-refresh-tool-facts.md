# 08: Refresh tool facts

Exa and Firecrawl changed materially inside this Stinger's six-month research window: new search types and categories, retired MCP tools, deprecated endpoints, new agent products (D3, D4). Treat [references/TOOLS.md](../references/TOOLS.md) as a dated snapshot (2026-09-23).

## Before a run

- List the session's tools (guide 02). If a name in TOOLS.md is missing or a new one appears, trust the session and note the difference in the lane notes.

## When maintaining this Stinger

1. Fetch the current primary sources: Exa docs index (`exa.ai/docs/llms.txt`), search, contents, agent, MCP pages, pricing, rate limits, changelog; Firecrawl docs (`docs.firecrawl.dev`), MCP server README, billing, rate limits, changelog.
2. Keep working captures outside this skill (this Stinger ships the distillation only, by owner decision on 2026-09-23). Give each new source an ID and add it to the Source index at the end of the distillation with URL, fetch date, and source type.
3. Update `references/research/distilled-icp-research.md` rows with citations to those IDs; record new conflicts rather than silently choosing.
4. Update `references/TOOLS.md`, the recipes in `examples/01-tool-call-recipes.md`, and any guide that named a changed tool or parameter.
5. Run `python scripts/icp_ledger.py --self-test` and the repository validator.

Prices and rate limits are the fastest-changing facts; never quote them as current without a refresh.
