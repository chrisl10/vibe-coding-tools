# Product Requirements Documents: the blueprint before the build

## The simple idea

Suppose a class wants to build a treehouse. "Build an awesome treehouse" sounds exciting, but it does not answer basic questions. How many people must it hold? How high is it? Does it need a railing? What materials are allowed? How will anyone know it is safe?

A Product Requirements Document, usually called a PRD, turns the wish into a testable agreement. It explains the problem, the people affected, the desired outcome, the boundaries, and the proof that the result works.

A PRD is a blueprint for **what and why**. It may include technical constraints, but it should not pretend every implementation decision is already known.

## Why write one?

A good PRD prevents five expensive problems:

1. Different people building different versions of the same idea.
2. Important safety or user needs being discovered too late.
3. Work growing forever because no boundary was written down.
4. A feature being called "done" without proof.
5. Future teammates forgetting why a decision was made.

The PRD is not paperwork for its own sake. It is a tool for making uncertainty visible before code makes it costly.

## What belongs in a PRD

### 1. Identity and status

Give the document a stable number, short title, owner, lifecycle state, and dates.

```yaml
id: PRD-014
title: Passwordless email sign-in
status: backlog
owner: Identity team
created: 2026-08-14
updated: 2026-08-14
```

The number stays the same when the file moves from `backlog` to `in-work` to `completed`.

### 2. Problem

Describe the real difficulty in plain language. Include evidence when possible.

Weak:

```text
Login is bad.
```

Strong:

```text
New members must invent and remember a password before they can accept an invitation. Support records show that forgotten passwords are the largest source of failed first sign-ins. We need a secure sign-in path that does not require a password.
```

### 3. Who is affected

Name the people or systems. Avoid saying "users" when different groups have different needs.

- Invited members signing in for the first time.
- Returning members who prefer email links.
- Support staff helping someone regain access.
- Security staff reviewing authentication events.

### 4. Goal and measurable outcome

A goal says what should improve. A measure says how you will recognize improvement.

```text
Goal: Make first sign-in easier without weakening account security.

Success measures:
- At least 90 percent of valid sign-in links complete successfully in the test environment.
- A link can be used only once.
- An expired link never creates a session.
- Support can identify the failure reason without seeing the secret token.
```

### 5. Non-goals

Non-goals protect the boundary. They are not promises that something will never happen. They say it is not part of this delivery.

```text
Non-goals:
- Replacing social sign-in providers.
- Redesigning the account settings page.
- Building SMS sign-in.
```

Without non-goals, a small feature can quietly become a full identity rewrite.

### 6. User stories

A user story connects a person, an action, and a reason.

```text
As an invited member, I want to request a one-time email link so that I can sign in without creating a password.
```

Stories help people understand the experience. They are not enough to prove completion. Acceptance criteria provide that proof.

### 7. Acceptance criteria

Acceptance criteria are numbered, observable statements. Each one should be possible to mark VERIFIED, OPEN, PARTIAL, BLOCKED, or EXTERNAL.

Good criteria:

```text
AC-01: Given a registered email address, requesting sign-in creates a single-use token with a 15-minute expiration.

AC-02: Given a valid unused token, opening the link creates one session and marks the token used in the same transaction.

AC-03: Given an expired, changed, or already-used token, opening the link creates no session and returns the same public error message.

AC-04: Application logs contain the request identifier and outcome, but never contain the raw token or full email address.
```

Weak criteria:

```text
AC-01: Login works well.
AC-02: The page looks nice.
AC-03: It is secure.
```

The weak version cannot be tested consistently. Words such as good, easy, fast, secure, and user-friendly need a measurable definition.

### 8. Constraints and risks

Constraints are limits the team must respect. Risks are uncertain events that could hurt the outcome.

```text
Constraints:
- Existing password sign-in must keep working during rollout.
- Email delivery uses the approved provider.
- Tokens must not appear in analytics or logs.

Risks:
- Email scanners may open a one-time link before the person clicks it.
- Delayed email can make a short expiration confusing.
- Account enumeration can leak whether an email is registered.
```

Write a response for each serious risk. A risk list without action is only a worry list.

### 9. Dependencies and human decisions

List other teams, provider settings, legal approvals, data migrations, or credentials. Mark who owns each one.

An AI assistant must not invent evidence across a human or provider boundary. If the feature needs a real provider setting, the PRD should name the required artifact, such as a redacted test-environment configuration record.

### 10. Validation plan

Connect each acceptance criterion to evidence before implementation starts.

| Criterion | Evidence |
|---|---|
| AC-01 | Automated token creation and expiration test |
| AC-02 | Transaction test proving one session and one use |
| AC-03 | Negative tests for expired, changed, and reused tokens |
| AC-04 | Log capture plus secret scan |

This table exposes criteria that sound testable but are not yet connected to a real check.

## The acceptance ledger

During delivery, keep a ledger instead of relying on memory.

| ID | Status | Evidence | Remaining work |
|---|---|---|---|
| AC-01 | VERIFIED | `token.test.ts`, 6 passing cases | None |
| AC-02 | PARTIAL | Single-use test passes | Transaction rollback case missing |
| AC-03 | VERIFIED | Negative test group passes | None |
| AC-04 | EXTERNAL | Local logger test passes | Hosted log export needs human access |

Status meanings:

- **VERIFIED:** Direct evidence proves the complete criterion.
- **OPEN:** Work has not started or no evidence exists.
- **PARTIAL:** Some behavior is proven, but the full statement is not.
- **BLOCKED:** Progress cannot continue without a named decision or dependency.
- **EXTERNAL:** Local work is complete, but real-world confirmation belongs to another system or person.

Never turn PARTIAL or EXTERNAL into VERIFIED just because the rest of the feature looks good.

## PRD lifecycle in Library Schema v2

PRDs live under:

```text
library/requirements/
  backlog/
  in-work/
  completed/
  reports/
```

1. **Backlog:** The need and criteria are clear enough to consider, but implementation has not started.
2. **In work:** The PRD is the active contract. Its ledger records evidence and gaps.
3. **Completed:** Every criterion is honestly resolved, required gates are complete, and the final state is recorded.

Move the whole PRD folder through the lifecycle. Do not make copies that can disagree.

## PRD versus other documents

| Document | Main question |
|---|---|
| PRD | What product change should exist, for whom, and how will we prove it? |
| ADR | Which important technical decision did we make, and why? |
| IRD | What defect or incident happened, what caused it, and how will we correct it? |
| Knowledge document | What durable fact or procedure should the team remember? |
| Task list | What small actions must someone perform? |

One change may use several documents. A PRD can link to an ADR for a storage choice and to knowledge docs for an API contract.

## A small complete example

```markdown
# PRD-014: Passwordless email sign-in

## Problem
Invited members often fail first sign-in because they must create and remember a password.

## Goal
Allow invited and returning members to sign in with a secure, single-use email link.

## Non-goals
- SMS sign-in
- Social provider changes
- Account settings redesign

## Acceptance criteria
- AC-01: A registered email can request a 15-minute single-use link.
- AC-02: One valid token creates exactly one session.
- AC-03: Invalid tokens create no session and reveal no account details.
- AC-04: Logs and analytics contain no raw token.

## Risks
- Link scanners may consume tokens. Mitigation: separate safe preview from the final state-changing confirmation.
- Requests may reveal accounts. Mitigation: return the same public response for registered and unregistered addresses.

## Validation
- Unit tests for token hashing and expiration.
- Integration tests for transaction and replay behavior.
- Browser test for the complete email-link flow using a test inbox.
- Secret scan of logs and changed files.
- Security review followed by independent quality review.
```

It is short, but it gives the team a shared problem, a boundary, observable behavior, known risk, and proof plan.

## Final review questions

Before implementation:

- Is the problem supported by evidence or a clear observation?
- Are the affected people named?
- Is the goal measurable?
- Are non-goals explicit?
- Can every acceptance criterion be tested or evidenced?
- Are provider and human boundaries named?

Before completion:

- Does the ledger have one row for every criterion?
- Is each VERIFIED row backed by direct evidence?
- Are PARTIAL, EXTERNAL, and BLOCKED rows still labeled honestly?
- Did security run before independent quality?
- If quality caused changes, were both gates rerun?
- Does the completed document explain the final behavior and any remaining external work?

A PRD succeeds when it helps people make the same promise, build the same thing, and recognize the same proof.
