---
name: implement
description: "Run the next step of a plan handoff with /do-next, test-first, one commit per step. With no handoff, implement a spec or tickets with /tdd at agreed seams. /build runs every step, then tests and reviews in a loop."
argument-hint: "[@handoff path | spec or tickets]"
---

# Implement

Run one step of a plan handoff, then stop. `/do-next` does the work. Each step that changes
behaviour follows `/tdd` at the seams that the step names.

To run every remaining step, then test and review in a loop until the branch is ready to ship, use
`/build` instead.

## Step 1: Find the handoff

1. If `$ARGUMENTS` holds a handoff path, use it.
2. Else find it the way `/claim` Step 3 does. Take the ticket key from the branch name, then look
   in the folder that `/write-to-file` uses for doctype `handoff` and `plan`.
3. If no file matches, and `$ARGUMENTS` or the conversation holds a spec or tickets, go to Step 3.
4. If no file matches and there is no spec, or more than one file matches, ask for the path.

**Done when:** you have one handoff path, or a spec with no handoff.

## Step 2: Implement one step

Run `/do-next @<handoff path>`.

**Done when:** `/do-next` finished one step and updated the handoff.

## Step 3: Implement a spec with no handoff

Implement the work that the spec or the tickets describe.

1. Use `/tdd` where possible, at seams that the user agreed.
2. Run the typecheck and single test files often. Run the full test suite once at the end.
3. Commit the work to the current branch.

**Done when:** every acceptance criterion in the spec or the tickets holds, the typecheck passes,
and the full test suite is green.

## Step 4: Hand on

Give the next command:

- Handoff steps remain: `/implement @<handoff path>`, or `/build @<handoff path>` to run them all
  and loop test and review.
- The build steps are done: `/build @<handoff path>` to loop test and review, or `/test`, then
  `/review`.
- No handoff: `/test`, then `/review`.

**Done when:** the user has the next command.
