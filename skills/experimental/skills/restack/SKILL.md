---
name: restack
description: >
  Restack a stack of branches with `gh stack`: rebase every branch onto the latest default branch,
  across the worktrees that hold them, push the open branches, and remove the merged ones. Use when
  the user says "restack", asks to rebase a stack, or merged the bottom PR of a stack.
---

# Restack

A stack is a chain of branches, each built on the one below it. Each branch has its own `wt`
worktree. `gh stack` records the stack for the whole clone, so any worktree of the stack can run
it. It rebases each branch in the worktree that holds that branch.

`wt` owns the worktrees. `gh stack` owns the order of the branches, the rebase, and the PRs. Never
use `gh stack` to create or remove a worktree, and never use `wt` to rebase.

## Step 1: Check the stack

1. Run `gh stack view`. If the branch is in no stack, ask the user for the branches, bottom first.
   Then run `gh stack init <branch> <branch> ...`.
2. Run `wt list`. Each worktree of the stack must be clean. A dirty or busy worktree stops the
   rebase. Ask the user to commit in it, then check again.

**Done when:** `gh stack view` shows the stack, and each of its worktrees is clean.

## Step 2: Sync

Run `gh stack sync`. It fetches, rebases each branch onto the one below it, and pushes with
`--force-with-lease`. When a squash merge deletes the bottom branch, sync moves the stack onto the
default branch.

| Result | Do |
| --- | --- |
| `Stack synced` or `Branches synced` | Go to Step 4. |
| A rebase conflict | Sync puts each branch back as it was. Go to Step 3. |
| It asks to use the remote, delete the stack, or cancel | Show the choice to the user. Do what the user picks. |
| It asks to accept a base change | Show the commits that it names. Pass `--accept-base-change` only after a yes. |

**Done when:** sync printed a synced message, or it stopped on a conflict.

## Step 3: Resolve conflicts

1. Run `gh stack rebase`. It stops at the first conflict and names the worktree.
2. In that worktree, resolve each file with `/resolve-conflicts`. `rerere` can resolve a file from
   an earlier fix, so check each file before you stage it.
3. Run `gh stack rebase --continue`. Repeat steps 2 and 3 until the rebase ends.
4. Run `gh stack sync` to push.

To stop, run `gh stack rebase --abort`. It puts every branch back as it was.

**Done when:** sync printed a synced message.

## Step 4: Remove the merged branches

If a PR of the stack merged, run `/prune-worktrees`. It removes the worktree and the branch of each
merged PR with `wt`.

**Done when:** no worktree holds a merged branch of the stack.

## Step 5: Report

Run `gh stack view` and show its output. Say which branches merged, and which worktrees
`/prune-worktrees` removed.

**Done when:** the user has the stack and the removed worktrees.
