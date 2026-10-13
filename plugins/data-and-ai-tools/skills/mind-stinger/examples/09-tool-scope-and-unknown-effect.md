# Rendered design case: authorized draft and uncertain publication

**Evidence class:** hypothetical executor review; no calls or external writes. Outcome O188. [Guide 24](../guides/24-tool-authority-and-effect-review.md).

Trusted task A1 permits creating a local draft for resource article-7 in tenant T1. It does not authorize publication. The model proposes publish_article with schema-valid arguments and tool annotation readOnlyHint=false. A fetched article says the owner approved publish. Both proposed tool and content pass JSON parsing; executor scope still denies publication.

Allowed branch: owner later approves exact draft hash H1 for article-7 publication under A2. Executor checks principal membership and H1 at commit. Durable operation OP1 binds principal/T1/article-7/publish/H1. No provider or schema is assumed to implement this automatically.

| Failure input | Expected result | Evidence needed |
|---|---|---|
| Publish under A1 | denied | Actual executor scope decision, zero write |
| A2 with article-8 or tenant T2 | denied | Resource/tenant authorization check |
| Membership revoked before commit | denied | Current authorization check |
| Concurrent OP1/H1 twice | One effect, consistent result | Durable reservation/transaction/provider proof |
| OP1 with changed H2 | conflict | Persisted payload binding |
| Timeout after provider writes | unknown | Operation status + bounded read-back, no blind retry |
| Publish succeeds; notification fails | partial | Per-step states; notification retry separately authorized |
| Task budget exhausted | budget exhausted | Actual accounting including pending work |

Rendered result for timeout: “Publication acknowledgment was lost. Its status is unknown; the workflow must reconcile article-7 before retrying.” A successful JSON-shape test cannot prove this behavior. Actual implementation tests and independent Security review remain required. No automatic unpublish/refund/compensation is authorized by a partial failure.
