---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-35_engineering-compress
status: approved
goal: "The engineering domain loads fewer bytes per turn and per run, and no skill, lane, or trigger loses behaviour."
builds_on: pstack-34
---

# Plan: pstack-35 Compress the engineering domain

## Goal

Cut no-ops, duplication, and sediment from the engineering domain. Bring every `SKILL.md` under the 10,000-byte sprawl line. Merge five skills into a mode of another skill, and merge the principles from 24 to 15. Each cut passes a check that fits its risk before the next tier starts. Scope: SCOPED, one PR, 23 rows from the domain audit, in four risk tiers.

## Acceptance criteria

- [ ] **A.** List the byte size of each `SKILL.md` in `skills/engineering/skills/` → none is over 10,000.
- [ ] **B.** Run each changed persona lane, old and new, on its seeded diff → the new lane finds each seeded defect that the old lane found, at the same tier.
- [ ] **C.** Run `/eval-skill` on `build`, `start-ticket`, `mob-review`, and the `happy-path` sad mode → no trial gives a win to version A.
- [ ] **D.** Say the trigger phrase of each merged skill ("light review", "sad path", "maintain the verify skill", "pr news", "review PR 123") → it reaches the mode that replaced the skill, and no file in `skills/` names a skill that is gone.
- [ ] **E.** Run the gates in Context → each exits 0.
- [ ] **F.** Compare the size table at the start and the end → the always-loaded description bytes, the per-panel-run persona bytes, and the total `SKILL.md` bytes each go down.

## Context

- Source: the engineering domain audit of 2026-11-19 (five read-only auditors, one table of 23 rows). The row numbers below are the rows of that table.
- Approval: the user asked for this plan to run under `/work-on` in the background. Running it is the H2 approval. Every row is in scope.
- Stack: this branch starts from `pstack-34_pr-feedback-retro`, which is not pushed. `pstack-34` edited `start-ticket`, `ship`, and `apply-review`. Compress those edits too, and keep their meaning.
- Run with no stop. Take each choice that keeps behaviour, and write it to the decision log. Write a `D` entry only when two choices change behaviour in different ways and no rule here decides.
- Check failure rule: when a check step (8, 14, 22) shows a loss, `git revert` the commit of the step that caused it, add a Follow-up that names the row and the loss, and continue. A loss never stops the run.
- Baseline: before step 1, write the size table to `.ai/scratch_pstack-35_sizes.md`: each `SKILL.md` size, the total description bytes of model-invoked skills, and each persona's `SKILL.md` plus `diff-signals.md` bytes. Step 23 writes the same table again for F, then deletes the scratch file.
- Skill retirement: each skill that a merge removes goes through `/retire-a-skill`, which moves it to `deprecated`. Each caller moves to the new mode in the same commit.
- Commands are not user-invoked: `code-simplify` and the other ★ commands keep model invocation (domain `CLAUDE.md`).
- `check_principles.py` holds a hard-coded `EXPECTED` list of 24 names and demands one work-on index entry per principle folder. Step 15 and step 16 change the script, its spec, the index, and the folders in one commit each.
- Public repo: write each edit in general words. No employer, client, person, or ticket names. The scrub hook checks this.
- Versions: only step 23 changes a `plugin.json`. `engineering` 3.2.0 → 4.0.0, because skills leave. `deprecated` 2.22.0 → 2.23.0. `meta` and `primitives` get one minor bump each only when a step changed them.
- Commit convention: conventional commits with the domain as scope, such as `refactor(engineering): …`, and `docs(ai)` for `.ai/`. No Claude attribution line.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`, the plan check of `/write-to-file`, and the link check: each relative `.md` link under `skills/engineering/` resolves to a file, and each `/<skill>` name in `skills/` resolves to a skill folder or a `deprecated` entry.
- Model: no subagent model. Each step runs at the `worker` role.
- Push-only: the push step runs `gh stack view --json`, then `git push -u origin pstack-34_pr-feedback-retro pstack-35_engineering-compress`. No PR. The user sets the PR base.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A, F | sizes go down | L | a script measures them |
| B | a lane still finds its defects after a cut | H | a cut sweep line or severity note can drop a find with no error |
| C | a skill still takes its moved branch | M | the agent can miss a pointer to text that left `SKILL.md` |
| D | a merged skill's trigger and callers still resolve | M | a dangling `/name` fails only when a run reaches it |
| E | gates stay green | L | commands |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A, F | each `SKILL.md` ≤ 10,000 B, and the three totals go down | EP | Integration | the size script, step 23 |
| C2 | B | for each changed lane, the new lane finds each seeded defect that the old lane found, at the same tier | EP | Integration | the seeded-diff harness, step 8 |
| C3 | C | `/eval-skill` gives no win to version A | EP | Integration | step 14 and step 22 |
| C4 | D | each trigger phrase of a merged skill reaches its new mode | EP | Integration | one fresh subagent per phrase, step 22 |
| C5 | D, E | no dangling link or `/name`, and the gates exit 0 | EP | Integration | the link check and gates, each step and step 24 |

### Not testing

- The wording rows (step 3) get a read-through, not a trial. Each swap names a concept that the model already knows.
- `create-pr` and `work-on` pointer moves get a read-through, not a trial, because they carry less traffic than the three skills in step 14.

## Steps

### Tier 1: mechanical cuts

- [x] **1. Persona and principle boilerplate.** Kind: mechanical. Conditions: C5. Rows 4, 18, 21.
  - Row 4: in each persona, cut "Otherwise return zero findings and stop.", "Judge the hunks, not the file.", "Anything on an unchanged line.", each "You are read-only" section, and the restated output-field lines that `PERSONA-CONTRACT.md` Output defines. Keep the one-line contract pointer, because a user can call a persona directly. Move "Judge the hunks, not the file." into the contract Scope rule 4 when it is not there.
  - Row 18: put one line in `skills/engineering/CLAUDE.md`: read a principle's file before you apply it, and name it in the reply. Each skill keeps only the principle name.
  - Row 21: cut each "Adapted from pstack …" line (benchmark, blast-radius, interrogate, verify, why, loop-until).
  - Done: the gates are green, and a grep for each cut phrase finds only the single source.
- [ ] **2. Description load.** Kind: config. Conditions: C5. Row 5. Set `disable-model-invocation: true` on `gazette`, `pick-next-task`, `tidy-up`, `sync-docs`, and `qa-screenshots`, and cut each description to one human-facing line. First grep `skills/` for a caller of each. A skill with a caller keeps model invocation, and the decision log says why.
  - Done: each of the five has the flag or a logged reason, and the gates are green.
- [ ] **3. Leading words.** Kind: docs. Conditions: C5. Row 20. Swap each spelled-out passage for its term: benchmark (`Amdahl's law`, `interleaved A/B runs`, `apples-to-apples`), loop-until (`ratchet`, `negative control`, `pin`, `re-baseline`), constraints (`ratchet`), code-simplify (`Chesterton's fence`, `behaviour-preserving`), persona-test-quality (`change-detector test`, `tautological assertion`, `vacuous test`), resolve-conflicts (`trivial merge`, `semantic conflict`), interrogate (`reproduced`, `unreproduced`). Keep a passage when the term loses a condition that the passage states, and log it.
  - Done: each swap is made or logged, and the gates are green.
- [ ] **4. Catalogue sources.** Kind: mechanical. Conditions: C5. Row 23. Delete the `**Sources:**` lines from the catalogues of persona-value-display, persona-url-state, persona-text-input, and persona-resilience. Keep each `###` heading and each Fix line, because `/sad-path` reads them.
  - Done: no `**Sources:**` line remains in those four folders, and `/sad-path`'s catalogue reads still find their headings.

### Tier 2: lane cuts, then a recall check

- [ ] **5. Diff-signals cut.** Kind: docs. Conditions: C2. Rows 1, 2. In `diff-signals.md` of persona-form-behaviour, persona-value-display, persona-url-state, and persona-text-input, cut each sweep line that restates a numbered rule of its `SKILL.md`, such as the lines tagged `(rule N)`. Keep each ID that no rule owns. Keep the Spot text of each kept line. Record in this line the cut IDs of each file, for step 8.
  - Done: form-behaviour `diff-signals.md` ≤ 10,000 B, the other three shrink, and the cut IDs are listed here.
- [ ] **6. Severity into rule headings.** Kind: docs. Conditions: C2. Row 3. In each persona, delete the Severity section when each rule heading already holds the tier. When the section holds a tier rule that no heading holds, move it into that heading first.
  - Done: no persona has a Severity section that restates its headings, and each rule heading has a tier.
- [ ] **7. Lane boundaries and the two large lanes.** Kind: docs. Conditions: C2. Rows 15, 22.
  - Row 15: persona-api-integrity, move the backend lookup steps to `references/`. persona-vitest, move rules 7 and 8 to persona-test-quality, and drop the carve-out line in both.
  - Row 22: add one boundary line to each Out of lane section, and the same line to PANEL.md Known overlaps. api-spec starts from a changed backend or spec, api-integrity from a changed frontend call, and a finding that needs both ends goes to api-integrity. error-handling owns whether a failure is reported, and async-state owns what the screen shows after. Dedup is code-quality, where code lives is architecture, and which API is best-practice. form-behaviour owns bounds and keys, text-input owns characters and units, and file-upload owns File objects and imports.
  - Done: both lanes are under 10,000 B, and each pair names the same boundary.
- [ ] **8. Lane recall check.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C2. For persona-form-behaviour, persona-value-display, persona-vitest, persona-test-quality, and persona-async-state:
  1. Build one small project folder with a diff that seeds four to six defects for the lane. Take at least two from the IDs that step 5 cut, and one that each moved rule (step 7) owns.
  2. Run one fresh subagent with the lane at the commit before step 5, and one with the lane at HEAD. Use the brief of `mob-review/SKILL.md` Step 3. Name no purpose of the run in the folder or the brief.
  3. Compare the found IDs and tiers. On a miss by the new lane, run both once more. A miss on both new runs is a loss: apply the check failure rule to the step whose cut removed the text.
  - Done: a table in this line gives each lane's seeded IDs, the old and new finds, and pass or revert.

### Tier 3: sprawl, then trials

- [ ] **9. build under 10 KB.** Kind: docs. Conditions: C1, C3. Row 11. Move the review-report fix-round branch of Step 1 to `build/FIX-ROUND.md` behind the pointer "Arguments hold a review report → read FIX-ROUND.md". Move Step 5 to STEP.md. Replace the item 8 restatement with "escalate one effort step, by rule 1 of the `models` block".
  - Done: `build/SKILL.md` ≤ 10,000 B, and each moved line exists once.
- [ ] **10. start-ticket under 10 KB.** Kind: docs. Conditions: C1, C3. Row 12. Move the Step 7 layout bullets to a pointer to the `/write-to-file` plan template, and keep only what the template does not say. Move Step 8 to `references/inputs.md`. Replace the Step 1.4 check list with a pointer to the check of `/refine-ticket`. Keep the design note and the reviewer-yes line from pstack-34.
  - Done: `start-ticket/SKILL.md` ≤ 10,000 B.
- [ ] **11. mob-review under 10 KB.** Kind: docs. Conditions: C1, C3. Row 13. Cut the Step 0 rationale to one line. Move the Step 1 scope and ownership bash to SCOPE-CASES.md. Cut the Notes bullet "Personas are independently invocable too…".
  - Done: `mob-review/SKILL.md` ≤ 10,000 B.
- [ ] **12. create-pr and work-on.** Kind: docs. Conditions: C1. Rows 14, 16 (work-on H4 only). create-pr: move Step 1 items 3 to 8 to `references/read.md`, and cut the Step 5.7 bullets that copy DRAFT-SCAN. work-on: replace the H4 list of eight actions with "H4 holds each action of the `pause-list.md` rule."
  - Done: `create-pr/SKILL.md` ≤ 9,000 B, and each cut line has its single source.
- [ ] **13. Consume a report.** Kind: docs. Conditions: C5. Row 19. Put one "Consume a report" section in `mob-review/REPORT.md`: read the prompt, parse the `runs` JSON, and find each row ID. Point apply-review Step 1, post-review-comments Step 1, and resolve-feedback Step 2 to it, and keep each skill's own stop conditions.
  - Done: the parse steps exist once, and the gates are green.
- [ ] **14. Pointer trials.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C3. Run `/eval-skill` three times. Version A is the commit before step 9, and version B is HEAD. The rubric scores only the result, never the wording of the edit. A trial that gives the win to A is a loss.
  - `build`: a small project with a plan and a review report whose pasted prompt ticks two rows. The run must take the fix-round branch. Rubric: each ticked row gets a fix step and a commit, each behaviour fix has a test that went red then green, the plan records each step, and the report to the user is true.
  - `start-ticket`: a ticket given as a file, with no tracker. Rubric: vertical slices, a Test approach with condition IDs, the plan template layout with its header keys, lettered ACs, and no false claim of approval.
  - `mob-review`: a small diff with three seeded defects. Rubric: each defect found at its tier, a report with a `runs` block and a coverage table, and no finding on an unchanged line.
  - Done: the three verdicts and totals are in this line, with each loss reverted.

### Tier 4: merges, then trigger checks

- [ ] **15. Principles 24 → 15.** Kind: docs. Conditions: C5. Row 17. Merge attack-the-premise into fix-root-causes, outcome-oriented-execution and migrate-callers-then-delete-legacy-apis into redesign-from-first-principles, laziness-protocol into subtract-before-you-add, and boundary-discipline into type-system-discipline. Fold explain-the-number into benchmark, exhaust-the-design-space into prototype, test-behavior-not-implementation into tdd, and never-block-on-the-human into work-on. Retire foundational-thinking. Repoint each citer. Update `EXPECTED`, its spec, and the work-on index in the same commit.
  - Done: 15 principle folders, `check_principles.py` exits 0, and a grep finds no citer of a removed name.
- [ ] **16. work-on principle index.** Kind: docs. Conditions: C5. Row 16. Cut each index entry to the principle name and its trigger in at most ten words. When `check_principles.py` reads more than the name, change the script and its spec.
  - Done: `work-on/SKILL.md` drops about 3,000 B, and `check_principles.py` exits 0.
- [ ] **17. light-review into mob-review.** Kind: docs. Conditions: C4, C5. Row 6. Add a `light` mode to mob-review. Put the ten-lane list in a `light` column of PANEL.md. Point `/review` and `/build` to `mob-review light`. Retire light-review.
  - Done: no file names `/light-review` outside `deprecated`, and the gates are green.
- [ ] **18. sad-path into happy-path.** Kind: docs. Conditions: C3, C4, C5. Row 7. Add a `sad` mode to happy-path. Put the shared setup block and report arguments in a new `skills/engineering/QA-REPORT.md`, and add it to the shared-files table of the domain `CLAUDE.md`. Point `/test` and `/build` to `happy-path sad`. Retire sad-path.
  - Done: no file names `/sad-path` outside `deprecated`, and the sad mode still reads the form-behaviour and text-input catalogues.
- [ ] **19. maintain-verification-skill into create-verification-skill.** Kind: docs. Conditions: C4, C5. Row 8. Move it to `create-verification-skill/MAINTAIN.md` behind a `maintain` argument, and keep `check_driver.py` shared. Point `/verify` and each other caller to it. Retire maintain-verification-skill.
  - Done: no file names `/maintain-verification-skill` outside `deprecated`.
- [ ] **20. pr-news into stand-up.** Kind: docs. Conditions: C4, C5. Row 9. Add an optional time window to stand-up, and port the in-window event rules of pr-news. Retire pr-news.
  - Done: stand-up with a window gives the per-PR events that pr-news gave, and no file names `/pr-news` outside `deprecated`.
- [ ] **21. review-pr into pickup.** Kind: docs. Conditions: C4, C5. Row 10. Add a `--review` flag to pickup that runs the claim, sync, and confirm steps, then `/engineering:mob-review`. Point `/review` to it. Update `PR-HANDLE.md`'s reader list. Retire review-pr.
  - Done: no file names `/review-pr` outside `deprecated`.
- [ ] **22. Trigger and trial check.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C3, C4.
  1. For each trigger phrase in AC D, run one fresh subagent with the HEAD skills of the domain in `.claude/skills/`. Give it the phrase as a user request. Pass when it picks the skill and mode that replaced the old skill.
  2. Run `/eval-skill` on `happy-path` in the sad mode against `sad-path` at the commit before step 18. Rubric: each item cites a catalogue ID, the items target the changed fields, the setup table comes first, and the fail ticks build a `/engineering:fix` prompt.
  - Done: each phrase result and the trial verdict are in this line, with each loss reverted.

### Close

- [ ] **23. Versions, README, and sizes.** Kind: config. Conditions: C1. Set the versions in Context. Update the skill table of `skills/engineering/README.md` and the `deprecated` README. Write the size table again, and put the before and after totals in this line. Delete the scratch file.
  - Done: A and F hold, by the totals in this line.
- [ ] **24. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **25. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-35.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **26. Push.** Push-only: run `gh stack view --json`, then `git push -u origin pstack-34_pr-feedback-retro pstack-35_engineering-compress`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Progress

- 2026-11-19: plan written on `pstack-35_engineering-compress`. Playbook `new-ticket`. H2 passed: the user asked for a background run of the plan. Next step: 3 (`/build @.ai/plan_pstack-35.md`).
- Decision log: decisions_pstack-35.tsv
- 2026-11-19: step 1 done (1bc0bbc). Persona guard, unchanged-line, read-only, and generic output lines cut to `PERSONA-CONTRACT.md`; "Judge the hunks, not the file" now in contract Scope rule 4 and the PANEL.md header; the principle read-and-name line now in the domain `CLAUDE.md`; pstack attribution lines cut. Next step: 2.

## Follow-ups
