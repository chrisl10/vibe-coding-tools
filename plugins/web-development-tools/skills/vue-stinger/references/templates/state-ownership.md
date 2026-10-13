# State ownership template
| Value | Owner | Mutation contract | Reset boundary |
|---|---|---|---|
| Form title | Form instance ref | User input; emit save intent | Explicit accepted record change |
| Validation text | Computed | Derived, no side effects | Draft/attempt state |
| Loaded record | Composable refs | Validated current request only | Param change/unmount |
| Shared selection | Existing app store if needed | Named actions | Accepted session/app lifecycle |
| Auth/tenant state | Accepted auth/backend owner | Server validation | Owner-defined sign-out/tenant change |

Do not introduce a store merely because it is fashionable. Pinia is the documented recommendation when shared production state needs it; installation is separate authorization. SSR state isolation belongs to the selected SSR owner.
