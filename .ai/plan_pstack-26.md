---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-26_fork-rule
status: approved
goal: "A grill looks up a fact instead of asking it."
spec: .ai/spec_pstack-26.md
builds_on: pstack-25
---

# Plan: pstack-26 the fork rule

## Goal

`grill`, `spec`, and the `plan` route classify each question before they ask it. A fact goes to a lookup or a prototype, and only a decision goes to the user. Scope: SCOPED, one PR: three skill edits.

## Spec

`.ai/spec_pstack-26.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `grill`, `spec`, and `plan` → each classifies a question before it asks: an observable fact goes to a lookup or a prototype, and only a decision goes to the user.
- [ ] **B.** Run a grill on a plan that turns on a fact in the corpus → the grill looks up the fact and does not ask it.

## Context

- Map: `.ai/map_pstack-program.md`, unit 26. Done line: a grill looks up a fact instead of asking it.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-25_sharpen`, because the unit 20 to 25 PRs are not merged. The home machine sets the unit 26 PR base to that branch. Keep the unit 20 to 25 `.ai/` files.
- Intent: see the spec. Source: pstack `skills/poteto-mode`, its fork rule. Before a question, classify it. An observable fact goes to a prototype or a lookup, not the user. Credit pstack in one line of prose in `grill`.
- Decisions: the HITL line is on actions (map Decision "Autonomy and the HITL line"). The pause list stays in the `pause-list.md` rule. This unit does not change it.
- One source for the rule: `grill` holds the fork rule. `spec` Step 3 already follows `/grill`, and gets one line that applies the rule to its gaps. `plan` holds no steps of its own, because `/start-ticket` does the work, so the line for the plan route goes into `start-ticket`, beside its "No questions" rule. `plan` itself does not change.
- The three classes: a fact that the corpus holds (look it up), a fact that a run or a prototype can settle (run it, then report what it showed), and a decision (ask the user, with a recommended answer). `grill` already says to look up a corpus fact. The new parts are the classify-first step and the prototype class.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-26_fork-rule`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the three skills hold the classify-first rule | L | skill text |
| B | a grill looks up a corpus fact and does not ask it | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a fresh agent follows the `grill` text on a short plan whose first open point is a fact in this repo. It looks the fact up and asks only a decision | EP | Manual | the live run in step 3 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [ ] **1. The fork rule in `grill`.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. In `skills/primitives/skills/grill/SKILL.md`, replace the fact line with the fork rule: before each question, classify it. A fact that the corpus holds: look it up. A fact that a run or a prototype can settle: run it, and report what it showed. A decision: ask the user, with a recommended answer. Credit pstack's `poteto-mode` in one line of prose. Keep the skill short and everything-agnostic.
  - Seam: `skills/primitives/skills/grill/SKILL.md`.
  - Done: AC A holds for `grill` on a read, and the pre-commit test passes.
- [ ] **2. `spec` and the plan route.** Kind: docs. In `skills/engineering/skills/spec/SKILL.md` Step 3, add one rule: classify each gap by the `/grill` fork rule first, and ask only the decisions. In `skills/engineering/skills/start-ticket/SKILL.md`, beside the "No questions" rule, add one line: before a question to the user, classify it by the `/grill` fork rule. Search the repo for other copies of the old `grill` fact line, and update each one.
  - Seam: the two skill files.
  - Done: AC A holds for `spec` and the plan route on a read.
- [ ] **3. Live run.** Kind: config. Conditions: C1. Give a fresh agent the `grill` text and this plan: "Add a `## See also` section to every skill in the `primitives` domain." Tell it to return the questions it would ask, and each fact it looked up instead, with the file it read. Copy the result in short form into this Done line.
  - Seam: the `grill` skill text, as an agent follows it.
  - Done: AC B holds. The agent looked up at least one fact in the repo, and asked only decisions.
- [ ] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-26.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: the report path, the reviewed base and head, and the result are in this line.
- [ ] **6. Push.** Push-only map: run `git push -u origin pstack-26_fork-rule`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-26.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-26.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-25_sharpen`, for the branch `pstack-26_fork-rule`.
- Decision log: decisions_pstack-26.tsv
- 2026-11-18: playbook `map`, step 3: three choices logged. Next: step 4, branch and `/build`.
