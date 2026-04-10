---
name: do-it
description: >
  Execute a plan from /plan-it or a simple task using TDD. Walks through each step, delegates
  implementation to /tdd, checkpoints between steps for commits. Use when the user says "do it",
  "execute", "build it", "implement", "go", or wants to start coding after planning.
---

# Do It

Execute implementation steps using `/tdd` for each one. Expects either a `/plan-it` output or a
simple task that skipped planning.

## Step 1: Find the Work

Check these sources in order:

1. **`$ARGUMENTS`** — a plan file path (e.g. `.ai/plan_TICKET-123.md`) or ticket key
2. **Conversation context** — a `/plan-it` output or a simple task description the user confirmed
3. If nothing found, use **AskUserQuestion**: "What are we building? Give me a plan file path,
   ticket key, or description."

For plan files, read and parse the steps. For ticket keys without a plan file, fetch the ticket from
the issue tracker and assess — if it's simple (1-3 files, obvious approach), proceed directly;
otherwise suggest running `/plan-it` first.

## Step 2: Confirm Before Starting (optional)

If proceeding directly present a summary:

> **Ready to execute `{ticket/task}`**
>
> **Steps:** {N} (or "single task" if no plan) **Files:** {key files to modify/create}
>
> 1. {step 1 title}
> 2. {step 2 title} ...
>
> Shall I proceed?

Wait for confirmation. If the user wants changes, adjust.

**If following from a plan or spike file, there is no need to confirm and summarize**

## Step 3: Execute Steps via /tdd

For each step in the plan (or the single task if no plan):

1. **Invoke `/tdd`** with:
   - The **behaviour to achieve** from this step's "What" description
   - The **files** listed for this step
   - The plan's **acceptance criteria** relevant to this step
   - The **reference implementation** from the plan (if provided)

2. Let `/tdd` own the full RED-GREEN-REFACTOR cycle. Do not duplicate its workflow — pass it the
   context and let it drive.

3. After `/tdd` completes the step, run **typecheck** for affected projects.

### Migration steps

If a step involves migrating existing code, `/tdd` handles it as a single behaviour goal. But
respect the migration phase ordering from the plan — each phase is a separate step with its own
`/tdd` invocation and checkpoint.

## Step 4: Checkpoint Between Steps

After each step completes:

- Summarise: files changed, tests added/modified, behaviours verified
- Report: **"Step {N} of {M} complete"**
- Run the full test suite for affected projects
- Make a commit message following conventions
- Each checkpoint is a commit boundary.

## Step 5: Final Review

After all steps are complete:

1. Run the full test suite one final time
2. Run typecheck for all affected projects
3. List all files created or modified
4. Note any deviations from the original plan
5. Run `/simplify` to review changed code for quality — fix any issues found
6. Ask if the user wants to create a PR
