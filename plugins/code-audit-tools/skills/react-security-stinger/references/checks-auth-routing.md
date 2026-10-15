# Checks: auth, routing, and client trust (AR)

Load when: running guide 04. A React SPA runs on the user's machine; anything it decides can be changed with dev tools. Every client-side check must have a matching server-side check, which is CWE-602 (A06:2025) when missing raw/owasp--top10-2025-and-cwe-mapping.md.

---

## AR-01 Client-only route guards and role checks

- **Detect:** `ProtectedRoute`, `PrivateRoute`, `RequireAuth`, `AuthGuard`, `RequireAdmin`, `isAdmin`, `role === 'admin'` in components or routes.
- **Confirm:** for each guarded page, list the API calls, loaders, or Server Functions it uses, then read those handlers. The guard is fine as UX; the finding is the backend that serves the same data or action without its own check. If the backend is outside the audited paths, record the guard in notes as "Not confirmed" and hand off.
- **False positive:** every backing endpoint checks session and role server-side.
- **Severity:** admin API reachable without a server-side role check: `critical` when unauthenticated, `high` for any logged-in user.
- **Vulnerable:**
  ```tsx
  <Route path="/admin" element={user?.role === 'admin' ? <Admin /> : <Navigate to="/" />} />
  // server: app.get('/api/admin/users', (req, res) => res.json(db.users.all()))
  ```
- **Fixed:** keep the route guard for UX, and add `requireRole('admin')` to `/api/admin/*` on the server.
- **Refs:** CWE-602, CWE-862, OWASP A01:2025, OWASP A06:2025.

## AR-02 Authorization from client-held data

- **Detect:** `jwtDecode(token).role` used to unlock features or decide which API to call; `localStorage.getItem('role')`, `isAdmin` query params, feature flags read from cookies the client can write.
- **Confirm:** the decision changes what the server does or returns, and the server does not re-check. Decoding a JWT on the client is fine for display; trusting it is not (the client can swap the token payload in storage).
- **Severity:** as AR-01.
- **Vulnerable:** `if (localStorage.getItem('isAdmin') === 'true') await api.post('/refunds', order)` with no server check.
- **Fixed:** server verifies the session and role on `/refunds`.
- **Refs:** CWE-602, CWE-639, OWASP A01:2025.

## AR-03 Open redirect through router parameters

- **Detect:** `searchParams.get('next' | 'redirect' | 'returnTo' | 'callbackUrl')` feeding `navigate()`, `redirect()` in loaders or actions, `window.location.href =`, `location.assign`, `location.replace`, `window.open`.
- **Confirm:** an attacker-chosen absolute URL (`https://evil.example`, `//evil.example`, `javascript:...`) is accepted. `window.location` assignments are not protected by React 19's URL sanitization. React Router versions below 7.18.0 have their own redirect advisories (script).
- **False positive:** target validated as a same-origin relative path (`startsWith('/') && !startsWith('//')` plus `new URL` origin check) or matched against an allow-list.
- **Severity:** open redirect to any site: `medium`; `high` when `javascript:` executes (XSS) or when the redirect carries tokens (OAuth callbacks).
- **Vulnerable:**
  ```ts
  const next = new URLSearchParams(location.search).get('next');
  window.location.href = next!;
  ```
- **Fixed:**
  ```ts
  function safeNext(raw: string | null) {
    if (!raw) return '/';
    const u = new URL(raw, window.location.origin);
    return u.origin === window.location.origin ? u.pathname + u.search + u.hash : '/';
  }
  window.location.assign(safeNext(new URLSearchParams(location.search).get('next')));
  ```
- **Refs:** CWE-601, OWASP A01:2025, CVE-2026-22029, CVE-2025-68470, raw/owasp--cheatsheet-xss-dom-xss-redirects.md, raw/router--react-router-advisories.md.

## AR-04 postMessage without origin checks

- **Detect:** `addEventListener('message', ...)`, `onmessage =`, `postMessage(data, '*')`.
- **Confirm:** the listener does not compare `event.origin` to an exact allow-list before acting, or uses substring checks (`includes`, `indexOf`, `endsWith` without a leading dot and scheme); or the handler writes `event.data` into a DOM sink, navigation, or state that drives auth. For senders, `'*'` with tokens or personal data is a leak.
- **False positive:** strict equality against a fixed origin list, plus schema validation of `data`.
- **Severity:** message data to an HTML or code sink: `high`. Missing origin check that changes app state: `medium`. Sensitive data sent with `'*'`: `medium`.
- **Vulnerable:**
  ```ts
  window.addEventListener('message', (e) => { if (e.origin.includes('partner.com')) setToken(e.data.token); });
  ```
- **Fixed:**
  ```ts
  const ALLOWED = new Set(['https://app.partner.com']);
  window.addEventListener('message', (e) => {
    if (!ALLOWED.has(e.origin)) return;
    const msg = TokenMessage.safeParse(e.data);
    if (msg.success) setToken(msg.data.token);
  });
  ```
- **Refs:** CWE-346, CWE-79, OWASP A07:2025, raw/browser--mdn-postmessage.md, raw/owasp--cheatsheet-html5-security.md.

## AR-05 CSRF on cookie-authenticated calls

- **Detect:** `credentials: 'include'`, `withCredentials: true`, cookies set with `SameSite=None`, React Router actions and Server Functions using cookie sessions.
- **Confirm:** the server accepts state-changing requests with only the cookie (no CSRF token, no required custom header, no Origin or Fetch Metadata check). CORS settings that reflect any origin with credentials make it worse.
- **False positive:** bearer tokens in headers only; server checks Origin or `Sec-Fetch-Site`; double-submit or synchronizer tokens.
- **Severity:** `high` with `SameSite=None` or no SameSite and no other defense; `medium` behind `SameSite=Lax` (contract example).
- **Vulnerable:** cookie session, `app.post('/api/transfer', handler)` with no CSRF check, and `fetch('/api/transfer', { method: 'POST', credentials: 'include', body })` in the client.
- **Fixed:** server rejects cross-site requests (`Sec-Fetch-Site` with Origin fallback) and sets `SameSite=Lax` or `Strict`; or require a custom header such as `X-Requested-With` on JSON APIs.
- **Refs:** CWE-352, OWASP A01:2025, raw/owasp--cheatsheet-csrf.md.

## AR-06 Tokens in URLs

- **Detect:** `?access_token=`, `?token=`, `#id_token=` built into links or read from the URL and kept; implicit OAuth flows.
- **Confirm:** the token stays in the address bar, history, referrer headers, or analytics page-view events.
- **Severity:** `medium`; `low` for single-use, short-lived tokens that are removed with `history.replaceState` immediately.
- **Vulnerable:** `navigate(`/dashboard?token=${session.token}`)`
- **Fixed:** keep tokens in an httpOnly cookie or memory; use the authorization code flow with PKCE.
- **Refs:** CWE-598 (A06:2025 maps it).
