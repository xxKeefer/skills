---
name: code-simplify
description: "★ Code-simplify: make working code easier to read without a change in behaviour, one change at a time, with the tests run after each change."
argument-hint: "[path, default the branch diff]"
disable-model-invocation: true
---

# Code Simplify

Make code that works easier to read. Behaviour stays the same: same output for each input, same
errors, same side effects.

## Step 1: Pick the scope

Use the path in `$ARGUMENTS`. Else use the files that the branch changed against its base. Do not
simplify code outside the scope.

**Done when:** you have the list of files.

## Step 2: Understand before you touch

For each candidate, read its callers, its tests, and its git history. Code that looks needless can
hold a reason: a bug fix, a performance need, or an edge case. If you cannot find the reason, ask.
Do not remove the code.

Run the tests once, and record the result. If tests fail before you start, stop and report them.

**Done when:** you know why each candidate exists, and you have a passing test run.

## Step 3: Find the changes

Look for these:

- deep nesting that a guard clause makes flat
- a long function that does more than one job
- a nested ternary
- a vague name
- duplicated logic, three times or more
- dead code, after a search shows that nothing calls it
- hand-written logic that the language or an installed library already gives

Follow the project's conventions and its rules. Prefer the plain form over the short clever form.

**Done when:** you have a list of changes, each with its file and line.

## Step 4: Change one thing at a time

For each change:

1. Make the change.
2. Run the tests.
3. If a test fails, revert the change and note why.

If a change can give a different result for some input, say so, and name the input. Do not claim
that two versions are the same unless the tests or a reading of every path prove it.

**Done when:** each change is kept with a passing test run, or reverted with a reason.

## Step 5: Commit and hand on

Commit the kept changes once, on the current branch. Report each change and each revert. Give the
next command: `/review`.

**Done when:** the commit exists, and the user has the report.
