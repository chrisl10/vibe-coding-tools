# Website Audit Tools

Audit a public website with crawl, SEO, accessibility, conversion and evidence-backed reports.

A public-site engagement has its own intake, saved crawl, scoring, passive security and reporting contract.

Requires `wasp-nest-core`, `browser-and-app-testing-tools`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 21 skills, 20 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [accessibility-audit-stinger](skills/accessibility-audit-stinger/SKILL.md) | Automated-plus-heuristic WCAG 2.1 AA audit across crawled site-data/, a 0-100% score and AA/AAA-style rating, every finding cited with evidence. Not a legal EAA-conformance determination. |
| [aeo-audit-stinger](skills/aeo-audit-stinger/SKILL.md) | 100-page AEO audit: llms.txt presence, per-engine AI-crawler robots.txt access (GPTBot, PerplexityBot, ClaudeBot, etc.), citation-relevant structured data, subjective topical alignment. Wave W5. |
| [analytics-stack-stinger](skills/analytics-stack-stinger/SKILL.md) | Foundational, industry-specific, and lawful-only de-anonymization analytics audit, built on the vendor census. Flags jurisdiction questions rather than a compliance verdict. |
| [audit-intake-stinger](skills/audit-intake-stinger/SKILL.md) | Runs the four-question intake, scaffolds the shared audit workspace, hydrates every template with the answers. First Drone in every engagement, no authorization-capture step by design. |
| [audit-reporting-stinger](skills/audit-reporting-stinger/SKILL.md) | Generates customer- and auditor-facing reports (Markdown + styled HTML), subtly Legion Code Inc.-branded, rendered only from the scored findings register. |
| [audit-scoring-stinger](skills/audit-scoring-stinger/SKILL.md) | N/A-aware weighted rollup engine (leaf to sub-audit to category to final), critical-security-override, populates the branded named-range-driven XLSX scorecard. |
| [blog-content-stinger](skills/blog-content-stinger/SKILL.md) | Bonus, conditional blog audit: 10 recent posts, word count, subjective quality read, AI-authorship reported only as a probability band with method and error rate, never a verdict. Wave W6a. |
| [content-semantics-stinger](skills/content-semantics-stinger/SKILL.md) | Quantified reading-level estimate (Flesch Reading Ease/Grade Level) plus a subjective ICP-relevancy score per crawled page, kept in separate sections. Wave W5. |
| [ecommerce-catalog-stinger](skills/ecommerce-catalog-stinger/SKILL.md) | Bonus, conditional ecommerce audit: up to 25 products, schema.org Product metadata completeness (quantified) plus subjective copy/conversion quality, kept separate. Wave W6b. |
| [icp-positioning-stinger](skills/icp-positioning-stinger/SKILL.md) | Niche/ICP/goal assessment, conversion-action taxonomy, two-stage buyer-readiness model. Owns the run's hard focus-undeterminable gate: halts and asks rather than guessing. |
| [internal-linking-stinger](skills/internal-linking-stinger/SKILL.md) | Internal link-graph analysis: orphan-page detection, click-depth via BFS, four-dimension anchor-text scoring plus cannibalization detection, internal-PageRank-style equity flow. Wave W5. |
| [keyword-intelligence-stinger](skills/keyword-intelligence-stinger/SKILL.md) | Compiles 75-100 keywords + 25-50 questions via a strict 4-tier source chain: Search Console MCP, then customer Trends export, then EXA/Firecrawl inference, then paid API. Degrades gracefully. |
| [master-website-auditor](skills/master-website-auditor/SKILL.md) | Fallback orchestrator for harnesses without native command dispatch. Activates the same 20 Drone/Stinger pairs as /perform-website-audit, same order, same shared workspace. |
| [performance-cwv-stinger](skills/performance-cwv-stinger/SKILL.md) | CDN/caching-header audit plus Core Web Vitals scoring for an external site, from an outside unauthenticated posture. Cross-linked with lighthouse-pagespeed-stinger, not duplicated. |
| [site-crawler-stinger](skills/site-crawler-stinger/SKILL.md) | Platform-aware crawl to depth 100, raw HTML+MD storage in site-data/, which nine Wave-5 Drones then read read-only with zero write contention. |
| [social-presence-stinger](skills/social-presence-stinger/SKILL.md) | Facebook/LinkedIn/Instagram presence audit via the harness's own browser tooling, opt-in auth per platform; decline or unavailable auth is a silent no-op, never a score penalty. |
| [stack-fingerprint-stinger](skills/stack-fingerprint-stinger/SKILL.md) | Landing-page-only stack and render-mode fingerprinting (React/Vite, Next.js, SvelteKit, WordPress, Shopify, Magento). Writes target-profile.json every later Drone reads. |
| [technical-seo-stinger](skills/technical-seo-stinger/SKILL.md) | 100-page technical SEO audit: crawlability/indexability, sitemap/robots.txt validation, canonicalization, log-file/crawl-budget analysis, keyword-frequency and long-tail semantic analysis. Wave W5. |
| [vendor-inventory-stinger](skills/vendor-inventory-stinger/SKILL.md) | Third-party vendor census after a real JS-executed page load, including GTM-hydrated scripts and content-injection/metadata-manipulation tools like Search Atlas, classified by function. |
| [visual-funnel-stinger](skills/visual-funnel-stinger/SKILL.md) | 25-page visual funnel walk, real desktop (1440x900) and mobile (390x844) Chrome, screenshots at every checkpoint. No state-creating actions unless interactive mode is opted into. |
| [web-security-posture-stinger](skills/web-security-posture-stinger/SKILL.md) | External, passive security-posture audit: headers, TLS coarse-check, cookies, CSP, injection surface, payment-path integrity. Highest-weighted category (20%); a critical leaf caps the grade at C. |

## Start one task

Required packs: `wasp-nest-core`, `browser-and-app-testing-tools`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install browser-and-app-testing-tools@wasp-nest
/plugin install website-audit-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Run perform-website-audit for [public website]. Use passive public observations and report source evidence and missing access.
```

Expected result: A saved audit workspace, findings, scores and customer/auditor reports. Browser and App Testing is also required.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/website-audit-tools:perform-website-audit` ([procedure](commands/perform-website-audit.md)) | Runs a full Website Auditor by Legion Code Inc. engagement end to end: intake through branded reports, sequencing all 20 Drone/Stinger pairs per the dependency graph. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [accessibility-audit-wasp-drone](agents/accessibility-audit-wasp-drone.md) | Automated-plus-heuristic WCAG 2.1 AA accessibility audit of a crawled third-party site, scored 0-100% with an AA/AAA-style rating band, every finding cited to its success criterion with evidence. | [accessibility-audit-stinger](skills/accessibility-audit-stinger/SKILL.md) |
| [aeo-audit-wasp-drone](agents/aeo-audit-wasp-drone.md) | 100-page-depth Answer Engine Optimization audit: `llms.txt` presence/correctness, per-engine AI-crawler robots.txt access (GPTBot, PerplexityBot, ClaudeBot, Googlebot, Google-Extended, Cohere-AI), citation-relevant structured data, and a subjective topical-alignment read against `content-targets/questions.md`. | [aeo-audit-stinger](skills/aeo-audit-stinger/SKILL.md) |
| [analytics-stack-wasp-drone](agents/analytics-stack-wasp-drone.md) | Foundational, industry-specific, and (where lawful) de-anonymization analytics audit, built on vendor-inventory-wasp-drone's census. | [analytics-stack-stinger](skills/analytics-stack-stinger/SKILL.md) |
| [audit-intake-wasp-drone](agents/audit-intake-wasp-drone.md) | First Drone in every website-audit engagement. | [audit-intake-stinger](skills/audit-intake-stinger/SKILL.md) |
| [audit-reporting-wasp-drone](agents/audit-reporting-wasp-drone.md) | Generates the customer-facing and auditor-facing reports, in Markdown and styled HTML, subtly Legion Code Inc.-branded. | [audit-reporting-stinger](skills/audit-reporting-stinger/SKILL.md) |
| [audit-scoring-wasp-drone](agents/audit-scoring-wasp-drone.md) | The rubric engine: rolls every leaf finding up through sub-audit, category, and final scores using the N/A-aware weighted formulas from the build plan, applies the critical-security-override, and populates the branded XLSX scorecard. | [audit-scoring-stinger](skills/audit-scoring-stinger/SKILL.md) |
| [blog-content-wasp-drone](agents/blog-content-wasp-drone.md) | Bonus, conditional audit of the 10 most recent blog posts: word count, [subjective] semantic/quality read, and AI-authorship-probability analysis reported strictly as a probability band with method and error rate, never a verdict. | [blog-content-stinger](skills/blog-content-stinger/SKILL.md) |
| [content-semantics-wasp-drone](agents/content-semantics-wasp-drone.md) | Subjective copy interpretation for the crawled content set: a quantified reading-level estimate per page plus a `[subjective]`-labelled ICP-relevancy score. | [content-semantics-stinger](skills/content-semantics-stinger/SKILL.md) |
| [ecommerce-catalog-wasp-drone](agents/ecommerce-catalog-wasp-drone.md) | Bonus, conditional audit of up to 25 products across categories: metadata completeness (quantified, schema.org Product field checks by Google surface) and on-page copy/conversion-potential quality ([subjective]). | [ecommerce-catalog-stinger](skills/ecommerce-catalog-stinger/SKILL.md) |
| [icp-positioning-wasp-drone](agents/icp-positioning-wasp-drone.md) | Determines the audited site's niche, ICP, and conversion-action taxonomy, and owns this run's one hard stop: if the site's focus can't be determined, the run halts and asks rather than guessing. | [icp-positioning-stinger](skills/icp-positioning-stinger/SKILL.md) |
| [internal-linking-wasp-drone](agents/internal-linking-wasp-drone.md) | Internal link-graph analysis across the crawled page set: orphan pages, click-depth outliers (BFS from defined entry points), anchor-text quality and cannibalization, internal-PageRank-style link-equity flow. | [internal-linking-stinger](skills/internal-linking-stinger/SKILL.md) |
| [keyword-intelligence-wasp-drone](agents/keyword-intelligence-wasp-drone.md) | Compiles 75-100 keywords and 25-50 customer questions using a strict four-tier source priority: Google Search Console MCP (if connected and has data) before a customer-supplied Google Trends export, before EXA/Firecrawl inference, before a paid keyword API as last resort. | [keyword-intelligence-stinger](skills/keyword-intelligence-stinger/SKILL.md) |
| [performance-cwv-wasp-drone](agents/performance-cwv-wasp-drone.md) | CDN/caching strategy and Core Web Vitals audit for an external site the customer does not necessarily control the infrastructure of, from the outside. | [performance-cwv-stinger](skills/performance-cwv-stinger/SKILL.md) |
| [site-crawler-wasp-drone](agents/site-crawler-wasp-drone.md) | Platform-aware crawl to a depth of 100 pages, storing raw HTML and Markdown per page under `site-data/`, which every Wave-5 Drone then reads read-only. | [site-crawler-stinger](skills/site-crawler-stinger/SKILL.md) |
| [social-presence-wasp-drone](agents/social-presence-wasp-drone.md) | Facebook, LinkedIn, and Instagram presence audit using the harness's own browser tooling, explicitly prompting the user to authenticate per platform if deeper data is wanted, defaulting to a silent no-op (never a score penalty) when declined or unavailable. | [social-presence-stinger](skills/social-presence-stinger/SKILL.md) |
| [stack-fingerprint-wasp-drone](agents/stack-fingerprint-wasp-drone.md) | Fingerprints the audited site's technology stack (React+Vite, Next.js, SvelteKit, WordPress, Shopify, or Magento) and render mode (SSR/CSR/hybrid) from the landing page alone. | [stack-fingerprint-stinger](skills/stack-fingerprint-stinger/SKILL.md) |
| [technical-seo-wasp-drone](agents/technical-seo-wasp-drone.md) | 100-page-depth SEO audit: technical structure (title/meta/canonical/robots/sitemap/structured-data), keyword-frequency analysis against `content-targets/keywords.md`, long-tail semantic analysis against `content-targets/questions.md`, and deep-linking findings cross-linked with internal-linking-stinger. | [technical-seo-stinger](skills/technical-seo-stinger/SKILL.md) |
| [vendor-inventory-wasp-drone](agents/vendor-inventory-wasp-drone.md) | Full third-party vendor census of the audited landing page after a real headless-browser load, including anything Google Tag Manager injects at runtime and content-injection/metadata-manipulation tools such as Search Atlas. | [vendor-inventory-stinger](skills/vendor-inventory-stinger/SKILL.md) |
| [visual-funnel-wasp-drone](agents/visual-funnel-wasp-drone.md) | 25-page-depth visual customer-funnel audit using real desktop (1440x900) and mobile (390x844, real mobile UA) Chrome sessions. | [visual-funnel-stinger](skills/visual-funnel-stinger/SKILL.md) |
| [web-security-posture-wasp-drone](agents/web-security-posture-wasp-drone.md) | External, passive security-posture audit of a third-party site: headers, TLS coarse-check, cookies, CSP, platform exposure, client-side injection surface, and payment-path integrity at an observational level only, the highest-weighted category (20%) in the final score. | [web-security-posture-stinger](skills/web-security-posture-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
