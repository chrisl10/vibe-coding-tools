# 06: Synthesize the dossier

Build [templates/icp-dossier.md](../templates/icp-dossier.md) and `icp.json` ([templates/icp.schema.json](../templates/icp.schema.json)) from `score.json` and `evidence.md` only. Do not add claims that are not in the ledger.

## Order of work

1. **Customer distribution first.** Tally industry, size band, region, and business model across profiled customers. This is the revealed ICP.
2. **Primary ICP.** Take strong and moderate claims that co-occur in that distribution. Combine firmographics with technographics where both are strong (D1).
3. **Segments and tiers.** Distinct clusters become segments; tier them by fit strength and by structural signals of deal size (security features, contact-sales gating, enterprise titles) [D1, D2]. State why each tier sits where it does.
4. **Buying committee.** Map persona claims to the six roles (D1). Scale expectations with company size: committees of 10 or more belong to 1,000-plus employee accounts (D1). Roles only.
5. **Pains and jobs.** From voice and customer-story evidence, in the customer's words where short. Label this section as synthesis (G6).
6. **Triggers.** Dated events and hiring shifts, as timing, never as intent (G5).
7. **Disqualifiers.** Only verified conditions from the ledger (D1): unsupported regions, stated minimums, incompatible platforms.
8. **Positioning gap.** Compare stated-only claims with revealed segments. This section is often the most useful to the requester (C5).
9. **Confidence.** Count missing lanes against the depth mode's lane set (Quick runs onsite, customers, and hiring by design, so `score` listing the other four as missing does not count against a Quick run). High only when the primary ICP rests on strong claims from at least three lanes including customers; Medium when it rests on moderate claims or a lane is missing; Low when first-party evidence dominates or two or more lanes are missing (**derived** rule).

## Writing rules

- Every sentence in the summary and primary ICP traces to a claim in `evidence.md`.
- Hedge by grade, not by habit: findings are stated plainly, hypotheses are labeled.
- Ranges beat false precision ("about 51 to 200 employees, possibly up to 1,000" when buckets disagree).
- No personal data anywhere, including examples and quotes.
- Name what public research cannot see (intent, win rates, churn, deal sizes).
