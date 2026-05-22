---
name: do-it
description: >
  Execute a plan from /plan-it or a simple task using TDD. Walks through each step, delegates
  implementation to /tdd, checkpoints between steps for commits. Use when the user says "do it",
  "execute", "build it", "implement", "go", or wants to start coding after planning.
---

# Do It

Execute work via `/tdd`. Two steps: gather context, then build.

## Step 1: Gather Context

Invoke `/look-up` with `$ARGUMENTS`. If no arguments, check conversation context for plan file
paths, ticket keys, or task descriptions.

**Exit early** if neither arguments nor conversation provide actionable context. Ask:
> What are we building? Give me a plan file path, ticket key, or link.

After `/look-up` returns, classify the work:

- **Plan file provided** → parse steps, this is a multi-step execution
- **Ticket or description only** → this is a one-shot task

## Step 2: Execute

### Multi-step (plan file)

For each step in the plan:

1. Invoke `/tdd` with the step's behaviour goal, files, and acceptance criteria
2. Run typecheck for affected projects
3. Commit following project git conventions
4. Report: **"Step {N}/{M} complete"**

### One-shot (no plan)

1. Invoke `/tdd` with the task description
2. Run typecheck for affected projects
3. Commit following project git conventions

### Summary

After all work is done:

1. Run the full test suite one final time
2. List files changed, tests added, behaviours verified
3. Note any deviations from the original plan (if multi-step)
