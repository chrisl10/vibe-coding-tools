# Example 02: a worked run on a fictional company

Harborline (`harborline.example`) is invented, and every party uses a reserved `.example` domain, so no real company or person is described. The ledger is [02-sample-ledger.jsonl](02-sample-ledger.jsonl). The table below copies the values `scripts/icp_ledger.py score` prints for it, one row per claim.

## Commands

```text
python scripts/icp_ledger.py validate examples/02-sample-ledger.jsonl
python scripts/icp_ledger.py score examples/02-sample-ledger.jsonl --company-domain harborline.example --pretty
python scripts/icp_ledger.py render examples/02-sample-ledger.jsonl --company-domain harborline.example -o evidence.md
```

## Score output

14 items; grades: strong 1, moderate 1, contested 1, weak 6; lanes missing: market.

| claim_type | value | grade | independent_domains | contradicting_domains | revealed | stated | first_party_only |
|---|---|---|---|---|---|---|---|
| employee_band | 51-200 | moderate | 2 | 0 | 2 | 0 | false |
| employee_band | 51-1000 | weak | 1 | 0 | 1 | 0 | false |
| industry | Outpatient clinics | strong | 4 | 0 | 3 | 1 | false |
| pain | No-shows and double bookings | weak | 1 | 0 | 1 | 0 | false |
| pricing_tier | Self-serve per-seat plans with SSO on top tier | weak | 1 | 0 | 1 | 0 | true |
| segment | Enterprise | contested | 1 | 1 | 0 | 1 | true |
| segment | Mid-market | weak | 1 | 0 | 1 | 0 | false |
| technographic | Practice management system integration | weak | 1 | 0 | 1 | 0 | false |
| trigger | New clinic location or merger | weak | 1 | 0 | 0 | 1 | false |

## How the dossier reads this

- **Primary ICP:** outpatient clinics (physical therapy, dental, specialty practices), graded strong from two customers' own sites, a review site's reviewer mix, and the company's industry page. Company size about 51 to 200 staff, graded moderate from two customer sites; the review site's "Mid-Market (51-1000)" bucket is consistent but was kept as its own weak claim rather than folded into 51-200, because the bucket is ambiguous (LEDGER-SCHEMA normalization rule). The dossier writes "about 51 to 200 employees, possibly up to 1,000".
- **Positioning gap (contested):** the homepage says "built for the enterprise", but the careers page lists only mid-market and SMB sales roles, and pricing is self-serve per seat. The dossier leads with the revealed segment and treats the enterprise claim as aspiration or a planned move, not current fit.
- **Hypotheses (weak):** mid-market as the sales segment, no-show reduction as the core pain, practice-management integration as a technographic requirement, and growth through new locations as a trigger. The trigger is `stated` because the news story reports what the company said. Each needs a second independent source.
- **Coverage and confidence:** the market lane is missing, so category and competitors are unknown. The primary ICP rests on one strong and one moderate claim, so confidence is Medium.

## What made this run trustworthy

1. The seed lane named customers, which gave the customers lane real companies to profile.
2. Revealed evidence (customer sites, reviews, hiring) outvoted stated copy.
3. A contradicting item was recorded rather than ignored, which surfaced the positioning gap.
4. An ambiguous size bucket was kept as its source stated it instead of being forced into a band, which kept the size claim honest at moderate.
5. No person appears anywhere: roles and companies only.
