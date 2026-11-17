---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-12_decision-log-sitrep
status: approved
goal: After a /build, /sitrep lists the choices the agent made alone.
spec: .ai/spec_pstack-12.md
---

# Plan: pstack-12 the decision log and sitrep

## Goal

Add a decision log, `decisions_<KEY>.tsv` beside the plan, that `/build` writes through
`/update-plan`. Add `primitives/sitrep`, which shows the open decisions, the choices made alone,
the skipped steps, and the follow-ups of a plan. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-12.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Run `log_decision.py` on a plan with no log → it makes `decisions_<KEY>.tsv` beside the plan with the header row, appends the row, and prints the log path.
- [ ] **B.** Read `build` and its step brief → each step gives `/update-plan` each choice that the plan does not record, `/update-plan` appends each one with `log_decision.py`, and the plan's `Progress` links the log.
- [ ] **C.** Read `primitives/sitrep` → it lists every pending decision with the evidence, the risk, and the agent's pick, from the log, `Pending Decisions`, skipped steps, and `Follow-ups`.
- [ ] **D.** Run `/build` on a plan, then `/sitrep` → it lists the choices that the agent made alone.

## Context

- Map: `.ai/map_pstack-program.md`, unit 12. Done line: after a `/build`, `/sitrep` lists the choices the agent made alone.
- Approval: the map (H0).
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-12_decision-log-sitrep`. The home machine opens the PR into `pstack-inspired`.
- Spec Intent: each choice that the agent makes alone during a build goes into the log. `/sitrep` shows it with the open decisions, the skipped steps, and the follow-ups. Constraint: `primitives` depends on no other domain, and engineering skills reach a primitive only by its skill name. Out of scope: `/checkpoint` (unit 13), model escalation entries (unit 20), and a new doctype.
- Spec Decisions:
  - Name: `decisions_<KEY>.tsv` beside the plan, `<KEY>` from `plan_<KEY>.md`.
  - Columns: `decision`, `reason`, `evidence`, `result`, with one header row. A tab or a newline in a field becomes a space.
  - Writer: `skills/primitives/skills/update-plan/scripts/log_decision.py`. `/update-plan` appends each choice that its caller gives, and adds one `Progress` line that links the log, the first time.
  - `build` writes the log: each step subagent gives `/update-plan` its choices, and `/build` gives its own recorded decisions.
  - `primitives/sitrep` reads the plan and the log with a script, and gives the evidence, the risk, and the agent's pick for each item. It writes no file, and has no `disable-model-invocation`.
  - `/retro` reads the log, and compares each decision with its result.
- Production gate: none. A plan with no log behaves as before. `/sitrep` only reads.
- Commit convention: conventional commits with the domain as scope, such as `feat(primitives): ...`. No Claude attribution line, by the user's global rule. Change no `plugin.json` version (only unit 33 does).
- Gates: `python3 skills/primitives/skills/update-plan/scripts/log_decision.spec.py`, `python3 skills/primitives/skills/sitrep/scripts/sitrep.spec.py`, `python3 skills/primitives/skills/write-to-file/scripts/check_plan.spec.py`, `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, `.githooks/pre-commit`, `sh .githooks/pre-commit_test.sh`, and `sh .githooks/commit-msg_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the log path and the row format | H | new script, and `/sitrep` and `/retro` parse what it writes |
| B | the build writes the log | M | prose in three skills, and a missed choice makes `/sitrep` incomplete |
| C | the sitrep collection | H | new script that parses four parts of a plan and the log |
| D | a live build, then `/sitrep` | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | a plan with no log gets `decisions_<KEY>.tsv` beside it, with the header row and one row, and the script prints the log path | EP | Unit | `log_decision.spec.py` |
| C2 | A | a second call appends a row, and the header stays once | EP | Unit | `log_decision.spec.py` |
| C3 | A | a tab or a newline in a field becomes a space, so the row stays one line of four fields | error guessing | Unit | `log_decision.spec.py` |
| C4 | A | an empty field, or a plan whose name does not start with `plan_`, exits 1 and names the fault | EP | Unit | `log_decision.spec.py` |
| C5 | C | each open `D`, `B`, and `N` entry is listed with its options, its `Blocks` line, and the recommended option | EP | Unit | `sitrep.spec.py` |
| C6 | C | each row of the log is listed with its four fields | EP | Unit | `sitrep.spec.py` |
| C7 | C | each `[-]` step is listed with its `Skipped:` reason, and each `Follow-ups` item is listed | EP | Unit | `sitrep.spec.py` |
| C8 | C | a plan with no log and nothing open prints that nothing is pending, exit 0 | boundary | Unit | `sitrep.spec.py` |
| C9 | B | the step brief, `/build`, and `/update-plan` name the log and the script | review | Manual | the review step |
| C10 | D | a build step on a scratch plan logs a choice, and `/sitrep` lists it | use case | Manual | step 4 |

### Not testing

- The risk and the pick that `/sitrep` adds to each item: judgement in prose. Step 4 reads the output.

## Steps

- [x] **1. The decision log writer.** Seam: `python3 skills/primitives/skills/update-plan/scripts/log_decision.py <plan path> --decision <text> --reason <text> --evidence <text> --result <text>`. Conditions: C1, C2, C3, C4.
  - Write `log_decision.spec.py` first, red. Then `log_decision.py`, with the path rule and the row format in functions that `sitrep.py` can import. Then `update-plan/SKILL.md`: when the caller gives choices made with no user, append each one with the script, and add `- Decision log: decisions_<KEY>.tsv` to `Progress` once.
  - Done: `log_decision.spec.py` covers C1 to C4 and passes. A user can ask `/update-plan` to record a choice, and the log holds it.
- [x] **2. `/sitrep`.** Seam: `python3 skills/primitives/skills/sitrep/scripts/sitrep.py <plan path>`. Conditions: C5, C6, C7, C8.
  - Write `sitrep.spec.py` first, red. Then `sitrep.py`: it prints one section each for the open entries, the log rows, the skipped steps, and the follow-ups, and leaves out an empty section. It reads the log through `log_decision.py` by a sibling path. Then `sitrep/SKILL.md`: run the script, then give each item its evidence, its risk (H, M, or L, with the reason), and the agent's pick. Add the row to `skills/primitives/README.md`.
  - Done: `sitrep.spec.py` covers C5 to C8 and passes. A user can run `/sitrep` on a plan.
- [x] **3. The build writes the log.** Kind: docs.
  - `build/STEP.md` section 4: give `/update-plan` each choice that the step made and that the plan does not record, with the reason, the evidence, and the result. `build/SKILL.md`: give each recorded decision of Step 1 and Step 2 to `/update-plan` the same way, and name `/sitrep` in Step 4. `work-on/playbooks/map.md` step 3: give each judgement call to `/update-plan` as a choice. `retro/SKILL.md` Step 3: read the log beside the plan, and compare each decision with its result. `skills/engineering/CLAUDE.md`: name the log in the `build` row of the composed-by table.
  - Done: `grep -rn "decision log\|decisions_" skills` finds each of the five files, and each relative path resolves.
- [x] **4. Run it.** Seam: one step of `/build` on a scratch plan, then `/sitrep`. Conditions: C10.
  - Make a git repo in `/tmp/sitrep-demo` with a plan whose one docs step leaves a choice open, such as the wording of a file. Dispatch one fresh subagent on that step with `build/STEP.md`, as `/build` Step 2 does. Then run `/sitrep` on that plan. Record the commands and the output in Progress.
  - Done: the scratch plan's `Progress` links `decisions_<KEY>.tsv`, the log holds the choice, and `/sitrep` lists it with its evidence, risk, and pick.
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at HEAD d334c85. Tests: log_decision 5, sitrep 5, check_plan 33, check_principles 11, map_units 14. The pre-commit hook, `pre-commit_test.sh`, and `commit-msg_test.sh` pass.
- [x] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-12.md`. This step changes no code. Use `/engineering:mob-review`.
  - Done: the report is `.ai/review_pstack-12_decision-log-sitrep.html`. Reviewed: base 400344b, head 9d3fe88 (panel read a759e5d). The panel fixed all 4 findings in 9d3fe88, and none is open.
  - Recorded decision: the fix commit 9d3fe88 changes the behaviour of `sitrep.py`, so `/build` rule 7.2 adds a new round of test and review (steps 7 and 8).
- [x] **7. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at HEAD 2c0922a. Tests: log_decision 5, sitrep 7, check_plan 33, check_principles 11, map_units 14. The pre-commit hook, `pre-commit_test.sh`, and `commit-msg_test.sh` pass.
- [x] **8. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-12.md`. This step changes no code. Use `/engineering:mob-review`. Run 1 has no open row. Do not raise the rows of run 1 again.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
  - Result: the report is `.ai/review_pstack-12_decision-log-sitrep.html`, run 2. Reviewed: base 400344b, head a8757d8 (panel read faf296b). The panel fixed 1 finding in a8757d8. Row r2.1 stays open: `build/SKILL.md` is over 10 KB, and it was before this branch. The fix touched a test only, so rule 7.2 adds no new round.
- [x] **9. Review fix r1.1.** A build step commits only the plan, so the new decision log never enters git, at `skills/engineering/skills/build/STEP.md` section 4 item 4. Report: `.ai/interrogate_pstack-12_decision-log-sitrep.html`.
  - Done: STEP.md section 4 item 4 commits the decision log with the plan edit. Map playbook step 4 commits the log with the spec and the plan when the log exists.
- [x] **10. Review fix r1.2.** Callers give `/update-plan` choices that are already in the plan, and `/update-plan` says not to log those, at `skills/primitives/skills/update-plan/SKILL.md`. Report: `.ai/interrogate_pstack-12_decision-log-sitrep.html`.
  - Done: `/update-plan` logs each choice that the caller gives, and skips only a choice that the log already holds.
- [x] **11. Review fix r1.3.** `sitrep.py` drops the wrapped or nested lines of a Follow-ups bullet, at `skills/primitives/skills/sitrep/scripts/sitrep.py`. Report: `.ai/interrogate_pstack-12_decision-log-sitrep.html`.
  - Done: a Follow-ups item that wraps to more lines prints in full. A spec case covers it.
- [x] **12. Review fix r1.4.** `log_decision.py` cannot record a field value that starts with a dash, at `skills/primitives/skills/update-plan/scripts/log_decision.py`. Report: `.ai/interrogate_pstack-12_decision-log-sitrep.html`.
  - Done: `update-plan/SKILL.md` writes the command line in the `--field=value` form, and a spec case records a value that starts with a dash. `log_decision.py` also accepts a plan named `handoff_<KEY>.md`, with the log `decisions_<KEY>.tsv` (the blast-radius risk). A spec case covers it.
  - Recorded decision: rows r1.3 and r1.4 change runtime behaviour, so `/build` Step 1 item 1.3 adds a new round of test and review (steps 13 and 14). Every row of the interrogate run is ticked, so no row stays open.
- [x] **13. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at HEAD 24d6e87. Tests: log_decision 8, sitrep 8, check_plan 33, check_principles 11, map_units 14. The pre-commit hook, `pre-commit_test.sh`, and `commit-msg_test.sh` pass.
- [x] **14. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-12.md`. This step changes no code. Use `/engineering:mob-review`. Add this run as run 3 of `.ai/review_pstack-12_decision-log-sitrep.html`. Row r2.1 stays open. Do not raise the rows of runs 1 and 2 again, or a row that only repeats them.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
  - Result: the report is `.ai/review_pstack-12_decision-log-sitrep.html`, run 3. Reviewed: base 400344b, head 3fa230c. The panel found 1 Future finding (r3.1) and fixed none. Rows r3.1 and r2.1 stay open.
- [x] **15. Push.** Push the branch with `git push -u origin pstack-12_decision-log-sitrep`. Push-only map: open no PR.
  - Done: pushed `3799d7b` to `origin/pstack-12_decision-log-sitrep`.

## Suggested skills

- `/build @.ai/plan_pstack-12.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-12.md`: one step per session, from the worktree.
- `/tdd`: steps 1 and 2.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-12_decision-log-sitrep`.
- 2026-11-17: step 1 done in fc77509. `log_decision.py` and its spec are in `update-plan/scripts`, and `update-plan/SKILL.md` records choices.
- 2026-11-17: step 2 done in be3599c. `sitrep.py` and its spec, `sitrep/SKILL.md`, and the README row are in `primitives`.
- 2026-11-17: step 3 done in ef262bd. `STEP.md`, `build/SKILL.md`, `work-on/playbooks/map.md`, `retro/SKILL.md`, and `engineering/CLAUDE.md` name the decision log.
- 2026-11-17: judgement calls that the unit does not decide:
  - The scope verdict came from the planner, with no `/scope-ticket` run. The unit is two scripts, one new skill, and caller lines, which the map put in one unit.
  - `log_decision.py` lives in `update-plan`, not in `build`, because `/sitrep` in `primitives` must read the same format, and `primitives` depends on no other domain. Engineering skills already reach `/update-plan` by name.
  - The log has the four columns of the map and no step column. The evidence field names the step.
  - `/retro` reads the log in this unit, because the map's flow says so and no later unit adds it.
  - The map playbook's judgement calls also go to the log, so `/sitrep` shows them.
  - The live run uses a scratch plan in `/tmp`, so the proof does not depend on the choices of this unit's own build.
- Decision log: decisions_pstack-12.tsv
- 2026-11-17: the six judgement calls above went into the decision log after step 4, by map playbook step 3. The log did not exist at planning time.
- 2026-11-17: step 4 done. The live run needed one attempt, and no repo fix.
  - Commands: built `/tmp/sitrep-demo` (git repo, branch `demo-greeting`, plan `.ai/plan_DEMO-1.md`, one docs step with no wording set). `check_plan.py` on it printed `open decisions: 0`. One fresh general-purpose subagent ran step 1 with only the plan path, the step ID, the goal, and `build/STEP.md`. It was not told what to choose or that a log was expected.
  - Result of the subagent: `Status: done`, commits `c6635a6` (GREETING.md) and `e5e5f08` (`docs(ai): mark step 1 done`), tree clean.
  - Scratch plan `Progress` holds `- Decision log: decisions_DEMO-1.tsv`.
  - Log `decisions_DEMO-1.tsv` (header, then one row):
    - decision: Write GREETING.md as a short, friendly welcome of four lines that points to README.md
    - reason: The plan sets no wording, tone, or length. A short pointer serves the goal of welcoming a new reader.
    - evidence: Plan step 1 says the plan sets no wording, no tone, and no length.
    - result: GREETING.md has a heading, a welcome line, a pointer to README.md, and a line that invites questions.
  - `python3 skills/primitives/skills/sitrep/scripts/sitrep.py /tmp/sitrep-demo/.ai/plan_DEMO-1.md` printed one section, `## Choices made alone`, with that decision, reason, evidence, and result.
  - Judgement by `/sitrep` Step 2: Evidence: `/tmp/sitrep-demo/GREETING.md` (four lines, matches the result) and commit `c6635a6`. Risk: L, because the file is copy only and the plan left the wording open. Pick: keep, because it welcomes a new reader and points to `README.md`.
- 2026-11-17: step 5 done at d334c85. All eight gates green, and the step changed no file except this plan.
- 2026-11-17: step 6 done. Report `.ai/review_pstack-12_decision-log-sitrep.html`, base 400344b, head 9d3fe88 (panel read a759e5d). Fix commit 9d3fe88 holds 4 fixes, and no row is open. The gates stay green.
- 2026-11-17: step 7 done at 2c0922a. All eight gates green, and the step changed no file except this plan.
- 2026-11-17: step 8 done. Run 2 of the report, base 400344b, head a8757d8 (panel read faf296b). 1 finding fixed, 1 open (r2.1, nit). The gates stay green. Four panel choices went into the decision log.
- 2026-11-17: `/blast-radius` verdict: `risk`.
  - Safety fact: `log_decision.py` adds only `decisions_<KEY>.tsv` beside a `plan_*.md` plan, and does not change the plan. Rung 4. Command: a shell proof that copies this plan to a temp folder as `plan_X.md` and `handoff_Y.md`, runs the script on each, and checks the folder list, the plan hash, and the exit codes. Output: `PASS`.
  - Confirmed risk: `/do-next` and `/update-plan` accept a plan named `handoff_*.md`, but `log_decision.py` exits 1 on that name and writes no row (`log_decision.py:23`). A `/build` on a migrated `handoff_` plan loses each choice, and `update-plan/SKILL.md` does not say what to do on that exit. Chance: low, one such plan exists on this machine. Cost: the choices of that build are missing from `/sitrep`. Check: run the script on a `handoff_X.md` plan.
  - Cleared: a caller that gives no choices runs no log script, so `/do-next` and the vault plans keep their old behaviour. `sitrep.py` imports `check_plan.py` and `layout.py`, and the `sitrep.spec.py` gate covers a change to either. `check_plan.py` passes on a plan whose `Progress` links the log.
- 2026-11-17: step 9 done. `STEP.md` section 4 item 4 and map playbook step 4 commit the decision log.
- 2026-11-17: step 10 done. `/update-plan` logs each choice that the caller gives, and skips only a choice that the log holds.
- 2026-11-17: step 11 done. `sitrep.py` joins the wrapped and nested lines of a Follow-ups bullet, and a spec case covers it.
- 2026-11-17: step 12 done. `update-plan/SKILL.md` writes the flags as `--field=value`, `log_decision.py` accepts `handoff_<KEY>.md`, and two spec cases cover both.
- 2026-11-17: step 13 done at 24d6e87. All eight gates green, and the step changed no file except this plan.
- 2026-11-17: step 14 done. Run 3 of the report, base 400344b, head 3fa230c. 1 Future finding open (r3.1), 6 lanes clean. The gates stay green. Two panel choices went into the decision log.
- 2026-11-17: `/interrogate` kept 4 of 4 findings (report removed after the fix round, git history holds it). Steps 9 to 12 fixed them, and the blast-radius `handoff_` risk with r1.4. Steps 13 and 14 ran a third round. Review rows r2.1 (nit) and r3.1 (Future) stay open. `/ship` steps 1 to 3 gave go, and step 15 pushed the branch.
- 2026-11-17: `/work-on` map playbook, batch of unit 12. Steps 1 to 7 done. Stop: H5, the `/retro` offer (step 8). Next: the user runs `/retro` or says no, then `/work-on @.ai/map_pstack-program.md` starts unit 13 after the home machine merges this branch.
