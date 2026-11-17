---
name: start-ticket
description: >
  Start work on a ticket: refine, scope, or split it as needed, claim its worktree, and write the
  plan. Use when the user asks to start or pick up a ticket or a sub-task.
argument-hint: "<ticket key>"
---

# Start Ticket

Turn a ticket into a worktree and an approved plan. The next session builds the plan with
`/do-next`, so this skill ends at the plan.

```
read → /refine-ticket (on a gap) → /scope-ticket → /claim → move the ticket → draft the plan
     → plan gate → write the plan
```

Scope comes before the claim. When a ticket splits into sub-tasks, the run stops after
`/split-ticket`, and each sub-task gets its own `/start-ticket` run.

**No questions.** When the user says to ask no questions, follow
[`references/inputs.md`](references/inputs.md#no-questions).

## Step 1: Read the ticket

1. Read the key from `$ARGUMENTS`. If it is not there, ask for it. When `/plan` gives a spec in
   place of the key, read it as [`references/inputs.md`](references/inputs.md#a-spec) says.
2. Read the ticket and each linked ticket with `/look-up`, in parallel. Linked tickets hold earlier
   decisions, related work, and constraints. Note each attachment or design link for the plan, and
   fetch no external URL.
3. Note the goal, the ACs, the issue type, the state, and the comments.
4. Check the ticket. Run `/refine-ticket` when one of these holds:
   - The ticket does not say who gains, what changes, and why (the user story).
   - The ticket has no ACs.
   - An AC holds a vague scope word from [`../scope-ticket/SKILL.md`](../scope-ticket/SKILL.md)
     Step 2.
   - An AC contradicts the domain glossary, if the repo has one, such as a rule that the glossary
     forbids. The glossary can be out of date, so give the contradiction as a question.

   Give it the key and the text from item 2, so it reads nothing again. From here on, use its ACs
   in place of the ticket's ACs, even if it wrote nothing. Take the goal from its summary. Note
   whether it wrote them (Step 8).
5. Letter the ACs. An AC has the form `- [ ] **A.** <action> → <expected>`, and a sub-check is
   `A.1`. Keep the letters that the ticket or `/refine-ticket` gave. If the ACs have no letters,
   letter them in order, and note that the ticket needs the letters (Step 8).
6. If the ticket is a sub-task, read its map unit as
   [`references/inputs.md`](references/inputs.md#a-sub-task-map) says.

**Done when:** you have the goal and every AC with a letter. If `/refine-ticket` ran, you know
whether it wrote the ACs.

## Step 2: Scope the ticket

Run `/scope-ticket` with the key, and give it the Step 1 context, so it reads nothing again. If
`/refine-ticket` said that the answers show more than one goal, give that too. Use the
`/scope-ticket` verdict as given. The verdict is a hard gate:

| Verdict | Do |
|---|---|
| SCOPED | Plan the whole ticket. |
| SPLIT, path 1 | Plan the whole ticket. Each slice is a phase of the plan, in slice order. |
| SPLIT, path 2 | Run `/split-ticket` with the key, the slices, and the ticket text. Then stop. Return its report path, its sub-task keys, and its wave 1 commands. |
| CLARIFY | Wait. `/scope-ticket` gives its questions to `/refine-ticket` and runs again. Use the new verdict. Use the refined ACs in place of the Step 1 ACs, and note whether `/refine-ticket` wrote them (Step 8). If the verdict is still CLARIFY, stop and return the open questions. |

**Done when:** the verdict is SCOPED or SPLIT path 1, and you know the scope of the plan. On SPLIT
path 2, `/split-ticket` returned and you stopped.

## Step 3: Claim the worktree

Run `/claim` with the key. It returns the worktree path, the branch, and a plan path or `none`.

- `none`: continue.
- Another plan: the work may have started. Show the path. Ask whether to continue that plan
  or to write a new plan. To continue it, go to Step 9 with that plan.

If `/claim` stops to ask a question, put the question to the user, and continue with the answer.

**Done when:** you have the worktree path and the branch.

## Step 4: Move the ticket

Read the states from the repo's issue tracker doc, if its steering files name one. A label can be
a state. If the ticket is in a to-do state, move it to the tracker's in-progress state. Leave a
ticket that is further along. Say in one line what you did.

**Done when:** the ticket is in progress or further along.

## Step 5: Draft the plan

Plan only the scope from Step 2. Read the code in the worktree from Step 3. If the area that
changes is unknown, send one search subagent to find it. Its brief names no model. When a step
rewrites a rule, search the repo for the rule's old words, and give each copy a step.

The plan holds:

- **Steps.** Each step is a vertical slice: when it is done, a user can exercise it end to end.
  Put the most uncertain or risky work first. Each step that changes behaviour names its seam and
  the IDs of its test conditions. Its done line names the tests that it adds, and the letter of
  each AC that it proves. Each AC has one step.
- **The production gate.** Name the flag, permission, or setting that gates the change, and what a
  user without it sees. If nothing gates it, say why that is safe.
- **The Test approach.** Read [`../../TEST-APPROACH.md`](../../TEST-APPROACH.md)
  and follow it: rate each AC, derive the conditions, and give each condition the cheapest level.
  Use its section format, with the `ID` column. When a flag gates the change, the flag-off path is
  a condition.

Before you rate the ACs, read the defect hotspots of this repo, as
[`references/inputs.md`](references/inputs.md#defect-hotspots) says.

For each `—` row, ask whether the ticket needs an AC for that behaviour. A yes adds the AC with the
next free letter, and the row takes that letter. A no keeps the `—` row.

**Done when:** each AC has a Risks row, each H and M row has a condition, and each condition is in
the Conditions list of a step or under Not testing.

## Step 6: Plan gate

Show the draft plan in the Step 7 format. Revise it with the user until they approve it. The
user approves the steps and the Test approach together.

If the plan is much bigger than the `/scope-ticket` estimate, say so before the approval. Give the
size that the plan shows and the points that it should have had. Then ask whether to keep the
ticket whole or to take one of the two SPLIT paths. Write no points, because an estimate never
overwrites a value.

On SPLIT path 2, follow [`references/inputs.md`](references/inputs.md#split-at-the-plan-gate).

**Done when:** the user approved the plan. On SPLIT path 2, `/split-ticket` returned and you
stopped.

## Step 7: Write the plan

Write the plan with `/write-to-file`, doctype `plan`, named for the key: `plan_<KEY>.md`. Write in
Simplified Technical English. Read [`STE.md`](../../STE.md) before you write, and follow every rule
in it.

The plan has the layout of the `/write-to-file` plan template. Fill it this way:

- **Header.** `ticket` is the key. `worktree` and `branch` come from Step 3. `status` is
  `approved`, or `draft` when the user waived questions. `goal` is the one-sentence goal. Add
  `spec` when `/plan` gave a spec. For a sub-task with a map unit (Step 1), add `merge` and
  `builds_on` from the unit. `/claim` and `/do-next` read `worktree` and `branch`. `/create-pr`
  reads `merge`.
- **Goal.** The goal, the scope (SCOPED, or SPLIT path 1), and the `/scope-ticket` estimate.
- **Acceptance criteria.** The lettered ACs from Step 1 and Step 5.
- **Context.** What the linked tickets, the comments, and the attachments decide. The production
  gate. For a sub-task with a map unit, the map path and the unit's `Done:` line.
- **Test approach.** The section from Step 5, in the format of
  [`../../TEST-APPROACH.md`](../../TEST-APPROACH.md).
- **Steps.** The steps from Step 5, then a review step and a push step, as the template shows. The
  review step names this plan's path.
- **Progress.** One line: the date, and the branch that the plan is on.
- Add a `## Suggested skills` section after `## Steps`:
  - `/build @<plan path>`: every step, then the test and review loop, from the worktree.
  - `/implement @<plan path>`: one step per session, from the worktree.
  - `/tdd`: each step that changes behaviour.
  - `/engineering:mob-review`: the review step.
  - `/create-pr`: the push step.

More rules:

- Write no stack order into the plan, because it goes stale when a lower layer merges. When the
  ticket builds on another, set `builds_on: <key>` in the header. The stack tool holds the order.
- On SPLIT path 1, put the steps of each slice under `### Phase <n>: <slice goal>`, in slice
  order. The review and push steps come after the last phase.
- Name `/engineering:mob-review` only if this session has it.

**Done when:** the file exists, and the plan check of `/write-to-file` passed on it.

## Step 8: Write the letters back

Skip this step in these cases:

- The user said no to the last `/refine-ticket` run. The ticket does not hold the plan's ACs, so
  the letters have nothing to go on.
- The ticket holds its letters, and Step 5 added no AC. ACs that `/refine-ticket` wrote are in the
  ticket with their letters.

1. Show the exact change: the letter on each AC, and each new AC from Step 5. Write a new AC in
   plain words that every reader of the ticket understands. Change no other text.
2. Ask once. Write after a yes, or at once when the user waived questions.
3. Read the ticket back. Check that only the letters and the new ACs changed. Show any other
   difference.

**Done when:** the ticket holds the letters after a yes, or you said why you wrote nothing.

## Step 9: Return

Give the worktree path, the branch, the plan path, and the next command. The user starts a new
session in the worktree and runs `/do-next @<plan path>`.

**Done when:** the user has the worktree path and the command.
