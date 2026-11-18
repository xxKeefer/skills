---
name: ship
description: >
  ★ Ship: check that the branch is ready (plan steps, tests, review, constraints), give a go or
  no-go, open or update the PR through /create-pr, and merge it when it needs no gate. Use when the
  user says "ship" or "ship it", or asks if the branch is ready to merge.
argument-hint: "[@plan path]"
---

# Ship

Decide if the branch is ready, then open the PR. `/create-pr` pushes and writes the PR. This
command adds the gate before it.

## Step 1: Gather

1. Find the plan as `/implement` Step 1 does. A branch with no plan is fine.
2. Find the latest review report for the branch, from the plan's review step, or in the folder
   that `/write-to-file` uses for doctype `report`.

**Done when:** you have the plan or none, and the review report or none.

## Step 2: Check

Check each item, and note pass, fail, or not found:

| Check | Pass when |
|---|---|
| Plan | Each build step in the plan is done, and `## Pending Decisions` is empty. |
| Tests | The project's test command passes on the branch head. Run it. |
| Review | A review report exists for the branch head, and none of its rows at the top severity is open. A report of an earlier head also passes when each later commit is a review fix step that the plan records, or when `git patch-id --stable` gives one ID for `git diff <from> <to> -- . ':!.ai'` on the reviewed base and head, and on `$(git merge-base origin/<base> HEAD)` and `HEAD`. A review fix step is a plan step titled `Review fix <row ID>.`, not a note in another step's line. Else it fails, and the fix is `/review`. A run whose coverage table shows no lane that ran fails the check, and the fix is `/engineering:mob-review`. |
| ACs | When a commit landed after the review report, read each AC of the ticket or plan against the full branch diff at HEAD, and each AC still holds. Each behaviour change in the diff maps to an AC or to a line of the PR body. On a fail, the fix is to restore the AC, to update the ticket and the PR body, or to split the change to its own ticket. |
| Stack | The branch is in no gh stack. Else, after `git fetch origin`, each lower branch is at the SHA of its remote, and `gh stack view` shows no branch that needs a rebase. On a fail, show each lower branch commit that this branch does not have. The fix is `gh stack sync`. If a lower branch holds temporary commits, such as a test that is in progress, wait until its PR removes them. |
| Constraints | `/constraints` finds nothing, when `CONSTRAINTS.md` exists. |
| Tree | The working tree is clean. |

**Done when:** each check has a result.

## Step 3: Decide

- **Go**: every check passes, or is not found where that is allowed (no plan, no
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
   `gh pr merge <number> --squash`. Then `gh pr view <number> --json state,mergeCommit` must show
   `MERGED`.
4. Find the run on the default branch for the `mergeCommit` with `gh run list --branch <default>`.
   Watch it with `gh run watch <id> --exit-status`.
5. Run each QA row that waits for the merge, as `/build` Step 3 runs `agent` rows.
6. In a gh stack, run `gh stack sync`.

**Done when:** the PR is merged, the default branch run is green or its failure is shown, and each
post-merge QA row has a result.
