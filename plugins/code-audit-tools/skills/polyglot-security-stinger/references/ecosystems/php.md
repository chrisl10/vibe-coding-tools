# PHP reference (Laravel, Symfony, plain PHP)

Loaded by [guides/06-php.md](../../guides/06-php.md). Stack id `php`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md). Library names in sink tables are search hints; a hit becomes a finding only after the call site is read.

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| PH1 | No SQL built with `.` or `"...$var..."` into `mysqli_query`, `PDO::query`, `PDO::exec`, `DB::select/statement/unprepared`, `whereRaw`, `orderByRaw`, `selectRaw`, `havingRaw`, `DB::raw`, Doctrine `createQuery` / `executeQuery` | CWE-89 |
| PH2 | Values are bound (`prepare` plus `execute([...])`, `?` bindings in `whereRaw('x = ?', [$v])`, Doctrine `setParameter`) | CWE-89 |
| PH3 | Laravel models define `$fillable` (or a non-empty `$guarded`); no `$guarded = []` with `create($request->all())` / `fill($request->all())` / `update($request->all())` | CWE-915 |
| PH4 | Laravel uses `$request->validated()` or `$request->only([...])` for writes | CWE-915 |
| PH5 | No `exec`, `system`, `shell_exec`, `passthru`, `popen`, `proc_open`, or backticks with user data; if a shell is unavoidable, `escapeshellarg` per argument | CWE-78 |
| PH6 | No `unserialize()` on cookies, request data, or cache values an attacker can write | CWE-502 |
| PH7 | No `include` / `require` / `include_once` / `require_once` with a user-influenced path; no `eval`, `assert` with strings, `create_function`, `preg_replace` with `/e` | CWE-98, CWE-94 |
| PH8 | File reads and downloads (`file_get_contents`, `fopen`, `readfile`, `Storage::download`, `response()->download`) confine user paths | CWE-22 |
| PH9 | `file_get_contents($url)` / curl / Guzzle with user URLs are allowlisted | CWE-918 |
| PH10 | Blade uses `{{ }}`; `{!! !!}` only for trusted HTML. Twig: no `|raw` on user data. Plain PHP: `htmlspecialchars($v, ENT_QUOTES)` on output | CWE-79 |
| PH11 | Laravel: `VerifyCsrfToken` exceptions (`$except` or `validateCsrfTokens(except: [...])`) are only webhooks with signature checks. Symfony: no `'csrf_protection' => false` on forms used by browsers | CWE-352 |
| PH12 | `APP_DEBUG=false` and `APP_ENV=production` in production; `.env` not committed; Symfony `APP_SECRET` not a committed literal | CWE-489, CWE-798 |
| PH13 | Routes needing auth use `auth` middleware / `#[IsGranted]` / `access_control`, and policies or voters check ownership | CWE-862, CWE-639 |
| PH14 | Plain PHP: sessions regenerate on login (`session_regenerate_id(true)`), cookies `httponly`, `secure`, `samesite` | CWE-384 |
| PH15 | Passwords use `password_hash` / `password_verify` (or framework hashing), never `md5` / `sha1` | CWE-916 |
| PH16 | `extract($_GET)`, `parse_str($x)` without a result array, and `$$var` are absent | CWE-621 |

Sources: [raw/php--laravel-mass-assignment.md], [raw/php--unserialize-warning.md], [raw/php--symfony-csrf.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md].

## Sources of untrusted input

`$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`, `$_FILES`, `$_SERVER['HTTP_*']`, `php://input`; Laravel `$request->input()`, `->all()`, `->query()`, route parameters, `->file()`; Symfony `$request->query`, `->request`, `->getPayload()`, `->headers`, `->cookies`, route attributes.

## ripgrep patterns

```bash
# SQL building
$RG -t php -e '(mysqli_query|->query|->exec|->prepare)\(\s*["\x27][^"\x27]*(\$\w|["\x27]\s*\.)' -e '(whereRaw|orderByRaw|selectRaw|havingRaw|groupByRaw|DB::raw|DB::select|DB::statement|DB::unprepared)\(\s*["\x27][^"\x27]*(\$|\.\s*\$)' -e 'createQuery\(\s*["\x27][^"\x27]*\$'
# Mass assignment
$RG -t php -e 'protected\s+\$guarded\s*=\s*\[\s*\]' -e '(create|fill|update|forceFill|forceCreate)\(\s*\$request->all\(\)' -e 'Model::unguard\(' -e '\$request->all\(\)'
# Command execution
$RG -t php -e '\b(exec|system|shell_exec|passthru|popen|proc_open)\s*\(' -e '`[^`]*\$'
# Deserialization and code execution
$RG -t php -e '\bunserialize\s*\(' -e '\beval\s*\(' -e '\bassert\s*\(\s*\$' -e 'create_function' -e 'preg_replace\(\s*["\x27].*\/e["\x27]'
# Includes
$RG -t php -e '\b(include|require)(_once)?\s*\(?\s*[^;]*\$_(GET|POST|REQUEST|COOKIE)' -e '\b(include|require)(_once)?\s*\(?\s*\$\w+'
# Paths and SSRF
$RG -t php -e '(file_get_contents|fopen|readfile|file|unlink)\(\s*\$(_GET|_POST|_REQUEST|request|path|url|file)' -e 'curl_setopt\([^,]+,\s*CURLOPT_URL,\s*\$' -e '->(download|file)\(\s*\$request'
# Output escaping
$RG -g '*.blade.php' -e '\{!!' ; $RG -t twig -e '\|\s*raw' ; $RG -t php -e 'echo\s+\$_(GET|POST|REQUEST|COOKIE)'
# CSRF exceptions
$RG -t php -e 'protected\s+\$except\s*=' -e 'validateCsrfTokens\(\s*except' -e '["\x27]csrf_protection["\x27]\s*=>\s*false' -e 'csrf_protection:\s*false'
# Debug and secrets
$RG -g '.env*' -e '^APP_DEBUG=true' -e '^APP_ENV=(local|dev)' ; $RG -t php -e '(password|secret|api_key|token)["\x27]?\s*(=>|=)\s*["\x27][^"\x27]{12,}["\x27]'
# Variable variables and extract
$RG -t php -e '\bextract\(\s*\$_' -e 'parse_str\(\s*\$[^,]+\)' -e '\$\$\w+'
# Weak hashing
$RG -t php -e '\b(md5|sha1)\(\s*\$(password|pass|pwd)'
```

## Vulnerable vs fixed pairs

**Laravel raw SQL**

```php
// vulnerable
$users = DB::select("SELECT * FROM users WHERE email = '$email'");
User::whereRaw("name LIKE '%" . $request->q . "%'")->get();
// fixed
$users = DB::select('SELECT * FROM users WHERE email = ?', [$email]);
User::where('name', 'like', '%'.$request->q.'%')->get();
```

**Plain PDO**

```php
// vulnerable
$pdo->query("SELECT * FROM orders WHERE id = " . $_GET['id']);
// fixed
$stmt = $pdo->prepare('SELECT * FROM orders WHERE id = ?');
$stmt->execute([$_GET['id']]);
```

**Mass assignment (Laravel docs example of the risk)**

```php
// vulnerable: model has protected $guarded = [];
User::create($request->all());   // attacker adds is_admin=1
// fixed
class User extends Model { protected $fillable = ['name', 'email']; }
User::create($request->validated());
```

**unserialize**

```php
// vulnerable
$prefs = unserialize($_COOKIE['prefs']);
// fixed
$prefs = json_decode($_COOKIE['prefs'] ?? '{}', true, 8, JSON_THROW_ON_ERROR);
```

**Local file inclusion**

```php
// vulnerable
include $_GET['page'] . '.php';
// fixed
$pages = ['home' => 'home.php', 'about' => 'about.php'];
include __DIR__ . '/pages/' . ($pages[$_GET['page'] ?? 'home'] ?? 'home.php');
```

**Command**

```php
// vulnerable
shell_exec("convert " . $_FILES['f']['name'] . " out.png");
// fixed: avoid the shell; if unavoidable, quote each argument
$cmd = 'convert ' . escapeshellarg($safePath) . ' out.png';
```

**Symfony CSRF**

```php
// vulnerable: browser form with CSRF turned off
$resolver->setDefaults(['csrf_protection' => false]);
// fixed: keep the default (enabled), or for manual forms
if (!$this->isCsrfTokenValid('delete-item', $request->getPayload()->get('token'))) { throw $this->createAccessDeniedException(); }
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads composer.lock [raw/deps--osv-scanner-supported-lockfiles.md].
2. Fallback: `composer audit --locked --format=json` (no vendor install needed; also flags abandoned packages) [raw/deps--composer-audit.md].
3. Plain PHP with no composer.lock: dependency audit is `not-run` for that path; record the cap and list any vendored libraries you can identify by folder name as `info`.

## Sources

[raw/php--laravel-mass-assignment.md], [raw/php--unserialize-warning.md], [raw/php--symfony-csrf.md], [raw/deps--composer-audit.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md]
