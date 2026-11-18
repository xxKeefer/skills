---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-30_text-diagrams
status: approved
goal: "`/show-me` draws a flow that the check passes."
spec: .ai/spec_pstack-30.md
builds_on: pstack-29
---

# Plan: pstack-30 text diagrams in `show-me`

## Goal

`primitives/show-me` gets a text diagram view for a flow or a dependency graph, and a script, `show-me/scripts/check_diagram.py`, that checks the width of each character and the corners of each box. Scope: SCOPED, one PR: one script with its tests, and one new view in the skill.

## Spec

`.ai/spec_pstack-30.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Ask `/show-me` for a flow or a dependency graph in a text view → it draws a box diagram with box-drawing characters and ASCII only, no emoji, one route per line, and a label on each line. Mermaid stays the HTML view.
- [x] **B.** Run `show-me/scripts/check_diagram.py` on a diagram → it passes when each character is one column wide and the box corners line up, and fails when either is false.
- [ ] **C.** Run `/show-me` on a flow, then run the check on its diagram → the check passes.

## Context

- Map: `.ai/map_pstack-program.md`, unit 30. Done line: `/show-me` draws a flow that the check passes.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-29_why`, because the unit 20 to 29 PRs are not merged. The home machine sets the unit 30 PR base to that branch. Keep the unit 20 to 29 `.ai/` files.
- Intent: see the spec. Mermaid does not render in a terminal or in plain markdown. A text diagram does.
- Decisions: the map names none for this unit.
- Examples: the diagrams in the map are the examples of the view. They use the arrow heads `▲ ► ▼ ◄` beside the box-drawing block (U+2500 to U+257F). So the check allows ASCII, the box-drawing block, and these four arrow heads. Each of these is one column wide in a monospace font. Any other character fails, with its line and column.
- Corner rule: for each `┌`, the first `┐` to its right on the same line is its top-right corner. A label can sit in the top edge, as in the map's `build loop` box. Down the column of `┌`, the first `└` is its bottom-left corner. The `┘` must sit on the line of `└`, in the column of `┐`. A missing corner fails, with the line and column of the `┌`.
- Interface: `python3 check_diagram.py <file>` reads every line of the file, or reads stdin when the path is `-`. It prints `ok` and exits 0, or prints one line for each error and exits 1. A fenced block in a markdown file is out of scope: the caller gives the diagram alone.
- Skill text: the new view goes in the view list of `show-me/SKILL.md`, after the Mermaid view, with one short example and the rules from AC A. The skill says what `$SKILL_DIR` is before it uses `$SKILL_DIR/scripts/check_diagram.py`, as the pre-commit hook requires. Mermaid stays the view for an HTML file.
- Tests: `scripts/check_diagram.spec.py`, run with `python3 check_diagram.spec.py`, as the other `*.spec.py` files in `primitives`. Copy two map diagrams into the tests as passing cases.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-30_text-diagrams`. Run no `gh` command.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`, and `python3 skills/primitives/skills/show-me/scripts/check_diagram.spec.py`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill draws a box diagram by the rules | L | skill text |
| B | the check passes a good diagram and fails a bad one | H | new logic, with edge cases in the corner scan |
| C | `/show-me` draws a flow that the check passes | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | two map diagrams, one with a label in a top edge, pass | EP | Unit | `test_map_diagrams_pass` |
| C2 | B | an emoji, a wide CJK character, and a combining mark each fail with line and column | EP | Unit | `test_wide_character_fails` |
| C3 | B | a box with its `┘` one column off fails, and a box with no `└` fails | BVA | Unit | `test_misaligned_corner_fails` |
| C4 | B | stdin with `-` gives the same result as a file | EP | Unit | `test_stdin` |
| C5 | C | a fresh agent follows `show-me/SKILL.md` on a flow of this repo, and the check passes on its diagram | EP | Manual | the live run in step 3 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The check.** Seam: the `check_diagram.py` command line. Conditions: C1, C2, C3, C4. Write the tests first and see them fail. Then write `skills/primitives/skills/show-me/scripts/check_diagram.py` by the character set, the corner rule, and the interface in Context.
  - Done: `check_diagram.spec.py` adds the four tests in the Conditions table, and each passes. AC B holds.
- [x] **2. The view.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. Add the text diagram view to `show-me/SKILL.md` as Context says, and name the check as the last action of the view. Update the `description` to name the new view. Add one line to `CREDITS.md`: the text diagram view is new here.
  - Done: AC A holds on a read, and the pre-commit test passes.
- [ ] **3. Live run.** Kind: config. Conditions: C5. Give a fresh agent the new `show-me/SKILL.md` and one flow of this repo, such as the stops of `/work-on`. Run the check on its diagram. Copy the result in short form into this Done line.
  - Done: AC C holds.
- [ ] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-30.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **6. Push.** Push-only map: run `git push -u origin pstack-30_text-diagrams`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-30.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-30.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-29_why`, for the branch `pstack-30_text-diagrams`.
- Decision log: decisions_pstack-30.tsv
- 2026-11-18: playbook `map`, step 3: plan status `approved`, four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `check_diagram.py` and its four tests, commit fa411ef. AC B holds.
- 2026-11-18: step 2 done: text diagram view in `show-me/SKILL.md`, commit 8edd8cc. AC A holds. The example passes the check.
