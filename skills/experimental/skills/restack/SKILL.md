---
name: restack
description: >
  Restack a stack of branches: move every branch onto the latest default branch in one rebase,
  drop the commits of each squash-merged branch, push the open branches, and delete the merged
  ones. Use when the user says "restack", asks to rebase a stack, or merged the bottom PR of a
  stack.
---

# Restack

A stack is a chain of branches in one worktree, each built on the one below it. The bottom PR
targets the default branch. Each higher PR targets the branch below it. New work goes on the top
branch. When the bottom PR merges, a restack moves the rest of the stack onto the default branch.

Squash merge puts new commits on the default branch, so git cannot see that a merged branch is
already there. The script finds each merged branch from its PR, and cuts the stack above it.

```sh
script="${CLAUDE_SKILL_DIR}/scripts/restack.py"
```

## Step 1: Go to the top branch

Run the script from the top branch of the stack, in the worktree that holds the stack. If the user
is on a lower branch, the script names the branches above it. Switch to the top one.

**Done when:** `HEAD` is the top branch.

## Step 2: Run the script

```sh
python3 -I "$script"
```

Pass `--base <ref>` only when `origin/HEAD` is not set.

The script stops with a message, and changes nothing, in these cases:

| Message | Do |
| --- | --- |
| The working tree has changes | Ask the user to commit or stash them. Run again. |
| Run restack from the top branch | Switch to the branch that it names. Run again. |
| Another worktree has checked out a branch | Show the paths. Ask the user to remove those worktrees, then run again. Git does not move a branch that another worktree holds. |
| A branch is merged, but a branch below it is not | Tell the user. The stack merges from the bottom. Stop. |

**Done when:** the script exits 0, or it stopped on a conflict.

## Step 3: Resolve conflicts

A conflict leaves the rebase in progress. `rerere` can resolve a file from an earlier fix, so a
file in the conflict list can have no markers. Check each file before you stage it.

1. Resolve the conflicts with `/resolve-conflicts`.
2. Run `git rebase --continue`. Repeat until the rebase ends.
3. Run the script again. The second run pushes the branches and deletes the merged ones.

**Done when:** the script exits 0.

## Step 4: Report

Give the three lines that the script printed: the branches it moved, the branches it pushed, and
the merged branches it deleted. Say that a branch that was not on origin stays local.

GitHub changes the base of a PR to the default branch when its base branch is deleted on merge. If
a PR still targets a merged branch, say so, and give its number.

**Done when:** the user has the three lines and any PR with a stale base.
