---
name: claim
description: >
  Find or create the worktree for a ticket key, a PR, or a branch, then record the branch and the
  worktree in the handoff for that work. Needs worktrunk (`wt`). Use when the user says "claim" or
  asks which worktree holds a ticket, or when another skill needs a worktree before work starts.
argument-hint: "<ticket key | PR number or URL | branch>"
---

# Claim

Answer one question before work starts: which worktree holds this work? Find the worktree, create
it when none exists, and stop when another session may hold it.

## Step 1: Read the input

1. Check that `wt` runs and that the current folder is in a git repo. If a check fails, stop and
   say which one.
2. Read the argument:
   - A ticket key, such as `PROJ-123`: that is the key.
   - A PR number or URL: get its branch with `gh pr view <pr> --json headRefName`.
   - A branch: that is the branch.
3. For a PR or a branch, the key is the ticket key in the branch name. If the name has no ticket
   key, the key is the branch name.
4. Fetch from the remote, so that Step 2 sees its branches.

**Done when:** you have the key, and the branch for a PR or a branch input.

## Step 2: Find the worktree

Run `wt list --format=json --branches --remotes`. A remote row has `kind` `branch`, and its
`branch` starts with `<remote>/`. Drop that prefix before you give the name to `wt`, and count a
local branch and its remote copy as one branch.

A row matches when its `branch` is the input branch. With only a key, a row matches when its
`branch` holds the key in any case, with no digit after it.

Use the first line of this table that fits the matching rows:

| Matching rows | Do |
| --- | --- |
| A worktree with `is_current` true | Continue there. Its marker is this session's own. |
| Two or more worktrees, or two or more branches and no worktree | List them with their paths and markers. Continue with the one that the user picks. |
| One worktree whose `symbols` hold 🤖 or 💬 | Ask about the marker (below). |
| One worktree | Continue there. |
| One branch | Run `wt switch <branch> --no-cd`. |
| None, for a PR | Run `wt switch pr:<number> --no-cd`. |
| None | Create the branch and its worktree (below). |

**The marker.** The worktrunk plugin for Claude Code sets 🤖 while a session works in a worktree,
and 💬 while the session waits for its user. A session that crashed leaves its marker. Show the
worktree's `path` and `symbols`, then ask whether a session is live there. Continue there only when
the user says that no session is live. Otherwise stop.

**Create.**

1. Name the branch with the git conventions that the repo or the user's guidance names. If the name
   needs the ticket's type or title, read the ticket with `/look-up`. With no convention, use the
   key. For a branch input, use that branch.
2. Run `wt switch --create <branch> --base <remote>/<default> --no-cd`.
3. If `wt` says that a project hook needs approval, stop. Show the commands that it lists, and ask
   the user to approve them with `! wt hook approvals add`. Then claim again. Leave out `--yes`,
   because it runs repo commands that the user has not read.

Get the path of a new worktree from `wt list --format=json`.

**Done when:** you have one worktree path on the branch, or you stopped and asked.

## Step 3: Record the claim in the handoff

1. Find the handoff folder the way `/write-to-file` picks it: the folder that the user's
   instructions name for handoffs or plans, else `.ai/` in the parent folder of
   `git rev-parse --path-format=absolute --git-common-dir`.
2. Find the files in that folder and its subfolders whose name holds the key. If no name holds it,
   find the files whose text holds it.
   - No file: go to Step 4. The calling skill writes the handoff.
   - Two or more files: ask which one.
3. Write `Worktree: <path>. Branch: <branch>.` on the line after the file's title. If the file
   already has a `Worktree:` line, replace that line. `/do-next` reads this line to check the
   branch.

**Done when:** the handoff holds the line for this claim, or no handoff names the key.

## Step 4: Return

Return the worktree path, the branch, the handoff path or `none`, and whether the worktree is new.
A caller that writes a new handoff puts the Step 3 line in it.

With no calling skill, tell the user to start the next session in the worktree. If a handoff
exists, give the command for that session: `/do-next @<handoff path>`.

**Done when:** the caller or the user has the worktree path, the branch, and the handoff path or
`none`.
