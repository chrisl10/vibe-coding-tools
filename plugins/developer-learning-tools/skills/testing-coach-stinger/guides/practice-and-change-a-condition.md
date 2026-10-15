# Practice and change a condition

Give the contract and hide the solution initially. Ask the learner to predict one valid result and one rejection, write an assertion, and explain where the expected result came from. Wait for the real response. If they decline, record NOT_ATTEMPTED and give the requested explanation without fabricating an answer from them.

Review the observed attempt. A test that recomputes the same expression as the implementation may reproduce the same mistake. Ask whether an independently stated result would expose it. Internal details can matter when the contract requires them; do not ban white-box testing as a universal rule.

Give one hint at a time and invite a retry. If a complete solution was requested, show it and label the later response solution-assisted. Ask a changed-condition task: now capacity is 12, and booking 12 must leave zero. Ask which expected values and boundaries change. Ask a teach-back question: why can the decrement property pass despite an off-by-one bug?

The included [exercise](../references/examples/seat-contract.md) and fixture are synthetic owned teaching material. An authorized orchestrator can run the fixed local fixture without imports from a learner repository; the read-only Drone returns the explanation. No install, broad discovery, arbitrary subprocess, eval, supplied module import or remote upload. unittest source documents that discovery imports test modules, so discovery is not a safe way to inspect untrusted learner code.
