---
name: do-next
description: >
  Cold-start from a handoff or plan, run its next step, and update the document for the next run.
  Use when the user says "do next" or hands you a handoff to continue.
argument-hint: "@path/to/handoff-or-plan.md"
---

Read the @-tagged file as a cold agent, do the next step of work it describes, then leave the
document ready for the next run.

## Step 1: Cold Start

Read the file. It is the only context you have — treat it as the source of truth for what's done
and what's next. Follow any artifacts it references (plans, ADRs, issues, commits) as needed.

If the handoff names the branch for its work, compare it with `git branch --show-current`. On
another branch, stop the run before Step 2. Name the worktree that has the handoff's branch: the
path the handoff records, else the match in `git worktree list`. If no worktree has the branch, say
so.

**Done when:** you are on the handoff's branch, or the handoff names no branch, and you can name
the next undone step and its done line. Or you stopped and named the correct worktree.

## Step 2: Do the Next Step

Do the next undone step yourself: one step, the next vertical slice of progress, not the whole
backlog. If the handoff names a skill for the step, use that skill. If the step needs a decision
from the user, put each decision to them with `/grill` and wait for the answers.

If the next step is ambiguous or blocked, stop and say so rather than guessing.

**Done when:** the step's own done line holds, or you stopped and said what blocks it.

## Step 3: Update the Handoff

Invoke `/update-handoff` on the same file to fold this run's progress back in, so the next
`/clear` + `/do-next` cold-starts cleanly.

**Done when:** the handoff marks this step done and names the next one.
