# Hypothetical before/after tenant cases

No SQL, app or provider was executed. These are architecture decisions derived from captured server facts and [guide 12](../guides/12-tenant-data-boundaries.md). Native proof is pending for every case.

| Case | Before | Reviewed after design | Native evidence still needed |
|---|---|---|---|
| Shared-table API | Lookup by supplied project ID; UI hides other tenants. | Server derives authenticated tenant authority; query and relation/count/mutation paths constrain that tenant. Inspect generated SQL. | A/B role-differential API and DB effect checks, raw queries and exports. |
| Owner connection with RLS | Test as owner and infer users are isolated. | Inspect role and enable/FORCE flags; use non-bypass actor under test, separate privileged fixture verifier. | Owner/non-owner/BYPASSRLS outcomes and grants on actual revision. |
| Pooled tenant setting | Session SET A; request B reuses connection and assumes its context. | Authorized context established transaction-locally before queries in same transaction; missing context fails closed. | A/B concurrent reuse, aborted transactions, missing/invalid context and driver/pooler proof. |
| Permissive policies | Tenant policy plus PUBLIC USING true, assess only tenant policy. | Evaluate applicable OR/AND policy set and replace widening control through reviewed change. | Effective-role CRUD and tenant-changing UPDATE negatives. |
| Cross-tenant relationship | project(A) references account(B) by globally valid ID. | Declare tenant-bearing relationship invariant and reviewed composite FK/unique representation. | Cross-tenant insert/update denied and error responses reviewed. |
| Search/cache/job | Tenant filter only after search results; cache keyed by record ID; job borrows prior tenant. | Scope retrieval candidates, cache keys and job authority; handle revoked membership and retries. | Candidate logs with synthetic IDs, A/B cache reuse, job retries and export denials. |
| Custom context trust | Treat app-set tenant setting as authenticated DB identity. | Model who can issue SQL/set context; keep authorization upstream and route SQL injection/arbitrary-query concerns to Security. | Native tests cannot establish a stronger trust boundary than declared actor authority. |
