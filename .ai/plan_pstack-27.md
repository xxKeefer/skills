---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-27_design-it-twice
status: approved
goal: "A design-it-twice run shows the rubric and the grafts."
spec: .ai/spec_pstack-27.md
builds_on: pstack-26
---

# Plan: pstack-27 the design-it-twice rubric

## Goal

`codebase-design/DESIGN-IT-TWICE.md` sketches the caller's usage first, writes a rubric before the fan-out, scraps a design on a known tell, picks a base by the rubric, and grafts the strong parts of the other designs onto it. Scope: SCOPED, one PR: one reference file and its two pointers.

## Spec

`.ai/spec_pstack-27.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `DESIGN-IT-TWICE.md` → it writes a rubric before the fan-out, sketches the caller's usage first, picks a base, grafts the strong parts of the other designs, and scraps a design on a known tell.
- [x] **B.** Run design-it-twice on a module → the output shows the rubric, the score of each design, the base, and each graft.

## Context

- Map: `.ai/map_pstack-program.md`, unit 27. Done line: a design-it-twice run shows the rubric and the grafts.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-26_fork-rule`, because the unit 20 to 26 PRs are not merged. The home machine sets the unit 27 PR base to that branch. Keep the unit 20 to 26 `.ai/` files.
- Intent: see the spec. Source: pstack `skills/arena` and `skills/architect` (research row r1.19). Write a rubric before the fan-out, pick a base, graft the strong parts of the losers. Sketch the caller's usage first. Scrap a design on known tells, such as a cast that it needs to compile. Credit pstack in one line of prose in `DESIGN-IT-TWICE.md`.
- Decisions: the map names none for this unit.
- Out of scope: `DEEPENING.md`, and the flow of `improve-codebase-architecture`. Its pointer line to design-it-twice changes only if its words go stale.
- The current file: Step 1 frames the problem, Step 2 fans out to 3 or 4 sub-agents with fixed briefs, Step 3 compares in prose and proposes a hybrid. The new parts: the caller sketch and the rubric in Step 1, a scrap check on each returned design, then a base and named grafts in place of a free-form hybrid.
- The rubric: three to five criteria, each with a weight, from the vocabulary of `codebase-design` (depth, locality, seam placement, testability through the interface) plus the constraints of the problem. The user sees it before the sub-agents return, so the designs cannot shape it.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-27_design-it-twice`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the file holds the caller sketch, rubric, scrap tells, base, and grafts | L | skill text |
| B | a run shows the rubric, the scores, the base, and the grafts | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a fresh agent follows `DESIGN-IT-TWICE.md` on one small module of this repo. Its output shows the caller sketch, the rubric before the designs, a score for each design, any scrapped design with its tell, the base, and each graft | EP | Manual | the live run in step 2 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The rubric in `DESIGN-IT-TWICE.md`.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. In `skills/engineering/skills/codebase-design/DESIGN-IT-TWICE.md`: in Step 1, add a sketch of the caller's code as it would read with an ideal interface, before any design. Then write a rubric of three to five weighted criteria, and show it to the user before the fan-out. In Step 2, add the caller sketch and the rubric to each brief. Add a scrap check after the fan-out: scrap a design on a known tell, such as a cast that it needs to compile, a caller that must know the order of calls, or an interface as wide as its implementation. Replace the free-form hybrid in Step 3: score each design that survives against the rubric in a table, pick the top score as the base, and name each graft from another design with its reason. Credit pstack `arena` and `architect` in one line of prose. Update the "Exploring alternative interfaces" line in `codebase-design/SKILL.md` to name the rubric and the grafts. Search the repo for other copies of the old Step 3 words ("propose a hybrid"), and update each one.
  - Seam: `skills/engineering/skills/codebase-design/DESIGN-IT-TWICE.md`.
  - Done: AC A holds on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1. Give a fresh agent the new `DESIGN-IT-TWICE.md` and `codebase-design/SKILL.md`, and one small module of this repo, such as `skills/engineering/skills/work-on/scripts/map_units.py`. The agent writes the designs itself in place of sub-agents, because a subagent cannot start its own. Tell it to return its output in the shape that the file asks for. Copy the result in short form into this Done line.
  - Seam: the `DESIGN-IT-TWICE.md` text, as an agent follows it.
  - Done: AC B holds. A fresh agent followed the file on `map_units.py`, and wrote three designs itself. Its output showed the caller sketch, a rubric of four weighted criteria before the designs, design B scrapped on the tell "interface as wide as its implementation", a score table (A 480, C 360), base A, and one graft from C (an all-or-none `tick` of several units) with its reason. Weak spot: the agent kept design C although C drops `show` from the caller sketch. It read the tell "does not serve the caller sketch" as soft.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [ ] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-27.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: the report path, the reviewed base and head, and the open rows are in this line.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-27_design-it-twice`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-27.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-27.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-26_fork-rule`, for the branch `pstack-27_design-it-twice`.
- 2026-11-18: playbook `map`, step 3: three choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: caller sketch, rubric, scrap check, base, and grafts in `DESIGN-IT-TWICE.md`, and the `SKILL.md` line.
- Decision log: decisions_pstack-27.tsv
- 2026-11-18: step 2 done: the live run proves AC B. See the step 2 Done line.
- 2026-11-18: step 3 done: the gates each exit 0.
