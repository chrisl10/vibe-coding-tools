# Security responsibilities in plain words

Use alongside the [guide](../guides/explain-security-responsibilities.md) and digest. These are learning prompts, not a complete control checklist or an app verdict.

| Boundary | What it means | Beginner/product decision | Actual owner work and evidence gap |
|---|---|---|---|
| Sign-in | How the app knows who is asking | Which people need accounts and recovery? | Selected Auth owner designs/implements identity behavior; Security reviews actual evidence. No owner selected means pending. |
| Permissions | What that person may read or change | State allowed actions, items and customer boundaries | Authorized implementation/data owners enforce real paths; reviewers need allowed and denied cases. A hidden button is not permission proof. |
| Data | Information the app holds or shares | What is needed, who receives it, and who decides retention? | Selected DB/platform owners implement accepted storage/access/recovery requirements; actual behavior stays unproven. |
| Secrets | Private keys used to reach services | Identify a needed service without pasting keys | Authorized secret/platform owner manages access; Security reviews intended exposure surfaces. The learner does not supply secret values here. |
| Dependencies | Other people's software your app uses | Ask what is included and who keeps it maintained | Selected Dependency Audit and implementation owners inspect artifact/component evidence and updates. A list is not a safety guarantee. |
| Providers and operations | Outside services and what happens after release | Name the operator and approved service use; ask about reports/recovery | Platform/provider owners implement accepted integration and runtime controls; operator follows the actual response plan. Buying a service does not establish that app behavior was checked. |

The owner can be a learner, a colleague or an authorized team. Write actual names or "unknown"; never assign consent by implication. AI proposals, vendor docs and security reports do not authorize paid accounts, settings changes or release. Existing review gates and action permissions still apply. Sources for the underlying concepts and derived Wasp Nest boundaries are in the digest.
