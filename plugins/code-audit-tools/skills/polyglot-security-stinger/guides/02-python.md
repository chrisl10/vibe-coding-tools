# 02 Python (Django, FastAPI, Flask)

For every path under stack id `python`. Loads [../references/ecosystems/python.md](../references/ecosystems/python.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

## Steps

1. **Identify the framework** from `detect.json.details.python[]`. A path can be a library or a script collection with no web framework; then skip web checks (P8 to P15) and focus on deserialization, command execution, SQL, and secrets.
2. **Find the production settings.**
   - Django: the settings module used in production (`DJANGO_SETTINGS_MODULE` in Dockerfiles, Procfiles, `wsgi.py` / `asgi.py`). Check P8 there, not only in `settings.py` defaults [raw/python--django-security.md].
   - Flask: the app factory and config classes; check `SECRET_KEY`, `SESSION_COOKIE_*`, `MAX_CONTENT_LENGTH` (not set by default), `TRUSTED_HOSTS`, and any `app.run(debug=True)` reachable in production [raw/python--flask-security.md].
   - FastAPI: app creation, middleware (CORS), routers, and dependency wiring.
3. **Map routes and auth.**
   - Django: `urls.py` to views; check `login_required`, `LoginRequiredMixin`, DRF `permission_classes` and `DEFAULT_PERMISSION_CLASSES`.
   - FastAPI: list every `@app` / `@router` route and whether it or its router carries an auth dependency; a route without one is public [raw/python--fastapi-oauth2-jwt.md].
   - Flask: `@login_required` or `before_request` hooks.
4. **Run the checklist P1 to P16** using the reference's `rg` blocks. Read every production hit and trace the value to a request source.
5. **SQL.** Django ORM calls are parameterized; focus on `raw`, `extra`, `RawSQL`, `cursor.execute`, and SQLAlchemy `text()` / `execute()` with built strings (P1, P2) [raw/python--django-security.md].
6. **Deserialization and execution.** Every `pickle`, `yaml.load`, `subprocess(..., shell=True)`, `os.system`, `eval`, `render_template_string` hit gets a source trace (P3 to P5) [raw/python--pickle-warning.md] [raw/python--subprocess-security.md].
7. **Templates.** Search templates for `|safe`, `autoescape off`, and code for `mark_safe` / `Markup` on user data, plus unquoted attributes in Jinja (P10) [raw/python--flask-security.md].
8. **Mass assignment.** DRF serializers and Django ModelForms with `fields = "__all__"` on writable models, Pydantic models that include role or owner fields and are dumped straight into the ORM (P11) [raw/owasp--mass-assignment-cheat-sheet.md].
9. **CSRF.** Django: `@csrf_exempt` on cookie-session views. Flask: no CSRF extension with cookie sessions (P9, P15).
10. **JWT and passwords.** `jwt.decode` with an explicit `algorithms` list; no disabled signature checks; Argon2 or bcrypt for passwords (P14, P16) [raw/python--fastapi-oauth2-jwt.md].
11. **Dependencies.** Follow the reference's dependency section (pin status matters for pip-audit); detail in guide 10 [raw/deps--pip-audit.md].
12. **Write findings** per guide 14 with `tags: ["python", "<framework>", "<class>"]`.

## Done when

Production settings were read, every route has an auth verdict, every checklist item has a result in notes, and every pattern hit in production code was read.

## Sources

[raw/python--django-security.md], [raw/python--flask-security.md], [raw/python--fastapi-oauth2-jwt.md], [raw/python--pickle-warning.md], [raw/python--subprocess-security.md], [raw/deps--pip-audit.md], [raw/owasp--mass-assignment-cheat-sheet.md]
