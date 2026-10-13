# Detection patterns (ripgrep)

Run from the audited repository root (read only), limited to the stack paths from `intake.json` when there are several apps. Save each command and its output to `<workspace>/02-security/raw/sveltekit-rg-<check>.txt` so the evidence index can point at it. Every hit is a candidate, never a finding: confirm with the steps in [check-catalog.md](check-catalog.md).

Define this helper once per shell session. It skips build output and dependencies:

```bash
srg() { rg -n --no-heading --hidden \
  -g '!node_modules' -g '!.svelte-kit' -g '!build' -g '!dist' -g '!.git' -g '!.vercel' -g '!.netlify' -g '!.output' "$@" ./; }
```

The trailing `./` matters: without a path, ripgrep reads standard input when it is not a terminal, and an agent shell can hang waiting on it. For the same reason, every plain `rg` below names its files. Patterns are written for ripgrep's default regex engine unless the command has `-P` (PCRE, needed for lookarounds). All commands below were run against a fixture repository on 2026-09-30 to check that they parse.

## Inventory

```bash
srg --files | rg '/\+(page|layout)\.server\.(ts|js)$|/\+server\.(ts|js)$'      # server loads, actions, endpoints
srg --files | rg '/\+(page|layout)\.(ts|js)$'                                 # universal loads
srg --files | rg 'src/hooks(\.server|\.client)?\.(ts|js)$'                    # hooks
srg --files | rg '\.remote\.(ts|js)$'                                         # remote function files
srg -e 'export const \w+\s*=\s*(query(\.batch|\.live)?|form|command|prerender)\(' -g '*.remote.*'
srg -e 'export const (prerender|ssr|csr|config)\s*='                          # page options
srg --files | rg 'src/service-worker'
```

## Versions (SVK-V1, SVK-V2)

```bash
rg -n '(svelte|@sveltejs/kit|devalue|@sveltejs/adapter-[a-z]+)@[0-9]' pnpm-lock.yaml yarn.lock bun.lock 2>/dev/null
rg -n -A1 '"node_modules/(svelte|@sveltejs/kit|devalue|@sveltejs/adapter-[a-z]+)"' package-lock.json 2>/dev/null
rg -n -P "NODE_ENV\s*[=:]\s*[\"']?(?!production)\w+" package.json .github Dockerfile* vercel.json netlify.toml fly.toml render.yaml 2>/dev/null
```

## Boundary (SVK-B1 to B7)

```bash
# B1 whole-row returns from server code
srg -e 'findMany\(|findFirst\(|select\(\)\s*\.from|SELECT \*' -g '+*.server.*' -g '*.remote.*'
# B2 what root and group layouts return
srg -e 'return' -A6 -g 'src/routes/+layout.server.*' -g 'src/routes/**/(*)/+layout.server.*'
# B3 secret-looking public names, and Vite client env
srg -e 'PUBLIC_[A-Z0-9_]*(SECRET|PRIVATE|PASSWORD|SERVICE_ROLE|DATABASE|DB_URL|TOKEN)'
srg -e 'import\.meta\.env\.VITE_'
# B3 committed env files: list names only, never print values
git ls-files | rg '(^|/)\.env(\.|$)'
rg -o -P '^[A-Z0-9_]+(?==)' path/to/.env.file
# B4 credentials in universal loads
srg -e 'Authorization|x-api-key|Bearer |apiKey' -g '+page.ts' -g '+page.js' -g '+layout.ts' -g '+layout.js'
# B5 module state shared across requests
srg -e '^(let|var) \w+' -g '*.server.*' -g 'src/lib/server/**' -g '*.remote.*'
srg -e '^export (const|let) \w+\s*=\s*(writable|readable|derived)\(' -g 'src/lib/**'
srg -e '^export (const|let) \w+\s*=\s*\$state' -g '*.svelte.ts' -g '*.svelte.js'
# B6 client components importing server code (build should fail; find dead or test-only files)
srg -e '\$env/(static|dynamic)/private|\$lib/server' -g '*.svelte'
# B7 Buffers or typed arrays returned from server code
srg -e 'Buffer\.from\(|readFileSync\(|new Uint8Array\(' -g '+*.server.*' -g '*.remote.*'
```

## Actions, endpoints, remote functions (SVK-E1 to E9)

```bash
srg -e 'export const actions' -A30 -g '+page.server.*'                                   # E1
srg -e 'export (async )?(function|const) (GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD|fallback)\b' -g '+server.*'   # E2
srg -c -e 'locals\.(user|session)|getRequestEvent\(\)|error\(\s*40[13]' -g '+*.server.*' -g '+server.*' -g '*.remote.*'   # auth hint counts
srg -e "(query|command|form|prerender)(\.batch)?\(\s*['\"]unchecked" -g '*.remote.*'      # E4
srg -e '(v|z)\.(any|unknown)\(\)|passthrough\(\)|looseObject' -g '*.remote.*'            # E4 loose schemas
srg -e 'params\.\w*[iI]d\b|\.get\(.\w*[iI]d.\)' -g '+*.server.*' -g '+server.*' -g '*.remote.*'   # E5
srg -e 'getRequestEvent\(\)' -A8 -g '*.remote.*' | rg 'url\.|route\.|params\.'           # E6
srg -e 'trustedOrigins|checkOrigin' -g 'svelte.config.*'                                 # E7
srg -i -e 'access-control-allow-(origin|credentials)'                                    # E7 CORS
srg -e 'export (async )?(function|const) GET' -A20 -g '+server.*' | rg 'insert|update|delete|\.set\(|cookies\.set'   # E7 writes in GET
srg -e 'Object\.fromEntries\(\s*(await\s+)?(\w+\.)?formData' -g '+*.server.*' -g '+server.*' -g '*.remote.*'   # E8
srg -e 'requested\([^)]*Infinity|BODY_SIZE_LIMIT\s*=\s*(Infinity|0)\b'                   # E9
```

## Hooks and authorization (SVK-H1 to H7)

```bash
srg -e 'redirect\(|error\(\s*40[13]' -g '+layout.server.*'                                # H1
srg -e 'url\.pathname|route\.id|isRemoteRequest' -g 'src/hooks.server.*'                 # H2
srg -e 'jwtDecode|jwt\.decode|decodeJwt|atob\(|JSON\.parse\(.*cookies\.get|headers\.get\(.x-(user|role)' -g 'src/hooks.server.*' -g 'src/lib/server/**'   # H3
srg -P -e "fetch\(\s*+(?![\"'/])" -g '+*.server.*' -g '+server.*' -g '*.remote.*' -g 'src/hooks.server.*' -g 'src/lib/server/**'   # H4
srg -e 'handleFetch' -A15 -g 'src/hooks.server.*' | rg -i 'headers\.set\(.(cookie|authorization)'   # H4
srg -e 'filterSerializedResponseHeaders' -A2                                             # H5
srg -e 'handleError' -A10 -g 'src/hooks*'                                                # H6
srg -P -e "error\(\s*\d{3}\s*,\s*+(?![\"'])"                                              # H6 dynamic messages
srg -P -e "redirect\(\s*\d{3}\s*,\s*+(?![\"'/])"                                          # H7
srg -e 'searchParams\.get\(.(next|redirect|redirectTo|returnTo|returnUrl|callback).\)'  # H7
```

## XSS, CSP, cookies (SVK-X1 to X7)

```bash
srg -e '\{@html' -g '*.svelte' -g '*.md' -g '*.svx'                                       # X1
srg -e "from ['\"](marked|markdown-it|mdsvex|snarkdown|showdown|micromark|remark|rehype|svelte-exmarkdown)" ; srg -e 'happy-dom'   # X2
srg -e '\.innerHTML\s*=|\.outerHTML\s*=|insertAdjacentHTML|document\.write|createContextualFragment'   # X3
srg -e '<[a-zA-Z][^>]*\{\.\.\.' -g '*.svelte' ; srg -e '<svelte:element|hydratable\(|contenteditable' -g '*.svelte'   # X4
srg -e 'csp\s*:' -A12 -g 'svelte.config.*' ; srg -i -e 'content-security-policy'          # X5
srg -e 'cookies\.(set|serialize)\(' -A4 | rg 'httpOnly:\s*false|secure:\s*false|sameSite:\s*.none|domain:'   # X6
srg -e 'document\.cookie\s*='                                                            # X6
srg -i -e "(local|session)Storage\.setItem\(\s*['\"][^'\"]*(token|jwt|session|secret|key)"   # X7
```

## Config, adapters, prerender (SVK-C1 to C6)

```bash
srg -l -e 'prerender\s*=\s*true'        # C1: then read each file and its layouts for cookies, locals, getRequestEvent, db
srg -e 'isr\s*:|bypassToken'            # C2
rg -n 'ORIGIN|PROTOCOL_HEADER|HOST_HEADER|ADDRESS_HEADER|XFF_DEPTH|BODY_SIZE_LIMIT' Dockerfile* docker-compose* fly.toml render.yaml .env.example .github 2>/dev/null   # C3
srg -i -e 'x-forwarded-for|x-real-ip|cf-connecting-ip|getClientAddress'                   # C3
srg -e 'platform\??\.env' -g '+*.server.*' -g '+server.*'                                 # C4
srg -e 'cache\.put|caches\.open' -g 'src/service-worker*'                                 # C5
srg -e 'dangerZone|relative\s*:|publicPrefix|privatePrefix' -g 'svelte.config.*'          # C6
```

## AI-generated patterns (SVK-A1 to A5)

```bash
srg -e 'onMount|\$effect' -A8 -g '*.svelte' | rg 'goto\(|isAdmin|role|login'               # A1
srg -e 'export const ssr\s*=\s*false'                                                     # A1
srg -U -P -e 'try\s*\{[^}]*\b(redirect|error)\(' -g '+*.server.*' -g 'src/hooks.server.*' -g '*.remote.*'   # A2
srg -e "from ['\"](svelte/store|\\\$app/stores)['\"]" -g 'src/lib/**'                       # A3
srg -l -e 'export let |^\s*\$: |on:click|createEventDispatcher' -g '*.svelte'              # A5
```

Sources: [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md), [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md), [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md), [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md), [raw/kit-docs--adapter-node.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-node.md), [raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md), [raw/markdown--mdsvex-marked-dompurify.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/markdown--mdsvex-marked-dompurify.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md).
