---
name: squash-bugs
description: Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision.
argument-hint: "[--max N] <ticket> [<ticket> ...]"
disable-model-invocation: true
---

# Squash Bugs

Fix a batch of QA bug tickets with one user checkpoint at the start and one at the end. Each ticket
gets its own branch, its own worktree, and one fresh subagent that follows [`BUG.md`](BUG.md). Each
subagent writes a hunt doc for its ticket. A ticket that needs the user ends with a verdict in its
hunt doc, and the user answers all of them in one batch. All work stays local: the skill pushes
nothing and writes nothing to the tracker.

## Step 1: Pre-flight

1. Read the arguments: the tickets, and `--max N`. The default for `N` is 3.
2. Read each ticket with `/look-up`.
3. Fetch from the remote.
4. Name a branch for each ticket. Use the repo's convention for a fix branch. If there is none, use
   `fix/<ticket>`.
5. Name a worktree path for each ticket. Use the layout that the user's or the repo's guidance
   names. If there is none, use the sibling folder `<repo>.<branch>`, with each `/` changed to `-`.
6. Find the existing work for each ticket: each worktree or branch whose name holds the ticket key
   in any case, with no digit after it. Read it from `wt list --format=json --branches --remotes`.
   Without `wt`, read `git worktree list` and `git branch --all`, and treat each worktree as
   unmarked. Use the first line of this table that fits, and ask nothing:

   | Existing work | Do | Note |
   | ------------- | -- | ---- |
   | A worktree whose `symbols` hold 🤖 or 💬 | Skip | a session may be live |
   | A worktree | Skip | work exists at `<path>`, continue with `/claim` |
   | A branch | Skip | branch exists, continue with `/claim` |
   | A file or folder at the worktree path | Skip | the path exists |
   | None | Create it in Step 2 | |

7. Show this table, then wait for the user to say go:

   | Ticket | Title | Branch | Worktree | Note |
   | ------ | ----- | ------ | -------- | ---- |

   In Note, mark a ticket that you cannot read, a ticket that is not a bug report, and the note
   from item 6.

**Done when:** every ticket has a row, and the user said go.

## Step 2: Create the worktrees

For each ticket that is not skipped, one at a time:

1. Find its existing work again, as in Step 1 item 6. If the result changed since the user said
   go, skip the ticket, and report the change in Step 4.
2. Create its worktree at its path, on a new branch from the remote default branch. Use the tool or
   the skill that the user's or the repo's guidance names. If there is none, use
   `git worktree add -b <branch> <path> <remote>/<default>`.
3. Do the setup that the guidance names, such as copying ignored files or installing dependencies.
   Skip the setup that the tool already did.
4. If item 2 or item 3 fails, stop the run. Report the failure, and start no subagents.

**Done when:** each ticket that is not skipped has its worktree with its setup done, or the run
stopped on a failure.

## Step 3: Dispatch

Run one fresh `general-purpose` subagent per worktree. Keep at most `N` running at the same time.
When one returns, start the next ticket.

Give each subagent the ticket ID, the absolute worktree path, and the absolute path to
[`BUG.md`](BUG.md). Tell it to follow `BUG.md`. On a rerun from Step 5, also give it the hunt doc
path.

When a subagent returns, check its worktree, not its summary:

| Verdict | Check |
| ------- | ----- |
| `fixed`, `trivial` | `git log` holds the commit it names. The worktree has no modified or staged files. |
| `not a bug`, `cannot reproduce`, `decision`, `blocked` | The branch has no commits after the default branch. |
| Every verdict | The hunt doc exists and holds the same verdict. |

If a check fails, the ticket's status is the failed check.

**Done when:** every subagent returned, and you checked every return.

## Step 4: Report

Give one table, with a row for each ticket from Step 1:

| Ticket | Branch | Status | Root cause | Files changed | Tests |
| ------ | ------ | ------ | ---------- | ------------- | ----- |

Status is the verdict, `skipped` with its Step 1 note or its Step 2 change, or the failed check.
Take Root cause, Files changed, and Tests from the subagent's return.

Below the table, give each ticket that is not `fixed` or `trivial`, with its hunt doc path:

- `not a bug`, `cannot reproduce`: the evidence, in two sentences or fewer.
- `decision`: the options and the recommendation, in full.
- `blocked`: the gate that stays red.

Then wait for the user's answers.

**Done when:** every ticket from Step 1 has a row, and every ticket that is not `fixed` or
`trivial` appears below the table.

## Step 5: Record the answers

1. Write each answer into its ticket's hunt doc, under `## Decisions`.
2. Go back to Step 3 for each ticket that an answer sends back to work, in its existing worktree.

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.

Stop when the user says stop, or when no answer sends a ticket back to work.

**Done when:** every answer is in its hunt doc, and Step 4 reported every rerun.
