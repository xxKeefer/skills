---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-13_checkpoint
status: approved
goal: /checkpoint mid-step leaves a clean tree, and /do-next or /work-on resumes from the plan.
spec: .ai/spec_pstack-13.md
---

# Plan: pstack-13 checkpoint

## Goal

Remove the duplicate context trigger and the dead fallback line, then add `primitives/checkpoint`:
a thin skill that stops at a safe point, makes one `wip:` commit, and writes the resume note
through `/update-plan`. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-13.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `/update-plan` and `principle-guard-the-context-window` → the context trigger is only in `/checkpoint`, and the fallback line is gone.
- [ ] **B.** Read `primitives/checkpoint` → it finishes or backs out the step, makes one `wip:` commit, writes the note through `/update-plan`, and pushes nothing.
- [ ] **C.** Run `/checkpoint` mid-step on a plan, then `/do-next` on the same plan → the tree is clean after `/checkpoint`, and `/do-next` continues the same step from the note.

## Context

- Map: `.ai/map_pstack-program.md`, unit 13. Done line: `/checkpoint` mid-step leaves a clean tree, and `/do-next` or `/work-on` resumes from the plan.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Removal comes first (step 1). `/checkpoint` adds no script and no template.
- Source: pstack `poteto-mode/playbooks/pause-safely.md`.
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-13_checkpoint`. The home machine opens the PR into `pstack-inspired`.
- Spec Decisions: thin skill, `/update-plan` writes the note. The context trigger moves from `/update-plan` to `/checkpoint`. The principle drops its fallback line. No push and no PR during a pause.
- Out of scope: a change to `/do-next` or `/work-on`. The retirement of `/handoff` or `/do-next`.
- Production gate: none. A new skill that runs only on request, and two deleted lines.
- Commit convention: conventional commits with the domain as scope, such as `feat(primitives): ...`. No Claude attribution line, by the user's global rule. Change no `plugin.json` version (only unit 33 does).
- Gates: `python3 skills/primitives/skills/write-to-file/scripts/check_plan.spec.py`, `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py "$PWD"`, `.githooks/pre-commit`, `sh .githooks/pre-commit_test.sh`, and `sh .githooks/commit-msg_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the trigger and the fallback line | L | two deleted lines |
| B | the checkpoint steps | M | prose that another agent follows, and a wrong commit step loses work |
| C | a live checkpoint, then a resume | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | `checkpoint/SKILL.md` names the safe stop, one `wip:` commit, `/update-plan`, `/handoff` with no plan, and no push | review | Manual | the review step |
| C2 | C | a subagent runs `/checkpoint` mid-step on a scratch plan, and `git status --porcelain` is empty after it | use case | Manual | step 3 |
| C3 | C | a fresh subagent runs `/do-next` on the same plan, and continues the same step from the note | use case | Manual | step 3 |

### Not testing

- AC A: two deleted lines. `grep` in the step 1 done line proves it.
- No unit test: `/checkpoint` adds no script. The live run (C2, C3) is the closest real check, by the TDD skip rule.

## Steps

- [x] **1. Subtract.** Kind: docs.
  - Remove "or context is about to blow out" from the `/update-plan` description. Remove the line "If `/checkpoint` is not installed, ..." from `principle-guard-the-context-window`.
  - Done: `grep -rn "blow out\|not installed" skills/primitives/skills/update-plan skills/engineering/skills/principle-guard-the-context-window` finds nothing.
- [x] **2. `/checkpoint`.** Kind: docs.
  - Write `skills/primitives/skills/checkpoint/SKILL.md`: stop at a safe point, one `wip:` commit, the note through `/update-plan` (or `/handoff` when no plan exists), and a reply that names the commit, the clean tree, and the command to continue. Take the context trigger into its description. Add the row to `skills/primitives/README.md`.
  - Done: the skill and the README row exist. A user can run `/checkpoint`.
- [x] **3. Run it.** Seam: `/checkpoint` mid-step on a scratch plan, then `/do-next`. Conditions: C2, C3.
  - Make a git repo in `/tmp/checkpoint-demo` with a plan of one two-part docs step. One subagent does part one, then runs `/checkpoint`. A second fresh subagent runs `/do-next` on the plan. Record the commands and the output in Progress.
  - Done: `git status --porcelain` is empty after `/checkpoint`, the log holds one `wip:` commit, and the second subagent finishes the step from the note.
- [x] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at HEAD 3227d58. `check_plan.spec.py` and `check_principles.spec.py` print OK, `check_principles.py` exits 0, and the pre-commit hook, `pre-commit_test.sh`, and `commit-msg_test.sh` pass.
- [x] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-13.md`. This step changes no code.
  - Done: report `.ai/review_pstack-13.html`, base 3919d30, head 1978660. Light run, lanes skills and decisions-log, 0 findings.
- [x] **6. Push.** Push the branch with `git push -u origin pstack-13_checkpoint`. Push-only map: open no PR.
  - Done: pushed `c30165a` to `origin/pstack-13_checkpoint`.

## Suggested skills

- `/build @.ai/plan_pstack-13.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-13.md`: one step per session, from the worktree.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-13_checkpoint`.
- 2026-11-17: step 1 done in commit 036ddba. The trigger and the fallback line are gone.
- 2026-11-17: step 2 done in commit 0baa225. /checkpoint and its README row exist.
- Decision log: decisions_pstack-13.tsv
- 2026-11-17: step 3 done. The live run needed two attempts, and no repo fix.
  - Setup: scratch repo `/tmp/checkpoint-demo`, branch `demo-branch`, plan `.ai/plan_demo.md` with one docs step in two parts (part one writes `# Notes` to `notes.md`, part two appends `End of notes.`).
  - Checkpoint (C2): one fresh subagent did part one, then followed `checkpoint/SKILL.md`. It wrote the note through `/update-plan` ("Step 1 part one is done ... Next action: append the line `End of notes.`") and made one commit, `2dacf40 wip: 1 part one done, notes.md holds the title line`. `git status --porcelain` printed nothing.
  - Attempt 1 of the resume did not count. The step subagent returned before its nested subagents were done, and a nested `/do-next` that it started finished the step while the main thread ran its own. The main thread reset the scratch repo to `2dacf40`.
  - Resume (C3): one fresh subagent, given only `do-next/SKILL.md` and the plan path, read the checkpoint note, ran only part two, and committed `f45fa47`. `notes.md` holds `# Notes` and `End of notes.`, and `git status --porcelain` printed nothing.
- 2026-11-17: step 5 done. Light run on 1978660 against pstack-inspired (3919d30): 0 findings. Report `.ai/review_pstack-13.html`.
- 2026-11-17: blast radius: `clear`.
  - Safety fact: no file reads the two removed lines, and `checkpoint` is the only skill with that name in the repo, `~/.claude/skills`, and `~/.claude/plugins`. Rung 4: a Python script walks every `*.md` outside `.git` and `.ai` for the removed text, and every `SKILL.md` for `name: checkpoint`. It printed `ok: removed lines unread, one checkpoint skill` and exited 0.
  - Cleared: `/update-plan` keeps its "update plan" triggers, and `principle-guard-the-context-window` sends the context case to `/checkpoint`, which calls `/update-plan`. The primitives `plugin.json` lists no skills, so the new folder loads at the next `/reload-plugins` (ADR 0001). `/checkpoint` step 4 stages every change, but it pushes nothing, so a wrong `wip:` commit stays local and can be amended.
  - Confirmed risks: none.
- 2026-11-17: `/work-on` map playbook at step 8, stop H5: the `/retro` offer. Retro lead: a build step whose subagent starts nested subagents returned before they were done (step 3), because subagents run in the background. Next: `/work-on @.ai/map_pstack-program.md` starts unit 14.
- 2026-11-17: after the retro, the user asked to retire `/handoff`. ed71eb0 moved it to `deprecated` (dated 2026-11-17). 2a4c966 makes `/checkpoint` write the plan with `/write-to-file` when none exists, and updates the Handoff entry in `CONTEXT.md`. No version bump, by the map rule.
