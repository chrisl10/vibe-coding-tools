# Lane playbooks

One section per research lane. Every lane reads the seed brief from the on-site lane, writes `lane-<name>.jsonl` in the ledger format ([LEDGER-SCHEMA.md](LEDGER-SCHEMA.md)), and stops at its page budget or its stop condition, whichever comes first. Tool calls are named by capability; bind them with [TOOLS.md](TOOLS.md). `<co>` is the company name, `<domain>` its domain, `<category>` the product category from the seed brief.

Query style for search tools: describe the page you want, in a sentence, with the source type in it [D3]. Put the company's own domain in `excludeDomains` for off-site searches, except Exa `category: "company"` searches: that category does not support `excludeDomains` or date filters [D3], so drop the company's own results after they return.

## Lane `onsite` (seed, runs first)

**Question:** What does the company sell, how is it priced, and whom does it say it serves?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | Read `https://<domain>/robots.txt`; note disallowed paths and crawl-delay | none (compliance note) |
| 2 | Map the site with relevance searches: pricing, customers, case studies, industries, solutions, integrations, partners, careers, security, trust, about, docs | page inventory |
| 3 | Fetch the homepage and the top page per class (markdown or highlights) | `stated` segment, use_case, industry, persona claims |
| 4 | Pricing page: plan names, seat or usage limits, SSO, SCIM, audit logs, SOC 2 or ISO mentions, "contact sales" gating [D2] | `revealed` pricing_tier, employee_band, business_model |
| 5 | Customers and case-study index: list named customer companies and the industries, sizes, and regions the page attributes to them [D2] | `revealed` customer_example, industry, segment |
| 6 | Integrations page: listed platforms and categories [D1] | `revealed` technographic |
| 7 | Security or trust page: certifications, data residency, regulated-industry claims | `revealed` industry, geography, segment |

**Seed brief (write before fan-out):** one paragraph plus lists: product category, pricing model, stated audience, named customers (up to the depth mode's cap: 8 Quick, 20 Standard, 40 Deep), named competitors or alternatives mentioned, integration ecosystems, careers URL, regions served. Every other lane reads it.

**Stop:** all page classes fetched once, or page budget reached.

## Lane `customers` (the strongest revealed signal)

**Question:** What do the company's actual customers have in common?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | For each named customer from the seed brief (largest budgets first, up to the lane cap), find the customer's own site with a company-type search, for example "company website of <customer name>, <industry hint>" | customer domain |
| 2 | Fetch the customer's homepage or about page highlights: industry, size signals (locations, "team of", customer counts), region, business model | `revealed` industry, employee_band, geography, business_model with `source_type: customer_site` |
| 3 | Search third-party customer stories: "case study of <customer> using <co>" and "<co> customer story" with `excludeDomains: [<domain>]` | `revealed` customer_example, use_case, pain with `source_type: customer_story` |
| 4 | Tally the distribution across customers (industry, size band, region); record each customer once per claim | distribution table for synthesis |

Rules: firmographics come from the customer's own site or a reputable directory, never from guesses about a logo. Record a size band only when a page states it or states something that fixes it (employee count, locations). Never record people at the customer.

**Stop:** lane cap reached, or three consecutive customers add no new value to any claim.

## Lane `market`

**Question:** Which category is this, which companies compete for the same buyers, and whom do they serve?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | Company-type search: "companies that offer <category> for <stated audience>"; remove `<domain>` from the results afterward (no `excludeDomains` with the company category) | `revealed` competitor |
| 2 | Comparison and alternatives pages: "<co> alternatives comparison", "<co> vs" | `stated` competitor, segment (from third parties) |
| 3 | For the top 3 to 5 competitors, fetch pricing or homepage highlights for their stated audience | context for segment boundaries (use `polarity: contradicts` when a competitor owns a segment the company claims) |
| 4 | Analyst, marketplace, or directory category pages that list the company | `revealed` segment, industry with `source_type: directory` or `partner_marketplace` |

**Stop:** category named and 3 to 5 competitors characterized.

## Lane `hiring`

**Question:** How does the company segment its own go-to-market, and where is it investing now?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | Fetch the careers page and open-role list; if hosted on an applicant-tracking site, fetch that listing page | role inventory |
| 2 | Sales and success titles: Enterprise, Mid-Market, SMB, Commercial, Strategic, territory and region names, industry-specialist titles [D2] | `revealed` segment, geography, industry with `source_type: job_posting` |
| 3 | New-logo versus expansion language in sales roles | `revealed` company_stage, segment |
| 4 | Engineering and solutions roles naming customer-facing technologies or compliance regimes (HIPAA, FedRAMP, PCI) | `revealed` technographic, industry |
| 5 | Hiring volume by function, compared across the snapshot | `revealed` trigger (upmarket push, expansion) |

Rules: job postings are role-level evidence; never record the hiring manager or recruiter. Anecdotal inference (hiring bursts implying funding) stays a `trigger` hypothesis unless news confirms it [D2].

**Stop:** all open go-to-market roles read once.

## Lane `voice`

**Question:** Who reviews and discusses the product, and what problems do they describe?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | Search review sites: "<co> reviews on G2", "<co> Capterra reviews", pinning `includeDomains` to review sites | review pages |
| 2 | Read segment data the page shows (company-size split, industries, regions of reviewers) as stated on the page [D2, G2] | `revealed` employee_band, industry, geography with `source_type: review_site` |
| 3 | Extract recurring pains, jobs, and switching reasons as short quotes, without reviewer names | `revealed` pain, use_case, trigger |
| 4 | Community discussions (forums, public Q&A) about choosing or leaving the product | `revealed` pain, disqualifier, competitor with `source_type: community` |

Rules: quote the problem, not the person; drop reviewer names, titles attached to names, and profile links. Cite the product's review listing page as `source_url`, not a single review's permalink, which can lead back to the reviewer. Respect each site's terms; if a site blocks automated access, record that the lane was limited rather than bypassing it.

**Stop:** one page per major review site plus up to five community threads.

## Lane `news`

**Question:** What recent events change who the company sells to or when buyers act?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | News search for the company in the last 12 to 18 months: funding, acquisitions, launches, new regions, new verticals, leadership changes at the company level, pricing changes | `stated` or `revealed` trigger, company_stage, geography |
| 2 | Funding and company databases (public pages) for stage, total raised, headcount band | `revealed` company_stage with `source_type: funding_database` |
| 3 | Partnership and marketplace announcements | `revealed` technographic, segment |

Rules: record dates in the quote or note; older than 24 months is context, not a trigger. Leadership changes are recorded as event types ("sales leadership change"), never with the person's name, prior employer, or career details: a single-holder role at a named company identifies the person.

**Stop:** 10 to 15 dated items or 18 months covered.

## Lane `technographic`

**Question:** Which technologies do the company's buyers already run, and what does the product require?

| Step | Action | Evidence produced |
|---|---|---|
| 1 | Integration directory and marketplace listings (both on-site and on partner marketplaces) | `revealed` technographic with `source_type: partner_marketplace` |
| 2 | Docs: system requirements, supported platforms, deployment options (cloud, on-premises, region) | `revealed` technographic, disqualifier, geography |
| 3 | Customer evidence of stack from the customers lane where pages state it | `revealed` technographic |

Hard technical incompatibilities found here are candidate `disqualifier` claims; record them only when a page states the limitation [D1].

**Stop:** integration catalogue and deployment requirements read once.

## Optional synthesis pass (deep tools)

After the ledger is scored, a single deep call may test the draft ICP: Exa `deep` or `deep-reasoning` search with an `outputSchema` of account-level fields, or a Firecrawl or Exa agent run with a hard budget (`maxCredits` or `budget.maxCostDollars`). Treat its output as one more source: every field it returns becomes ledger items with the citation it grounds to, never as a conclusion by itself [D3, D4].
