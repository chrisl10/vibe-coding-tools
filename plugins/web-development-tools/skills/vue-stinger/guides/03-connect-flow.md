# Connect routes, forms and state
1. Preserve the existing router. Declare typed or explicitly normalized route params, lazy feature views and a not-found route. Watch the specific reused parameter, not merely onMounted. [Route contract](../references/templates/routes.ts) is an adaptation example.
2. Confirm actual hosting mode. HTML history requires deep-link fallback and application not-found handling. Obtain deployment/config approval separately; document fallback pending if unproved. Hash history is a product decision, not an automatic escape.
3. Keep draft form state local. Emit an intent to the parent/service owner; report pending, validation and retryable failure states. Validate server input independently and do not log bodies or credentials. Disable duplicate UI submission while pending, but backend idempotency and authorization remain backend responsibilities.
4. Separate server resources from UI drafts and derive filtered/display state with computed. Keep shared mutations behind actions; reset sensitive app/session state using the accepted authentication boundary.
5. Integrate the composable using a getter for the current parameter and an accepted same-origin endpoint. Reject malformed responses and stale results. Do not add provider calls, keys or account writes to make an example live.

Grounding: router, history, forms, state, security. Server authorization and idempotency are retained application contracts, not Vue features.
