# Select assets by the work they support

This is a preparation recipe, not a vendor shopping list. The provider purposes below derive from the [research digest](research/distilled-launch-readiness.md). Their inclusion conditions and deferral triggers are workflow recommendations.

| Capability | Asset to prepare when selected | Include when | Defer when |
|---|---|---|---|
| Public web presence | Domain ownership reference, DNS contact, hosting project, HTTPS owner, brand/content | A public address is needed | Private/local proof uses an approved local route |
| Persistent customer data | Selected DB project/environment, region, recovery owner, backup evidence request | Product stores server-side data | Static brochure site has no remote records |
| Supabase or Neon | The selected service's project and environment references | Accepted architecture chooses it | Do not require both for one SQL need |
| Qdrant or another vector store | Capacity, access, index/update ownership | Accepted retrieval design needs it | Basic search or chosen Postgres retrieval suffices |
| Search/crawl | Exa/Firecrawl or approved alternative access, permitted sources, usage budget | Market/source acquisition or runtime search needs it | Supplied documents already satisfy the workflow |
| Customer identity | WorkOS or selected auth owner; callback/consent/contact assets | Real users sign in or enterprise identity is needed | Public read-only site has no login |
| Social login | Google/Apple/Facebook provider's current project/app/verification checklist | User journey explicitly needs that provider | Do not add every social network by default; unresearched provider requirements remain unknown |
| Secret delivery | Chosen Doppler/config reference and custodian | Deployment needs secrets | Never ask for values in the ledger |
| Private connectivity | Selected Tailscale scope and network-policy owner | Operators/services need private reachability | Public hosting alone does not require a tailnet |
| Reliability/support | Error project, external availability check, recipient, support contact, recovery owner | Paying users need response/recovery | Choose required outcomes before a specific vendor |
| Payments | Payment account business/environment reference, webhook/recovery owner, billing design | Money moves in the product | Free static website does not need Stripe |
| Distribution | Store account, signing identity, screenshots/listing, device proof | Accepted mobile/desktop release route | Web product does not need app-store membership |

Record load balancers, firewalls, Terraform and Ansible only when the chosen topology/operator procedure calls for them. This Stinger prepares assets; Infrastructure Fit chooses topology and implementation specialists own setup. An unselected capability gets a reason and a trigger, not an invented account requirement.

## HTTPS is different from executable signing

HTTPS uses a TLS certificate for a network service. A host may manage issuance and renewal. Executable signing identifies a publisher and protects signed content. Apple notarization and Windows SmartScreen reputation have separate roles. A site's HTTPS certificate cannot sign an installer. OV/EV are validation categories in certificate contexts; neither label substitutes for checking the exact intended code-signing product or ensures Windows reputation. See the cited TLS, Windows and Apple sources in the digest.
