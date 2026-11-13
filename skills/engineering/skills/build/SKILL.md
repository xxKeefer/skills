---
name: build
description: "★ Build: run every remaining step of the plan handoff in fresh subagents, then loop test and review until the branch is ready for /ship, then write the QA checklist. Pass it a review report's prompt to add a fix round. /implement runs one step."
argument-hint: "[@handoff path] | [@<review report> <row IDs>]"
disable-model-invocation: true
---

# Build

Run a handoff until the branch is ready to ship, with no user input between steps. Each step runs
in a fresh subagent that cold-starts from the handoff, as one `/clear` + `/implement` run would.
After the build steps, the run loops a test step and a review step until the branch passes the
`/ship` checks. Then it writes the QA checklist. It never runs the push step. `/ship` pushes.

```
build steps → test → review → (fix changed behaviour?) → test → review → … → QA checklist
```

A step that needs the user becomes an entry under `## Pending Decisions`, and the run continues
with the steps that do not depend on it. The user answers every entry in one batch at the end.

A review step fixes the findings that have a fix, writes the report, and writes no entry. The rows
that stay open wait for QA. To fix them, the user ticks them and runs `/build` on the report's
prompt. A fix round adds a new test and review only when the round can change behaviour.

## Step 1: Pre-flight

1. If the arguments hold a review report and row IDs, add a fix round first:
   1. Parse the JSON in the `<script type="application/json" id="runs">` block of the report. Find
      each ticked row in its run. Read the handoff path from the `Handoff` key of the run's
      `meta`. With no `Handoff` key, stop, and name `/engineering:apply-review`.
   2. Before the push step, add one step for each ticked row:
      `**<n>. Review fix <row ID>.** <issue> at <where>. Report: <report path>.` Its done line is
      the row's recommendation, with the row's note when it has one.
   3. After the fix steps, decide if the round needs a new round of test and review. It needs one
      when a ticked row changes runtime behaviour, or when the round has more than three fix steps.
      A row that changes only tests, comments, names, or file locations does not change behaviour.
      If the round needs one, add a new round as item 6 says. If the round does not need one, add
      no round. Write that choice into the handoff as a recorded decision.
   4. Write the unticked row IDs of the run into the handoff as a recorded decision, at the new
      review step. With no new review step, write them at the first step after the fix steps. Add
      the reason for each row when the report gives one.
   5. Delete the `D` entry that names this report. The ticks are its answer.
2. Read the handoff: the @-tagged one, or the one from item 1. Find the push step: the last step,
   which pushes the branch or opens the PR.
3. If the handoff names the branch for its work, compare it with `git branch --show-current`. On
   another branch, stop the run. Name the worktree that has the handoff's branch: the path the
   handoff records, else the match in `git worktree list`. If no worktree has the branch, say so.
4. If the working tree has modified or staged files, stop and ask the user about them. Those files
   are their in-flight work.
5. If the current branch is the default branch, make a branch named from the handoff and switch to
   it. Ask nothing.
6. Make sure the handoff has a test step and a review step after its last build step, before the
   push step. Add each one that is missing:
   - `**<n>. Test.** Run the project's test suite, and add a test for each changed behaviour that no
     test covers. This step changes no behaviour.` Its done line: the suite passes, and each
     behaviour that the branch changes has a test. Put it before the review step.
   - `**<n>. Review.** Review the branch with this handoff: <handoff path>. This step changes no
     code.` Its done line: the report path and the reviewed base and head SHAs are in this line.
     Name `/engineering:light-review`.

   To add a new round, add a new test step and a new review step after the last review step. Copy
   the text of the last test step and the last review step. In the new review step, add the row
   IDs that stay open in the last report. Tell the panel not to raise those rows again, and not to
   raise any row that only repeats them.
7. Write the changes with `/update-handoff`.
8. List the remaining steps in handoff order. Leave out the push step.

**Done when:** for a report, the handoff holds a fix step for each ticked row, and either a new
round or the choice to add none. The handoff has a test step and a review step before the push
step. The step list exists, the current branch is the handoff's branch or the handoff names no
branch, the tree has no modified or staged files, and the branch is not the default branch.

## Step 2: Run each step

For each remaining step, in handoff order:

1. Read the handoff again, because a subagent can add entries.
2. If an entry under `## Pending Decisions` lists the step in its `Blocks` line, mark the step
   skipped with that entry ID. Go to the next step.
3. Record the `HEAD` SHA. Dispatch one fresh `general-purpose` subagent. Give it the handoff
   path, the step ID, and the absolute path to [`STEP.md`](STEP.md). Tell it to follow `STEP.md`.
   To save subagents, give one subagent a batch: a run of consecutive review fix steps from the
   same round, at most four. Pick steps that are small or that touch the same files. Give it the
   list of step IDs in place of one ID. Any other step gets its own subagent.
4. Wait for it to return. Run one subagent at a time, because the steps share one working tree.
5. Check the result against the repo, not the summary. For a batch, check each step on its own,
   in order. For status `done`, the handoff marks the step done, and `git log` holds the commit it
   names. With `Commit: none`, `HEAD` is still the SHA from before that step. For an entry ID,
   the handoff holds that entry. For both, the tree has no modified or staged files. A batch
   stops at the first step that writes an entry. Mark each later step of the batch `not run`,
   and dispatch it again in a later pass.
6. If the check fails, stop the run and go to Step 4.
7. After a review step that is done, read its report from the step's done line, and decide the
   next round:
   1. If a row at tier Change Requested stays open, write one `D` entry in the format of
      `STEP.md`. Name the open rows and the report path. Option A: tick the rows in the report and
      run its prompt, which adds a fix step for each. Option B: leave the rows open, with a reason
      for each. The entry blocks the push step. Stop the loop.
   2. Else, if the review's fix commit changes runtime behaviour, add a new round, as Step 1
      item 6 says. Write it with `/update-handoff`, and add its steps to the list. Use the same
      behaviour rule as Step 1 item 1.3.
   3. Else stop the loop.

   Stop the loop after the third review step of this run, even if a fix changed behaviour. Say so
   in the report.

**Done when:** every remaining step is done, skipped with an entry ID, or the run stopped on a
failed check, and the loop stopped.

## Step 3: Write the QA checklist

Skip this step when the run stopped on a failed check, or `## Pending Decisions` holds an entry.

Dispatch one fresh `general-purpose` subagent. Tell it to run `/happy-path`, then `/sad-path` when
its guard matches the diff, as `/test` Step 2 says. Both write to one QA report. Tell it to return
the report path.

**Done when:** the QA report exists, or the step is skipped.

## Step 4: Report

Give one table with a row for each step from the Step 1 list, and for each step that the loop
added:

| Step | Workflow | Commit | Tests | Status |
| ---- | -------- | ------ | ----- | ------ |

Give each step of a batch its own row. Take Workflow, Commit, and Tests from the subagent's
return for that step. Status is `done`, the entry ID the
subagent wrote, `skipped (<entry ID>)`, the failed check, or `not run`.

Below the table, give the next command:

- An entry is pending: every entry under `## Pending Decisions` in full, in ID order. Then wait for
  the user's answers.
- The loop stopped at the third review step: the open rows and the report path. Say to run
  `/review`, or `/build` on the report's prompt.
- Else: the QA report path. QA items that fail build a `/fix` prompt. When every item passes, run
  `/ship`.

**Done when:** every step has a row, and the user has every entry or the next command.

## Step 5: Record the answers

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
