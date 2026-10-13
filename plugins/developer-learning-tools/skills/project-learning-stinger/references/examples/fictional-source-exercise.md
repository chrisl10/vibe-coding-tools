# Fictional source-linked exercise record

This completed Reference example shows preparation and fictional response recording for one supplied technical note. Every source and learner response below is FICTIONAL. It is not a real learner trial, repository behavior, security review or native-host run. Real learner understanding remains PENDING; runtime is NOT_RUN.

## Supplied fictional source, revision example-r1

The entire supplied source contains these three numbered statements:

1. A report request names a workspace and requires a signed-in requester.
2. The service returns the report only when that requester also has membership in the named workspace.
3. If either condition fails, the service refuses the request. This note does not specify an HTTP status code.

The record uses line numbers in the [supplied fictional source](fictional-supplied-source.txt) as exact source locators. Source identity: example-r1, SHA-256 `f17e4cc8f9fc1dd0c3732630990ac2af6fc21188b77488962fc8be9737b915f6`. The stage manifest pins the complete record separately. No external product or framework behavior is asserted.

## Preparation record

Outcome: Given requester and workspace facts, classify a request and explain the two conditions. Prerequisites: the meanings of requester, workspace and membership. Response format: chat text or spoken response transcribed in the current conversation. Knowledge facts: statements 1-3. Technical Explainer account: requester asks the service for the named workspace report; both sign-in and membership are necessary; refusal status code is unknown. Analogy: none needed. Subject owner: not selected in this fictional scenario; no domain interpretation or implementation claim is assessed.

Exercise prompt: A requester is signed in and belongs to workspace Cedar. The request names workspace Birch, where the requester has no membership. Does the note permit returning the report? Identify the source statement supporting your answer.

First hint: Compare the workspace named in the request with the workspace where membership exists.

Retry prompt: Reclassify the same request and name both required conditions.

Changed condition: Keep the request naming Birch and add membership in Birch. All other facts remain constant. Classify the request again.

Teach-back: In your own words, explain why sign-in alone does not establish access to every workspace, and identify what the note leaves unknown.

## Separate answer key

The initial request is refused under statement 2 because membership must match Birch. The changed request meets sign-in and Birch membership, so the note permits the report. Statement 3 leaves the HTTP status unknown. These are answers about the fictional note only.

## Criterion rubric

| ID | Source claim and locator | Exact evidence | Expected observable response | Counterexample |
|---|---|---|---|---|
| C1 | example-r1 statement 1 | requires a signed-in requester | Name sign-in as necessary | Membership alone is enough |
| C2 | example-r1 statement 2 | membership in the named workspace | Refuse initial Birch request; permit changed Birch membership case | Cedar membership permits Birch |
| C3 | example-r1 statement 3 | does not specify an HTTP status code | Say the status is unspecified | Invent a 403 response |

## Fictional evidence demonstration

| ID | Fictional first attempt | Support | Fictional retry | Fictional changed condition | Fictional teach-back | Fictional criterion interpretation |
|---|---|---|---|---|---|---|
| C1 | FICTIONAL: Sign-in is required. | independent | FICTIONAL: Both conditions are needed. | FICTIONAL: Sign-in still holds. | FICTIONAL: Sign-in identifies the requester. | DEMONSTRATED_IN_THIS_EXERCISE in fictional scenario only |
| C2 | FICTIONAL: Return it because the requester is signed in. | hint-assisted after the targeted hint above | FICTIONAL: Refuse it because Birch membership is missing. | FICTIONAL: Return it now because Birch membership exists. | FICTIONAL: Membership applies to the requested workspace. | First attempt PARTIAL; retry and transfer demonstrate fictional criterion with hint-assisted support |
| C3 | FICTIONAL: Return 403. | independent; feedback: reread statement 3, no solution shown | FICTIONAL: The status code is unspecified. | FICTIONAL: The note still supplies no status code. | FICTIONAL: Refusal is specified; its HTTP status is unknown. | First attempt PARTIAL; corrected response is hint-assisted, never relabeled independent |

Actual learner evidence: C1-C3 PENDING, support not-attempted. The fictional interpretation is a format demonstration. It cannot close an outcome's real learner proof or establish mastery. Next fictional practice recommendation: distinguish a permission decision from its protocol representation, because the initial response invented a status code. No source code runs, no learner data is saved and no application file changes.
