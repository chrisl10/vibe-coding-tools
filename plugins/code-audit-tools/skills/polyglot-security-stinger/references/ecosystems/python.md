# Python reference (Django, FastAPI, Flask)

Loaded by [guides/02-python.md](../../guides/02-python.md). Stack id `python`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md).

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| P1 | Django: no `raw()`, `extra()`, `RawSQL()`, or `cursor.execute()` with f-strings, `%` formatting, `.format`, or `+` | CWE-89, OWASP A05:2025 |
| P2 | SQLAlchemy: no `text(f"...")` or `execute(f"...")`; values go through bound parameters | CWE-89 |
| P3 | No `pickle.load(s)`, `yaml.load` without `SafeLoader`, `jsonpickle.decode`, `shelve`, `marshal.loads`, `dill` on request or user-controlled data | CWE-502 |
| P4 | No `subprocess` with `shell=True`, no `os.system` / `os.popen` with user data | CWE-78 |
| P5 | No `eval` / `exec` / `compile` on user strings; no `Template(user_input)` in Jinja2 (server-side template injection) | CWE-94, CWE-1336 |
| P6 | `send_file` / `FileResponse` / `open()` with user paths are confined; Flask uses `send_from_directory` | CWE-22 |
| P7 | Outbound `requests` / `httpx` / `urllib` with user URLs are allowlisted, redirects off | CWE-918 |
| P8 | Django: `DEBUG = False` in production settings, `ALLOWED_HOSTS` not `['*']`, `SECRET_KEY` not a literal, `SECURE_*` and cookie `SECURE` flags set | OWASP A02:2025 |
| P9 | Django: no `@csrf_exempt` on cookie-authenticated views; `CsrfViewMiddleware` present | CWE-352 |
| P10 | Django / Jinja: no `mark_safe`, `|safe`, `Markup(user)`, `{% autoescape off %}` around user data | CWE-79 |
| P11 | Django REST Framework / Ninja / ModelForm: serializers and forms list explicit `fields`, not `__all__` or `exclude` only, for writable models | CWE-915 |
| P12 | FastAPI: every non-public route has an auth dependency (`Depends(...)` or router-level `dependencies=[...]`) | CWE-862 |
| P13 | Object access checks ownership (`get_object_or_404(Model, pk=pk, owner=request.user)`) | CWE-639 |
| P14 | JWT: `jwt.decode(..., algorithms=[...])`, no `verify_signature: False`, secret not a literal | CWE-347, CWE-798 |
| P15 | Flask: CSRF via an extension (Flask-WTF) for cookie sessions, `MAX_CONTENT_LENGTH` set, `TRUSTED_HOSTS` set, `app.run(debug=True)` not reachable in production | CWE-352, CWE-489 |
| P16 | Password hashing uses Argon2, bcrypt, or scrypt (pwdlib, passlib, Django hashers), never md5/sha1 | CWE-916 |

Sources: [raw/python--django-security.md], [raw/python--flask-security.md], [raw/python--fastapi-oauth2-jwt.md], [raw/python--pickle-warning.md], [raw/python--subprocess-security.md], [raw/owasp--deserialization-cheat-sheet.md].

## Sources of untrusted input

`request.GET`, `request.POST`, `request.body`, `request.FILES`, `request.headers`, `request.COOKIES`, `request.META` (Django); `request.args`, `request.form`, `request.json`, `request.files`, `request.get_data()` (Flask); path, query, body, header, cookie parameters and Pydantic models (FastAPI); Celery task arguments; webhook bodies.

## Sinks

| Class | Sink |
| --- | --- |
| SQL | `Model.objects.raw`, `.extra(`, `RawSQL(`, `connection.cursor().execute`, `sqlalchemy.text`, `session.execute`, `engine.execute` |
| Command | `subprocess.*(..., shell=True)`, `os.system`, `os.popen`, `commands.getoutput` |
| Code / template | `eval`, `exec`, `compile`, `jinja2.Template(user)`, `Environment().from_string(user)`, `render_template_string(user)` |
| Deserialization | `pickle.load(s)`, `cPickle`, `yaml.load`, `yaml.unsafe_load`, `jsonpickle.decode`, `shelve.open`, `marshal.loads` |
| Path | `open`, `send_file`, `FileResponse`, `os.path.join(base, user)`, `zipfile.extractall`, `tarfile.extractall` |
| SSRF | `requests.get/post`, `httpx.get`, `urllib.request.urlopen`, `aiohttp.ClientSession().get` |
| Redirect | `redirect(request.GET['next'])` or `redirect(request.args['next'])` without a host allowlist |

## ripgrep patterns

```bash
# SQL text built from strings
$RG -t py -e '\.(raw|extra)\(\s*f?["\x27]' -e 'RawSQL\(' -e 'execute\(\s*f["\x27]' -e 'execute\([^)]*(%\s*\(|\.format\(|\+\s*\w)' -e 'text\(\s*f["\x27]'
# Deserialization
$RG -t py -e 'pickle\.loads?\(' -e 'yaml\.(unsafe_)?load\(' -e 'jsonpickle\.decode' -e 'shelve\.open' -e 'marshal\.loads'
# Command and code execution
$RG -t py -e 'shell\s*=\s*True' -e 'os\.(system|popen)\(' -e '\b(eval|exec)\s*\(' -e 'render_template_string\(' -e 'from_string\('
# Path traversal
$RG -t py -e 'send_file\(' -e 'FileResponse\(' -e 'open\([^)]*request\.' -e 'extractall\('
# SSRF
$RG -t py -e '(requests|httpx)\.(get|post|put|request)\(\s*(url|target|request\.)' -e 'urlopen\('
# Django settings
$RG -t py -e '^\s*DEBUG\s*=\s*True' -e 'ALLOWED_HOSTS\s*=\s*\[\s*["\x27]\*' -e 'SECRET_KEY\s*=\s*["\x27]' -e 'CORS_ALLOW_ALL_ORIGINS\s*=\s*True' -e 'SESSION_COOKIE_SECURE\s*=\s*False' -e 'CSRF_COOKIE_SECURE\s*=\s*False'
# Django CSRF and XSS escapes
$RG -t py -e '@csrf_exempt' -e 'mark_safe\(' -e 'Markup\(' ; $RG -g '*.html' -g '*.jinja*' -e '\|\s*safe\b' -e 'autoescape\s+(off|false)'
# Mass assignment in serializers and forms
$RG -t py -e 'fields\s*=\s*["\x27]__all__["\x27]' -e 'Model(Serializer|Form)\)' -e '\*\*request\.(data|POST|json)' -e '\*\*(payload|body|data)\.(dict|model_dump)\(\)'
# FastAPI routes (list them, then confirm each has an auth dependency)
$RG -t py -e '@(app|router)\.(get|post|put|patch|delete)\(' -e 'Depends\('
# JWT
$RG -t py -e 'jwt\.decode\(' -e 'verify_signature["\x27]?\s*:\s*False' -e 'algorithms\s*=\s*\[\s*["\x27]none'
# Flask debug and CSRF
$RG -t py -e 'debug\s*=\s*True' -e 'CSRFProtect|flask_wtf' -e 'MAX_CONTENT_LENGTH' -e 'WTF_CSRF_ENABLED\s*=\s*False'
# Weak hashing for passwords
$RG -t py -e 'hashlib\.(md5|sha1)\(' -e 'MD5PasswordHasher|UnsaltedMD5'
```

## Vulnerable vs fixed pairs

**Django raw SQL**

```python
# vulnerable
User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{request.GET['u']}'")
# fixed
User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [request.GET["u"]])
```

**SQLAlchemy**

```python
# vulnerable
session.execute(text(f"SELECT * FROM orders WHERE id = {order_id}"))
# fixed
session.execute(text("SELECT * FROM orders WHERE id = :id"), {"id": order_id})
```

**Deserialization**

```python
# vulnerable
data = pickle.loads(base64.b64decode(request.cookies["state"]))
cfg = yaml.load(request.data, Loader=yaml.Loader)
# fixed
data = json.loads(signer.unsign(request.cookies["state"]))
cfg = yaml.safe_load(request.data)
```

**Command injection**

```python
# vulnerable
subprocess.run(f"ping -c 1 {host}", shell=True)
# fixed
subprocess.run(["ping", "-c", "1", "--", host], check=True)
```

**Server-side template injection (Flask)**

```python
# vulnerable
return render_template_string("Hello " + request.args["name"])
# fixed
return render_template_string("Hello {{ name }}", name=request.args["name"])
```

**FastAPI missing auth**

```python
# vulnerable: no dependency, anyone can read any invoice
@app.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return db.get(Invoice, invoice_id)
# fixed
@app.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int, user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    inv = db.scalar(select(Invoice).where(Invoice.id == invoice_id, Invoice.owner_id == user.id))
    if inv is None:
        raise HTTPException(status_code=404)
    return inv
```

**DRF mass assignment**

```python
# vulnerable: is_staff and owner are writable
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
# fixed
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "display_name", "bio"]
        read_only_fields = ["id"]
```

**Django production settings**

```python
# vulnerable
DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "django-insecure-..."
# fixed
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
SECRET_KEY = env("SECRET_KEY")
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads uv.lock, poetry.lock, pdm.lock, Pipfile.lock, pylock.toml, and requirements.txt (best effort; unpinned lines produce no match) [raw/deps--osv-scanner-supported-lockfiles.md].
2. Fallback: `pip-audit --no-deps -r requirements.txt -f json` on fully pinned files, or `pip-audit --locked .` for lockfiles. Without pins, `pip-audit -r` resolves like `pip install`, so run only inside the throwaway copy [raw/deps--pip-audit.md].
3. Unpinned requirements are themselves a `low` finding (supply chain, OWASP A03:2025) because nothing can be audited reproducibly.

## Sources

[raw/python--django-security.md], [raw/python--flask-security.md], [raw/python--fastapi-oauth2-jwt.md], [raw/python--pickle-warning.md], [raw/python--subprocess-security.md], [raw/deps--pip-audit.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md]
