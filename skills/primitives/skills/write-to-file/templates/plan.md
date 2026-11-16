---
doctype: plan
ticket: <KEY, or none>
worktree: <absolute path of the worktree>
branch: <branch>
status: draft
goal: <one-sentence goal>
# Optional. Remove each key that does not apply.
spec: <path or URL of the spec>
builds_on: <KEY of the ticket below this one in the stack>
merge: <how the PR merges, from /split-ticket>
---

# Plan: <KEY> <title>

<!-- status values: draft, approved, building, done. Ask /write-to-file to check this plan after each write. After approval, change only the step marks, the steps that /build adds, Progress, Pending Decisions, and Follow-ups. -->

## Goal

<The goal, the scope, and the estimate.>

## Spec

<!-- Optional. Remove when no spec exists. -->

<The path or URL of the spec, and the part of it that this plan builds.>

## Acceptance criteria

<!-- Optional. Remove when the plan has no ACs. -->

- [ ] **A.** <action> → <expected>
  - [ ] **A.1.** <sub-check>

## Context

<!-- Optional. Remove when nothing to record. -->

<The decisions, the gates, the commit convention, and the production gate.>

## Test approach

<!-- Optional. Remove when no step changes behaviour. -->

<The risks, the test conditions with their IDs (C1, C2), and what is not tested.>

## Steps

<!--
Each step: `- [ ]` open, `- [x]` done, `- [-]` skipped with a `Skipped: <reason>` sub-line.
Each step has a `Done:` sub-line.
A step that changes behaviour names `Seam:` and `Conditions:`.
A step with `Kind: docs`, `Kind: config`, or `Kind: mechanical`, or a title whose first word is Test, Review, or Push, does not change behaviour.
-->

- [ ] **1. <slice goal>.** Seam: `<seam>`. Conditions: C1, C2.
  - Done: <the tests that it adds, and what a user can do now>.
- [ ] **2. <docs change>.** Kind: docs.
  - Done: <what the docs say now>.
- [ ] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **4. Review.** Depends on every earlier step. Review the branch with this plan: `<plan path>`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **5. Push.** Push the branch and open a draft PR with `/create-pr @<plan path>`.
  - Done: the draft PR URL is in this line.

## Progress

- <YYYY-MM-DD>: plan written on `<branch>`.

## Pending Decisions

<!-- Optional. Each open entry is a level-3 heading `D<n>: <question>`, `B<n>: <blocker>`, or `N<n>: <action>`, with its options or action, its `Work:` line, and its `Blocks:` line. Remove an entry when the user answers it. -->

## Follow-ups

<!-- Optional. Work found during the build that is out of scope. -->
