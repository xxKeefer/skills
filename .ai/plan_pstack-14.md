---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-14_stack-claim
status: approved
goal: claim on a branch inside a stack returns the stack's worktree, synced.
spec: .ai/spec_pstack-14.md
---

# Plan: pstack-14 stacks in claim and stand-up

## Goal

Remove the dead and repeated text in `claim`, `stand-up`, and `install-agents-md`, then teach
`claim` and `stand-up` about stacks and stale branches, and move the worktrunk template into
`install-agents-md`. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-14.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `claim`, `stand-up`, and `install-agents-md` → the repeated `plans or plans`, the `stand-up` Principles section that restates its steps, and the wrong `lists:` line are gone.
- [ ] **B.** Read `claim` → a branch inside a stack resolves to the worktree that holds the stack, with `gh stack checkout <branch>` there. A worktrunk refusal because another worktree sits at the expected path resolves the same way.
- [ ] **C.** Read `claim` → a stack branch whose local copy differs from the remote gets `gh stack sync` first, and the sync asks first when another person wrote a PR in the stack.
- [ ] **D.** Read `stand-up` → each PR row names the worktree that holds it, and a local branch that differs from its remote is flagged.
- [ ] **E.** Run the template in a scratch repo with `wt --config` → a ticket branch gets `<repo>.<KEY>`, a second branch with the same key is refused, and a branch with no key keeps its sanitized name. `install-agents-md` offers it, with relocate and the system map line.
- [ ] **F.** Run the `claim` stack check on a real stack whose worktree holds its top branch → the check returns that worktree for the bottom branch, and not the trunk worktree.

## Context

- Map: `.ai/map_pstack-program.md`, unit 14. Done line: `claim` on a branch inside a stack returns the stack's worktree, synced.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Step 1 removes text before any step adds it. No step adds a script.
- Source: the worktree note, items 1 to 5. It lives outside the repo, so the spec carries what the build needs.
- Push-only map: the build machine runs no `gh` command on this repo. The push step runs `git push -u origin pstack-14_stack-claim`.
- Evidence rule: the repo is public. A run on a work repo goes into Progress with no repo name, branch name, or ticket key.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, `python3 skills/primitives/skills/write-to-file/scripts/check_plan.spec.py`, `.githooks/pre-commit`, `sh .githooks/pre-commit_test.sh`, and `sh .githooks/commit-msg_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | removed text | L | deletions |
| B, C | the stack rows in `claim` | M | prose that another agent follows, and a wrong sync can push |
| D | the `stand-up` column and flag | L | one column and one status rule |
| E | the template | M | a TOML key in the wrong table does nothing, with no error |
| F | the stack check | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | E | `wt --config` with the template gives `<repo>.<KEY>`, refuses a second branch with the key, and keeps a branch with no key | use case | Manual | step 3 |
| C2 | F | the stack check in a real worktree set returns the stack's worktree for its bottom branch, and skips the trunk worktree | use case | Manual | step 4 |

### Not testing

- No unit test: the unit adds no script. The live runs (E, F) are the closest real check, by the TDD skip rule.
- `gh stack sync` and `gh stack checkout` are not run: both reach the remote of a work repo. The run in step 4 proves the detection and the stale counts only.

## Steps

- [x] **1. Subtract.** Kind: docs.
  - `claim`: fix `plans or plans`. `stand-up`: delete `## Principles`, and fold "say I did not check" into the empty-cell rule. `install-agents-md`: delete `lists: <repo>.<KEY>/` from `sections/tools.md`.
  - Done: `grep -rn "plans or plans\|## Principles\|<repo>.<KEY>" skills/engineering/skills/claim skills/engineering/skills/stand-up skills/utility/skills/install-agents-md` finds nothing, and the install spec passes.
- [x] **2. Stacks in `claim` and `stand-up`.** Kind: docs.
  - `claim` Step 2: the stack check, the stack row, the refusal rule, and the stale sync with its ask. `stand-up`: a `worktree` column and the stale flag, from `wt list --format=json`.
  - Done: ACs B, C, and D hold when you read the two skills.
- [x] **3. The worktrunk template.** Kind: docs.
  - Add `worktrunk.toml` to `install-agents-md` and a step that asks first, adds the key above the first table, runs `wt step relocate --dry-run` then the move, updates each moved plan's `worktree:` key, and lists the system map line. Prove the template in `/tmp` with `wt --config`. Conditions: C1.
  - Done: AC E holds, with the commands and output in Progress.
- [x] **4. Run the stack check.** Seam: the `claim` Step 2 stack check on a real stack. Conditions: C2.
  - Done: AC F holds, with the result in Progress, scrubbed of work facts.
- [x] **5. Test.** Run the gates from Context.
  - Done: every gate is green.
- [x] **6. Review.** Review the branch with this plan.
  - Done: a review report with each kept row fixed.
- [x] **7. Push.** `git push -u origin pstack-14_stack-claim`. Push-only map: open no PR.
  - Done: the branch is on the remote.

## Progress

### 2026-11-17: steps 1 to 6 (playbook `map`, unit 14)

- Step 1: removed `plans or plans`, the `stand-up` Principles section, and the `lists: <repo>.<KEY>/` line (`6de92a5`). The `grep` finds nothing, and the install spec prints OK.
- Step 3 (run before step 2, because `claim` needs the refusal text): in `/tmp/wtdemo` with `wt --config` (wt 0.26.0), `feat/ABC-12-first` → `repo.ABC-12`, `refactor/ABC-12-second` → refused with "there's a worktree at the expected path ... on branch feat/ABC-12-first", `ABC-500-plain` → `repo.ABC-500`, `fix/add-dark-theme` → `repo.fix-add-dark-theme`. The same line below a `[pre-merge]` header was ignored with no error (`repo.feat-XYZ-7-a`). `wt step relocate --dry-run` listed 2 moves to the key paths. C1 holds (`7312b03`).
- Step 2: the stack row, the refusal, and the sync in `claim`, and the `worktree` column and stale flag in `stand-up` (`4eec5b8`).
- Step 4: on a real work repo with one stack whose worktree holds its top layer, the check found exactly one worktree that holds the stack. The trunk worktree returned the stack, and the check skipped it. The bottom open layer has no worktree of its own. C2 holds. The run also showed that `wt list` gives no `remote` field on a branch row with no worktree, so the `claim` stale check moved to `git rev-list --left-right --count` (`0207bb9`). `gh stack checkout` and `gh stack sync` were not run, because both reach the remote of a work repo.
- Step 5: the install spec, `check_plan.spec.py`, `check_plan.py`, `check_spec.py`, `pre-commit_test.sh`, and `commit-msg_test.sh` pass. The pre-commit hook ran on each commit.
- Step 6: one review subagent, 9 findings, all fixed in `3e4381e`. The sync now skips a PR input, because `/review-pr` and `/pickup` sync in their own step. The author check uses `gh pr view --json author`. The new return value was removed. `stand-up` runs `gh stack view --json` for the `worktree` column, and the sync advice moved to `next step`, for the user's own PRs only.
- Choice: kept the `handoff_` names and the migration in `claim` Step 3. Reason: 22 plans in the user's plan folder still have no YAML header. Result: no subtraction there.
- Choice: no script for the stack check. Reason: the user's focus on subtraction, and two commands do the check. Result: prose only, proved by the step 4 run.
- Not done: `/plan` and `/build` were not invoked. The agent wrote the spec and plan in the unit 13 layout, ran each step in the main thread, and used one review subagent in place of `/light-review`. `/blast-radius` was folded into that review, which read each caller of `claim`.
- Step 7: pushed `pstack-14_stack-claim`. Unit 14 ticked on the map.
- Next: the home machine opens the PR into `pstack-inspired`. Then `/retro` on unit 14, or no.
