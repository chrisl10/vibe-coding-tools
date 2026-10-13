# Ruby on Rails reference

Loaded by [guides/05-ruby-on-rails.md](../../guides/05-ruby-on-rails.md). Stack id `ruby`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md). Library names in sink tables are search hints; a hit becomes a finding only after the call site is read.

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| RB1 | No `where`, `order`, `group`, `having`, `joins`, `find_by_sql`, `select`, `pluck`, or `exists?` with string interpolation of params | CWE-89 |
| RB2 | Controllers use strong parameters (`params.require(...).permit(...)`); no `permit!`, no `params.to_unsafe_h` into models | CWE-915 |
| RB3 | `protect_from_forgery` is active (default in `ActionController::Base`); no `skip_forgery_protection` / `skip_before_action :verify_authenticity_token` on cookie-authenticated actions | CWE-352 |
| RB4 | No `system`, backticks, `%x()`, `exec`, `spawn`, `IO.popen`, or `Open3` with a single interpolated string | CWE-78 |
| RB5 | No `Kernel#open` / `URI.open` with user input (pipes run commands; URLs fetch remote) | CWE-78, CWE-918 |
| RB6 | No `Marshal.load`, `YAML.unsafe_load`, or `YAML.load` with broad permitted classes on untrusted data | CWE-502 |
| RB7 | Views do not use `raw`, `html_safe`, or `<%==` on user data; `sanitize` uses allowlists | CWE-79 |
| RB8 | `redirect_to params[...]` is not used without an allowlist | CWE-601 |
| RB9 | `send_file` / `send_data` / `File.read` with user paths verify the expanded path stays under the base | CWE-22 |
| RB10 | Validation regexes use `\A` and `\z`, not `^` and `$` | CWE-625 |
| RB11 | `config.force_ssl = true` in production; `reset_session` after login | CWE-319, CWE-384 |
| RB12 | Secrets live in `config/credentials.yml.enc` or env; `config/master.key` and `.env` are not committed | CWE-798 |
| RB13 | Every controller that needs auth has a `before_action` for authentication and an authorization check (Pundit `authorize`, CanCanCan `authorize!`, or explicit scoping like `current_user.posts.find`) | CWE-862, CWE-639 |
| RB14 | Login, password reset, and token endpoints are rate limited (`rate_limit` in Rails 8, or Rack::Attack) | CWE-307 |
| RB15 | `constantize`, `send`, `public_send`, `safe_constantize` are not called with user strings | CWE-470 |

Sources: [raw/ruby--rails-security-guide.md], [raw/ruby--marshal-warning.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md].

Thin spot: Psych `YAML.load` safety defaults are not in the archive; treat every YAML load of untrusted input as a manual read [research/distilled-polyglot-security.md].

## Sources of untrusted input

`params`, `request.headers`, `request.body`, `cookies`, `request.env`, uploaded files (`original_filename`), ActiveJob arguments from external producers, webhook payloads.

## ripgrep patterns

```bash
# SQL interpolation
$RG -t ruby -e '\.(where|order|group|having|joins|select|pluck|find_by_sql|exists\?|lock|reorder)\(\s*"[^"]*#\{' -e 'find_by_sql\(' -e 'connection\.execute\('
# Mass assignment
$RG -t ruby -e 'permit!' -e 'to_unsafe_h' -e '\.(new|create|update|assign_attributes|update_attributes)\(\s*params\[' -e '\.(new|create|update)\(\s*params\s*\)'
# CSRF disabled
$RG -t ruby -e 'skip_forgery_protection' -e 'skip_before_action\s+:verify_authenticity_token' -e 'protect_from_forgery\s+with:\s*:null_session'
# Command execution and Kernel#open
$RG -t ruby -e '\b(system|exec|spawn)\s*\(?\s*"[^"]*#\{' -e '`[^`]*#\{' -e '%x[\(\{\[]' -e 'IO\.popen' -e 'Open3\.' -e '(^|[^.\w])open\(\s*params' -e 'URI\.open\('
# Deserialization
$RG -t ruby -e 'Marshal\.load' -e 'YAML\.(unsafe_)?load\(' -e 'Psych\.(unsafe_)?load\('
# XSS escapes
$RG -t ruby -t erb -t haml -e '\.html_safe' -e '\braw\s*\(' -e '<%==' -e '!=\s'
# Redirects and files
$RG -t ruby -e 'redirect_to\s*\(?\s*params' -e 'send_file\s*\(?[^)]*params' -e 'File\.(read|open)\([^)]*params'
# Regex anchors in validations
$RG -t ruby -e 'format:\s*\{\s*with:\s*/\^' -e 'validates_format_of.*\/\^'
# Reflection
$RG -t ruby -e '(constantize|safe_constantize)' -e '\.(send|public_send)\(\s*params'
# Settings
$RG -t ruby -e 'force_ssl\s*=\s*false' -e 'config\.hosts\.clear' ; $RG -g 'config/master.key' -g '.env' --files
```

## Vulnerable vs fixed pairs

**SQL**

```ruby
# vulnerable
Project.where("name = '#{params[:name]}'")
User.order("#{params[:sort]} #{params[:dir]}")
# fixed
Project.where(name: params[:name])
User.order(SORTABLE.fetch(params[:sort], "created_at") => (params[:dir] == "asc" ? :asc : :desc))
```

**Strong parameters**

```ruby
# vulnerable
@user.update(params[:user].permit!)
# fixed
@user.update(params.require(:user).permit(:name, :email))
```

**Command injection**

```ruby
# vulnerable
system("convert #{params[:file]} out.png")
# fixed
system("convert", "--", safe_name(params[:file]), "out.png", exception: true)
```

**Path traversal (from the Rails guide)**

```ruby
# vulnerable
send_file("/var/www/uploads/" + params[:filename])
# fixed
basename = File.expand_path("../../files", __dir__)
filename = File.expand_path(File.join(basename, @file.name))
raise if basename != File.expand_path(File.dirname(filename))
send_file filename
```

**Authorization**

```ruby
# vulnerable: any signed-in user can read any invoice
@invoice = Invoice.find(params[:id])
# fixed: scope through the owner
@invoice = current_user.invoices.find(params[:id])
```

**Open redirect**

```ruby
# vulnerable
redirect_to params[:return_to]
# fixed
redirect_to(safe_return_path(params[:return_to]) || root_path)
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads Gemfile.lock and gems.locked [raw/deps--osv-scanner-supported-lockfiles.md].
2. Fallback: `bundle-audit check --update --format json --output bundle-audit.json` (also flags `http://` and `git://` gem sources) [raw/deps--bundler-audit.md].
3. Brakeman is the standard Rails static analyzer; it is not in this archive, so if you run it record its version and treat its confidence labels as your `possible` or `likely` only after reading each hit.

## Sources

[raw/ruby--rails-security-guide.md], [raw/ruby--marshal-warning.md], [raw/deps--bundler-audit.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md]
