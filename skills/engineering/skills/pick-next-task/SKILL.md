---
name: pick-next-task
description: >
  Rank the open work in your team's backlog by focus, priority, iteration, and effort. You pick up
  to three tickets, then each one is assigned to you, moved to in progress, and given its /plan
  command. Use when the user says "pick next task", "what should I work on next", or "backlog
  priority", or wants help to choose work.
---

# Pick Next Task

Rank the open work for your team, let the user pick up to three tickets, then start each one.

> **Tracker:** use the tracker that the repo's `## Agent skills` block names, else the tracker in
> the user's `## Tools on this machine` block, else ask. That block can point to a notes file with
> the tracker's queries, field names, and statuses. Read it before Step 1.

## Step 1: Cold start

Find these, with the tracker notes when they exist:

1. Your account in the tracker.
2. Your team, when the tracker has teams. Take it from the tickets that you hold now. If you hold
   none, ask for it.
3. The current iteration, when the tracker has iterations (a sprint, a milestone, a cycle). It is
   the open iteration that most of your tickets share.
4. Your focus, when the tracker notes give one, such as "frontend", with the signals that mark it.

**Done when:** you have your account, and your team, iteration, and focus or a note that the
tracker has none.

## Step 2: Fetch the candidates

Search for open tickets of your team that are yours or have no assignee, and that are not started
or in review. Get up to 100, with the summary, the status, the type, the priority, the labels, the
iteration, and the estimate.

**Done when:** you have the candidate list.

## Step 3: Drop started work

Run `git fetch --prune`, then `git branch -a`. Drop each ticket whose key is in a branch name.

## Step 4: Score and rank

Lower scores go first:

| Factor | Condition | Score |
|---|---|---|
| Focus | The ticket matches a focus signal, or there is no focus | 0 |
| Focus | No focus signal | +10 |
| Priority | Highest | 0 |
| Priority | High | +1 |
| Priority | Medium, or none | +3 |
| Priority | Low or lowest | +5 |
| Iteration | The current iteration, or the tracker has no iterations | 0 |
| Iteration | A later iteration | +2 |
| Iteration | No iteration (backlog) | +4 |
| Effort | An estimate of 2 or less, or a quick-win label | 0 |
| Effort | An estimate of 3 to 5 | +1 |
| Effort | An estimate over 5, or none | +2 |

Score a later iteration that is a holding bucket, such as one with "Backlog" in its name, as
backlog.

**Done when:** each candidate has a score.

## Step 5: Show the ranking

Show the top 10:

```
| Rank | Ticket | Priority | Iteration | Estimate | Summary | Why |
```

- Link each key to the ticket.
- The Why column gives the reason in a few words, such as "focus, high priority, current
  iteration, quick win".

## Step 6: The user picks

Use `AskUserQuestion` with `multiSelect: true`, so the user picks up to 3 tickets. It holds at most
four options, so list the top four, each with its summary. The user can type other keys from the
table in "Other".

## Step 7: Start each pick

For each picked ticket:

1. **Assign:** if the ticket is not yours, assign it to you.
2. **Iteration:** if the tracker has iterations and the ticket is not in the current one, add it.
3. **Status:** move it to the tracker's in-progress status.
4. **Read back:** fetch the ticket. Confirm the assignee, the iteration, and the status.

If a step fails, report the ticket and the step, then go on with the next ticket.

**Done when:** each picked ticket reads back as yours, in the current iteration, and in progress.

## Step 8: Hand on

Give one command for each picked ticket: `/engineering:plan <key>`. It claims the worktree and names
the branch. Ask which ticket to start first.

**Done when:** the user has the commands.
