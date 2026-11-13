---
name: stand-up
description: >
  Show your day as one table per epic, from your open tickets, your open PRs, the PRs you are
  asked to review, and your local branches, then write a short news bulletin about the day. Each
  row has a type: PR, REVIEW, IN DEV, or PLANNED. Use when the user says "stand-up", "standup",
  "what is on today", "brief me on my day", or "morning bulletin".
---

# Stand-up

Join the work that sits in the tracker, the code host, and the local checkouts into one view. The
user reads the tables to see each item, and the bulletin to see what to do first.

> **Tools:** use the tracker and the code host that the repo's `## Agent skills` block names, else
> the ones in the user's `## Tools on this machine` block, else ask. That block can point to a
> notes file with the tracker's queries, statuses, and URL forms. Read it before Step 1. When a role
> has no tool, skip its step and say so in the notes under the tables.

## Step 1: Collect the sources

Run these four searches. They do not depend on each other, so run them in parallel.

1. **Tracker:** the open tickets assigned to the user, with the summary, the status, the type, the
   parent, and the last update.
2. **Code host, own PRs:** the user's open PRs in every repo they can see. With GitHub:
   `gh search prs --author=@me --state=open --json repository,number,title,url,isDraft,updatedAt`.
3. **Code host, review requests:** the open PRs that ask the user for a review. With GitHub:
   `gh search prs --review-requested=@me --state=open --json repository,number,title,url,author,updatedAt`.
4. **Local branches:** each worktree or clone in the user's work folder, with its branch, its last
   commit, and its count of changed files. The user's instructions name the work folder.

**Done when:** you have the four lists, or a note for each source that has no tool.

## Step 2: Read each PR

For each PR from Step 1, get the review decision, the merge state, the base branch, the head
branch, the check results, and the reviews. With GitHub:

```sh
gh pr view <number> -R <owner/repo> --json \
  reviewDecision,mergeStateStatus,baseRefName,headRefName,statusCheckRollup,reviews
```

- Name each check that failed.
- A dismissed approval means that a later push needs a new approval.
- A PR whose base is another open PR is part of a **stack**. Follow the bases down to the default
  branch to get the order.
- For each local branch with no open PR from the user, find its PR in any state. A merged PR means
  that the user can remove the worktree.

**Done when:** each PR has its state, its failed checks, and its place in a stack, if it has one.

## Step 3: Fill in the tickets

Take the ticket key from each PR title or branch name. The Step 1 tracker search returns only the
tickets assigned to the user, so a PR or a review can point to a ticket that it left out. Fetch
each of these tickets, with the status and the parent. Then fetch each parent that is an epic, for
its summary.

- A ticket that is done, with a PR that is still open, is a finding. The next step is to ask the
  author whether the PR is still needed.
- A ticket that is in progress, with no branch and no PR, is a finding. Say how long it has not
  changed.

**Done when:** each row has its ticket status and its epic, or `—` when it has none.

## Step 4: Type each row

| Type | Rule |
| --- | --- |
| `PR` | The user's own open PR |
| `REVIEW` | A PR that asks the user for a review |
| `IN DEV` | A ticket in progress that has no open PR |
| `PLANNED` | A ticket that is not started |

A ticket with an open PR is a `PR` row only. Do not also add an `IN DEV` row for it. Give each PR
in a stack its own row.

**Done when:** each item has exactly one type.

## Step 5: Build the tables

One table per epic, headed by the epic key as a link and its summary. Put the rows that have no
epic in a last table called `Other`. When a group has only `REVIEW` rows, or only `PLANNED` rows,
from small epics, join them in one table, such as `Other review requests` or `Other backlog`, and
name the epic in the short description.

Order the tables by today's work: the epics with `PR` rows first, then `REVIEW`, then `IN DEV`,
then `PLANNED`. Inside a table, use the same order. Put the PRs of a stack in merge order.

```markdown
### [<EPIC-KEY>](<epic-url>) · <epic summary>

| # | repo | key | type | short desc | status | next step |
| --- | --- | --- | --- | --- | --- | --- |
```

- `#`: the row number. Count from 1 across all tables, so the user can refer to "row 7".
- `repo`: the repo name without the owner. Write `—` when no branch or PR exists.
- `key`: the ticket key as a link to the ticket. Write `—` when there is no ticket.
- `type`: the type from Step 4.
- `short desc`: a short phrase. Link each PR number, such as `[#123](<url>)`. For a stack, start
  with `Stack 2/4:`. For a review, name the author.
- `status`: the review state, the failed checks by name, and the ticket status when it is a
  finding.
- `next step`: one action, such as "Fix the unit test shard" or "Mark it ready after #120 merges".
- Each reference to a ticket or a PR is a link, in every cell and every heading.
- More than four `PLANNED` tickets in one epic with no change today can share one row. List each
  key as its own link.
- An empty cell gets `—`, never a guess.

**Done when:** each item from Steps 1 to 3 is in one row, and each reference is a link.

## Step 6: Present

1. Show the tables.
2. Below the tables, write at most four notes: worktrees that the user can remove, tickets that the
   tracker search left out, and each source that had no tool.
3. Write the bulletin. Give it a dated headline. Then write one short paragraph for each group
   with an action today, the most urgent first: a stack that one merge unblocks, a failed check on
   the user's PR, a dismissed approval, reviews that wait on the user, then housekeeping. Refer to
   rows by `#`. End with one line called **Suggested order**, which lists the actions in sequence.

If the user asks to keep the result, delegate to `/write-to-file`.

## Principles

- **One row per item.** A PR, a review, or a ticket gets one row, never two.
- **Unblock first.** A merge that unblocks a stack comes before new work.
- **Evidence only.** Every cell traces to a ticket, a PR, a check, or a commit. Say "I did not
  check" before you guess.
- **Links everywhere.** The user acts from the table, so each key and each PR number opens its page.
