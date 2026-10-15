# Constructed ICU and RTL examples
These illustrate integration shape, not an executed framework app or reviewed Arabic translation. Grounding: ICU, W3C, logical CSS.

```text
{count, plural, =0 {No files} one {# file} other {# files}}
```
Compile with the installed ICU-compatible library before use. Provide translator notes explaining what count represents and whether exact zero is intended. This package does not execute that parser.

```html
<html lang="ar" dir="rtl">
  <body>
    <p>Account: <bdi dir="auto">SAMPLE-42</bdi></p>
    <button type="button">Draft label requiring language review</button>
  </body>
</html>
```
Labels are illustrative placeholders, not usable translated copy. Dynamic account text must be assigned through escaped framework bindings or textContent, never inserted as HTML. Preserve accessible semantics and actual text review.

```css
.panel { padding-inline: 1rem; margin-inline-start: 0.5rem; }
.label { text-align: start; max-inline-size: 30rem; }
```
Browser output, mixed bidi ordering, focus and screen-reader behavior remain NOT_RUN. Run scoped UI review on the actual selected framework surface under Impeccable before delivery claims.
