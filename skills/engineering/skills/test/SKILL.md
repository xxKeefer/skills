---
name: test
description: "★ Test: prove the change works. A bug gets a failing test first through /tdd. A built change gets /happy-path, then /sad-path when it touches forms or fields."
argument-hint: "[bug description | seam to test]"
disable-model-invocation: true
---

# Test

Prove the change works. This command picks the right test skill for the state of the branch.

## Step 1: Route

Use the first row that holds:

| State | Run |
|---|---|
| `$ARGUMENTS` describes a bug | `/tdd`. The first test reproduces the bug and goes red before any fix. Then fix it in the same loop. |
| `$ARGUMENTS` names a seam or a behaviour | `/tdd` at that seam. |
| The branch changes behaviour that no test covers | `/tdd` at the seams that the plan handoff names. Else confirm the seams with the user, as `/tdd` says. |
| The branch is built, and its tests pass | `/happy-path`. |

To find the state, read the branch diff against its base, the plan handoff if one exists, and the
test output of the project's test command.

**Done when:** one skill ran.

## Step 2: Add the sad path

After `/happy-path`, run `/sad-path` when its guard matches the diff: a form, a field, a text input,
or a file upload changed. It adds its run to the same report.

**Done when:** `/sad-path` ran, or its guard does not match.

## Step 3: Hand on

Give the next command:

- QA items failed: the `/fix` prompt that the report builds.
- Everything passed: `/review`.

**Done when:** the user has the next command.
