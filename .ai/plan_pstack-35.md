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

- [x] **A.** List the byte size of each `SKILL.md` in `skills/engineering/skills/` → none is over 10,000.
- [x] **B.** Run each changed persona lane, old and new, on its seeded diff → the new lane finds each seeded defect that the old lane found, at the same tier.
- [x] **C.** Run `/eval-skill` on `build`, `start-ticket`, `mob-review`, and the `happy-path` sad mode → no trial gives a win to version A.
- [x] **D.** Say the trigger phrase of each merged skill ("light review", "sad path", "maintain the verify skill", "pr news", "review PR 123") → it reaches the mode that replaced the skill, and no file in `skills/` names a skill that is gone.
- [x] **E.** Run the gates in Context → each exits 0.
- [x] **F.** Compare the size table at the start and the end → the always-loaded description bytes, the per-panel-run persona bytes, and the total `SKILL.md` bytes each go down.

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
- [x] **2. Description load.** Kind: config. Conditions: C5. Row 5. Set `disable-model-invocation: true` on `gazette`, `pick-next-task`, `tidy-up`, `sync-docs`, and `qa-screenshots`, and cut each description to one human-facing line. First grep `skills/` for a caller of each. A skill with a caller keeps model invocation, and the decision log says why.
  - Done: each of the five has the flag or a logged reason, and the gates are green.
- [x] **3. Leading words.** Kind: docs. Conditions: C5. Row 20. Swap each spelled-out passage for its term: benchmark (`Amdahl's law`, `interleaved A/B runs`, `apples-to-apples`), loop-until (`ratchet`, `negative control`, `pin`, `re-baseline`), constraints (`ratchet`), code-simplify (`Chesterton's fence`, `behaviour-preserving`), persona-test-quality (`change-detector test`, `tautological assertion`, `vacuous test`), resolve-conflicts (`trivial merge`, `semantic conflict`), interrogate (`reproduced`, `unreproduced`). Keep a passage when the term loses a condition that the passage states, and log it.
  - Done: each swap is made or logged, and the gates are green.
- [x] **4. Catalogue sources.** Kind: mechanical. Conditions: C5. Row 23. Delete the `**Sources:**` lines from the catalogues of persona-value-display, persona-url-state, persona-text-input, and persona-resilience. Keep each `###` heading and each Fix line, because `/sad-path` reads them.
  - Done: no `**Sources:**` line remains in those four folders, and `/sad-path`'s catalogue reads still find their headings.

### Tier 2: lane cuts, then a recall check

- [x] **5. Diff-signals cut.** Kind: docs. Conditions: C2. Rows 1, 2. In `diff-signals.md` of persona-form-behaviour, persona-value-display, persona-url-state, and persona-text-input, cut each sweep line that restates a numbered rule of its `SKILL.md`, such as the lines tagged `(rule N)`. Keep each ID that no rule owns. Keep the Spot text of each kept line. Record in this line the cut IDs of each file, for step 8.
  - Done: form-behaviour `diff-signals.md` ≤ 10,000 B, the other three shrink, and the cut IDs are listed here.
  - Cut IDs (7768ebf). The numbered rule states each of these: form-behaviour FM-A4, B1, D1, D2, D6, D14, E1, F3, F13, G1, G2, G3, H7, H11, J4, J5, M1, M2, M6, N2, N8, O1, IN-A1, IN-E1; value-display DS-B1, B11, B13, B15, D1, D2, D5, D7, D9, D11, D12, D13, D14, D16, E2, E3, E4, E5, E6, E7, E8, E10, F1, F2, F5, G11, L3, L4, L5, IN-G6; url-state NV-A1, A2, A3, A4, A5, A6, A7, B1, B4, B8, B9, C1, C2, D1, D2, D5, F5, G1, G2, H1, H3, H4, H5, I13, J1, J5, K2, L1, M1, M4, M5, M6, M7, N1, N2, P1, Q2, Q4, R2, R3; text-input IN-A3, A5, B1, B2, B3, C1, C5, C6, C9, C10, C13, D1, D3, D6, F1, F2, F4, F6, G4, H2, H3, H4, I3, J3, K1, K2, K3, K5, K6, K7, NV-D6, NV-I7, NV-I8, NV-I9, DS-A7.
  - Moved into the rule text, then cut (form-behaviour only): FM-A1, A2, A3, A7, B2 (rules 3 to 5), IN-A2 (rule 2), FM-D5, D8, D9, D12, D15, D17 (rules 6, 8, 9), FM-C6, F2, G5, H6, J3 (rules 10 to 13).
  - Kept with a `(rule N)` tag, because the line adds a case that the rule lacks: value-display DS-B3, B12, B14, D4, D6, D8, D10, E12, F3, L1; url-state NV-C3, C4, C6, E1, G3, H6, J7, K1, K3, M3; text-input IN-A4, B4, B6, C4, C7, F5, I4, J10, NV-H7.
- [x] **6. Severity into rule headings.** Kind: docs. Conditions: C2. Row 3. In each persona, delete the Severity section when each rule heading already holds the tier. When the section holds a tier rule that no heading holds, move it into that heading first.
  - Done: no persona has a Severity section that restates its headings, and each rule heading has a tier.
- [x] **7. Lane boundaries and the two large lanes.** Kind: docs. Conditions: C2. Rows 15, 22.
  - Row 15: persona-api-integrity, move the backend lookup steps to `references/`. persona-vitest, move rules 7 and 8 to persona-test-quality, and drop the carve-out line in both.
  - Row 22: add one boundary line to each Out of lane section, and the same line to PANEL.md Known overlaps. api-spec starts from a changed backend or spec, api-integrity from a changed frontend call, and a finding that needs both ends goes to api-integrity. error-handling owns whether a failure is reported, and async-state owns what the screen shows after. Dedup is code-quality, where code lives is architecture, and which API is best-practice. form-behaviour owns bounds and keys, text-input owns characters and units, and file-upload owns File objects and imports.
  - Done: both lanes are under 10,000 B, and each pair names the same boundary.
- [x] **8. Lane recall check.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C2. For persona-form-behaviour, persona-value-display, persona-vitest, persona-test-quality, and persona-async-state:
  1. Build one small project folder with a diff that seeds four to six defects for the lane. Take at least two from the IDs that step 5 cut, and one that each moved rule (step 7) owns.
  2. Run one fresh subagent with the lane at the commit before step 5, and one with the lane at HEAD. Use the brief of `mob-review/SKILL.md` Step 3. Name no purpose of the run in the folder or the brief.
  3. Compare the found IDs and tiers. On a miss by the new lane, run both once more. A miss on both new runs is a loss: apply the check failure rule to the step whose cut removed the text.
  - Done: a table in this line gives each lane's seeded IDs, the old and new finds, and pass or revert.
  - Result: old lane at 60d8bd8, new lane at 84e0f39, one fresh reviewer each with the `mob-review` Step 3 brief, on neutral fixture paths. Every seed found by the old lane was found by the new lane at the same tier, so no second run and no revert.

    | Lane | Seeded IDs (owner) | Old finds | New finds | Result |
    | --- | --- | --- | --- | --- |
    | form-behaviour | S1 FM-A2, S2 FM-D15, S3 FM-C6, S4 FM-D14, S5 FM-M2, S6 IN-A1 (all CR) | 6/6 CR | 6/6 CR (S2 merged with the cleared-quantity finding) | pass |
    | value-display | S1 DS-B1, S2 DS-D12, S3 DS-D5, S4 DS-E2, S5 DS-L5 (CR), S6 DS-F1 (Nit) | 6/6 at tier | 6/6 at tier, plus one extra Nit | pass |
    | vitest | S1 rule 1, S2 rule 2 (Nit), S3 to S6 rules 3 to 6 (CR) | 6/6 at tier | 6/6 at tier | pass |
    | test-quality | S1 rule 1, S2 rule 2 (CR), S3 old vitest rule 8, S4 old vitest rule 7, S5 rule 5 (Nit) | S1, S2, S5 at tier (S3, S4 sent to vitest by the old text) | 5/5: S1, S2, S4 CR, S3, S5 Nit | pass |
    | async-state | S1 rule 1, S2 rule 5, S3 rule 3, S4 rule 8, S5 rule 9 (CR), S6 rule 10 (Nit) | 6/6 at tier | 6/6 at tier | pass |

### Tier 3: sprawl, then trials

- [x] **9. build under 10 KB.** Kind: docs. Conditions: C1, C3. Row 11. Move the review-report fix-round branch of Step 1 to `build/FIX-ROUND.md` behind the pointer "Arguments hold a review report → read FIX-ROUND.md". Move Step 5 to STEP.md. Replace the item 8 restatement with "escalate one effort step, by rule 1 of the `models` block".
  - Done: `build/SKILL.md` ≤ 10,000 B, and each moved line exists once.
  - Result (17043e5): `build/SKILL.md` 12,898 → 9,992 B. Fix round in `build/FIX-ROUND.md`, Step 5 text in `build/ANSWERS.md`.
- [x] **10. start-ticket under 10 KB.** Kind: docs. Conditions: C1, C3. Row 12. Move the Step 7 layout bullets to a pointer to the `/write-to-file` plan template, and keep only what the template does not say. Move Step 8 to `references/inputs.md`. Replace the Step 1.4 check list with a pointer to the check of `/refine-ticket`. Keep the design note and the reviewer-yes line from pstack-34.
  - Done: `start-ticket/SKILL.md` ≤ 10,000 B.
  - Result (aec4476): `start-ticket/SKILL.md` 10,336 → 9,428 B.
- [x] **11. mob-review under 10 KB.** Kind: docs. Conditions: C1, C3. Row 13. Cut the Step 0 rationale to one line. Move the Step 1 scope and ownership bash to SCOPE-CASES.md. Cut the Notes bullet "Personas are independently invocable too…".
  - Done: `mob-review/SKILL.md` ≤ 10,000 B.
  - Result (d0a4422): `mob-review/SKILL.md` 10,464 → 9,213 B. The scope, SHA, and ownership commands are in `SCOPE-CASES.md`, which Step 1 now reads on each run.
- [x] **12. create-pr and work-on.** Kind: docs. Conditions: C1. Rows 14, 16 (work-on H4 only). create-pr: move Step 1 items 3 to 8 to `references/read.md`, and cut the Step 5.7 bullets that copy DRAFT-SCAN. work-on: replace the H4 list of eight actions with "H4 holds each action of the `pause-list.md` rule."
  - Done: `create-pr/SKILL.md` ≤ 9,000 B, and each cut line has its single source.
  - Result (b87bdcc): `create-pr/SKILL.md` 10,030 → 8,605 B, Step 1 items 3 to 8 in `references/read.md`; `work-on/SKILL.md` 8,834 → 8,553 B.
- [x] **13. Consume a report.** Kind: docs. Conditions: C5. Row 19. Put one "Consume a report" section in `mob-review/REPORT.md`: read the prompt, parse the `runs` JSON, and find each row ID. Point apply-review Step 1, post-review-comments Step 1, and resolve-feedback Step 2 to it, and keep each skill's own stop conditions.
  - Done: the parse steps exist once, and the gates are green.
  - Result (ef79058): `mob-review/REPORT.md` has a Consume a report section. apply-review 7,506 → 7,082 B, post-review-comments 7,257 → 6,771 B, resolve-feedback 7,584 → 7,654 B (pointer only), and `build/FIX-ROUND.md` item 1 points to it too.
- [x] **14. Pointer trials.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C3. Run `/eval-skill` three times. Version A is the commit before step 9, and version B is HEAD. The rubric scores only the result, never the wording of the edit. A trial that gives the win to A is a loss.
  - `build`: a small project with a plan and a review report whose pasted prompt ticks two rows. The run must take the fix-round branch. Rubric: each ticked row gets a fix step and a commit, each behaviour fix has a test that went red then green, the plan records each step, and the report to the user is true.
  - `start-ticket`: a ticket given as a file, with no tracker. Rubric: vertical slices, a Test approach with condition IDs, the plan template layout with its header keys, lettered ACs, and no false claim of approval.
  - `mob-review`: a small diff with three seeded defects. Rubric: each defect found at its tier, a report with a `runs` block and a coverage table, and no finding on an unchanged line.
  - Done: the three verdicts and totals are in this line, with each loss reverted.
  - Result: version A at 05fcd6c, version B at 96c0241. Each candidate folder held the domain and primitives skills of its version in `.claude/skills/`. Four opus candidates per trial, one sonnet judge, labels shuffled. No trial gives the win to A, so no revert.

    | Trial | A totals | B totals | Verdict | Note |
    | --- | --- | --- | --- | --- |
    | build (fix round) | 19, 20 (of 20) | 17, 19 | no difference | all four took the fix-round branch through FIX-ROUND.md or the old Step 1. The B 17 is a reply that called the tree clean with the QA report uncommitted. One A run also left the QA report uncommitted. |
    | start-ticket | 22, 24 (of 25) | 22, 25 | no difference | the first prompt stopped all four at the same refine question. The second prompt gave the answers up front. All four plans are `draft`, pass the plan check, and claim no approval. |
    | mob-review | 20, 19 (of 25) | 21, 21 | B wins | all four found the three seeds and ran the light set. The gap is only in fix detail. The key's Nit tier for the wrong comment was the key's error, and it marked down every output. |

### Tier 4: merges, then trigger checks

- [x] **15. Principles 24 → 15.** Kind: docs. Conditions: C5. Row 17. Merge attack-the-premise into fix-root-causes, outcome-oriented-execution and migrate-callers-then-delete-legacy-apis into redesign-from-first-principles, laziness-protocol into subtract-before-you-add, and boundary-discipline into type-system-discipline. Fold explain-the-number into benchmark, exhaust-the-design-space into prototype, test-behavior-not-implementation into tdd, and never-block-on-the-human into work-on. Retire foundational-thinking. Repoint each citer. Update `EXPECTED`, its spec, and the work-on index in the same commit.
  - Done: 15 principle folders, `check_principles.py` exits 0, and a grep finds no citer of a removed name.
  - Result (35d6d68): 14 principle folders, not 15, because the step names ten removals. The ten folders are in `deprecated`, and `check_principles.py` and its spec exit 0.
- [x] **16. work-on principle index.** Kind: docs. Conditions: C5. Row 16. Cut each index entry to the principle name and its trigger in at most ten words. When `check_principles.py` reads more than the name, change the script and its spec.
  - Done: `work-on/SKILL.md` drops about 3,000 B, and `check_principles.py` exits 0.
  - Result (f73d285): the index 3,671 → 1,289 B, each entry a name and a trigger of at most ten words. `work-on/SKILL.md` 8,553 → 6,786 B over steps 15 and 16, after the never-block rules moved in. The script reads only the name, so it and its spec do not change.
- [x] **17. light-review into mob-review.** Kind: docs. Conditions: C4, C5. Row 6. Add a `light` mode to mob-review. Put the ten-lane list in a `light` column of PANEL.md. Point `/review` and `/build` to `mob-review light`. Retire light-review.
  - Done: no file names `/light-review` outside `deprecated`, and the gates are green.
  - Result (4e84a30): mob-review takes `light`, and `LIGHT.md` holds the old step changes. PANEL.md has a Light column with the ten lanes. mob-review/SKILL.md 9,213 → 9,551 B, build 9,992 → 9,996 B.
- [x] **18. sad-path into happy-path.** Kind: docs. Conditions: C3, C4, C5. Row 7. Add a `sad` mode to happy-path. Put the shared setup block and report arguments in a new `skills/engineering/QA-REPORT.md`, and add it to the shared-files table of the domain `CLAUDE.md`. Point `/test` and `/build` to `happy-path sad`. Retire sad-path.
  - Done: no file names `/sad-path` outside `deprecated`, and the sad mode still reads the form-behaviour and text-input catalogues.
  - Result (f0c104d): happy-path takes `sad`, and `happy-path/SAD.md` holds the old sad-path steps, with the same two lane links to the form-behaviour and text-input fixtures and catalogues. `QA-REPORT.md` holds the shared setup block and report inputs. happy-path 3,706 → 3,249 B, build 9,996 → 9,993 B.
- [x] **19. maintain-verification-skill into create-verification-skill.** Kind: docs. Conditions: C4, C5. Row 8. Move it to `create-verification-skill/MAINTAIN.md` behind a `maintain` argument, and keep `check_driver.py` shared. Point `/verify` and each other caller to it. Retire maintain-verification-skill.
  - Done: no file names `/maintain-verification-skill` outside `deprecated`.
  - Result (1e00e47): create-verification-skill takes `maintain`, and `MAINTAIN.md` holds the old steps. create-verification-skill/SKILL.md 8,230 → 8,801 B. `check_driver.py` stays in its `scripts/` folder for both modes.
- [x] **20. pr-news into stand-up.** Kind: docs. Conditions: C4, C5. Row 9. Add an optional time window to stand-up, and port the in-window event rules of pr-news. Retire pr-news.
  - Done: stand-up with a window gives the per-PR events that pr-news gave, and no file names `/pr-news` outside `deprecated`.
  - Result (fbf1496): stand-up takes a time period, and `NEWS.md` holds the old pr-news steps whole. stand-up/SKILL.md 7,172 → 7,775 B. gazette's desk reporter runs stand-up with no time period.
- [x] **21. review-pr into pickup.** Kind: docs. Conditions: C4, C5. Row 10. Add a `--review` flag to pickup that runs the claim, sync, and confirm steps, then `/engineering:mob-review`. Point `/review` to it. Update `PR-HANDLE.md`'s reader list. Retire review-pr.
  - Done: no file names `/review-pr` outside `deprecated`.
  - Result (469a304): pickup takes `--review`, and `REVIEW.md` holds the old review-pr steps and stops. pickup/SKILL.md 4,188 → 4,621 B, mob-review/SKILL.md 9,551 → 9,557 B. `/review` routes a PR handle to `/pickup --review`.
- [x] **22. Trigger and trial check.** Kind: mechanical. Runs in this thread, because it needs fresh agents. Conditions: C3, C4.
  1. For each trigger phrase in AC D, run one fresh subagent with the HEAD skills of the domain in `.claude/skills/`. Give it the phrase as a user request. Pass when it picks the skill and mode that replaced the old skill.
  2. Run `/eval-skill` on `happy-path` in the sad mode against `sad-path` at the commit before step 18. Rubric: each item cites a catalogue ID, the items target the changed fields, the setup table comes first, and the fail ticks build a `/engineering:fix` prompt.
  - Done: each phrase result and the trial verdict are in this line, with each loss reverted.
  - Result: HEAD 8330875. No loss, so no revert.

    | Phrase | Picked | Result |
    | --- | --- | --- |
    | "light review" | `/mob-review light` | pass |
    | "sad path" | `/happy-path sad` | pass |
    | "maintain the verify skill" | `/create-verification-skill maintain` | pass |
    | "pr news" | `/stand-up 1 week` (news mode) | pass |
    | "review PR 123" | `/review` → `/pickup --review 123` → `/engineering:mob-review` in the claimed worktree | pass |

    Sad-mode trial: `sad-path` at fa02780 (A) against `happy-path sad` at HEAD (B), on a form fixture, four opus candidates, one sonnet judge. A 25, 24 and B 24, 24 (of 25): no difference. Every report cites a catalogue ID on each item, puts the setup table first, and builds an `/engineering:fix` prompt from the fail ticks.

### Close

- [x] **23. Versions, README, and sizes.** Kind: config. Conditions: C1. Set the versions in Context. Update the skill table of `skills/engineering/README.md` and the `deprecated` README. Write the size table again, and put the before and after totals in this line. Delete the scratch file.
  - Done: A and F hold, by the totals in this line.
  - Result (f4209fe): `SKILL.md` bytes 657,458 → 593,497. Model-invoked description bytes 12,628 → 11,469. Persona bytes 331,267 → 307,048. `SKILL.md` files over 10,000 B: 6 → 0. Versions: engineering 3.2.0 → 4.0.0, deprecated 2.22.0 → 2.23.0, utility 1.27.0 → 1.28.0. Both READMEs already match the skill folders. The scratch file is deleted.
- [x] **24. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
  - Result: at 53e4d48, each gate exits 0: pre-commit test, commit-msg test, `check_principles.py`, the plan check, and the link check with the five retired skill names.
- [x] **25. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-35.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: `/engineering:mob-review light`, report `.ai/review_pstack-35_engineering-compress.html`. Reviewed base 17b2b61 (`pstack-34_pr-feedback-retro`), panel read ba23252, reviewed head 79bc8e0 (the fix commit). 10 findings (8 Change Requested, 2 Nit), all fixed, none open.
- [x] **26. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
  - Result: at 7a7b1a6, each gate exits 0: pre-commit test, commit-msg test, `check_principles.py`, the plan check, and the link check with the five retired skill names.
- [x] **27. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-35.md`. This step changes no code. Lanes: the six light lanes that ran in step 25 (skills, correctness, test-design, test-quality, comments, code-quality), because skills raised findings and the fix commit 79bc8e0 changed files that each of their guards matched. No row stays open from step 25, so the panel has no rows to skip. Do not raise a row that only repeats a fixed row of step 25.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: `/engineering:mob-review light`, run 2 of report `.ai/review_pstack-35_engineering-compress.html`. Reviewed base 17b2b61 (`pstack-34_pr-feedback-retro`), panel read 6ca57a5, reviewed head 25792c3 (the fix commit). persona-skills ran in seven shards, one of them on 79bc8e0 only. 13 findings (8 Change Requested, 5 Nit), all fixed, none open. Each `SKILL.md` is at most 10,000 B.
- [x] **28. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
  - Result: at b3d6e79, each gate exits 0: pre-commit test, commit-msg test, `check_principles.py`, the plan check, and the link check with the five retired skill names.
- [x] **29. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-35.md`. This step changes no code. Lanes: the six light lanes of step 27 (skills, correctness, test-design, test-quality, comments, code-quality), because skills and correctness raised findings and the fix commit 25792c3 changed files that each of their guards matched. No row stays open from step 27. Do not raise a row that only repeats a fixed row of step 25 or step 27. This is the third review step since approval, so `/build` stops the loop after it.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: `/engineering:mob-review light`, run 3 of report `.ai/review_pstack-35_engineering-compress.html`. Reviewed base 17b2b61 (`pstack-34_pr-feedback-retro`), panel read e8355e7, reviewed head fbbffe7 (the fix commit). persona-skills ran in seven shards, one of them on 25792c3 only. 17 findings (7 Change Requested, 10 Nit), all fixed, none open. Each `SKILL.md` is at most 10,000 B.
- [x] **30. Review fix r1.1.** A block moved to a sibling file that the skill reads on every run, so the run loads more bytes: apply-review and post-review-comments (all of `mob-review/REPORT.md` for one section), mob-review (`SCOPE-CASES.md`), start-ticket (`references/inputs.md`), happy-path (`QA-REPORT.md`), and create-pr (`references/read.md`). Report: `.ai/interrogate_pstack-35_engineering-compress.html`.
  - Done: `python3 /tmp/pstack-35/int/repro/repro_per_run_bytes.py apply-review post-review-comments mob-review start-ticket happy-path create-pr`, run from the repo root, exits 0. Or, for each skill that still grows, this line names the growth and the text that causes it. Fix by location only: put "Consume a report" in its own small file that the readers load, and put each block that a skill reads on every run back inline where its `SKILL.md` stays at or under 10,000 B. Change no rule text. The gates are green.
  - Decision (user, D1): option B. Fix finding r1.1, and accept r1.2.
  - Decision: no new test and review round. Row r1.1 changes only file locations, so it changes no behaviour (`build/FIX-ROUND.md` item 3). The loop also stopped after step 29, the third review since approval.
  - Decision: row r1.2 stays open by the user's choice. A plain run of stand-up, pickup, create-verification-skill, and tdd loads about 400 to 840 B more. That is the cost of a merge, against 1,159 B less description load on every turn and five fewer skills.
  - Result (7ef92cb): apply-review 7,506 → 7,506 B per run, start-ticket 10,336 → 9,960, create-pr 10,030 → 9,983. The parse steps, start-ticket Step 8, and create-pr Step 1 items 3 to 8 are inline again, and `Consume a report` and `references/read.md` are gone. Three skills still grow. post-review-comments +6 B: the `/engineering:pickup --review` name of the review-pr merge. mob-review +1,036 B full and +473 B light: the Light column of PANEL.md (+678 B), the light-mode paragraph, and the `SCOPE.md` pointer. The scope commands stay in `SCOPE.md`, because inline they put `SKILL.md` at 10,497 B. The special cases are in `SCOPE-CASES.md` again, read only when a case is true. happy-path +916 B: the sad-mode description and paragraph, and the shared setup block and report inputs, now in `SKILL.md` in place of `QA-REPORT.md`. The repro script lists the old file names, so it still exits 1. With the file lists set to the reads at 7ef92cb it prints the numbers above.
- [ ] **31. Push.** Push-only: run `gh stack view --json`, then `git push -u origin pstack-34_pr-feedback-retro pstack-35_engineering-compress`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Progress

- 2026-11-19: plan written on `pstack-35_engineering-compress`. Playbook `new-ticket`. H2 passed: the user asked for a background run of the plan. Next step: 3 (`/build @.ai/plan_pstack-35.md`).
- Decision log: decisions_pstack-35.tsv
- 2026-11-19: step 1 done (1bc0bbc). Persona guard, unchanged-line, read-only, and generic output lines cut to `PERSONA-CONTRACT.md`; "Judge the hunks, not the file" now in contract Scope rule 4 and the PANEL.md header; the principle read-and-name line now in the domain `CLAUDE.md`; pstack attribution lines cut. Next step: 2.
- 2026-11-19: step 2 done (5eceed5). gazette, pick-next-task, tidy-up, sync-docs, and qa-screenshots have `disable-model-invocation: true` and a one-line description. No caller in `skills/` for any of the five. Next step: 3.
- 2026-11-19: step 3 done (36f3882). Terms swapped in benchmark, loop-until, constraints, code-simplify, persona-test-quality (and its persona-vitest pointer), resolve-conflicts, and interrogate. Six kept passages are in the decision log. Next step: 4.
- 2026-11-19: step 4 done (f5f297a). 258 `**Sources:**` lines cut from the value-display, url-state, text-input, and resilience catalogues (about 46,000 B). Each `###` heading and each Fix line stays, so the `/sad-path` heading list and Fix read of the text-input catalogue still work. Next step: 5.
- 2026-11-19: step 5 done (7768ebf). 129 restating sweep lines cut from four diff-signals files, and 17 form-behaviour lines moved into their rules. form-behaviour diff-signals 22,334 → 9,675 B; value-display 17,482 → 11,715; url-state 15,896 → 8,418; text-input 12,402 → 5,530. Next step: 6.
- 2026-11-19: step 6 done (2450c81). The Severity section is gone from all 38 personas and from comments `other-pr.md`. Each rule heading holds its tier and condition; Future and Never lines close What you review. The contract, domain `CLAUDE.md`, and update-personas name the new form. Next step: 7.
- 2026-11-19: step 7 done (b6a7ec9). api-integrity lookup in `references/backend-lookup.md` (SKILL.md 8,871 B); vitest rules 7 and 8 now test-quality Vitest sub-bullets with their tiers (vitest 6,962 B); boundary lines in ten Out of lane sections and PANEL.md Known overlaps. Next step: 8.
- 2026-11-19: step 8 done. Lane recall check: all five lanes pass, no revert. AC B holds. Next step: 9.
- 2026-11-19: step 9 done (17043e5). build 12,898 → 9,992 B. Fix round and the new-round rule in `FIX-ROUND.md`, Step 5 in `ANSWERS.md` behind a pointer, item 8 cut to the rule 1 line, and a few restated sentences cut. Next step: 10.
- 2026-11-19: step 10 done (aec4476). start-ticket 10,336 → 9,428 B. Step 7 keeps only what the plan template leaves open, Step 8 is in `references/inputs.md` behind a pointer, and Step 1 item 4 points to the `/refine-ticket` checks. The design note and the reviewer-yes line stay. Next step: 11.
- 2026-11-19: step 11 done (d0a4422). mob-review 10,464 → 9,213 B. Step 0 rationale is one line, the Step 1 commands are in `SCOPE-CASES.md` behind an each-run pointer, and the Notes bullet is cut. Next step: 12.
- 2026-11-19: step 12 done (b87bdcc). create-pr 10,030 → 8,605 B: Step 1 items 3 to 8 are in `references/read.md` behind an each-run pointer, and Step 5 item 7 drops the line that DRAFT-SCAN holds. work-on 8,834 → 8,553 B: H4 points to the `pause-list.md` rule. Next step: 13.
- 2026-11-19: step 13 done (ef79058). The prompt read, the `runs` parse, the run `meta` keys, and the `git -C` and `-R` rule are once in the Consume a report section of `mob-review/REPORT.md`. apply-review, post-review-comments, and the build fix round point to it and keep their own stops and row cells. resolve-feedback names it in its cell-change note. Next step: 14.
- 2026-11-19: step 14 done. Pointer trials: build and start-ticket no difference, mob-review a B win. No revert. Next step: 15.
- 2026-11-19: step 15 done (35d6d68). Principles 24 → 14. Five merged into their receiving principle as rule text, four folded into benchmark, prototype, tdd, and work-on, and foundational-thinking retired with its rules in model-the-domain and sequence-verifiable-units. All ten moved to `deprecated`. Each citer, the README table, CONTEXT.md, and the typescript-conventions rule source point to the new homes. Next step: 16.
- 2026-11-19: step 16 done (f73d285). Each principle index entry is its name and a trigger of at most ten words. Index 3,671 → 1,289 B; work-on 7,942 → 6,786 B. `check_principles.py` reads only the name, so no script change. Next step: 17.
- 2026-11-19: step 17 done (4e84a30). light-review is the `light` mode of mob-review: the arguments or a light or quick review request select `LIGHT.md`, and the Light column of PANEL.md lists the lanes. review, build, pickup, the domain CLAUDE.md, REPORT.md, and the README point to the mode. light-review is in `deprecated`. Next step: 18.
- 2026-11-19: step 18 done (f0c104d). sad-path is the `sad` mode of happy-path: the arguments or a sad-path, edge-case, or break-a-form request select `SAD.md`. `QA-REPORT.md` is in the shared-files table. test, build, fix, the domain CLAUDE.md, and the README point to the mode. sad-path is in `deprecated`. Next step: 19.
- 2026-11-19: step 19 done (1e00e47). maintain-verification-skill is the `maintain` mode of create-verification-skill: the arguments, a maintain or audit request, or a driver that fails because the app moved select `MAINTAIN.md`. verify, the README, and the create hand-over point to the mode. maintain-verification-skill is in `deprecated`. Next step: 20.
- 2026-11-19: step 20 done (fbf1496). pr-news is the news mode of stand-up: a time period, a PR news or review catch-up request, or a return from leave selects `NEWS.md`, which keeps the pr-news window, searches, in-window event rules for own PRs and review requests, per-repo tables, and quiet list. gazette and the README point to the mode. pr-news is in `deprecated`. Next step: 21.
- 2026-11-19: step 21 done (469a304). review-pr is the review mode of pickup: `--review` or a review-a-PR request selects `REVIEW.md`, which keeps the show-without-asking step, the claim, the stop on local commits, the panel run in the worktree, and the report pointer. review, PR-HANDLE.md, the domain CLAUDE.md, mob-review, post-review-comments, and the README point to the mode. review-pr is in `deprecated`. Next step: 22.
- 2026-11-19: step 22 done. All five trigger phrases reach their new mode, and the sad-mode trial is no difference. AC C and AC D hold. Next step: 23.
- 2026-11-19: step 23 done (f4209fe). No `SKILL.md` is over 10,000 B, and the three totals go down (see the step 23 line). engineering 4.0.0, deprecated 2.23.0, utility 1.28.0. The READMEs needed no change. Next step: 24.
- 2026-11-19: step 24 done. Every gate is green. AC E holds. Next step: 25.
- 2026-11-19: step 25 done (79bc8e0). Light panel: six lanes ran, and persona-skills ran in five shards. The fix commit puts back the principle read-and-name rule in nine skills, an inline H4 action list for a session with no pause-list rule, and working links in four retired copies. It also fixes two lane-routing drifts and drops the hard-coded principle count. No row stays open. Each `SKILL.md` is at most 10,000 B. Next step: 26.
- 2026-11-19: build round 2. The step 25 fix changes skill behaviour, so build rule 7.2 adds a new round: step 26 Test and step 27 Review. Push is now step 28. Next step: 26.
- 2026-11-19: step 26 done. Every gate is green after the step 25 fix. Next step: 27.
- 2026-11-19: step 27 done (25792c3). Light panel run 2: six lanes ran, and persona-skills ran in seven shards. The fix commit puts back ten sweep lines that lazy rule files did not cover, a retired principle rule, a principle read rule, and two persona tier conditions. It also makes the retired maintain-verification-skill find its script in the plugin cache, and fixes test-lane routing and Future-line rule drift. No row stays open. The fix changes skill behaviour, so build rule 7.2 applies. Next step: 28.
- 2026-11-19: build round 3. The step 27 fix 25792c3 changes skill behaviour (ten sweep lines back, a cache-safe script path, routing fixes), so build rule 7.2 adds step 28 Test and step 29 Review. Push is now step 30. Step 29 is the third review since approval. Next step: 28.
- 2026-11-19: step 28 done. Every gate is green after the step 27 fix. Next step: 29.
- 2026-11-19: step 29 done (fbbffe7). Light panel run 3: six lanes ran, and persona-skills ran in seven shards. The fix commit puts back twelve more sweep lines, the retired shared-state rule, the unused generic check, and two resolve-conflicts lines. It also finishes four step 27 fixes and corrects two tiers. No row stays open. The fix changes skill behaviour, but step 29 is the third review since approval, so the loop stops. Next step: 30.
- 2026-11-19: blast radius on `pstack-34_pr-feedback-retro...HEAD`, outside the diff. Verdict: **risk**.
  - Safety fact: outside the diff, no live file names a retired skill or principle, and no file makes the model call one of the five user-only skills, except one stale copy of a rule whose source the diff already fixes. The `xxkeefer-skills` marketplace is a directory source at this worktree, so an install ships the change. Rung 4: the script below exits 0, and exits 1 on any other hit.
  - Confirmed risk: `~/.claude/rules/typescript-conventions.md:210` names `principle-boundary-discipline`. The diff fixes the source in `install-rules`, but the installed copy changes only when `/install-rules` runs after the utility 1.28.0 update. Until then, each TypeScript edit loads a rule that points to a principle that engineering 4.0.0 does not ship (`deprecated` is not installed). Chance high, cost low: the agent cannot read the principle by path. Check: after the update, run `/install-rules`, then `grep -n 'principle-' ~/.claude/rules/typescript-conventions.md`.
  - Cleared: ADRs and done plans name the old skills as history. One open plan in another repo names a review skill under a plugin namespace that was already gone before this change. `skillOverrides` turns `pick-next-task` off, which still holds. Another marketplace and a work overlay ship their own `review-pr` and `pr-news` under their own namespace, and neither is installed. The installed primitives, meta, and scribe caches name no retired skill.
  - Command: `bash proof.sh`, with this script:

    ```bash
    #!/usr/bin/env bash
    set -u
    WT="$HOME/studio/code/pstack-inspiration"
    RET='light-review|sad-path|maintain-verification-skill|pr-news|review-pr|attack-the-premise|outcome-oriented-execution|migrate-callers-then-delete-legacy-apis|laziness-protocol|boundary-discipline|explain-the-number|exhaust-the-design-space|test-behavior-not-implementation|never-block-on-the-human|foundational-thinking'
    USR='gazette|pick-next-task|tidy-up|sync-docs|qa-screenshots'
    PAT="(^|[^a-z-])(/|engineering:|principle-|\`)($RET)([^a-z-]|$)"
    fail=0
    mp=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/plugins/known_marketplaces.json')))['xxkeefer-skills']['source']['path'])")
    [ "$mp" = "$WT" ] && echo "ok marketplace -> $mp" || { echo "FAIL marketplace -> $mp"; fail=1; }
    hits=$( { grep -rnIE "$PAT" ~/.claude/CLAUDE.md ~/.claude/AGENTS.md ~/.claude/rules ~/.claude/settings.json ~/.claude/hooks ~/.claude/tools ~/.claude/skills ~/.claude/output-styles ~/.claude/statusline.sh 2>/dev/null
      grep -rnIE "$PAT" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=claude-code-plugins --exclude-dir=.ai --exclude-dir="*-skills*" --exclude-dir=pstack-inspiration ~/studio/code 2>/dev/null
      grep -rnIE "$PAT" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.ai --exclude-dir=plans ~/studio/work 2>/dev/null
      grep -rnIE "^ *- \[ \].*$PAT" ~/studio/work/.ai ~/studio/work/plans ~/studio/code/.ai 2>/dev/null
      grep -rnIE "$PAT" --exclude-dir=.git --exclude-dir=.ai --exclude-dir=deprecated --exclude-dir=adr "$WT" 2>/dev/null; } | sort -u)
    expected="$HOME/.claude/rules/typescript-conventions.md:210:Principle: \`principle-boundary-discipline\`."
    while IFS= read -r h; do
      [ -z "$h" ] && continue
      if [ "$h" = "$expected" ]; then echo "known break: $h"; else echo "FAIL unexpected: $h"; fail=1; fi
    done <<< "$hits"
    d=$(diff ~/.claude/rules/typescript-conventions.md "$WT/skills/utility/skills/install-rules/rules/typescript-conventions.md" | grep -c '^[<>]')
    [ "$d" -le 2 ] && echo "ok installed rule differs from source by $d lines" || { echo "FAIL rule drift $d lines"; fail=1; }
    inv=$(grep -rnIiE "(run|invoke|call|use) .{0,20}($USR)" ~/.claude/CLAUDE.md ~/.claude/AGENTS.md ~/.claude/rules ~/.claude/hooks ~/.claude/tools ~/.claude/skills ~/.claude/statusline.sh 2>/dev/null; grep -rnIE "(/|engineering:)($USR)" --exclude-dir=.git --exclude-dir=.ai --exclude-dir=deprecated --exclude-dir=adr --exclude=README.md "$WT/skills" | grep -vE "skills/engineering/skills/($USR)/|engineering/CLAUDE.md|verify/SKILL.md|check_plan.py|fixtures/")
    [ -z "$inv" ] && echo "ok no model caller of a user-only skill" || { echo "FAIL caller: $inv"; fail=1; }
    exit $fail
    ```
- 2026-11-19: build stopped after step 29, the third review since approval (build rule 7). No row stays open. QA checklist skipped: the diff changes only skill text, docs, and check scripts. Playbook step 4: `/blast-radius` gives `risk` (the installed `~/.claude/rules/typescript-conventions.md` cites a retired principle until `/install-rules` runs), so `/interrogate` ran.
- 2026-11-19: `/interrogate` at 375633b: three adversaries, six findings, all reproduced, merged into two by root cause. Report `.ai/interrogate_pstack-35_engineering-compress.html`. No lost behaviour. Both findings say that some runs load more bytes. Stop H3 on D1. Next step: answer D1, then step 30.
- 2026-11-19: D1 answered: option B. Step 30 fixes r1.1 of the interrogate report. r1.2 stays open by the user's choice. Push is now step 31. Next step: 30.
- 2026-11-19: step 30 done (7ef92cb). Every-run blocks are inline again in apply-review, post-review-comments, the build fix round, start-ticket, create-pr, and happy-path. mob-review reads `SCOPE.md` on each run and `SCOPE-CASES.md` only for a special case. apply-review, start-ticket, and create-pr load no more than at the base. post-review-comments, mob-review, and happy-path still grow by the merge text that the step 30 line names. Next step: 31.

## Follow-ups

- The link check covers only `skills/engineering/`. A move into `deprecated` left dangling relative links that no gate found. Extend the check to `skills/deprecated/`, and make `/migrate-a-skill` repoint relative links on a move.
- The review panel has no rule for a very large patch. This run split one lane into shards by hand.
- The review panel writes the diff files to the system temp folder, and two trial runs found a lane that could not read them. Write them under `.ai/scratch/` of the repo.
- PANEL.md Known overlaps does not name test-design and test-quality. Both lanes flagged the same self-comparing test in every trial run.
- The comments lane flagged comments inside the generated review report under `.ai/`. Its guard should skip generated report files.
- The retired copies of light-review, review-pr, and sad-path link into the engineering plugin by relative paths. These links resolve in a repo checkout only, because each installed plugin has its own version folder. The step 27 fix covers the maintain-verification-skill script path only.
- The step 8 recall check did not cover url-state, text-input sweep lines in rule files that load on demand, or form-behaviour read-when triggers. Step 27 found ten sweep lines that the cut lost, and step 29 found twelve more. A script that lists each cut sweep line with no matching read-when trigger would find the rest.
