---
name: tidy-up
description: Delete the local state of finished work in one repo, and fix the stale lines in open plans.
disable-model-invocation: true
argument-hint: "[repo path, default the current repo]"
---

# Tidy Up

Work leaves state behind: plans, review reports, worktrees, branches, remote-tracking
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
- For each item: its size on disk, its dirty state (worktrees), its last commit date or file time,
  and its PR state from the code host. For each branch and worktree, its merged state from
  `git branch --merged <default branch>`.

**Done when:** you have each item and its path or ref.

## Step 2: Tie each item to its work

1. Read the ticket key or the PR from the file name, the branch name, or the `ticket` key of the
   plan's YAML header.
2. Read the state of each key from the tracker, as the repo's issue tracker doc says.
3. Give each item one action:

| Item | Action |
|---|---|
| A file for a closed ticket or a merged PR | delete |
| A report index that lists files that no longer exist | rewrite it with the files that exist, or delete it when none exist |
| A remote-tracking ref that `prune --dry-run` lists | delete |
| A clean worktree, or a branch, whose work merged | delete |
| A stack record that names a branch that is gone or merged | delete the local record only |
| An open plan that names finished work as current, such as a stack order or a base branch | fix the line |
| An item with uncommitted changes or unpushed commits | keep, and name it |
| An item that you cannot tie to work | keep, and name it |

**Done when:** each item has one action and a reason.

## Step 3: Checkpoint

Show one numbered table, one row for each item: item, work, size, merged, dirty, PR state, last
used, proposed action, reason. Write `-` where a column does not apply. Change nothing yet. Ask the
user to pick rows by number, `all`, or `none`. `all` picks each row whose action is not keep. A
picked keep row changes nothing.

**Done when:** the user picked rows. A pick of `none` ends the skill with no change.

## Step 4: Apply

Apply only the picked rows. Use the safe form of each command: `git worktree remove` without
`--force`, and `git branch -d`, not `-D`. On a refusal, keep the item and name it. Touch nothing on the remote.

**Done when:** each action ran or is named as refused.

## Step 5: Return

List what you deleted, what you fixed, and what you kept, with the reason for each kept item.

**Done when:** the user has the three lists.
