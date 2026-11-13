---
name: build
description: "★ Build: run the next step of the plan handoff with /do-next, test-first, one commit per step. /run-wave runs every remaining step."
argument-hint: "[@handoff path]"
disable-model-invocation: true
---

# Build

Run one step of a plan handoff, then stop. `/do-next` does the work. Each step that changes
behaviour follows `/tdd` at the seams that the step names.

To run every remaining step with no stops between them, use `/run-wave` instead.

## Step 1: Find the handoff

1. If `$ARGUMENTS` holds a handoff path, use it.
2. Else find it the way `/claim` Step 3 does. Take the ticket key from the branch name, then look
   in the folder that `/write-to-file` uses for doctype `handoff` and `plan`.
3. If no file matches, or more than one does, ask for the path.

**Done when:** you have one handoff path.

## Step 2: Build one step

Run `/do-next @<handoff path>`.

**Done when:** `/do-next` finished one step and updated the handoff.

## Step 3: Hand on

Give the next command from the handoff:

- Steps remain: `/build @<handoff path>`, or `/run-wave @<handoff path>` to run them all.
- The build steps are done: `/test`, then `/review`.

**Done when:** the user has the next command.
