---
name: ship
description: "★ Ship: check that the branch is ready (plan steps, tests, review, constraints), give a go or no-go, open or update the PR through /create-pr, and merge it when it needs no gate."
argument-hint: "[@handoff path]"
disable-model-invocation: true
---

# Ship

Decide if the branch is ready, then open the PR. `/create-pr` pushes and writes the PR. This
command adds the gate before it.

## Step 1: Gather

1. Find the plan handoff as `/implement` Step 1 does. A branch with no handoff is fine.
2. Find the latest review report for the branch, from the handoff's review step, or in the folder
   that `/write-to-file` uses for doctype `report`.

**Done when:** you have the handoff or none, and the review report or none.

## Step 2: Check

Check each item, and note pass, fail, or not found:

| Check | Pass when |
|---|---|
| Plan | Each build step in the handoff is done, and `## Pending Decisions` is empty. |
| Tests | The project's test command passes on the branch head. Run it. |
| Review | A review report exists for the branch head, and none of its rows at the top severity is open. A report of an earlier head also passes when each later commit is a review fix step that the handoff records, or when `git range-diff` shows each reviewed commit unchanged (`=`) after a rebase. |
| Constraints | `/constraints` finds nothing, when `CONSTRAINTS.md` exists. |
| Tree | The working tree is clean. |

**Done when:** each check has a result.

## Step 3: Decide

- **Go**: every check passes, or is not found where that is allowed (no handoff, no
  `CONSTRAINTS.md`).
- **No-go**: a check fails, or no review exists. Show each failed check with the command that fixes
  it, such as `/review`, `/test`, or `/build`. Then stop.

**Done when:** the user has the decision.

## Step 4: Open the PR

On go, run `/create-pr`. It checks the review for drift, writes the body, and pushes.

**Done when:** the user has the PR link.

## Step 5: Land

Skip this step when the change needs a gate, as [`CHECK-INS.md`](../../CHECK-INS.md) says, or when
`/create-pr` marked the door one-way. Then the user merges.

1. Mark the PR ready with `gh pr ready <number>`.
2. Wait for the PR checks with `gh pr checks <number> --watch`. If a check fails, stop and show it.
3. Merge. In a gh stack, run `gh stack merge <number> --yes`. Else run
   `gh pr merge <number> --squash`.
4. Find the run on the default branch for the merge commit with `gh run list --branch <default>`.
   Watch it with `gh run watch <id> --exit-status`.
5. Run each QA row that waits for the merge, as `/build` Step 3 runs `agent` rows.
6. In a gh stack, run `gh stack sync`.

**Done when:** the PR is merged, the default branch run is green or its failure is shown, and each
post-merge QA row has a result.
