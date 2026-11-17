---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills
branch: pstack-17_tidy-up-audit
status: approved
goal: "/tidy-up shows the table and deletes nothing until a pick."
spec: .ai/spec_pstack-17.md
---

# Plan: pstack-17 The `tidy-up` audit table

## Goal

Change `/tidy-up` so that it shows a read-only audit table first, and applies only the rows that the user picks. Scope: SCOPED, one PR, one file.

## Spec

`.ai/spec_pstack-17.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Run `/tidy-up` on a repo with a merged worktree and a dirty one → one table shows size, merged, dirty, PR state, and last used for each row.
- [ ] **B.** Read the skill → it deletes and fixes nothing until the user picks rows, and applies only the picked rows.
- [ ] **C.** Run `/tidy-up`, then pick no rows → no file, branch, or worktree changes.

## Context

- Map: `.ai/map_pstack-program.md`, unit 17. Done line: `/tidy-up` shows the table and deletes nothing until a pick.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Remove the bypass that applies the cleanup with no pick, and the repeated word in the opening list. Change Steps 1, 3, and 4 in place. Add no step, no script, and no file.
- Model: each subagent runs at `sonnet`, by the user's request.
- Production gate: none. The change is the text of one skill. It takes effect when the user reloads the plugin.
- Push-only map: this run uses no `gh` command on this repo. The push step runs `git push -u origin pstack-17_tidy-up-audit`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh` and `sh .githooks/commit-msg_test.sh`.

## Steps

- [x] **1. Rewrite the table and the pick in `tidy-up`.** Kind: docs. In `skills/engineering/skills/tidy-up/SKILL.md`: remove the repeated "plans" in the opening list. In Step 1, add the reads for the table columns: the size of each worktree and file, the dirty state of each worktree, the last commit date or file time, and the PR state from the code host. In Step 3, replace the table and the single yes: show one numbered row for each item with the columns item, work, size, merged, dirty, PR state, last used, proposed action, and reason, with `-` where a column does not apply. Change nothing in this step. Ask the user to pick rows by number, `all`, or `none`. Remove the bypass for a cleanup asked for by name. In Step 4, apply only the picked rows. Keep the description and the `README.md` row unless their words become false.
  - Done: the skill shows the table with the five columns, changes nothing before a pick, applies only the picked rows, and has no bypass. AC A, B, and C hold on a read of the skill.
- [x] **2. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. `pre-commit_test.sh` and `commit-msg_test.sh` print only `ok` lines.
- [x] **3. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-17.md`. This step changes no code.
  - Done: `.ai/review_pstack-17_tidy-up-audit.html`, base 54b3f0e, head b170da4 (panel read 5f67ec0). Two nits fixed in b170da4, none open. The fixes change only skill text, so no new round.
- [ ] **4. Push.** Push-only map: run `git push -u origin pstack-17_tidy-up-audit`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-17.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-17.md`: one step per session, from the worktree.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-inspired`, for the branch `pstack-17_tidy-up-audit`.
- 2026-11-17: step 1 done in commit d682824. Gates green.
- Decision log: decisions_pstack-17.tsv
