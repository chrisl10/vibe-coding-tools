# Derive observable assertions

Read the user's stated behavior before inspecting implementation. Ask only the missing input domain, expected output or rejection, and side-effect requirement. A requirement is the ruler: if the test copies the builder's mistaken ruler, both agree while the result is wrong. Keep that analogy tied to a concrete example, not a claim that all code-derived tests are useless.

Fill the [worksheet](../references/templates/lesson-worksheet.md). Choose one representative valid case, exact edges named in the contract and one invalid case. Distinguish absent, empty, malformed and forbidden only when relevant requirements define them. Expected values come from a requirement, independent worked example or authorized authoritative source. An unspecified behavior remains a question, not an invented assertion.

For a changed-condition or metamorphic check, state the promised relationship first. In the [seat exercise](../references/examples/seat-contract.md), increasing a valid booking by one reduces remaining seats by one. That relation is justified by the contract, not by copying subtraction from implementation. A relation alone can miss an off-by-one error, so retain exact examples.

Use existing unittest, Node strict assert or pytest assertions only where the user's environment supports them. Fixture, case and runner are different concepts in the unittest capture; assertion details are grounded in the Node capture and pytest capture. This tutor returns examples in chat; it never runs supplied code or changes product tests.
