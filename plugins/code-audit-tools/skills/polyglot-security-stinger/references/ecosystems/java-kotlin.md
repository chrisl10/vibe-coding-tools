# Java and Kotlin reference (Spring Boot)

Loaded by [guides/07-java-kotlin-spring.md](../../guides/07-java-kotlin-spring.md). Stack id `java-kotlin`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md). Library names in sink tables are search hints; a hit becomes a finding only after the call site is read.

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| J1 | No SQL, JPQL, or HQL built by `+`, `String.format`, `concat`, or Kotlin string templates into `createQuery`, `createNativeQuery`, `JdbcTemplate.query/update/execute`, `Statement.execute*`, or `@Query(nativeQuery = true)` with SpEL concatenation | CWE-89, CWE-564 |
| J2 | Values use `PreparedStatement` `?`, named parameters (`:name`), or Spring Data derived queries | CWE-89 |
| J3 | `Runtime.getRuntime().exec(String)` is absent; `ProcessBuilder` gets separate arguments and no `sh -c` with user data | CWE-78 |
| J4 | No `ObjectInputStream.readObject`, `XMLDecoder`, old XStream, SnakeYAML `new Yaml().load` on untrusted data; Jackson has no `enableDefaultTyping` / `activateDefaultTyping` with a permissive validator, no `@JsonTypeInfo(use = Id.CLASS)` on request types | CWE-502 |
| J5 | XML parsers disable external entities (`DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`) | CWE-611 |
| J6 | Controllers bind to request DTOs, not JPA entities with role or owner fields; or use `@InitBinder` `setAllowedFields` | CWE-915 |
| J7 | Spring Security: no `csrf.disable()` / `csrf(AbstractHttpConfigurer::disable)` when the app uses session cookies or form login | CWE-352 |
| J8 | `authorizeHttpRequests` ends with `.anyRequest().authenticated()` (or denyAll), not `permitAll()`; method security (`@PreAuthorize`) checks ownership where needed | CWE-862, CWE-639 |
| J9 | Actuator: `management.endpoints.web.exposure.include` is not `*` on a public port, or endpoints are secured with `EndpointRequest`; `show-values` is not `always` | CWE-200, OWASP A02:2025 |
| J10 | Files: `Paths.get(base, userInput)` / `new File(base, userInput)` are normalized and checked with `startsWith(base)`; zip entries checked | CWE-22 |
| J11 | `RestTemplate`, `WebClient`, `HttpClient`, `URL.openStream` with user URLs are allowlisted | CWE-918 |
| J12 | Thymeleaf uses `th:text`, not `th:utext` on user data; no SpEL / template expressions built from user strings | CWE-79, CWE-917 |
| J13 | No secrets in `application.properties` / `application.yml` committed to git; profiles do not ship `spring.h2.console.enabled=true` | CWE-798 |
| J14 | CORS is not `allowedOriginPatterns("*")` together with `allowCredentials(true)` | CWE-942 |
| J15 | Password encoder is BCrypt, Argon2, SCrypt, or Pbkdf2 (`DelegatingPasswordEncoder`), never `NoOpPasswordEncoder` | CWE-916 |

Sources: [raw/java--spring-boot-actuator.md], [raw/java--spring-security-csrf.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md].

Thin spot: Spring Data `@Query` native-query details and XXE parser flags are not quoted from fetched Spring or JDK pages; the rules above are the general OWASP classes applied to Spring. Confirm parser configuration by reading the code [research/distilled-polyglot-security.md].

## Sources of untrusted input

`@RequestParam`, `@PathVariable`, `@RequestBody`, `@RequestHeader`, `@CookieValue`, `@ModelAttribute`, `HttpServletRequest.getParameter/getHeader/getInputStream`, `MultipartFile.getOriginalFilename`, Ktor `call.receive`, `call.parameters`, message listeners (`@KafkaListener`, `@RabbitListener`).

## ripgrep patterns

```bash
# Query building
$RG -t java -t kotlin -e 'create(Native)?Query\(\s*"[^"]*"\s*\+' -e 'create(Native)?Query\([^)]*String\.format' -e '(jdbcTemplate|JdbcTemplate)\.(query|update|execute|queryForObject|queryForList)\(\s*"[^"]*"\s*\+' -e '\.(executeQuery|executeUpdate|execute)\(\s*"[^"]*"\s*\+' -e 'createQuery\("[^"]*\$\{?\w'
# Commands
$RG -t java -t kotlin -e 'Runtime\.getRuntime\(\)\.exec\(' -e 'new\s+ProcessBuilder\(' -e 'ProcessBuilder\(' -e '"(sh|bash|cmd)",\s*"(-c|/c)"'
# Deserialization
$RG -t java -t kotlin -e 'ObjectInputStream' -e 'readObject\(' -e 'XMLDecoder' -e 'XStream' -e '(enable|activate)DefaultTyping' -e 'JsonTypeInfo\.Id\.CLASS' -e 'new\s+Yaml\(\)' -e 'Yaml\(\)\.load'
# XML parsers (then check for disallow-doctype-decl / external entity features)
$RG -t java -t kotlin -e '(DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|TransformerFactory|SchemaFactory)\.newInstance' -e 'disallow-doctype-decl' -e 'IS_SUPPORTING_EXTERNAL_ENTITIES'
# Spring Security config
$RG -t java -t kotlin -e 'csrf\(\s*(\w+\s*->\s*\w+\.disable\(\)|AbstractHttpConfigurer::disable)' -e '\.csrf\(\)\.disable\(\)' -e 'anyRequest\(\)\.permitAll' -e 'NoOpPasswordEncoder' -e 'allowedOriginPatterns\(\s*"\*"' -e 'allowCredentials\(\s*true'
# Entities bound directly from requests
$RG -t java -t kotlin -e '@RequestBody\s+(final\s+)?\w*(Entity|User|Account|Order)\b' -e '@ModelAttribute\s+\w*(Entity|User|Account)\b' -e '@InitBinder'
# Actuator and config
$RG -g 'application*.properties' -g 'application*.yml' -g 'application*.yaml' -e 'exposure\.include\s*[=:]\s*["\x27]?\*' -e 'include:\s*["\x27]?\*' -e 'show-values\s*[=:]\s*always' -e 'h2\.console\.enabled\s*[=:]\s*true' -e '(password|secret|api-key|token)\s*[=:]\s*[^$\s{][^\s]{8,}'
# Templates and expressions
$RG -g '*.html' -e 'th:utext' ; $RG -t java -t kotlin -e 'SpelExpressionParser' -e 'parseExpression\('
# Paths and SSRF
$RG -t java -t kotlin -e 'Paths\.get\([^)]*(request|param|name|file)' -e 'new\s+File\([^)]*(request|param|name|getOriginalFilename)' -e 'ZipEntry' -e '(restTemplate|webClient|RestTemplate|WebClient)[^;]*(getForObject|exchange|uri)\(\s*\w*(url|Url|target)' -e 'new\s+URL\(\s*\w'
```

## Vulnerable vs fixed pairs

**JPQL**

```java
// vulnerable
em.createQuery("SELECT u FROM User u WHERE u.email = '" + email + "'").getResultList();
// fixed
em.createQuery("SELECT u FROM User u WHERE u.email = :email", User.class).setParameter("email", email).getResultList();
```

**JdbcTemplate**

```java
// vulnerable
jdbc.query("SELECT * FROM orders WHERE status = '" + status + "'", mapper);
// fixed
jdbc.query("SELECT * FROM orders WHERE status = ?", mapper, status);
```

**Spring Security CSRF and default deny**

```java
// vulnerable: session-cookie app with CSRF off and permissive fallback
http.csrf(csrf -> csrf.disable())
    .authorizeHttpRequests(a -> a.requestMatchers("/admin/**").hasRole("ADMIN").anyRequest().permitAll());
// fixed
http.authorizeHttpRequests(a -> a
        .requestMatchers("/", "/login", "/assets/**").permitAll()
        .requestMatchers("/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated());
```

**Actuator exposure**

```properties
# vulnerable on a public port
management.endpoints.web.exposure.include=*
management.endpoint.env.show-values=always
# fixed
management.endpoints.web.exposure.include=health,info
management.endpoint.env.show-values=never
```

**Entity binding (mass assignment)**

```java
// vulnerable: User has roles and enabled fields
@PutMapping("/me") User update(@RequestBody User body) { return repo.save(body); }
// fixed
record ProfileUpdate(@Size(max = 80) String displayName) {}
@PutMapping("/me") User update(@AuthenticationPrincipal Principal p, @Valid @RequestBody ProfileUpdate in) {
    User u = repo.findByUsername(p.getName()).orElseThrow(); u.setDisplayName(in.displayName()); return repo.save(u);
}
```

**Deserialization**

```java
// vulnerable
Object o = new ObjectInputStream(request.getInputStream()).readObject();
// fixed: parse JSON into a concrete type
Order o = objectMapper.readValue(request.getInputStream(), Order.class);
```

**Command**

```kotlin
// vulnerable
Runtime.getRuntime().exec("ping -c 1 $host")
// fixed
ProcessBuilder("ping", "-c", "1", "--", host).start()
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads pom.xml (transitive resolution through deps.dev, off in offline mode), gradle.lockfile, buildscript-gradle.lockfile, and gradle/verification-metadata.xml [raw/deps--osv-scanner-supported-lockfiles.md].
2. Gradle builds without dependency locking give osv-scanner nothing to read. Record the cap: "Gradle build has no lockfile; transitive dependencies not audited" and list direct dependencies with versions from build files as `info`.
3. Do not run `mvn` or `./gradlew` to resolve dependencies unless the user approved it: build scripts execute code. If approved, only inside the throwaway copy.

## Sources

[raw/java--spring-boot-actuator.md], [raw/java--spring-security-csrf.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md], [raw/deps--osv-scanner-supported-lockfiles.md]
