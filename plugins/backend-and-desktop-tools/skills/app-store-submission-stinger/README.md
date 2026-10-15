# app-store-submission-stinger

Operational playbook for `app-store-submission-wasp-drone`, the Wasp Nest's specialist for getting iOS and Android apps through App Store and Google Play review in 2025-2026.

This Stinger covers App Store Optimization (keywords, screenshots, preview videos), privacy compliance (Apple nutrition labels, PrivacyInfo.xcprivacy, Google data safety forms), rejection diagnosis and remediation, age rating, In-App Purchase configuration (StoreKit 2 / Google Play Billing Library 7+), and realistic timeline expectations for both platforms.

**Procedure:** [SKILL.md](SKILL.md)
**Research basis:** `research/research-summary.md` (normal depth, 2025-11 to 2026-05 window, 17 files)

## Folder layout

```
app-store-submission-stinger/
├── SKILL.md                  -  master index; read first
├── README.md                 -  this file
├── guides/                   -  procedural playbooks per stage
├── examples/                 -  worked happy-path and edge-case walkthroughs
├── templates/                -  fill-in-the-blank reports and checklists
├── reports/                  -  per-run submission audit logs
└── research/                 -  scripture-historian's sources (read-only)
```

## Current store readiness route

Start with [guide 06](guides/06-prepare-artifact-privacy-and-entitlement-evidence.md), [worksheet](templates/store-evidence-worksheet.md), [cases](examples/store-evidence-readiness-cases.md) and 2026-10-07 primary findings. Historical May billing/metadata/payment examples do not override current dated requirements. Native build and billing implementation remain separate owners.
