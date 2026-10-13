# ICP research decision reference

Decision tables behind the guides. Rows trace to [research/distilled-icp-research.md](research/distilled-icp-research.md) (sections `D1` to `D6`). Rows marked **derived** are this Stinger's operating choices built from documented primitives, not vendor or regulator statements.

## 1. Depth modes (derived)

| Mode | Use when | Lanes | Page budget | Customers profiled | Deep pass |
|---|---|---|---|---|---|
| Quick | A first read before a call; one analyst, minutes | onsite, customers, hiring | 25 pages | up to 8 | no |
| Standard (default) | Account planning, targeting, positioning input | all seven | 80 pages | up to 20 | optional |
| Deep | Market entry, a board or investor memo, a competitor's ICP | all seven, second pass on weak claims | 200 pages | up to 40 | yes, with a hard budget |

Split the page budget roughly: onsite 20%, customers 30%, others share the rest. Cost estimates for a run come from [TOOLS.md](TOOLS.md): for example, a Standard run with Firecrawl is about 80 scrape credits plus about a dozen map calls (one per page class) and search calls, with JSON extraction adding 4 credits per page used [D4]; with Exa, 20 to 40 searches plus contents for about 80 pages [D3]. Always state the budget in the brief and the spend in the dossier.

## 2. Execution shapes

| Situation | Shape |
|---|---|
| Orchestrator with subagents available | Run the onsite lane first (one Drone or inline), then dispatch one armed `icp-research-wasp-drone` per remaining lane **in parallel from the top level**, each with the seed brief and a lane brief from `templates/lane-brief.md`. Subagents do not spawn further subagents |
| Single agent (a dispatched Drone, or no subagents) | Run onsite, then run the remaining lanes in batches of parallel tool calls, writing each lane's ledger file as it completes |
| No Exa or Firecrawl | Degraded mode with generic search and fetch ([TOOLS.md](TOOLS.md)); same lanes, same ledger |

## 3. Which evidence outranks which

| Evidence | Weight in synthesis | Why |
|---|---|---|
| Named customers' own sites and third-party customer stories | Highest | Revealed buyers, independent domains [D2] |
| Review-site segment data | High | Verified reviewer firmographics [D2] |
| Sales job titles and territories | High | The company's own GTM segmentation, revealed [D2] |
| Pricing structure (security features, gating) | High | Structural signal [D2]; harder to change than copy (**derived** rationale) |
| Integrations and marketplaces | Medium | Technographic fit and compatibility [D1] |
| News and funding | Medium | Stage and timing, not fit [D1] |
| Homepage and marketing copy | Lowest | Stated, aspirational; useful to find the positioning gap (C5) |

## 4. Turning graded claims into the ICP

| Dossier section | Built from |
|---|---|
| Primary ICP | Strong claims across industry, employee_band, geography, business_model, and segment that co-occur in the customers lane |
| Secondary segments and tiers | Moderate claims and distinct clusters in the customer distribution; tier by fit strength and apparent deal size [D1] |
| Technographic profile | technographic claims; compatibility versus displacement noted separately [D1] |
| Buying committee | persona claims mapped to economic buyer, champion, technical buyer, end user, procurement, executive sponsor [D1]; committee size expectation from the size band |
| Pains and jobs | pain and use_case claims from voice and customer stories (synthesis, G6) |
| Triggers | trigger claims with dates; hiring and funding as timing only [D1, D2] |
| Disqualifiers | Verified disqualifier claims only [D1] |
| Positioning gap | Stated claims without revealed support, and revealed segments the copy never mentions (C5) |

## 5. Red flags

| Symptom | Likely cause | Response |
|---|---|---|
| Every strong claim is first-party | The run never left the company's site | Rerun customers, voice, hiring lanes |
| ICP says "enterprise" but pricing is self-serve and reviews skew small | Stated versus revealed gap | Report the gap; lead with revealed evidence |
| A lane returned nothing | Tool blocked, robots disallow, or no public footprint | Record the lane as missing with the reason; lower overall confidence |
| Tool call fails with an unknown tool name | Retired name from an old integration (C2) | Re-list tools; map by capability |
| Spend climbing fast | Crawl without `limit`, JSON extraction everywhere, agent without a budget | Stop, switch to map plus highlights, set caps [D3, D4] |
| A page lists staff names or contacts | People-level data in scope | Skip those lines; never copy them; the ledger rejects contacts |
| Size bands disagree across sources | Different bucket definitions (G2) | Keep source wording in notes; report a range |
| Intent language creeping in ("they are in market") | Public research cannot see intent (G5) | Replace with fit and dated timing signals |

## 6. Hand-offs

| Next step | Peer |
|---|---|
| Positioning or audit inside a website-audit engagement | `icp-positioning-wasp-drone` (website-auditor pack) |
| Competitor workbook, battlecards | `competitive-research-wasp-drone` |
| Outbound sequences to the ICP | `cold-outreach-wasp-drone` |
| CRM fields, scoring model, enrichment sync | `crm-integration-wasp-drone` |
| Discovery interviews to validate the ICP with real buyers | `discovery-research-wasp-drone` |
| Paid channel choice for the ICP | `alt-ads-platforms-wasp-drone` |
