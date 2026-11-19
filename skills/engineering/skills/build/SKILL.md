---
name: build
description: >
  ★ Build: run every remaining step of the plan in fresh subagents, then loop test and
  review until the branch is ready for /ship, then write the QA checklist. Use when the user says
  "build" or "run the plan", gives a plan, or pastes a review report's prompt for a fix
  round. /implement runs one step.
argument-hint: "[@plan path] | [@<review report> <row IDs>]"
---

# Build

Run a plan until the branch is ready to ship, with no user input between steps. Each step runs
in a fresh subagent that cold-starts from the plan, as one `/clear` + `/implement` run would.
The test and review loop ends when the branch passes the `/ship` checks. Then it writes the QA
checklist. It never runs the push step. `/ship` pushes.

Principles: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)) and **principle-sequence-verifiable-units** ([`../principle-sequence-verifiable-units/SKILL.md`](../principle-sequence-verifiable-units/SKILL.md)).

A step that needs the user becomes an entry under `## Pending Decisions`, and the run continues
with the steps that do not depend on it. The user answers every entry in one batch at the end.

A review step fixes the findings that have a fix, writes the report, and writes no entry. The rows
that stay open wait for QA. To fix them, the user ticks them and runs `/build` on the report's
prompt.

## Step 1: Pre-flight

1. Arguments hold a review report and row IDs → read [`FIX-ROUND.md`](FIX-ROUND.md), and add the
   fix round first.
2. Read the plan: the @-tagged one, or the one from item 1. Find the push step: the last step,
   which pushes the branch or opens the PR.
3. Ask `/write-to-file` to check the plan. If the check fails, stop the run, and give each error
   line.
4. Take the branch from the `branch` key of the plan's YAML header, and the worktree from the
   `worktree` key. When `git branch --show-current` gives another branch, stop the run. Name the
   worktree that has the plan's branch: the `worktree` path, else the match in
   `git worktree list`. If no worktree has the branch, say so.
5. If the working tree has modified or staged files, stop and ask the user about them.
6. If the current branch is the default branch, make a branch named from the plan and switch to
   it. Ask nothing.
7. Make sure the plan has a test step and a review step after its last build step, before the
   push step. Add each one that is missing:
   - `**<n>. Test.** Run the project's test suite, and add a test for each changed behaviour that no
     test covers. This step changes no behaviour.` Its done line: the suite passes, and each
     behaviour that the branch changes has a test. Put it before the review step.
   - `**<n>. Review.** Review the branch with this plan: <plan path>. This step changes no
     code.` Its done line: the report path and the reviewed base and head SHAs are in this line.
     Name `/engineering:mob-review light`.

   To add a new round → read the Add a new round section of [`FIX-ROUND.md`](FIX-ROUND.md).
8. Write the changes with `/update-plan`. Give it each recorded decision of `FIX-ROUND.md` items
   3 and 4 as a choice: the decision, the reason, the evidence, and the result. It adds each one to
   the decision log.
9. List the remaining steps in plan order. Leave out the push step.

**Done when:** the plan check passed. The plan has a test step and a review step before the push
step, and for a report, a fix step for each ticked row and a new round or the choice to add none.
The step list exists. The branch is the plan's branch, or the plan names none, and is not the
default branch. The tree has no modified or staged files.

## Step 2: Run each step

For each remaining step, in plan order:

1. Read the plan again, because a subagent can add entries.
2. If an entry under `## Pending Decisions` lists the step in its `Blocks` line, mark the step
   `[-]`, and add `  - Skipped: blocked by <entry ID>` under it. Go to the next step.
3. Record the `HEAD` SHA. Dispatch one fresh `general-purpose` subagent. Give it the plan
   path, the step ID, the `goal` key of the plan's header word for word, and the absolute path
   to [`STEP.md`](STEP.md), to follow. Run it at the `worker` role of the
   `models` block in `~/.claude/AGENTS.md`, or at the `mechanical worker` role for a step that the
   plan marks mechanical. With no `models` block, use the session model. When the plan's Context
   names a subagent model, use that model in place of the role.
   To save subagents, give one subagent a batch of at most four consecutive steps: review fix
   steps from the same round, or steps that the plan marks `Kind: docs` or `Kind: mechanical`.
   Pick steps that are small or that touch the same files. Give it the list of step IDs in place
   of one ID. Any other step gets its own subagent.
   Two kinds of step run in this thread, with no step subagent:
   - A `Test.` step whose gates are only commands. Run them, then mark the step done with the
     result.
   - A step whose check needs fresh agents, such as a live run of a skill. Dispatch those agents
     from this thread, so that no agent starts an agent of its own.
4. Wait for it to return. Run one subagent at a time, because the steps share one working tree.
5. Check the result against the repo, not the summary. For a batch, check each step on its own,
   in order. For status `done`, the plan marks the step done, and `git log` holds the commit it
   names. With `Commit: none`, each commit after the SHA from before that step changes only the plan. For an entry ID,
   the plan holds that entry. For both, the tree has no modified or staged files. A batch
   stops at the first step that writes an entry. Mark each later step of the batch `not run`,
   and dispatch it again in a later pass. For a review step, the report must hold the JSON `runs`
   block of `/write-report`, and the coverage table of the new run must show at least one lane
   that ran.
6. If the check fails, stop the run and go to Step 4.
7. After a review step that is done, read its report from the step's done line, and decide the
   next round:
   1. If a row at tier Change Requested stays open, write one `D` entry in the format of
      `STEP.md`. Name the open rows and the report path. Option A: tick the rows in the report and
      run its prompt, which adds a fix step for each. Option B: leave the rows open, with a reason
      for each. The entry blocks the push step. Stop the loop.
   2. Else, if the review's fix commit changes runtime behaviour, add a new round, as
      `FIX-ROUND.md` says. Write it with `/update-plan`, and add its steps to the list. Use the same
      behaviour rule as `FIX-ROUND.md` item 3.
   3. Else stop the loop.

   Stop the loop after the third review step that the plan holds since its approval, even if a
   fix changed behaviour. A run after Step 5 continues the count. Say so in the report.
8. When a step returns a `B` entry, escalate one effort step, by rule 1 of the `models` block.
   Below the ceiling, write under the step with `/update-plan`: resume from the patch on the
   entry's `Work` line, the entry's `Premise` line, and the new effort as a choice. Delete the `B`
   entry, and dispatch the step again as item 3 says, with the `Premise` line in the prompt. At the
   ceiling, or with no `models` block, the `B` entry stands.

**Done when:** every remaining step is done, skipped with an entry ID, or the run stopped on a
failed check, and the loop stopped. You can name the rule that stopped the loop: 7.1, 7.3, the
third review step, or a failed check.

## Step 3: Write the QA checklist

Skip this step when the run stopped on a failed check, or `## Pending Decisions` holds an entry.
Skip it also when the diff changes only docs, skill text, and tests. Step 4 then gives the plan's
live-run check, if it has one, in place of the QA report.

Dispatch one fresh `general-purpose` subagent. Tell it to run `/happy-path`, then `/happy-path sad`
when its guard matches, as `/test` Step 2 says. Both write to one QA report. Then tell it to
run each `agent` row with `gh`, git, or the test command. A CI run from an earlier step that shows
the result counts, so cite its ID and push no new commit for it. Tell it to return the report path,
and pass or fail with evidence for each `agent` row.

**Done when:** the QA report exists and each `agent` row has a result, or the step is skipped.

## Step 4: Report

Give one table with a row for each step from the Step 1 list, and each step that the loop added:

| Step | Workflow | Commit | Tests | Status |
| ---- | -------- | ------ | ----- | ------ |

Give each step of a batch its own row. Take Workflow, Commit, and Tests from the subagent's
return for that step. Status is `done`, the entry ID the
subagent wrote, `skipped (<entry ID>)`, the failed check, or `not run`.

Below the table, name the rule that stopped the loop, from the Step 2 done line. Name each skipped
step with the rule that allowed the skip.

Then name the decision log, `decisions_<KEY>.tsv` beside the plan, when it exists. Say that `/sitrep`
lists the choices that the agent made alone.

Then give the next command:

- An entry is pending: every entry under `## Pending Decisions` in full, in ID order. Then wait for
  the user's answers.
- The loop stopped at the third review step: the open rows and the report path. Say to run
  `/review`, or `/build` on the report's prompt.
- Else: the QA report path, the result of each `agent` row, and only the `you` rows for the
  user. QA items that fail build a `/fix` prompt. When every item passes, run
  `/ship`.

If the user asks to ship, run `/ship`, never the push step or `/create-pr`: they skip the `/ship`
checks.

**Done when:** every step has a row, and the user has every entry or the next command.

## Step 5: Record the answers

When the user answers the entries → read [`ANSWERS.md`](ANSWERS.md), and follow it.
