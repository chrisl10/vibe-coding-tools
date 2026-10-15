# Detection patterns (ripgrep)

Load when: you prefer ripgrep over `scripts/sink_scan.py`, need to widen a search, or a check's candidates look incomplete. These match the patterns compiled into `sink_scan.py`; the check ids are the same. Matches are candidates only. Confirm each one with its check in the `checks-*.md` files.

Run from the throwaway copy or with read-only flags. Always exclude build output and dependencies:

```bash
RG='rg -n --hidden -g !node_modules -g !dist -g !build -g !.next -g !coverage -g !.git -g !*.min.js'
T='-t js -t ts --type-add "jsx:*.{jsx,tsx,mdx}" -t jsx'
```

Table escaping: inside the tables below, `\|` is markdown for a plain `|`. Type `|` when you run a command; in ripgrep's regex syntax `\|` would match a literal pipe and silently find nothing. `'"'"'` is the shell idiom for a single quote inside single quotes.

If `rg` is missing, use `scripts/sink_scan.py --checks <id>` (same patterns, standard library only) and record the substitution in `coverage.caps`.

## XSS and SSR

| Check | Command |
| --- | --- |
| RX-01 | `$RG 'dangerouslySetInnerHTML\s*=' $T` then drop lines matching `__html:\s*["'][^"'$]*["']\s*\}` |
| RX-01 | `$RG 'eslint-disable.*react/no-danger'` |
| RX-02 | `$RG '\b(href\|src\|action\|formAction\|xlinkHref\|data\|srcDoc)\s*=\s*\{' $T` then drop relative templates starting with `` `/ `` |
| RX-02 | `$RG -i '["'"'"'`]\s*(javascript:\|data:text/html)' $T` |
| RX-03 | `$RG '\.(innerHTML\|outerHTML)\s*\+?=[^=]\|insertAdjacentHTML\s*\(\|document\.write(ln)?\s*\(' $T` |
| RX-04 | `$RG '(^\|[^\w.])eval\s*\(\|new\s+Function\s*\(\|set(Timeout\|Interval)\s*\(\s*["'"'"'`]' $T` |
| RX-05 | `$RG 'rehype-raw\|rehypeRaw\|urlTransform\s*[:=]\|\bmarked(\.parse)?\s*\(\|markdown-it\|showdown\|remark-html' $T` |
| RX-06 | `$RG 'next-mdx-remote\|@mdx-js/mdx\|mdx-bundler\|compileMDX\s*\(\|bundleMDX\s*\(\|blockJS\s*:\s*false\|blockDangerousJS\s*:\s*false' $T` |
| RX-07 | `$RG 'html-react-parser\|react-html-parser\|\bhtmr\b' $T` |
| RX-08 | `$RG 'ADD_TAGS\|ADD_ATTR\|ALLOW_UNKNOWN_PROTOCOLS\|IN_PLACE\|CUSTOM_ELEMENT_HANDLING\|WHOLE_DOCUMENT\|happy-dom\|\.replace\(\s*/<\s*/?\s*script' $T` |
| RX-08 | `$RG -A3 'DOMPurify\.sanitize\(' $T` (read what happens to the result next) |
| RX-09 | `$RG 'trustedTypes\.createPolicy\s*\(\|require-trusted-types-for'` |
| RX-10 | `$RG 'url\(\s*\$\{\|url\(\s*["'"'"']?\s*\+' $T` |
| RX-11 | `$RG 'target\s*=\s*["'"'"'{`]*_blank' $T` |
| RS-01 | `$RG '__(PRELOADED\|INITIAL\|APOLLO\|REDUX\|RELAY\|SSR\|DATA)[A-Z_]*__\|<script[^>]*dangerouslySetInnerHTML' $T` |
| RS-02 | `$RG 'bootstrapScriptContent\s*:' $T` |
| RS-03 | `$RG -i 'res\.(send\|end\|write)\s*\(\s*`[^`]*<\|\.replace\(\s*["'"'"'`]<!--\s*(app\|ssr\|html\|head)\|renderToString\s*\(' $T` |

## RSC and Server Functions

| Check | Command |
| --- | --- |
| RC-02, RC-04 | `$RG -l '^\s*["'"'"']use server["'"'"']' $T` (list files), then `$RG -n '^export (async )?function\|^export const' <file>` |
| RC-02 | `$RG -n -B2 -A12 '["'"'"']use server["'"'"']' $T` (read the first statements of each function) |
| RC-05 | `$RG 'enableActionEncryption\s*:\s*false\|defineEncryptionKey' -g 'vite.config.*'` |
| RC-06 | `$RG '["'"'"']server-only["'"'"']\|experimental_taint' $T` (positive signals) and `$RG -l '^["'"'"']use client["'"'"']' $T` (client boundary files) |
| RC-07 | `$RG 'decodeReply\s*\(\|decodeAction\s*\(\|decodeFormState\s*\(\|loadServerAction\s*\(' $T` |
| RC-10 | `$RG -- '--host\b\|host\s*:\s*(true\|["'"'"']0\.0\.0\.0)' -g 'package.json' -g 'vite.config.*'` |

## Secrets and data

| Check | Command |
| --- | --- |
| SD-01 | `$RG '\b(VITE\|REACT_APP\|PUBLIC\|EXPO_PUBLIC)_[A-Z0-9_]*(SECRET\|PRIVATE\|PASSWORD\|SERVICE_ROLE\|TOKEN\|API_KEY\|ACCESS_KEY)'` (include `.env*`; redact values) |
| SD-02 | `$RG '\b(sk\|rk)_(test\|live\|prod)_[a-zA-Z0-9]{10,99}\|sk-ant-api03-\|sk-(proj\|svcacct\|admin)-\|\bAIza[\w-]{35}\|ghp_[0-9a-zA-Z]{36}\|\b(A3T[A-Z0-9]\|AKIA\|ASIA\|ABIA\|ACCA)[A-Z2-7]{16}\b\|xoxb-[0-9]{10,13}-\|BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY'` |
| SD-01, SD-02 in a build | if the throwaway copy has `dist/` or `build/`: `rg -n -o -g '*.js' '<same pattern>' dist build` |
| SD-03 | `$RG 'envPrefix\s*:\|["'"'"']process\.env["'"'"']\s*:\|define\s*:\s*\{[^}]*process\.env\s*[,}]' -g '*.config.*'` |
| SD-04 | `$RG -i '(localStorage\|sessionStorage)\.setItem\(\s*["'"'"'`][^"'"'"'`]*(token\|jwt\|auth\|session\|refresh\|access)' $T` |
| SD-06 | `$RG 'sourcemap\s*:\s*(true\|["'"'"']hidden)\|GENERATE_SOURCEMAP\s*=\s*true\|devtool\s*:\s*["'"'"']source-map'` |
| SD-07 | `$RG -n '^(let\|const)\s+\w*(store\|cache)\w*\s*=' -g '*server*' -g '*entry*' $T` |
| SD-08 | `$RG 'dangerouslyAllowBrowser\s*:\s*true' $T` |
| SD-09 | `$RG -i 'console\.(log\|info\|debug)\([^)]*(token\|secret\|password\|apiKey\|api_key)' $T` |

## Auth, routing, client trust

| Check | Command |
| --- | --- |
| AR-01 | `$RG '\b(ProtectedRoute\|PrivateRoute\|RequireAuth\|AuthGuard\|RequireAdmin\|withAuth)\b\|\bisAdmin\b\|role\s*===?\s*["'"'"']admin' $T` |
| AR-02 | `$RG -i 'jwt-decode\|jwtDecode\s*\(\|localStorage\.getItem\(\s*["'"'"'](role\|isAdmin\|user\|permissions)' $T` |
| AR-03 | `$RG '(searchParams\|URLSearchParams\|query\|params)[^\n]{0,40}\b(next\|redirect\|redirectTo\|returnTo\|return_to\|returnUrl\|callbackUrl\|continue\|dest\|target)\b' $T` |
| AR-03 | `$RG 'window\.location(\.href)?\s*=\|location\.(assign\|replace)\s*\(\|window\.open\s*\(\|\bredirect\s*\(' $T` |
| AR-04 | `$RG 'addEventListener\(\s*["'"'"']message["'"'"']\|onmessage\s*=\|postMessage\([^)]*,\s*["'"'"']\*["'"'"']' $T` |
| AR-05 | `$RG -i 'credentials\s*:\s*["'"'"']include["'"'"']\|withCredentials\s*[:=]\s*true\|SameSite=None'` |
| AR-06 | `$RG -i '[?&#](access_token\|id_token\|token\|api_key\|apikey)=' $T` |

## AI-generated patterns

| Check | Command |
| --- | --- |
| AI-01 | `$RG -i '(TODO\|FIXME\|XXX)[^\n]{0,60}(auth\|permission\|secur\|validat\|sanitiz\|csrf\|rate.?limit)' $T` |
| AI-02 | `$RG '(isAuthorized\|isAdmin\|canAccess\|checkPermission\|hasPermission\|isAllowed\|verifyToken)\s*[=(][^\n{]*\{\s*return\s+true' $T` |
| AI-04 | `$RG -n 'function (sanitize\|escape\|validate)\w*\|const (sanitize\|escape\|validate)\w*\s*=' $T` (read each body) |

## Stack and mode markers (guide 00)

| Marker | Command |
| --- | --- |
| RSC in use | `$RG -l 'react-server-dom-(webpack\|parcel\|turbopack)\|@vitejs/plugin-rsc\|from ["'"'"']waku\|rwsdk\|@parcel/rsc'` |
| React Router mode | `ls react-router.config.* 2>/dev/null; $RG -l 'createBrowserRouter\|RouterProvider\|<BrowserRouter' $T` |
| SSR entry | `$RG -l 'renderToPipeableStream\|renderToReadableStream\|renderToString\|hydrateRoot' $T` |
| Next.js present (hand off) | `$RG -l '"next"\s*:' -g package.json` |

Sources: patterns derive from the checks files, which cite raw/owasp--cheatsheet-xss-dom-xss-redirects.md, raw/secrets--gitleaks-default-rules.md, raw/xss--react-markdown-readme-security.md, raw/rsc--react-docs-use-server-and-server-functions.md, and raw/lint--eslint-plugin-react-security-rules.md.
