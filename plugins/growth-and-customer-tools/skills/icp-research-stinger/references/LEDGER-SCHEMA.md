# Evidence ledger schema

Every lane writes JSON Lines: one object per piece of evidence. `scripts/icp_ledger.py validate` enforces this schema and the privacy guard; `merge`, `score`, and `render` build the graded evidence table.

## Fields

| Field | Required | Values |
|---|---|---|
| `lane` | yes | `onsite`, `customers`, `market`, `hiring`, `voice`, `news`, `technographic` |
| `claim_type` | yes | `industry`, `employee_band`, `revenue_band`, `geography`, `business_model`, `company_stage`, `segment`, `use_case`, `persona`, `pain`, `trigger`, `disqualifier`, `technographic`, `pricing_tier`, `competitor`, `customer_example` |
| `value` | yes | Normalized value up to 200 characters, for example `Healthcare providers`, `51-1000`, `North America`, `Economic buyer: VP Operations` (role, never a name) |
| `signal` | yes | `stated` (the company or its marketing says so) or `revealed` (customers, reviews, hiring, pricing structure, integrations show it) |
| `polarity` | yes | `supports` or `contradicts` |
| `source_url` | yes | Absolute http(s) URL of the page read |
| `source_type` | yes | `first_party`, `customer_story`, `customer_site`, `review_site`, `job_posting`, `news`, `funding_database`, `directory`, `partner_marketplace`, `community`, `other` |
| `quote` | yes | The minimum verbatim text that supports the claim, up to 400 characters |
| `retrieved` | yes | `YYYY-MM-DD` |
| `tool` | yes | `exa`, `firecrawl`, `websearch`, `webfetch`, `manual` |
| `confidence` | no | 0 to 1, the lane's own judgment of this single item |
| `note` | no | Short reasoning as a string up to 1,000 characters, for example how a size band was inferred |

Any other field is rejected, so nothing reaches the merged ledger without passing the privacy guard.

## What the privacy guard catches, and what it misses

`validate` rejects an item when `value`, `quote`, or `note` contains a plain-form email address or a common phone shape (North American 3-3-4, numbers starting with `+`, trunk-prefixed `0` numbers with separators), when `source_url` contains an email address, or when any of them contains a LinkedIn `/in/` or `/pub/` URL or a Facebook or Instagram account URL. Facebook and Instagram company vanity pages look like personal accounts and are rejected too; cite the company's own site instead.

It does not catch names, obfuscated emails (`jane [at] acme`), unseparated digit runs, many national phone formats, or profile URLs on other sites (X, GitHub, personal blogs). It is a backstop; the lane rules are the control.

## Normalization

- Size bands: `1-10`, `11-50`, `51-200`, `201-1000`, `1001-5000`, `5001+`. When a source uses its own buckets (review sites), keep its wording in `note` and map to the nearest band only if unambiguous (G2 in the distillation).
- Industries: the plainest common label (`Healthcare providers`, `Logistics`, `Fintech`), consistent across lanes so grading can group them.
- Personas: `<committee role>: <function or title level>`, using the roles economic buyer, champion, technical buyer, end user, procurement, executive sponsor [D1].
- Disqualifiers: only verified conditions (a stated limitation, a stated minimum, an unsupported region); unknowns are not disqualifiers [D1].

## Grading (computed by `score`)

| Grade | Rule |
|---|---|
| strong | 3 or more independent supporting domains, 2 or more source types, at least 1 revealed item |
| moderate | 2 or more independent supporting domains |
| weak | 1 supporting domain |
| contested | contradicting domains at least half as many as supporting domains |

An independent domain is a registrable domain (approximated by the script), so `jobs.vendor.com` and `blog.vendor.com` count once. Every host passed in `--company-domain` (and its subdomains) counts together as one source, so a company that owns `vendor.com` and `vendor.io` cannot lift its own claim from weak to moderate. `first_party_only` is true when every supporting item is tagged `first_party` or comes from a host passed in `--company-domain` (or its subdomains); pass every domain the company owns, comma-separated, for example `--company-domain vendor.com,vendor.io`. First-party matching uses the exact hosts given, so a company hosted on a shared platform (`vendor.webflow.io`) does not claim other sites on that platform.

`first_party_only` is therefore true when every supporting item comes from the company's own domains; `stated_only` is true when no revealed item supports the claim. The dossier may present strong and moderate claims as findings, weak claims as hypotheses, and contested claims with both sides.

## Example lines

```json
{"lane":"customers","claim_type":"industry","value":"Regional hospitals","signal":"revealed","polarity":"supports","source_url":"https://customer.example.org/about","source_type":"customer_site","quote":"serving 14 rural communities across three states","retrieved":"2026-09-23","tool":"exa","note":"named on vendor case study page"}
{"lane":"hiring","claim_type":"segment","value":"Mid-market","signal":"revealed","polarity":"supports","source_url":"https://jobs.example.com/vendor/mid-market-ae","source_type":"job_posting","quote":"Mid-Market Account Executive, East territory","retrieved":"2026-09-23","tool":"firecrawl"}
{"lane":"onsite","claim_type":"segment","value":"Enterprise","signal":"stated","polarity":"supports","source_url":"https://vendor.example.com/","source_type":"first_party","quote":"Built for the enterprise","retrieved":"2026-09-23","tool":"firecrawl"}
```
