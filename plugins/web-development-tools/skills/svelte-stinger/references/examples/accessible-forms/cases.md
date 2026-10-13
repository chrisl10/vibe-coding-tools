# Qualification cases

These are expected application behaviors, not observed browser results.

| Case | Stimulus | Required observation |
|---|---|---|
| Native path | Disable JavaScript, submit valid name with keyboard | Server validates and authorizes; useful result renders without enhancement. |
| Invalid server input | Direct POST empty, duplicate name fields, oversized string or File | 422 with field error; no write call. Browser constraints are irrelevant to this probe. |
| Permission | Missing adapter, denied identity, permission revoked during write | Unavailable or forbidden result; no unauthorized mutation. |
| Correctable error | Invalid submission with JS | Error summary receives focus after update; link reaches labeled field. |
| Repeat submission | Double click, Enter twice, retry after ambiguous timeout | Client guard cancels duplicate interaction; application server policy prevents duplicate effects. |
| Pending state | Slow response | Status changes, name remains readable, no payload loss from disabling controls. |
| Failure | Offline/server error or thrown adapter failure | No success announcement; route error recovery allows retry with a defined duplicate policy. |
| Async suggestion | Type A then B, return B response before A | Only B response may be applied; final POST revalidates server-side. |
| Sensitive form | Password/token/payment details | No secrets in response values, logs, query strings, fixtures or analytics. |
| Assistive tech | Browser + screen reader with keyboard | Label/help/error/summary/status understandable; no repetitive announcements. |
