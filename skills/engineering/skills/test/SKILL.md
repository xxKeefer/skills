---
name: test
description: >
  ★ Test: prove the change works. A bug gets a failing test first through /tdd. A built change gets
  /happy-path, then /happy-path sad when it touches forms or fields. Use when the user says "test", or
  asks to prove that a change or a bug fix works.
argument-hint: "[bug description | seam to test]"
---

# Test

Prove the change works. This command picks the right test skill for the state of the branch.

## Step 1: Route

Use the first row that holds:

| State | Run |
|---|---|
| `$ARGUMENTS` describes a bug | `/tdd`. The first test reproduces the bug and goes red before any fix. Then fix it in the same loop. |
| `$ARGUMENTS` names a seam or a behaviour | `/tdd` at that seam. |
| The branch changes behaviour that no test covers | `/tdd` at the seams that the plan names. Else confirm the seams with the user, as `/tdd` says. |
| The branch is built, and its tests pass | `/happy-path`. |

To find the state, read the branch diff against its base, the plan if one exists, and the
test output of the project's test command.

**Done when:** one skill ran.

## Step 2: Add the sad path

After `/happy-path`, run `/happy-path sad` when its guard matches the diff: a form, a field, a text input,
or a file upload changed. It adds its run to the same report.

**Done when:** `/happy-path sad` ran, or its guard does not match.

## Step 2b: See it live

After `/happy-path`, run `/verify`. `/verify` records `no driver` in the plan.

**Done when:** `/verify` returned a result, or `/happy-path` did not run.

## Step 3: Hand on

Give the next command:

- QA items failed: the `/fix` prompt that the report builds.
- `/verify` gave `fail` or `blocked`: `/fix` with the evidence path of the driver.
- Everything passed: `/review`.

**Done when:** the user has the next command.
