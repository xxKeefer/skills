---
name: plan-it
description: >
  Break a task into an executable plan for /do-it — or skip planning if the task is simple enough.
  Accepts an issue tracker ticket, a /spike-it output file, or a direct description. Use when the user
  says "plan it", "plan this", "break this down", "make a plan", or wants to prepare work for execution.
---

# Plan It

Assess a task and either produce an executable plan or hand off directly to `/do-it`.

## Step 1: Gather Context

`$ARGUMENTS` may contain any combination of:

- **Ticket keys** (e.g. `ENG-29019`) — fetch from the issue tracker
- **Spike file path** (e.g. `.ai/spike_ENG-29019.md`) — read the file
- **Free-text description** — anything else

If `$ARGUMENTS` is empty, check the current conversation for a `/spike-it` output. If still nothing, use **AskUserQuestion**:

> What are we planning? Give me a ticket key, spike file, or description.

Summarise the task back to the user in 2-4 bullets.

## Step 2: Explore Affected Code

Search the codebase for files that will be touched. Use Explore subagents if scope is broad.

Gather:

- **Files to modify** — modules, utilities, state management, API layer, routing
- **Files to create** — new modules, tests, types, shared logic
- **Existing tests** — what's already covered, what patterns are used nearby
- **Existing patterns** — how similar features are built in this codebase (find a reference implementation)

## Step 3: Assess Complexity

A task is **simple enough to skip planning** when ALL of these are true:

- Scope is 1-3 files
- No architectural decisions to make
- Clear single approach (no trade-offs to weigh)
- Implementation is obvious from the ticket/spike

If simple, tell the user:

> This is straightforward — [1-sentence summary of what to do]. Skip to `/do-it`?

If the user agrees, stop here. If they want a plan anyway, continue.

## Step 4: Break Down the Work

For complex tasks, decompose into **ordered implementation steps**. Each step must be:

- **Atomic** — one commit's worth of work
- **Testable** — has a clear "done" signal (tests pass, typecheck passes, behaviour verified)
- **Independent enough to checkpoint** — user can review and commit after each step

### Step structure

Each step needs:

```
### Step N: [Brief title]

**What:** 1-2 sentences describing the change
**Files:** list of files to create or modify
**Done when:** single sentence defining completion
```

### Testing approach

Steps do NOT include their own test specifications. The `/do-it` skill delegates each step to `/tdd`, which owns the full RED-GREEN-REFACTOR cycle. The plan describes **behaviours to achieve**, not tests to write.

If existing tests need tightening or migrating before implementation begins, make that Step 1 and note it should use `/tdd` to lock down current behaviour before any source changes.

### Ordering rules

1. **Test tightening first** — if existing tests need migration or gaps filled, that's step 1 (via `/tdd`)
2. **Infrastructure before features** — types, shared logic, state management before UI
3. **Migration phases in order** — if migrating existing code:
   - Phase 1: swap legacy dependencies/patterns keeping current interfaces
   - Phase 2: convert to modern patterns
   - Phase 3: clean up remaining legacy code
   See project-specific migration docs if applicable.
4. **Leaves before branches** — modify child dependencies before parents

### What NOT to plan

- Don't prescribe implementation details — `/do-it` and `/tdd` handle that
- Don't specify exact code to write — specify behaviour to achieve
- Don't add steps for "review" or "cleanup" — those happen naturally in TDD's refactor phase
- Don't duplicate test strategy — `/tdd` decides what to test and how

## Step 5: Write the Plan

Write the output using `/write-to-file` with filename `plan_{identifier}.md`.

Use the [output template](OUTPUT_TEMPLATE.md).

## Step 6: Confirm

Present a summary:

> **Plan for `{ticket}`** — {N} steps
>
> 1. {step 1 title}
> 2. {step 2 title}
> ...
>
> Ready to `/do-it`, or adjust anything?

Wait for the user. If they want changes, revise. If they want to execute, suggest running `/do-it`.
