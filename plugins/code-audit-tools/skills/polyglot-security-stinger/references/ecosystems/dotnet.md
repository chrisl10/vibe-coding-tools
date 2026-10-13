# .NET reference (ASP.NET Core)

Loaded by [guides/08-dotnet-aspnetcore.md](../../guides/08-dotnet-aspnetcore.md). Stack id `dotnet`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md). Library names in sink tables are search hints; a hit becomes a finding only after the call site is read.

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| D1 | EF Core: no `FromSqlRaw`, `ExecuteSqlRaw`, or `SqlQueryRaw` with interpolated or concatenated user data; prefer `FromSql`, `FromSqlInterpolated`, `ExecuteSql`, `SqlQuery` | CWE-89 |
| D2 | ADO.NET / Dapper: no `CommandText` or Dapper SQL built with `+` or `$"..."`; values passed as parameters | CWE-89 |
| D3 | No `BinaryFormatter`, `LosFormatter`, `NetDataContractSerializer`, `SoapFormatter`, `ObjectStateFormatter`; Json.NET `TypeNameHandling` is `None` for request data | CWE-502 |
| D4 | `Process.Start` does not run `cmd.exe /c` or `/bin/sh -c` with user data; use `ProcessStartInfo.ArgumentList` | CWE-78 |
| D5 | MVC / Razor Pages with cookie auth validate antiforgery: global `AutoValidateAntiforgeryTokenAttribute` or per-action `[ValidateAntiForgeryToken]`; `[IgnoreAntiforgeryToken]` only on non-cookie endpoints | CWE-352 |
| D6 | Minimal APIs with cookie auth and form binding call `AddAntiforgery` and `UseAntiforgery`; `.DisableAntiforgery()` only for bearer, API-key, or signed webhook endpoints | CWE-352 |
| D7 | Endpoints needing auth have `[Authorize]`, `.RequireAuthorization()`, or a fallback policy (`options.FallbackPolicy`); `[AllowAnonymous]` is deliberate; resource checks via `IAuthorizationService` or owner filters | CWE-862, CWE-639 |
| D8 | Model binding uses DTOs or `[Bind(...)]`; no EF entity with role or owner fields bound straight from `[FromBody]` / `[FromForm]` and saved | CWE-915 |
| D9 | `Path.Combine(base, userInput)` is checked with `Path.GetFullPath` plus `StartsWith(base)`; `PhysicalFile` / `File(...)` results confined | CWE-22 |
| D10 | `HttpClient.GetAsync(userUrl)` is allowlisted | CWE-918 |
| D11 | Razor: no `@Html.Raw(userData)` or `HtmlString` from user data | CWE-79 |
| D12 | `appsettings*.json` committed without real secrets; user secrets or a vault in use | CWE-798 |
| D13 | `UseDeveloperExceptionPage` only in Development; `UseHsts` and `UseHttpsRedirection` in production | CWE-209, CWE-319 |
| D14 | CORS: no `AllowAnyOrigin` with credentials, no `SetIsOriginAllowed(_ => true)` with `AllowCredentials` | CWE-942 |
| D15 | JWT bearer: `ValidateIssuer`, `ValidateAudience`, `ValidateLifetime`, `ValidateIssuerSigningKey` not set to false; `RequireHttpsMetadata` true in production | CWE-347 |
| D16 | XML: `XmlReaderSettings.DtdProcessing` not `Parse` on untrusted input; no `XmlResolver` on untrusted documents | CWE-611 |

Sources: [raw/dotnet--aspnetcore-antiforgery.md], [raw/dotnet--efcore-raw-sql.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md].

Version note: ASP.NET Core 11.0 documents an automatic `Sec-Fetch-Site` and `Origin` based CSRF middleware. At fetch time 11.0 was not generally available. For apps targeting `net10.0` or earlier, judge CSRF only by the token filters and `UseAntiforgery` that are actually in the code [raw/dotnet--aspnetcore-antiforgery.md].

## Sources of untrusted input

`[FromBody]`, `[FromQuery]`, `[FromRoute]`, `[FromForm]`, `[FromHeader]`, bound Razor Page properties (`[BindProperty]`), `HttpContext.Request.Query/Form/Headers/Cookies/Body`, `IFormFile.FileName`, SignalR hub method arguments, queue triggers.

## ripgrep patterns

```bash
# Raw SQL
$RG -t csharp -e '(FromSqlRaw|ExecuteSqlRaw|ExecuteSqlRawAsync|SqlQueryRaw)\(\s*\$"' -e '(FromSqlRaw|ExecuteSqlRaw|SqlQueryRaw)\([^)]*\+' -e 'CommandText\s*=\s*(\$"|"[^"]*"\s*\+)' -e '\.(Query|Execute|QueryFirst|QuerySingle)(Async)?<?\w*>?\(\s*\$"'
# Deserialization
$RG -t csharp -e 'BinaryFormatter' -e 'LosFormatter' -e 'NetDataContractSerializer' -e 'SoapFormatter' -e 'ObjectStateFormatter' -e 'TypeNameHandling\.(All|Auto|Objects|Arrays)'
# Commands
$RG -t csharp -e 'Process\.Start\(' -e '"(cmd(\.exe)?|/bin/(ba)?sh)"' -e 'Arguments\s*=\s*\$"'
# Antiforgery
$RG -t csharp -e 'IgnoreAntiforgeryToken' -e 'DisableAntiforgery\(' -e 'AutoValidateAntiforgeryToken' -e 'ValidateAntiForgeryToken' -e 'AddAntiforgery|UseAntiforgery'
# Authorization
$RG -t csharp -e '\[AllowAnonymous\]' -e '\[Authorize' -e 'RequireAuthorization\(' -e 'FallbackPolicy' -e 'Map(Get|Post|Put|Patch|Delete)\('
# Binding entities
$RG -t csharp -e '\[From(Body|Form)\]\s+\w*(Entity|User|Account|Order)\b' -e '\[Bind\(' -e '\[BindProperty\]'
# Paths and SSRF
$RG -t csharp -e 'Path\.Combine\([^)]*(Request|fileName|name|path)' -e 'PhysicalFile\(' -e '(GetAsync|GetStringAsync|PostAsync|SendAsync)\(\s*\w*(url|Url|target)'
# Razor raw output
$RG -t cshtml -g '*.razor' -e 'Html\.Raw\(' -e 'new\s+HtmlString\(' -e 'MarkupString'
# Startup hardening
$RG -t csharp -e 'UseDeveloperExceptionPage' -e 'UseHsts' -e 'UseHttpsRedirection' -e 'AllowAnyOrigin\(\)' -e 'SetIsOriginAllowed\(\s*\w+\s*=>\s*true' -e 'AllowCredentials\(\)'
# JWT validation flags
$RG -t csharp -e 'Validate(Issuer|Audience|Lifetime|IssuerSigningKey)\s*=\s*false' -e 'RequireHttpsMetadata\s*=\s*false'
# XML
$RG -t csharp -e 'DtdProcessing\s*=\s*DtdProcessing\.Parse' -e 'XmlResolver\s*=\s*new'
# Secrets in config
$RG -g 'appsettings*.json' -e '"(ConnectionString|Password|Secret|ApiKey|ClientSecret|Key)"\s*:\s*"[^"]{8,}"' -e 'Password=[^;"]{3,}'
```

## Vulnerable vs fixed pairs

**EF Core raw SQL**

```csharp
// vulnerable: FromSqlRaw inserts the interpolated value as SQL text
var blogs = await db.Blogs.FromSqlRaw($"SELECT * FROM Blogs WHERE Owner = '{user}'").ToListAsync();
// fixed: FromSql turns the interpolation into a DbParameter
var blogs = await db.Blogs.FromSql($"SELECT * FROM Blogs WHERE Owner = {user}").ToListAsync();
```

**Dapper**

```csharp
// vulnerable
conn.Query<Order>($"SELECT * FROM Orders WHERE Status = '{status}'");
// fixed
conn.Query<Order>("SELECT * FROM Orders WHERE Status = @status", new { status });
```

**Antiforgery for MVC with cookie auth**

```csharp
// vulnerable: cookie-auth controller action that changes state without validation
[HttpPost] public IActionResult Transfer(TransferModel m) { ... }
// fixed: global filter, opt out only for non-cookie APIs
builder.Services.AddControllersWithViews(o => o.Filters.Add(new AutoValidateAntiforgeryTokenAttribute()));
```

**Default deny**

```csharp
// vulnerable: new endpoints are public unless someone remembers [Authorize]
app.MapPost("/invoices/{id}/pay", PayInvoice);
// fixed
builder.Services.AddAuthorization(o => o.FallbackPolicy = new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());
app.MapPost("/invoices/{id}/pay", PayInvoice).RequireAuthorization("InvoiceOwner");
```

**Json.NET type handling**

```csharp
// vulnerable
JsonConvert.DeserializeObject(body, new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.All });
// fixed
JsonSerializer.Deserialize<OrderRequest>(body);
```

**Process**

```csharp
// vulnerable
Process.Start("cmd.exe", $"/c ping {host}");
// fixed
var psi = new ProcessStartInfo("ping"); psi.ArgumentList.Add("-n"); psi.ArgumentList.Add("1"); psi.ArgumentList.Add(host);
Process.Start(psi);
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads packages.lock.json, packages.config, and deps.json. A .csproj with only PackageReference and no packages.lock.json gives it nothing [raw/deps--osv-scanner-supported-lockfiles.md].
2. Fallback: `dotnet package list --vulnerable --include-transitive --format json` (.NET 10 SDK) or `dotnet list package --vulnerable --include-transitive --format json` (SDK 9 or earlier). It restores packages, so run only in the throwaway copy and only when the SDK is installed [raw/deps--dotnet-package-list.md].
3. If neither can run, record the cap and list `PackageReference` entries with versions as `info`.

## Sources

[raw/dotnet--aspnetcore-antiforgery.md], [raw/dotnet--efcore-raw-sql.md], [raw/deps--dotnet-package-list.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md]
