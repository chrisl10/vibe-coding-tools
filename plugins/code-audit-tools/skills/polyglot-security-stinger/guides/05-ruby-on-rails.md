# 05 Ruby on Rails

For every path under stack id `ruby`. Loads [../references/ecosystems/ruby.md](../references/ecosystems/ruby.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

## Steps

1. **Identify the app type** from `detect.json.details.ruby[]`: Rails app (has `rails`), Sinatra, Hanami, Grape, or a gem. Note the Rails version from Gemfile.lock.
2. **Read the base controller.** `app/controllers/application_controller.rb`: authentication `before_action`, `protect_from_forgery` (default on in `ActionController::Base`; API-only apps inheriting `ActionController::API` use tokens), Pundit or CanCanCan setup, `rescue_from` handlers [raw/ruby--rails-security-guide.md].
3. **Map routes.** `config/routes.rb` (or `bin/rails routes` only if Ruby is installed and the run allows booting the app in the copy; otherwise read the file). For each controller, note `skip_before_action` lines that remove authentication or CSRF checks.
4. **Run the checklist RB1 to RB15** with the reference's `rg` blocks; read each production hit.
5. **SQL.** String interpolation in `where`, `order`, `pluck`, `find_by_sql`, and similar (RB1). Hash conditions and `?` placeholders are safe [raw/ruby--rails-security-guide.md].
6. **Strong parameters.** `permit!`, `to_unsafe_h`, or raw `params[:model]` into `new`, `create`, `update` (RB2). Check permitted lists for `role`, `admin`, `owner_id`, `account_id`.
7. **Authorization.** Lookups like `Model.find(params[:id])` in controllers where other users' records exist; prefer `current_user.records.find` or policy `authorize` (RB13).
8. **Commands, files, deserialization, redirects.** RB4 to RB9 [raw/ruby--rails-security-guide.md] [raw/ruby--marshal-warning.md]. YAML loading defaults are a thin spot: read each `YAML.load` call [research/distilled-polyglot-security.md].
9. **Production config.** `config/environments/production.rb`: `force_ssl`, `config.hosts`; `config/credentials.yml.enc` present and `config/master.key` not committed (RB11, RB12).
10. **Dependencies.** osv-scanner on Gemfile.lock or bundle-audit (guide 10) [raw/deps--bundler-audit.md].
11. **Write findings** per guide 14 with `tags: ["ruby", "rails", "<class>"]`.

## Done when

The base controller and production config were read, every controller has an auth and CSRF verdict, every checklist item has a result in notes, and every production hit was read.

## Sources

[raw/ruby--rails-security-guide.md], [raw/ruby--marshal-warning.md], [raw/deps--bundler-audit.md], [raw/owasp--mass-assignment-cheat-sheet.md]
