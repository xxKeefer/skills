---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-20_premise-escalation
status: approved
goal: "A third fix attempt starts with a written premise and a higher effort."
spec: .ai/spec_pstack-20.md
---

# Plan: pstack-20 Two failures and model escalation

## Goal

After two failed fixes on one premise, the agent writes the premise down and tests it, and the third attempt runs one effort step up, to a ceiling of `opus` at max effort. Scope: SCOPED, one PR: edits to four skill files and one section file, and one test.

## Spec

`.ai/spec_pstack-20.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `diagnose` and `fix` → each cites `principle-attack-the-premise` and `principle-fix-root-causes` by sibling path.
- [ ] **B.** Read `build` `STEP.md` and `build` `SKILL.md` → after two failed fixes on one premise, the step writes the premise down, tests it, and returns it, and `build` runs the next attempt one effort step up, to a ceiling of `opus` max, and logs the step through `/update-plan`.
- [x] **C.** Run `install_agents_md.py` against a scratch home → the `models` block holds the effort ladder in rule 1.
- [ ] **D.** Fail a fix twice on one premise → the third fix attempt starts with a written premise and a higher effort.

## Context

- Map: `.ai/map_pstack-program.md`, unit 20. Done line: a third fix attempt starts with a written premise and a higher effort.
- Approval: the map (H0).
- Intent and Decisions: see the spec. The ladder lives once, in rule 1 of `skills/utility/skills/install-agents-md/sections/models.md`. Each skill points to "rule 1 of the `models` block in `~/.claude/AGENTS.md`" and does not copy the ladder.
- The ladder: `low`, `medium`, `high`, `xhigh`, `max`. At `max` on a model below `opus`, the next step is `opus` at `max`. The ceiling is `opus` at `max`. With no `models` block, the agent uses the same ladder from the session model and its effort.
- A subagent cannot raise its own effort. `build` raises it when it dispatches the step again. `fix` raises it by a subagent for the third attempt.
- The premise text follows `principle-attack-the-premise`: the one sentence that every failed fix assumed, and the observation that tests it.
- Model: each subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. The change is skill text and one section file. It takes effect when the user reloads the plugin and runs `/install-agents-md`.
- Push-only map: this run uses no `gh` command on this repo. The push step runs `git push -u origin pstack-20_premise-escalation`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | `diagnose` and `fix` cite both principles | L | skill text, one line each |
| B | `build` escalates a step after two failures | M | skill text across two files that must agree; a loop with no ceiling would never stop |
| C | the `models` block holds the ladder | L | section text; the installer has tests |
| D | the end-to-end flow | M | joins B and C |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | C | the real `models` section renders the ladder, `low` to `max`, and the `opus` ceiling into the block | EP | Unit | `install_agents_md.spec.py` |
| C2 | D | a trace of `STEP.md` and `build` `SKILL.md` for a gate that stays red: attempt 1 and 2 at `sonnet` medium, a `B` entry with a premise, attempt 3 at `sonnet` high; and at `opus` max, the `B` entry stands | State transition | Manual | a read trace in step 4 |

### Not testing

- A and B: skill text. The review step reads each against its AC.
- A live `/build` run with a gate that fails twice: expensive, and the failure must be staged. C2 traces the text in its place.

## Steps

- [x] **1. The ladder in the `models` block.** Seam: `install-agents-md/sections/models.md`. Conditions: C1. Add a test to `install_agents_md.spec.py` that renders the real `models` section and finds the ladder, and see it fail. Then rewrite rule 1: after two failed fixes on one premise, write the premise down and test it, then move the next attempt one effort step up. Give the ladder `low`, `medium`, `high`, `xhigh`, `max`; at `max` on a model below `opus`, the next step is `opus` at `max`; the ceiling is `opus` at `max`. Record each step in the decision log.
  - Done: `install_agents_md.spec.py` passes, C1. AC C holds.
- [ ] **2. `diagnose` and `fix` cite both principles.** Kind: docs. Change the `Principle:` line of each to a `Principles:` line that names **principle-attack-the-premise** and **principle-fix-root-causes**, each with its sibling path, in the form of `build/SKILL.md`. In `fix` Step 3, add: after two failed fixes on one premise, write the premise down and test it, as `principle-attack-the-premise` says. Then run the third attempt in a subagent one effort step up, by rule 1 of the `models` block, and record the step with `/update-plan` when a plan exists. In `diagnose` Step 3, add: when two hypotheses that share one premise fail, write the premise down and test it before the next.
  - Done: AC A holds on a read, and `check_principles.py` exits 0.
- [ ] **3. Escalation in `build`.** Kind: docs. In `build/STEP.md` section 3, replace "After 3 fix attempts" with: after two fix attempts on one premise leave a gate red, write the premise down and test it, as `principle-attack-the-premise` says, then save the work, write a `B` entry, and return. Add `- Premise: <the sentence>, tested by <observation>: <result>` and `- Effort: <model> <effort>` to the `B` format, and change `Tried` to two attempts. In `build/SKILL.md` Step 2, add one item after the check: when a step returns a `B` entry below the ceiling, dispatch the step again one effort step up, by rule 1 of the `models` block, with the `B` entry as its start. Record the step with `/update-plan` as a choice, then delete the `B` entry. At the ceiling, the `B` entry stands. Keep the `D` and `N` formats as they are.
  - Done: AC B holds on a read. `STEP.md` and `SKILL.md` agree on the `B` format.
- [ ] **4. End-to-end trace.** Kind: config. Conditions: C2. Trace a gate that stays red through `STEP.md` and `build/SKILL.md` at `sonnet` medium, and write each attempt, its effort, and the premise line in this Done line. Then trace the same at `opus` max, and confirm the `B` entry stands.
  - Done: AC D holds.
- [ ] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-20.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **7. Push.** Push-only map: run `git push -u origin pstack-20_premise-escalation`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-20.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-20.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-20_premise-escalation`.
- 2026-11-18: step 1 done. The `models` rule 1 holds the ladder and the premise rule.
- Decision log: decisions_pstack-20.tsv

## Pending Decisions

## Follow-ups
