# Choose data, storage and access boundaries

1. Derive DB/storage from persistence/query/tenancy/recovery needs. Reuse selected DB/Neon/Supabase/vector/storage specialists. Do not add both SQL providers or a separate vector DB without a requirement.
2. Record compute/data placement and connection characteristics. Native backend language is separate from where data lives. Verify actual region, pooling/access and service limits from current chosen-plan sources.
3. Map public ingress, trusted operator access, service-to-service traffic and secrets. Name the security review owner. Add private connectivity, load balancing, firewall policy or secret tooling only when the topology needs it.
4. Record backup scope/retention/export and an actual restore evidence request. A provider backup feature is not a completed restore drill or availability guarantee.
5. Return boundary decisions and missing owner contracts. No permissions, network controls, credentials or migration changes happen in this advisory workflow.

Grounding: Neon, Supabase production, AWS network/IAM responsibilities. Conditional layer rules are the topic contract.
