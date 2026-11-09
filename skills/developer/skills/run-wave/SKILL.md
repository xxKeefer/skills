---
name: run-wave
description: Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user. Also takes the prompt of a review report, and adds a fix round to the handoff first.
argument-hint: "@path/to/handoff-or-plan.md | @<review report> <row IDs>"
disable-model-invocation: true
---

# Run Wave

Run a handoff to the end with no user input between steps. Each step runs in a fresh subagent that
cold-starts from the handoff, as one `/clear` + `/do-next` run would. A step that needs the user
becomes an entry under `## Pending Decisions`, and the run continues with the steps that do not
depend on it. The user answers every entry in one batch at the end.

Run it again on each review report to loop: `run-wave` → review → the user ticks rows → `run-wave`
on the report's prompt → review, until the user is satisfied. A fix round adds a new review step
only when the round can change behaviour. A small round goes to the push step. When the user ticks
nothing and answers the review entry, `run-wave` goes on to the push step and opens a draft PR. A review
report with no rows writes no entry, so the run goes on to the push step with no stop.

## Step 1: Pre-flight

1. If the arguments hold a review report and row IDs, add a fix round first:
   1. Parse the JSON in the `<script type="application/json" id="runs">` block of the report. Find
      each ticked row in its run. Read the handoff path from the `Handoff` key of the run's
      `meta`. With no `Handoff` key, stop, and name `/code-review:apply-review`.
   2. Before the push step, add one step for each ticked row:
      `**<n>. Review fix <row ID>.** <issue> at <where>. Report: <report path>.` Its done line is
      the row's recommendation, with the row's note when it has one.
   3. After the fix steps, decide if the round needs a new review step. It needs one when a
      ticked row changes runtime behaviour, or when the round has more than three fix steps. A row
      that changes only tests, comments, names, or file locations does not change behaviour. If the
      round needs one, add a new review step. Copy the text of the last review step. Add the row IDs
      of the run that the user did not tick. Tell the panel not to raise those rows again, and not
      to raise any row that only repeats them. If the round does not need one, add no review step.
      Write that choice into the handoff as a recorded decision, and let the run go on to the push
      step.
   4. Write the unticked row IDs of the run into the handoff as a recorded decision, at the new
      review step. With no new review step, write them at the first step after the fix steps. Add
      the reason for each row when the report gives one.
   5. Delete the `D` entry that names this report. The ticks are its answer.
   6. Write the changes with `/update-handoff`.
2. Read the handoff: the @-tagged one, or the one from item 1. List the remaining steps in handoff
   order.
3. If the handoff names the branch for its work, compare it with `git branch --show-current`. On
   another branch, stop the run. Name the worktree that has the handoff's branch: the path the
   handoff records, else the match in `git worktree list`. If no worktree has the branch, say so.
4. If the working tree has modified or staged files, stop and ask the user about them. Those files
   are their in-flight work.
5. If the current branch is the default branch, make a branch named from the handoff and switch to
   it. Ask nothing.

**Done when:** for a report, the handoff holds a fix step for each ticked row. It also holds either
a new review step that names the unticked rows, or the choice to add no review step. The step list
exists, the current branch is the handoff's branch or the handoff names no
branch, the tree has no modified or staged files, and the branch is not the default branch.

## Step 2: Run each step

For each remaining step, in handoff order:

1. Read the handoff again, because a subagent can add entries.
2. If an entry under `## Pending Decisions` lists the step in its `Blocks` line, mark the step
   skipped with that entry ID. Go to the next step.
3. Record the `HEAD` SHA. Dispatch one fresh `general-purpose` subagent. Give it the handoff
   path, the step ID, and the absolute path to [`STEP.md`](STEP.md). Tell it to follow `STEP.md`.
4. Wait for it to return. Run one subagent at a time, because the steps share one working tree.
5. Check the result against the repo, not the summary. For status `done`, the handoff marks the
   step done, and `git log` holds the commit it names. With `Commit: none`, `HEAD` is still the
   SHA from item 3. For an entry ID, the handoff holds that entry. For both, the tree has no
   modified or staged files.
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
2. For an entry with a patch on its `Work` line, also write whether the next run resumes from that
   patch.
3. For an `N` entry the user has done, mark its step done.
4. Delete the entry.

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.

Then go back to Step 1, unless the user says to stop.

**Done when:** every answered entry is gone from `## Pending Decisions`, and its answer is in the
handoff.
