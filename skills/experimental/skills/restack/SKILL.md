---
name: restack
description: >
  Restack a stack of branches with `gh stack`: rebase each branch onto the one below it, across the
  worktrees that hold them, and push. Leave the bottom branch alone while its PR is open. Move the
  stack onto the default branch after the bottom PR merges, and remove the merged branches. Use
  when the user says "restack", asks to rebase a stack, changed a lower branch, or merged the
  bottom PR of a stack.
---

# Restack

A stack is a chain of branches, each built on the one below it. Each branch has its own `wt`
worktree. `gh stack` records the stack for the whole clone, so any worktree of the stack can run
it. It rebases each branch in the worktree that holds that branch.

`wt` owns the worktrees. `gh stack` owns the order of the branches, the rebase, and the PRs. Never
use `gh stack` to create or remove a worktree, and never use `wt` to rebase.

`gh stack` rebases. It never merges. Never merge the default branch, or a lower branch, into a stack
branch. A rebase cannot use a merge commit, so the next rebase replays every commit of the branch
and stops again on conflicts that the merge already fixed.

## Step 1: Check the stack

1. Run `gh stack view`. If the branch is in no stack, ask the user for the branches, bottom first.
   Then run `gh stack init <branch> <branch> ...`.
2. Run `wt list`. Each worktree of the stack must be clean. A dirty or busy worktree stops the
   rebase. Ask the user to commit in it, then check again.

**Done when:** `gh stack view` shows the stack, and each of its worktrees is clean.

## Step 2: Pick the mode

Run `gh pr view <bottom branch> --json state`.

| Bottom PR | Mode | Why |
| --- | --- | --- |
| Open | Inside the stack (Step 3) | The bottom branch can be in review or QA. A rebase onto the default branch changes it. |
| Merged | Onto the default branch (Step 4) | The stack must leave the merged branch. |

Use Step 4 with an open bottom PR only when the user asks to bring in the default branch.

**Done when:** you have the mode.

## Step 3: Rebase inside the stack

1. Run `gh stack rebase --no-trunk`. It rebases each branch onto the one below it. The bottom
   branch does not change.
2. On a conflict, go to Step 5. Then come back here.
3. Run `gh stack push`. It pushes with `--force-with-lease`, and skips a branch that did not change.

**Done when:** `gh stack push` printed the pushed branches. Go to Step 6.

## Step 4: Rebase onto the default branch

Run `gh stack sync`. It fetches, rebases the stack onto the default branch, and pushes. When a
squash merge deletes the bottom branch, sync moves the stack onto the default branch.

| Result | Do |
| --- | --- |
| `Stack synced` or `Branches synced` | Go to the next paragraph. |
| A rebase conflict | Sync puts each branch back as it was. Run `gh stack rebase`, go to Step 5, then run `gh stack sync` again. |
| It asks to use the remote, delete the stack, or cancel | Show the choice to the user. Do what the user picks. |
| It asks to accept a base change | Show the commits that it names. Pass `--accept-base-change` only after a yes. |

If a PR of the stack merged, run `/prune-worktrees`. It removes the worktree and the branch of each
merged PR with `wt`.

**Done when:** sync printed a synced message, and no worktree holds a merged branch of the stack.

## Step 5: Resolve conflicts

1. The rebase stops at the first conflict and names the worktree.
2. In that worktree, resolve each file with `/resolve-conflicts`. `rerere` can resolve a file from
   an earlier fix, so check each file before you stage it.
3. Run `gh stack rebase --continue`. Repeat steps 2 and 3 until the rebase ends.

To stop, run `gh stack rebase --abort`. It puts every branch back as it was.

**Done when:** the rebase ended.

## Step 6: Report

Run `gh stack view` and show its output. Say which mode ran, which branches changed, which branches
merged, and which worktrees `/prune-worktrees` removed.

**Done when:** the user has the stack and the changes.
