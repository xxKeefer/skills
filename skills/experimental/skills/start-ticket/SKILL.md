---
name: start-ticket
description: >
  Start work on a ticket: scope it, claim its worktree, and write the plan handoff that /do-next
  runs, with lettered ACs and a test approach for the user to approve. Use when the user asks to
  start or pick up a ticket.
argument-hint: "<ticket key>"
---

# Start Ticket

Turn a ticket into a worktree and an approved plan handoff. The next session builds the plan with
`/do-next`, so this skill ends at the plan.

```
read → /scope-ticket → /claim → move the ticket → draft the plan → plan gate → write the handoff
```

Scope comes before the claim. When a ticket splits, the worktree belongs to slice 1.

## Step 1: Read the ticket

1. Read the key from `$ARGUMENTS`. If it is not there, ask for it.
2. Read the ticket and each linked ticket with `/look-up`, in parallel. Linked tickets hold earlier
   decisions, related work, and constraints. Note each attachment or design link for the plan, and
   fetch no external URL.
3. Note the goal, the ACs, the issue type, the state, and the comments.
4. Letter the ACs. An AC has the form `- [ ] **A.** <action> → <expected>`, and a sub-check is
   `A.1`. Keep the letters that the ticket has. If its ACs have no letters, letter them in order,
   and note that the ticket needs the letters (Step 8).

**Done when:** you have the goal and every AC with a letter.

## Step 2: Scope the ticket

Run `/scope-ticket` with the key, and give it the Step 1 context, so it reads nothing again. Use
its verdict as given. The verdict is a hard gate:

| Verdict | Do |
|---|---|
| SCOPED | Plan the whole ticket. |
| SPLIT, path 1 | Plan the whole ticket. Each slice is a phase of the plan, in slice order. |
| SPLIT, path 2 | Plan only slice 1. Its ACs are the plan's ACs. The board owner makes the other tickets. |
| CLARIFY | Wait. `/scope-ticket` asks its questions and runs again with the answers. Use the new verdict. |

**Done when:** the verdict is SCOPED or SPLIT, and you know the scope of the plan.

## Step 3: Claim the worktree

Run `/claim` with the key. It returns the worktree path, the branch, and a handoff path or `none`.

- `none`: continue.
- A handoff: the work may have started. Show the path. Ask whether to continue that handoff or to
  write a new plan. To continue it, go to Step 9 with that handoff.

If `/claim` stops to ask a question, put the question to the user, and continue with the answer.

**Done when:** you have the worktree path and the branch.

## Step 4: Move the ticket

If the ticket is in a to-do state, move it to the tracker's in-progress state. Leave a ticket that
is further along. Say in one line what you did.

**Done when:** the ticket is in progress or further along.

## Step 5: Draft the plan

Plan only the scope from Step 2. Read the code in the worktree from Step 3. If the area that
changes is unknown, send one search subagent to find it. Its brief names no model.

The plan holds:

- **Steps.** Each step is a vertical slice: when it is done, a user can exercise it end to end.
  Put the most uncertain or risky work first. Each step that changes behaviour names its seam and
  the IDs of its test conditions. Its done line names the tests that it adds.
- **The production gate.** Name the flag, permission, or setting that gates the change, and what a
  user without it sees. If nothing gates it, say why that is safe.
- **The Test approach.** Read [`references/risk-and-technique.md`](references/risk-and-technique.md)
  and follow it: rate each AC, derive the conditions, and give each condition the cheapest level.
  Use its section format, with the `ID` column. When a flag gates the change, the flag-off path is
  a condition.

For each `—` row, ask whether the ticket needs an AC for that behaviour. A yes adds the AC with the
next free letter, and the row takes that letter. A no keeps the `—` row.

**Done when:** each AC has a Risks row, each H and M row has a condition, and each condition is in
the Conditions list of a step or under Not testing.

## Step 6: Plan gate

Show the draft handoff in the Step 7 format. Revise it with the user until they approve it. The
user approves the steps and the Test approach together.

If the plan is much bigger than the `/scope-ticket` estimate, say so before the approval. Give the
size that the plan shows and the points that it should have had. Then ask whether to keep the
ticket whole or to take one of the two SPLIT paths. Write no points, because an estimate never
overwrites a value.

**Done when:** the user approved the plan.

## Step 7: Write the handoff

Write the plan with `/write-to-file`, doctype `plan`, named for the key: `plan_<KEY>.md`. Write it
in Simplified Technical English. Read [`STE.md`](../../STE.md) before you write, and follow every
rule in it.

````markdown
# Plan: <KEY> <ticket title>
Worktree: <path>. Branch: <branch>.

Ticket: <key>. Goal: <one-sentence goal>. Scope: <SCOPED, or SPLIT path 1, or SPLIT path 2 slice 1 of n>. Estimate: <points>.

## Acceptance criteria

- [ ] **A.** <action> → <expected>
  - [ ] **A.1.** <sub-check>

## Context

<What the linked tickets, the comments, and the attachments decide. The production gate.>

## Test approach

<The section in the format of references/risk-and-technique.md.>

## Steps

- [ ] **1. <slice goal>.** Seam: `<seam>`. Conditions: C1, C2.
  - Done: <the tests that it adds, and what a user can do now>.
- [ ] **<n>. Review.** Depends on every earlier step. Review the branch with this handoff: `<handoff path>`. This step changes no code.
  - Done: each fix that the user picks is a step before the push step.
- [ ] **<n+1>. Push.** Push the branch and open a draft PR.

## Suggested skills

- `/do-next @<handoff path>`: one step per session, from the worktree.
- `/tdd`: each step that changes behaviour.
- `/mob-review`: the review step.
````

- The `Worktree:` line is the line after the title. `/claim` and `/do-next` read it.
- On SPLIT path 1, put the steps of each slice under `### Phase <n>: <slice goal>`, in slice
  order. The review and push steps come after the last phase.
- Name `/mob-review` only if this session has it.

**Done when:** the file exists, and its second line is the `Worktree:` line.

## Step 8: Write the letters back

Skip this step on SPLIT path 2, because the board owner rewrites the ticket from the proposal.
Also skip it when the ticket had its letters and Step 5 added no AC.

1. Show the exact change: the letter on each AC, and each new AC from Step 5. Write a new AC in
   plain words that every reader of the ticket understands. Change no other text.
2. Ask once. Write after a yes.
3. Read the ticket back. Check that only the letters and the new ACs changed. Show any other
   difference.

**Done when:** the ticket holds the letters after a yes, or you said why you wrote nothing.

## Step 9: Return

Give the worktree path, the branch, the handoff path, and the next command. The user starts a new
session in the worktree and runs `/do-next @<handoff path>`.

**Done when:** the user has the worktree path and the command.
