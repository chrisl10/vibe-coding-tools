# Negative decision exercises
All cases are fictional, unexecuted contract exercises. Expected answers are decision rules grounded in the linked snapshot.

| Request | Expected response | Evidence |
|---|---|---|
| Choose Railway with no workload details | Provisional candidate or batch required facts; no firm selection | [Worksheet](../templates/fit-worksheet.md) |
| Three replicas sharing the attached SQLite volume | Reject that topology; return to Infrastructure Fit | Volumes |
| Run cron every minute or at an exact second | Reject scheduled-service fit for timing requirement | Cron |
| Cron never exits and must execute every interval | Explain skipped next run, require different lifecycle decision | Cron |
| Zero downtime on volume region migration | Reject unsupported promise | Regions |
| Assume a private registry image works on Hobby | Flag Pro requirement and ask actual source/plan | Services |
| Give each service its own included $5 credit | Reject duplicated workspace allowance | Plans |
| Apply container rates to a sandbox VM | Reject meter mismatch; qualify VM table | Plans |
| No egress or backup quantities means zero cost | Preserve unpriced gaps; return to cost owner | [Cost guide](../../guides/02-cost-envelope.md) |
| A provider volume backup proves off-platform disaster recovery | Reject conclusion; identify separate export/restore proof | Backups |
| Keep serving after a hard spending stop | Flag availability tradeoff and missing acceptance | Billing |
| Deploy now using this selection report | Stop at action boundary; resolve authorized implementation owner | [Handoff guide](../../guides/03-decision-and-handoff.md) |
