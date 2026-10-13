# Example 01: tool call recipes per lane

Request bodies below use the documented API field names (distillation D3 and D4, dated 2026-09-23). MCP tools wrap the same capabilities, but their argument names are defined by each server's tool schema: read the schema the session exposes and map these fields onto it. `<co>`, `<domain>`, and `<category>` come from the seed brief.

## Onsite lane

Firecrawl map, ranked by relevance (one call per page class):

```json
{ "url": "https://<domain>", "search": "pricing plans", "sitemap": "include", "limit": 50 }
```

Firecrawl scrape of the pricing page, markdown plus a structured pass (the JSON format adds 4 credits):

```json
{
  "url": "https://<domain>/pricing",
  "formats": [
    { "type": "markdown" },
    { "type": "json", "schema": {
        "type": "object",
        "properties": {
          "plans": { "type": "array", "items": { "type": "object", "properties": {
            "name": { "type": "string" },
            "price_text": { "type": "string" },
            "seat_or_usage_limit": { "type": "string" },
            "security_features": { "type": "array", "items": { "type": "string" } },
            "contact_sales": { "type": "boolean" } } } }
        } } }
  ],
  "onlyMainContent": true,
  "maxAge": 0
}
```

Without Firecrawl, Exa contents with a schema-shaped summary:

```json
{ "urls": ["https://<domain>/pricing"], "summary": { "query": "plan names, prices, seat limits, SSO or SCIM or audit log availability, contact-sales tiers", "schema": { "type": "object", "properties": { "plans": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "price_text": { "type": "string" }, "security_features": { "type": "array", "items": { "type": "string" } }, "contact_sales": { "type": "boolean" } } } } } } }, "maxAgeHours": 0 }
```

## Customers lane

Exa company search for a named customer's own site:

```json
{ "query": "company website of <customer name>, a <industry hint> organization", "type": "fast", "category": "company", "numResults": 3 }
```

Exa contents with highlights on the customer's about page:

```json
{ "urls": ["https://<customer-domain>/about"], "highlights": { "query": "number of employees, locations, industry, regions served", "maxCharacters": 1200 } }
```

Third-party customer stories, excluding the company's own domain:

```json
{ "query": "case study describing how a customer uses <co> for <use case>", "type": "auto", "excludeDomains": ["<domain>"], "numResults": 10, "contents": { "highlights": true } }
```

## Market lane

The `company` category does not support `excludeDomains` or date filters (D3): send the query without them and drop the company's own domain from the results.

```json
{ "query": "companies offering <category> software for <stated audience>", "type": "auto", "category": "company", "numResults": 15 }
```

Firecrawl search for comparison pages:

```json
{ "query": "<co> alternatives comparison", "limit": 10, "sources": ["web"] }
```

## Hiring lane

```json
{ "url": "https://<domain>/careers", "formats": [{ "type": "highlights", "query": "sales, account executive, customer success roles with segment, territory, or industry" }] }
```

## Voice lane

```json
{ "query": "user reviews of <co> describing the problems it solved and company size", "type": "auto", "includeDomains": ["g2.com", "capterra.com", "trustradius.com"], "numResults": 10, "contents": { "highlights": true } }
```

## News lane

```json
{ "query": "news about <co> funding, acquisitions, product launches, or expansion", "type": "fast", "category": "news", "startPublishedDate": "<18 months ago, ISO 8601>", "numResults": 15 }
```

Firecrawl equivalent: `{ "query": "<co> funding, acquisition, or launch", "sources": ["news"], "limit": 15 }`. For a time window, the documented filter `tbs` belongs to the `web` source object, for example `"sources": [{ "type": "web", "tbs": "qdr:y" }]`; confirm the object form in the live search reference before relying on it.

## Optional deep pass with a hard budget

Exa deep search with account-level fields only:

```json
{
  "query": "Which kinds of organizations buy <co>'s <category> product, by industry, company size, and region? Use customer stories, reviews, and job postings as evidence.",
  "type": "deep",
  "outputSchema": { "type": "object", "properties": {
    "industries": { "type": "array", "maxItems": 5, "items": { "type": "string" } },
    "company_size_bands": { "type": "array", "maxItems": 3, "items": { "type": "string" } },
    "regions": { "type": "array", "maxItems": 5, "items": { "type": "string" } } } }
}
```

Firecrawl agent, capped: `{ "prompt": "<same question>", "maxCredits": 300, "effort": "low" }`. Exa agent: `{ "query": "<same question>", "effort": "low", "budget": { "maxCostDollars": 1 } }`, or `"effort": "auto"` with the same budget (guide 02: never run an agent without a budget).

Every field these return becomes ledger items tied to the cited URLs. The schemas never contain people, names, or contact fields.
