---
name: auto-handoff
description: Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user.
argument-hint: "@path/to/handoff-or-plan.md"
disable-model-invocation: true
---

# Auto Handoff

Run a handoff to the end with no user input between steps. Each step runs in a fresh subagent that
cold-starts from the handoff, as one `/clear` + `/do-next` run would. A step that needs the user
becomes an entry under `## Pending Decisions`, and the run continues with the steps that do not
depend on it. The user answers every entry in one batch at the end.

## Step 1: Pre-flight

1. Read the @-tagged handoff. List the remaining steps in handoff order.
2. If the working tree has modified or staged files, stop and ask the user about them. Those files
   are their in-flight work.
3. If the current branch is the default branch, ask the user once whether to commit there.

**Done when:** the step list exists, the tree has no modified or staged files, and the user accepts
the branch.

## Step 2: Run each step

For each remaining step, in handoff order:

1. Read the handoff again, because a subagent can add entries.
2. If an entry under `## Pending Decisions` lists the step in its `Blocks` line, mark the step
   skipped with that entry ID. Go to the next step.
3. Dispatch one fresh `general-purpose` subagent. Give it the handoff path, the step ID, and the
   absolute path to [`STEP.md`](STEP.md). Tell it to follow `STEP.md`.
4. Wait for it to return. Run one subagent at a time, because the steps share one working tree.
5. Check the result against the repo, not the summary. For status `done`, `git log` holds the
   commit it names and the handoff marks the step done. For an entry ID, the handoff holds that
   entry. For both, the tree has no modified or staged files.
6. If the check fails, stop the run and go to Step 3.

**Done when:** every remaining step is done, skipped with an entry ID, or the run stopped on a
failed check.

## Step 3: Report

Give one table with a row for each step from the Step 1 list:

| Step | Workflow | Commit | Tests | Status |
| ---- | -------- | ------ | ----- | ------ |

Take Workflow, Commit, and Tests from the subagent's return. Status is `done`, the entry ID the
subagent wrote, `skipped (<entry ID>)`, the failed check, or `not run`.

Below the table, give every entry under `## Pending Decisions` in full, in ID order. Then wait for
the user's answers.

**Done when:** every step from the Step 1 list has a row, and every entry appears below the table.

## Step 4: Record the answers

For each entry the user answers:

1. Write the answer into the handoff, at the step the entry blocks, as a recorded decision.
2. For a `B` entry, also write whether the next run resumes from the stash `auto-handoff: <step>`.
3. For an `N` entry the user has done, mark its step done.
4. Delete the entry.

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.

Then go back to Step 1, unless the user says to stop.

**Done when:** every answered entry is gone from `## Pending Decisions`, and its answer is in the
handoff.
