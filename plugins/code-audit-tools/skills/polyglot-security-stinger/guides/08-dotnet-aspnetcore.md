# 08 .NET (ASP.NET Core)

For every path under stack id `dotnet`. Loads [../references/ecosystems/dotnet.md](../references/ecosystems/dotnet.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

## Steps

1. **Identify the project types** from `detect.json.details.dotnet[]`: web projects (`aspnetcore` framework from the Web, Razor, or Blazor SDK), class libraries, workers. Note `target_framework`.
2. **Read startup.** `Program.cs` (and `Startup.cs` on older apps): authentication schemes (cookie vs JWT bearer), `AddAuthorization` and any `FallbackPolicy`, `AddAntiforgery` / `UseAntiforgery`, CORS policy, `UseDeveloperExceptionPage`, `UseHsts`, `UseHttpsRedirection`, JWT `TokenValidationParameters` (D5 to D7, D13 to D15).
3. **Decide the CSRF exposure.** CSRF matters only where authentication rides in a cookie [raw/dotnet--aspnetcore-antiforgery.md]. For cookie-auth apps check the global `AutoValidateAntiforgeryTokenAttribute` filter or per-action `[ValidateAntiForgeryToken]`, and every `[IgnoreAntiforgeryToken]` / `.DisableAntiforgery()`. Do not assume the ASP.NET Core 11 automatic middleware for `net10.0` or older targets.
4. **Map endpoints.** Controllers and actions with `[Authorize]` / `[AllowAnonymous]`; minimal API `Map*` calls with `.RequireAuthorization()`; Razor Pages folders with conventions. Without a fallback policy, an endpoint with no attribute is public.
5. **Run the checklist D1 to D16** with the reference's `rg` blocks; read each production hit.
6. **Data access.** `FromSqlRaw`, `ExecuteSqlRaw`, `SqlQueryRaw` with interpolated strings are the key targets; `FromSql` and `FromSqlInterpolated` are safe [raw/dotnet--efcore-raw-sql.md]. Also Dapper and ADO.NET string building (D1, D2).
7. **Deserialization.** `BinaryFormatter` and friends, Json.NET `TypeNameHandling` other than `None` (D3) [raw/owasp--deserialization-cheat-sheet.md].
8. **Binding.** Entities bound from `[FromBody]` / `[FromForm]` and saved (D8) [raw/owasp--mass-assignment-cheat-sheet.md].
9. **Config and secrets.** `appsettings*.json` for real connection strings and keys (D12).
10. **Dependencies.** osv-scanner on packages.lock.json or deps.json; otherwise, only when `intake.json.execution.allowed` is true, `dotnet package list --vulnerable --include-transitive --format json` in the copy when the SDK exists (it restores packages and evaluates MSBuild files, which is project code); else a recorded cap (guide 10) [raw/deps--dotnet-package-list.md].
11. **Write findings** per guide 14 with `tags: ["dotnet", "aspnetcore", "<class>"]`.

## Done when

Startup was read, the CSRF exposure decision is in notes, every endpoint has an auth verdict, every checklist item has a result, and every production hit was read.

## Sources

[raw/dotnet--aspnetcore-antiforgery.md], [raw/dotnet--efcore-raw-sql.md], [raw/deps--dotnet-package-list.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md]
