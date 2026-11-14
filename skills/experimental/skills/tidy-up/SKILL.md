---
name: tidy-up
description: Delete the local working state of finished work in one repo, and fix the lines in open handoffs that finished work made stale.
disable-model-invocation: true
argument-hint: "[repo path, default the current repo]"
---

# Tidy Up

Work leaves state behind: plans, handoffs, review reports, worktrees, branches, remote-tracking
refs, and stack records. When a ticket closes or a PR merges, that state is **stale**. This skill
finds it, ties each item to its work, and deletes or fixes only what it can tie to finished work.

`$ARGUMENTS` is the repo. The default is the current repo.

This is not `/triage-dir`. That skill sorts a junk folder by purpose. This skill acts only on the
working state of one repo, keyed to tickets and PRs.

## Step 1: List the state

Run these in one batch:

- The working-file folder that `/write-to-file` uses for this repo, and every file in it.
- `git worktree list`, `git branch -vv`, and `git remote prune origin --dry-run`.
- The local stack records, if the repo uses a stack tool.

**Done when:** you have each item and its path or ref.

## Step 2: Tie each item to its work

1. Read the ticket key or the PR from the file name, the branch name, or the handoff's `Ticket:`
   line.
2. Read the state of each key from the tracker, as the repo's issue tracker doc says.
3. Give each item one action:

| Item | Action |
|---|---|
| A file for a closed ticket or a merged PR | delete |
| A report index that lists files that no longer exist | rewrite it with the files that exist, or delete it when none exist |
| A remote-tracking ref that `prune --dry-run` lists | delete |
| A clean worktree, or a branch, whose work merged | delete |
| A stack record that names a branch that is gone or merged | delete the local record only |
| An open handoff that names finished work as current, such as a stack order or a base branch | fix the line |
| An item with uncommitted changes or unpushed commits | keep, and name it |
| An item that you cannot tie to work | keep, and name it |

**Done when:** each item has one action and a reason.

## Step 3: Checkpoint

Show one table: item, work, state, action, reason. Ask once. Apply after a yes, or at once when the
user asked for the cleanup by name.

**Done when:** the user approved, or asked for the cleanup up front.

## Step 4: Apply

Use the safe form of each command: `git worktree remove` without `--force`, and `git branch -d`,
not `-D`. On a refusal, keep the item and name it. Touch nothing on the remote.

**Done when:** each action ran or is named as refused.

## Step 5: Return

List what you deleted, what you fixed, and what you kept, with the reason for each kept item.

**Done when:** the user has the three lists.
