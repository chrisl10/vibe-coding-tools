# Rendered web evidence cases

These are actual written reviews of preserved source bytes. Case A reviews publicly retrieved provider documentation. Case B exercises explicitly fictional supplied vendor facts; no vendor runtime call or market conclusion occurred. Paths below resolve from this example directory. The existing helper only checks its fixed JSON bookkeeping and hashes.

## Case A: Documentation contract, not runtime proof

Question: What must a research receipt distinguish when using Exa or Firecrawl? Domain scope: official `exa.ai` and `docs.firecrawl.dev` documentation, three exact public documentation URLs. Acquisition: public urllib GET, UTC timestamps/status/resolved URLs and hashes in the [manifest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/growth-and-customer-tools/skills/competitive-research-stinger/references/research/2026-10-web-evidence/raw/manifest.json). The native web tool opened the corresponding public pages separately for human-readable inspection; no provider API credential/request was used. The retained capture is the public documentation GET, not a saved provider response or full browser trace.

| Claim | Class | Passage locator | Decision |
|---|---|---|---|
| Exa documentation exposes domain restrictions | vendor_claim about documented API | [Exa capture](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/growth-and-customer-tools/skills/competitive-research-stinger/references/research/2026-10-web-evidence/raw/exa-search.md), `includeDomains` schema | Supported as documentation, actual connector acceptance untested |
| Firecrawl documents separate target page status | vendor_claim about documented API | [Scrape capture](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/growth-and-customer-tools/skills/competitive-research-stinger/references/research/2026-10-web-evidence/raw/firecrawl-scrape.md), Response metadata and status codes | API success does not establish target-page content |
| Firecrawl cache bypass proves the product's current state | unsupported inference | Same capture, Freshness and item status | Rejected: cache policy and represented state differ |
| Both providers restrict domains in identical syntax | unsupported inference | Exa `includeDomains`; [Search capture](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/growth-and-customer-tools/skills/competitive-research-stinger/references/research/2026-10-web-evidence/raw/firecrawl-search.md), Domain Filters | Rejected: documented path handling differs |

Retrieval date is known; original publication dates are unknown. Re-read actual available tool contracts before use. No claims about search quality, costs, coverage, account readiness or current competitor prices follow from this case.

## Case B: Supplied contradictory and partial sources

Question: Among three fictional Basic/Starter account plans, which supplied facts support SAML SSO inclusion? Research date 2026-10-07; USD account/month; two dated Birch revisions are one entity. All source URLs use reserved `.example` domains and were not fetched. Input is [supplied JSON](supplied-competitive-evidence.json), captures are in [captures](captures/vendor-a.txt).

| Entity | Current scoped supplied claim | Support / limit | Comparable inclusion row |
|---|---|---|---|
| Atlas | Starter includes SAML SSO | [vendor-a](captures/vendor-a.txt), line 3; fictional vendor statement only | Yes |
| Birch | Basic excludes SAML SSO, Enterprise includes it | [current](captures/vendor-b-current.txt), line 3; [old](captures/vendor-b-old.txt), line 3 states inclusion on earlier effective date | No for Basic; historical contradiction retained |
| Cedar | Unknown | [partial](captures/vendor-c-partial.txt), lines 2-3; relevant passage missing | Unknown, excluded from known denominator |

Computed from the displayed supplied rows: 3 entities, 2 known comparable current statements, 1 unknown. Positive inclusion among known statements = 1 / 2 = 50%; known negatives = 1 / 2 = 50%. The old Birch revision adds no fourth entity and no second positive. These percentages describe this fictional fixture only. Price growth, market share, actual feature availability and buyer preference were not established. The partial Cedar capture supports extraction incompleteness only.

Unreachable variant: if an authorized acquisition returns a denied target-page status, preserve that actual status/error receipt without a nonexistent page hash; dependent facts stay unknown. This branch is a procedural supplied-case expectation, not an actual denied network request here. If plan/date scope cannot resolve contradictory sources, report disputed and exclude from settled-value arithmetic.

Run against the resolved skill root:

```text
python3 -B scripts/competitive_evidence.py examples/web-research-evidence/supplied-competitive-evidence.json --verify-archives
```

Exit 0 establishes mechanical consistency and four matching capture hashes. It does not establish the statements' truth, current state or representativeness. The richer acquisition and passage receipt remains a companion Markdown document, never extra unsupported JSON fields.
