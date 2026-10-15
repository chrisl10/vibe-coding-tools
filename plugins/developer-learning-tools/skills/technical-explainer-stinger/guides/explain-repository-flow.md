# Explain one repository flow

1. Lock one behavior: for example, what happens when a signed-in viewer requests a workspace invoice. Record authorized read scope and revision. Do not audit the entire repository when one flow is requested.
2. Read the entry point, called functions and relevant contract/configuration within scope. Use Core Knowledge for deep architecture when needed, resolved through the catalog or selected-plugin registry. Its presence is not proof that the flow was run.
3. Record each boundary: caller, identity, workspace/resource selection, permission check, work, response and error branch. Note checks whose implementations are unavailable. Distinguish declared tests from checks actually run; this workflow does not execute app commands merely to explain code.
4. Write the factual sequence, then a mapped analogy. Include one permitted and one denied input if the source defines both. Avoid asserting all routes share a check based on one handler.
5. Cite file/symbol/revision or a supplied source record for every behavior sentence. An accepted contract and divergent code create a visible conflict; do not quietly choose one.
6. Review the ledger against the source and request teach-back. List the missing files or runtime proof that would change the explanation. Leave application changes to the implementation owner under a separate task.

Grounding: named request actors and sequence MDN; bounded context Diataxis. Revision, permissions and non-mutation are topic contracts.
