---
name: do-next
description: >
  Cold-start from a plan or plan, run its next step, and update the document for the next run.
  Use when the user says "do next" or hands you a plan to continue.
argument-hint: "@path/to/plan.md"
---

Read the @-tagged file as a cold agent, do the next step of work it describes, then leave the
document ready for the next run.

## Step 1: Cold Start

Read the file. It is the only context you have — treat it as the source of truth for what's done
and what's next. Follow any artifacts it references (plans, ADRs, issues, commits) as needed.

If the file is a plan, run `python3 $SKILL_DIR/../write-to-file/scripts/check_plan.py <absolute plan path>`. `$SKILL_DIR` is this
skill's base directory. A plan has `doctype: plan` in its YAML header, or a name that starts with `plan_` or `handoff_`.
On exit 1, stop the run before Step 2, and give each error line. For a file with no YAML header,
say that `/write-to-file` can migrate it to the plan layout.

Take the branch from the `branch` key of the YAML header, and the worktree from the `worktree`
key. Compare the branch with `git branch --show-current`. On another branch, stop the run before
Step 2. Name the worktree that has the plan's branch: the `worktree` path, else the match in
`git worktree list`. If no worktree has the branch, say so. A plan with no `branch` key, or
`branch: none`, names no branch.

**Done when:** the plan check passed, or the file is not a plan. You are on the plan's branch,
or the plan names no branch, and you can name the next undone step and its done line. Or you
stopped and gave the check errors or named the correct worktree.

## Step 2: Do the Next Step

Do the next undone step yourself: one step, the next vertical slice of progress, not the whole
backlog. If the plan names a skill for the step, use that skill. If the step needs a decision
from the user, put each decision to them with `/grill` and wait for the answers.

If the next step is ambiguous or blocked, stop and say so rather than guessing.

**Done when:** the step's own done line holds, or you stopped and said what blocks it.

## Step 3: Update the Plan

Invoke `/update-plan` on the same file to fold this run's progress back in, so the next
`/clear` + `/do-next` cold-starts cleanly.

**Done when:** the plan marks this step done and names the next one.
