---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills
branch: pstack-18_correct-ladder
status: approved
goal: "A repeated mistake gets a fix at the highest rung that works."
spec: .ai/spec_pstack-18.md
---

# Plan: pstack-18 The correct ladder

## Goal

Write the fix ladder once, in `principle-encode-lessons-in-structure`, and make `constraints` and `self-improve` apply it by path. Scope: SCOPED, one PR, three skill files.

## Spec

`.ai/spec_pstack-18.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `principle-encode-lessons-in-structure` → it orders the fix rungs as architecture, types, a lint whose error names the fix, a test, then docs, and counts a mistake class after two times.
- [x] **B.** Read `constraints` → when it writes a rule, it backs the rule at the highest rung of the ladder that works, and reads the principle by path for the ladder.
- [x] **C.** Read `self-improve` → a codebase-specific theme goes to the highest rung that works, with the agent file last, and the step reads the principle by path.
- [x] **D.** Run `python3 skills/engineering/skills/work-on/scripts/check_principles.py .` → exit 0, and no skill outside the principle restates the ladder.
- [x] **E.** Feed a repeated mistake through either skill → its fix lands at the highest rung that works.

## Context

- Map: `.ai/map_pstack-program.md`, unit 18. Done line: a repeated mistake gets a fix at the highest rung that works.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. One definition of the ladder, two pointers. Change the existing text in place. Add no step, no script, and no file. Replace the unordered list in the principle; do not add a second list beside it.
- Model: each subagent runs at `sonnet`, by the user's request.
- Production gate: none. The change is the text of three skills. It takes effect when the user reloads the plugin.
- Push-only map: this run uses no `gh` command on this repo. The push step runs `git push -u origin pstack-18_correct-ladder`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Steps

- [x] **1. Write the ladder into the principle.** Kind: docs. In `skills/engineering/skills/principle-encode-lessons-in-structure/SKILL.md`: replace the unordered list "a lint, a metadata flag, a runtime check, or a script" with an ordered ladder: 1. architecture (make the mistake impossible to write), 2. types, 3. a lint or check whose error names the fix, 4. a test, 5. docs, last. Add: a mistake class counts after two times; fix it at the highest rung that works. Keep the judgement paragraph and the corollary. Update the `description` only if its words become false. Keep the file short.
  - Done: the principle holds the ordered ladder and the two-times count, and `check_principles.py` exits 0. AC A holds.
- [x] **2. Point `constraints` and `self-improve` at the ladder.** Kind: docs. In `skills/engineering/skills/constraints/SKILL.md` Step 4 item 2: back each rule at the highest rung of the ladder in `$SKILL_DIR/../principle-encode-lessons-in-structure/SKILL.md` that works; read it first. In `skills/engineering/skills/self-improve/SKILL.md` Step 3: the row "Specific to this codebase or team" picks its target by the same ladder, with the agent file (`CLAUDE.md`, `AGENTS.md`) last; read the principle by path. Do not copy the rungs into either skill. Do not change the self-improve theme threshold.
  - Done: both skills name the principle path and do not restate the rungs. AC B, C, and E hold on a read.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. `pre-commit_test.sh` and `commit-msg_test.sh` print only `ok` lines, and `check_principles.py` exits 0. No skill outside the principle restates the rungs.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-18.md`. This step changes no code.
  - Done: `.ai/review_pstack-18_correct-ladder.html`, base 5790422, head 3014e27 (panel read 04f7bac). Light run: no essential lane matched, so `persona-skills` ran alone. One CR and one nit, both fixed in 3014e27, none open. The fixes change only skill text, so no new round.
- [x] **5. Push.** Push-only map: run `git push -u origin pstack-18_correct-ladder`, in place of `/create-pr`.
  - Done: pushed head 0c81cbb to `origin/pstack-18_correct-ladder`. Ship: go.

## Suggested skills

- `/build @.ai/plan_pstack-18.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-18.md`: one step per session, from the worktree.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-inspired`, for the branch `pstack-18_correct-ladder`.
- 2026-11-17: step 1 done in commit e43d7f0. The principle holds the ladder. Next: step 2.
- 2026-11-17: step 2 done in commit dd75f5b. Both skills name the principle path. Next: step 3.
- Decision log: decisions_pstack-18.tsv
- 2026-11-17: step 4 done. Build loop stopped by rule 7.3: the review fix changes no runtime behaviour. QA checklist skipped: the diff changes only skill text.
- 2026-11-17: blast radius `clear`. Safety fact: each reader of the ladder resolves the principle file, and only the principle holds the rungs. Rung 4. Readers: `constraints` (sibling link), `self-improve` (sibling link, since the retro), the `work-on` index, and the `README.md` row, which still fits. No script reads the principle text; `check_principles.py` checks only names, flags, and the index. Proof, run from the repo root, exit 0:

  ```sh
  set -e
  cd "$(git rev-parse --show-toplevel)"
  d=skills/engineering/skills
  p=$d/principle-encode-lessons-in-structure/SKILL.md
  test -f "$d/constraints/../principle-encode-lessons-in-structure/SKILL.md"
  grep -q '](../principle-encode-lessons-in-structure/SKILL.md)' $d/constraints/SKILL.md
  grep -q '](../principle-encode-lessons-in-structure/SKILL.md)' $d/self-improve/SKILL.md
  for r in 'Architecture' 'Types' 'names the fix' 'A test' 'Docs, last' 'after two times'; do grep -q "$r" $p; done
  n=$(grep -rl 'Docs, last' skills | wc -l); [ "$n" -eq 1 ]
  python3 $d/work-on/scripts/check_principles.py .
  echo ok
  ```
- 2026-11-17: ship go, pushed 0c81cbb. Map unit 18 ticked. Next: the home machine opens the PR into `pstack-inspired`, then `/retro` (H5).
- 2026-11-17: retro done. All 5 rows applied: the `$SKILL_DIR` dir check in the pre-commit hook (6815c00), the `$BASE` in `mob-review` Step 1 and the skip of Step 0 for a caller skill (97ca991), AC ticks from the step that proves them and the map `subagent_model` key (c1f6fbb, d9ba02e, b438d3c). No version bump (map rule: only unit 33 bumps). The proof script above now checks the sibling links.
