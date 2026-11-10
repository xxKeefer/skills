---
name: prune-worktrees
description: >
  Prune stale git worktrees: remove the worktree and branch of each merged PR, remove the worktree
  of a branch that a stack in another worktree holds, and remove the worktree of an old branch with
  no PR. Then point each handoff at the worktree that still holds its branch. Use when the user
  says "prune worktrees", "clean up worktrees", or "remove the stale worktrees".
argument-hint: "[--stale-days N]"
---

# Prune Worktrees

Remove each worktree that holds no live work, after one yes. A removed worktree keeps its branch,
except the branch of a merged PR.

```sh
script="${CLAUDE_SKILL_DIR}/scripts/prune_worktrees.py"
plan="$(mktemp -t prune-worktrees).json"
```

## Step 1: Plan

Run the script from the main worktree of the repo. Pass `$ARGUMENTS` through.

```sh
python3 -I "$script" plan $ARGUMENTS > "$plan"
```

The script skips the main worktree and the current worktree. It gives each other worktree one
action:

| Action | When |
| --- | --- |
| `remove-branch` | Its PR is merged, and every local commit is in the merged PR |
| `remove-worktree` | A branch in another worktree builds on it (`held_by` names that worktree), or it has no open PR and no commit for `--stale-days` days (default 7) |
| `keep` | It has uncommitted changes, an open PR, recent commits, commits after its merge, or a detached HEAD |

**Done when:** the plan file holds one row for each worktree other than the main and current ones.

## Step 2: Gate

Show the plan as a table with the columns Worktree, Branch, Action, and Reason. Put the rows to
remove first. For a `remove-worktree` row, say that the branch stays.

Ask once whether to apply the plan. On a no, stop. If the user names rows to keep, set their
action to `keep` in the plan file.

**Done when:** the user said yes or no.

## Step 3: Apply

```sh
python3 -I "$script" apply --plan "$plan"
```

The script skips a worktree that changed after the plan, and reports it. Git refuses to remove a
worktree with untracked files, and the script reports that too.

**Done when:** the script printed each removal, and you have each failure.

## Step 4: Fix the handoffs

Find the handoff folder as `/write-to-file` does. Find each `Worktree:` line that names a removed
path.

- A row with `held_by`: change the path in the line to the `held_by` path. Keep the branch.
- Any other row: leave the line. The work is merged or idle.

**Done when:** no `Worktree:` line of a live branch names a removed path.

## Step 5: Report

List the worktrees removed, the branches deleted, the branches kept, the handoffs changed, and each
failure. Then list the worktrees that remain.

**Done when:** the user has the lists.
