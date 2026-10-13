# Negative decision exercises
All cases are fictional, unexecuted contract exercises. Expected answers are decision rules grounded in the linked snapshot.

| Request | Expected response | Evidence |
|---|---|---|
| Choose Railway with no workload details | Provisional candidate or batch required facts; no firm selection | [Worksheet](../templates/fit-worksheet.md) |
| Three replicas sharing the attached SQLite volume | Reject that topology; return to Infrastructure Fit | [Volumes](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/volumes.html) |
| Run cron every minute or at an exact second | Reject scheduled-service fit for timing requirement | [Cron](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/cron.html) |
| Cron never exits and must execute every interval | Explain skipped next run, require different lifecycle decision | [Cron](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/cron.html) |
| Zero downtime on volume region migration | Reject unsupported promise | [Regions](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/regions.html) |
| Assume a private registry image works on Hobby | Flag Pro requirement and ask actual source/plan | [Services](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/services.html) |
| Give each service its own included $5 credit | Reject duplicated workspace allowance | [Plans](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/plans.html) |
| Apply container rates to a sandbox VM | Reject meter mismatch; qualify VM table | [Plans](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/plans.html) |
| No egress or backup quantities means zero cost | Preserve unpriced gaps; return to cost owner | [Cost guide](../../guides/02-cost-envelope.md) |
| A provider volume backup proves off-platform disaster recovery | Reject conclusion; identify separate export/restore proof | [Backups](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/backups.html) |
| Keep serving after a hard spending stop | Flag availability tradeoff and missing acceptance | [Billing](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/infrastructure-decision-tools/skills/railway-platform-stinger/references/research/raw/billing.html) |
| Deploy now using this selection report | Stop at action boundary; resolve authorized implementation owner | [Handoff guide](../../guides/03-decision-and-handoff.md) |
