---
name: do-next
description: >
  Cold-start from a handoff/plan document and execute the next step, then update the document so
  the next run can pick up where this one left off. Takes one argument: the @-tagged file. Built
  to be run repeatedly — /clear, /do-next @file, repeat. Use when the user says "do next",
  "do the next step", or hands you a handoff to continue.
argument-hint: "@path/to/handoff-or-plan.md"
---

Read the @-tagged file as a cold agent, do the next step of work it describes, then leave the
document ready for the next run.

## Step 1: Cold Start

Read the file. It is the only context you have — treat it as the source of truth for what's done
and what's next. Follow any artifacts it references (plans, ADRs, issues, commits) as needed.

## Step 2: Do the Next Step

Identify the next undone step and delegate it to `/do-it` — one step, the next vertical slice of
progress, not the whole backlog.

If the next step is ambiguous or blocked, stop and say so rather than guessing.

## Step 3: Update the Handoff

Invoke `/update-handoff` on the same file to fold this run's progress back in, so the next
`/clear` + `/do-next` cold-starts cleanly.
