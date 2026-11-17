---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-21_eval-skill
status: approved
goal: "One run compares two versions of a skill and reports a winner or \"no difference\"."
spec: .ai/spec_pstack-21.md
builds_on: pstack-20
---

# Plan: pstack-21 `eval-skill`

## Goal

A new `meta/eval-skill` runs a blind A/B test of two versions of one skill, and reports a winner or "no difference". `/retro` offers it. Scope: SCOPED, one PR: one new skill with one script and its test, and edits to `retro` and the meta `README.md`.

## Spec

`.ai/spec_pstack-21.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `meta/eval-skill` → it frames the change with a rubric that only the judge sees, sets up folders and one prompt with no eval words, runs two candidates for each version, and has one blind judge score all outputs in one pass.
- [x] **B.** Read `/retro` → its summary offers `/eval-skill` for each applied row that edits a skill that a `work-on` playbook calls, and never requires it.
- [x] **C.** Run the leak check of `eval-skill` on a folder and a prompt that hold an eval word → it names the word and the path. On clean names → it prints nothing.
- [x] **D.** Run `eval-skill` on two versions of a skill → it reports a winner or "no difference".

## Context

- Map: `.ai/map_pstack-program.md`, unit 21. Done line: one run compares two versions of a skill and reports a winner or "no difference".
- Approval: the map (H0).
- Stack: this branch starts from `pstack-20_premise-escalation`, because the unit 20 PR is not merged. The home machine sets the unit 21 PR base to that branch. Do not delete the unit 20 `.ai/` files.
- Intent and Decisions: see the spec. Source: pstack `skills/poteto-mode/playbooks/eval.md`. Credit it in one line of prose in the skill.
- The banned words, from the source: `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, `arena`. A word matches as a whole word, with an optional plural `s`. `-`, `_`, `.`, `/`, and a space separate words. A word inside another word, such as `contest`, does not match.
- Candidate brief: the folder path and the organic prompt only. The candidate finds the skill where the project keeps its skills, at `<folder>/.claude/skills/<name>/SKILL.md`. The brief says the project's skills are there, in plain words.
- The judge runs at the `prover` role. Candidates run at the `worker` role. When the plan or the caller names a subagent model, candidates use it, and the judge uses a different model.
- `meta` uses `/grill` from `primitives`. `eval-skill` needs only the agent and git.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A new skill loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-21_eval-skill`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/meta/skills/eval-skill/scripts/leak_check.spec.py`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill's steps keep the candidates blind | M | skill text; one leaked word makes the run worthless, and nothing else catches it |
| B | `/retro` offers the skill | L | one line of skill text |
| C | the leak check names each banned word | M | new code: word boundaries, plurals, paths and prompt |
| D | the end-to-end run gives a verdict | M | joins A and C with live agents |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | C | a banned word in a folder or file name, split by `-`, `_`, `.`, or `/`, is listed with the path | EP | Unit | `leak_check.spec.py` |
| C2 | C | a banned word in the prompt file is listed, in any case, with a plural `s` | EP | Unit | `leak_check.spec.py` |
| C3 | C | a word inside another word (`contest`, `evaluate`) is not listed | BVA | Unit | `leak_check.spec.py` |
| C4 | C | a clean folder and prompt exit 0 with no output; a leak exits 1 | EP | Unit | `leak_check.spec.py` |
| C5 | D | a live run on two versions of `tabular-analysis`, one with a rule cut, gives a verdict | EP | Manual | the live run in step 4 |

### Not testing

- A and B: skill text. The review step reads each against its AC.

## Steps

- [x] **1. The leak check, test first.** Seam: `skills/meta/skills/eval-skill/scripts/leak_check.py <folder> <prompt file>`. Conditions: C1, C2, C3, C4. Write `leak_check.spec.py` first, in the style of `skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, and see it fail. Then write the script: walk every path under the folder, relative to it, and read the prompt file. Print `<path or "prompt">: <word>` for each match. Exit 1 on a match, else exit 0 with no output. Add no other option.
  - Done: `leak_check.spec.py` passes, C1 to C4. AC C holds.
- [x] **2. The `eval-skill` skill.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` and `skills/meta/skills/write-a-skill/SKILL.md` first. Write `skills/meta/skills/eval-skill/SKILL.md`, model-invoked. Say what `$SKILL_DIR` is. Steps, each with a done line: 1. Frame: the skill, versions A and B (defaults in the spec), what success looks like, and a rubric of 3 to 6 criteria that only the judge sees. 2. Set up four folders with project-shaped names under the temp folder, two for each version, with the version's `SKILL.md` and its sibling files at `.claude/skills/<name>/`, plus any project files an organic task needs. 3. Write one organic prompt to a file. Run the leak check on each folder and the prompt; fix each match. 4. Run the four candidates in parallel, with the same brief. 5. Run one judge: the rubric, and the four outputs under labels `P`, `Q`, `R`, `S` in a shuffled order; it scores each criterion for each output in one pass. 6. Read every output yourself, and say where you disagree with the judge. 7. Report: the versions, the rubric, the scores by version, the verdict (a winner, or "no difference", by the spec rule), and your read. Delete the four folders. Credit pstack in one line. Add a row to `skills/meta/README.md`.
  - Done: AC A holds on a read, and the pre-commit `$SKILL_DIR` check passes.
- [x] **3. `/retro` offers it.** Kind: docs. In `skills/engineering/skills/retro/SKILL.md` Step 7, add: for each applied row that edits a skill that a `work-on` playbook calls, offer `/eval-skill <skill>`. Never run it unasked.
  - Done: AC B holds on a read.
- [x] **4. Live run.** Kind: config. Conditions: C5. Run `/eval-skill` on `skills/primitives/skills/tabular-analysis`: version A is `HEAD`, version B is a scratch copy with Step 1 cut. Dispatch the candidates and the judge from this thread. Write the verdict and the scores in this Done line. Delete the scratch copy.
  - Done: AC D holds. Verdict: version B (Step 1 cut) wins. Judge totals out of 25: B 24 and 24, A 19 and 20. The scratch copy and the four folders are deleted.
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, `leak_check.spec.py` (6 tests), and `check_principles.py` each exit 0.
- [x] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-21.md`. This step changes no code.
  - Done: report `.ai/review_pstack-21_eval-skill.html`. Reviewed: base caa647d, head 680ffe7 (panel read 44dee66). The fix commit 680ffe7 holds 3 findings, 0 open.
- [ ] **7. Push.** Push-only map: run `git push -u origin pstack-21_eval-skill`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-21.md`: every step, then the test and review loop, from the worktree.
- `/tdd`: step 1.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-21_eval-skill`.
- 2026-11-18: step 1 done: `leak_check.py` and its spec, 6 tests green (commit 93ef4aa).
- 2026-11-18: step 2 done: `eval-skill/SKILL.md` and the meta README row (commit d4ebb97).
- 2026-11-18: step 3 done: `retro` Step 7 offers `/eval-skill`.
- Decision log: decisions_pstack-21.tsv
- 2026-11-18: checkpoint. Steps 1 to 3 are done, and the tree is clean. The step 2 and step 3 subagent ran only the pre-commit test; step 5 runs every gate. Open: step 4, the live run, which touches only a scratch copy of `skills/primitives/skills/tabular-analysis/SKILL.md` and temp folders. Next action: `/work-on @.ai/map_pstack-program.md`. It finds unit 21 open, skips the spec and plan (they exist), and resumes `/build @.ai/plan_pstack-21.md` at step 4 in the main thread, then `/blast-radius`, the ship checks, the push, and the tick. This branch starts from `pstack-20_premise-escalation` (pushed, not merged); keep the unit 20 `.ai/` files.
- 2026-11-18: step 4 done: live run on `tabular-analysis`. Candidates ran on `sonnet`, and the judge ran on `opus`. The judge scored each version on 5 criteria. Both B runs named the framework in each row, and both A runs left the rows unnamed with a key in the prose, which cost A on row identity and prose. My read: the gap comes from the Step 4 rule "don't invent a name column", which both versions hold, not from the cut Step 1. The run proves that the judge separates two versions, not that the cut made the skill better.
- 2026-11-18: step 5 done: every gate is green.
- 2026-11-18: step 6 done: light review fixed 3 findings in 680ffe7, 0 open.

## Pending Decisions

## Follow-ups

- `tabular-analysis` Step 4 says not to invent a name column. When the headers hold no name column, the rows lose their identity. The live run of step 4 showed this in both runs of the `HEAD` version. Offer the fix at the next `/retro`.
