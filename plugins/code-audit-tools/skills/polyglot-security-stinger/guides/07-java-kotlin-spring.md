# 07 Java and Kotlin (Spring Boot)

For every path under stack id `java-kotlin`. Loads [../references/ecosystems/java-kotlin.md](../references/ecosystems/java-kotlin.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

## Steps

1. **Identify the framework** from `detect.json.details.java-kotlin[]` (spring-boot with version, spring-security, quarkus, micronaut, ktor) and the language (Java, Kotlin). For non-Spring frameworks apply the same checklist classes and say in notes that the Spring-specific rows did not apply.
2. **Do not run the build** (`mvn`, `./gradlew`) unless the run allows it: build scripts execute code. Read the build files instead.
3. **Read the security configuration.** Find `SecurityFilterChain` beans (or older `WebSecurityConfigurerAdapter` subclasses): CSRF setting, `authorizeHttpRequests` rules and the final `anyRequest()` rule, CORS, session policy, password encoder (J7, J8, J14, J15) [raw/java--spring-security-csrf.md].
4. **Read the application config.** `application*.properties` / `.yml` for each profile: actuator exposure and `show-values`, H2 console, credentials, server port vs management port (J9, J13) [raw/java--spring-boot-actuator.md].
5. **Map controllers.** `@RestController` / `@Controller` methods with their mappings, `@PreAuthorize` / `@Secured`, and which ones bind entities directly (J6) [raw/owasp--mass-assignment-cheat-sheet.md].
6. **Run the checklist J1 to J15** with the reference's `rg` blocks; read each production hit.
7. **Query building.** String-built JPQL, native queries, and `JdbcTemplate` calls (J1, J2).
8. **Deserialization and XML.** `ObjectInputStream`, `XMLDecoder`, XStream, permissive Jackson default typing, SnakeYAML on untrusted input (J4) [raw/owasp--deserialization-cheat-sheet.md]; XML factories without external-entity protection (J5, read the factory setup; parser flags are a thin spot in this archive).
9. **Commands, files, SSRF, templates.** J3, J10, J11, J12.
10. **Dependencies.** osv-scanner on pom.xml or Gradle lockfiles; Gradle without locking is a recorded cap (guide 10) [raw/deps--osv-scanner-supported-lockfiles.md].
11. **Write findings** per guide 14 with `tags: ["java-kotlin", "spring-boot", "<class>"]`.

## Done when

The security filter chain and every profile's config were read, controllers have auth verdicts, every checklist item has a result in notes, and every production hit was read.

## Sources

[raw/java--spring-security-csrf.md], [raw/java--spring-boot-actuator.md], [raw/owasp--deserialization-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/deps--osv-scanner-supported-lockfiles.md]
