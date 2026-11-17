---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-11_verify-drivers
status: approved
goal: /create-verification-skill on a small app writes a driver that passes its own proof run, and /verify finds it from a diff.
spec: .ai/spec_pstack-11.md
---

# Plan: pstack-11 verify and the drivers

## Goal

Add `engineering/verify`, `engineering/create-verification-skill`, and
`engineering/maintain-verification-skill`. A driver is a plain skill that runs one app the way a
user does. `/verify` finds the drivers for a diff and runs them. The skills that must see a change
live call `/verify`. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-11.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `engineering/verify` → it reads the repo from `git remote`, finds the drivers from the diff paths with a script, runs each one, and returns `no driver` when none matches.
- [ ] **B.** Read `engineering/create-verification-skill` → it interviews the repo, writes a driver with the six sections and a feature map, picks the location by the owner rule, and proves the driver by one run before it hands it over.
- [ ] **C.** Read `engineering/maintain-verification-skill` → it keeps a driver and its feature map true to the app, with a source wave, a live pass, and the outcome `clean`, `changed`, or `blocked`.
- [ ] **D.** Read `/test`, `/interrogate`, `/blast-radius`, and `/qa-screenshots` → each calls `/verify` where it must see the change live. On `no driver`, the test step writes that in `Progress`, and `/retro` proposes `/create-verification-skill`.
- [ ] **E.** Run the layout check on a driver with a missing section → it exits 1 and names the section.
- [ ] **F.** Run `/create-verification-skill` on a small app, then `/verify` on a diff of that app → the driver passes its own proof run, and `/verify` finds it from the diff.

## Context

- Map: `.ai/map_pstack-program.md`, unit 11. Done line: `/create-verification-skill` on a small app writes a driver that passes its own proof run, and `/verify` finds it from a diff.
- Approval: the map (H0).
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-11_verify-drivers`. The home machine opens the PR into `pstack-inspired`.
- Sources: pstack `skills/create-verification-skill` (with `references/feature-map-example/`) and `skills/maintain-verification-skill`. A sparse clone is at `/tmp/pstack-src/plugins/pstack`. If it is gone, clone `https://github.com/cursor/plugins` again.
- Spec Intent: a driver `verify-<repo>-<app>` launches the app, drives it, and keeps the evidence. `/verify` is a thin router with no drive steps. Out of scope: `benchmark` (unit 24), a driver for this repo, and the pstack formal-verification skills.
- Spec Decisions:
  - Name: `verify-<repo>-<app>`, `<repo>` from `git remote get-url origin`. A library is driven as its consumer uses it.
  - Location: the user's own repo keeps its drivers in `.claude/skills/`, committed. Else `~/.claude/skills/`. A repo is the user's own when its remote owner is an owner that `~/.claude/AGENTS.md` names as the user's.
  - Paths: a driver's frontmatter holds `app-paths:`, a list of globs from the repo root. A script matches the diff paths against them.
  - `/verify` returns `no driver` on no match. The caller's test step writes that in `Progress`, and `/retro` proposes `/create-verification-skill`.
  - Driver layout: `SKILL.md` with Launch, Doctor, Drive, Evidence, Cleanup, Helpers. `features/README.md` indexes one file per feature, each with `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. A script checks the layout.
  - Drives run at the `verifier` role of the `models` block, else the session model.
  - No `disable-model-invocation` on the three skills.
  - `maintain-verification-skill` commits its fix on the agent's own branch, with a draft PR for a driver in the repo, or edits a driver in `~/.claude/skills/` in place.
- Production gate: none. The skills run only when the user types one or another skill calls `/verify`. With no driver, `/verify` returns `no driver`, so each caller keeps its current behaviour.
- Commit convention: conventional commits with the domain as scope, such as `feat(engineering): ...`. No Claude attribution line, by the user's global rule.
- Gates: `python3 skills/engineering/skills/verify/scripts/find_drivers.spec.py`, `python3 skills/engineering/skills/create-verification-skill/scripts/check_driver.spec.py`, `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, `python3 skills/engineering/skills/interrogate/scripts/rerun_findings.spec.py`, and `.githooks/pre-commit`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the driver match from the diff | H | new script, globs and two locations; a wrong match runs the wrong app or none |
| B | the create workflow and its location rule | M | prose, but a wrong location commits a driver into a team repo |
| C | the maintain workflow | L | prose, no caller depends on its words |
| D | the callers name `/verify` | L | prose, a few lines in each skill |
| E | the layout check | M | new script that `create` and `maintain` trust |
| F | a live create, then a match | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | a diff path that matches one driver's glob returns that driver | EP | Unit | `find_drivers.spec.py` |
| C2 | A | a diff path that matches no glob returns `no driver`, exit 0 | EP | Unit | `find_drivers.spec.py` |
| C3 | A | drivers in the repo's `.claude/skills/` and in the home skills folder are both found, and a driver for another repo is not | decision table | Unit | `find_drivers.spec.py` |
| C4 | A | the repo name comes from an SSH and an HTTPS remote URL, with and without `.git` | EP | Unit | `find_drivers.spec.py` |
| C5 | A | a driver with no `app-paths` key is not matched, and the output names it | error guessing | Unit | `find_drivers.spec.py` |
| C6 | E | a complete driver passes, exit 0 | EP | Unit | `check_driver.spec.py` |
| C7 | E | each missing `SKILL.md` section, a missing `features/README.md`, a feature file not in the index, and a missing feature H2 each exit 1 with the name | EP | Unit | `check_driver.spec.py` |
| C8 | E | a missing `name` or `app-paths` frontmatter key exits 1 | EP | Unit | `check_driver.spec.py` |
| C9 | B | the location rule, the six sections, the feature map, and the proof run are in the skill | review | Manual | the review step |
| C10 | F | a live run on a scratch app writes a driver that passes `check_driver.py` and its own proof run, and `find_drivers.py` finds it from a diff of the app | use case | Manual | step 3 |

### Not testing

- C (maintain) and D (callers): prose with no script. The review step reads them, by the TDD skip rule.

## Steps

- [x] **1. The `/verify` router.** Seam: `python3 skills/engineering/skills/verify/scripts/find_drivers.py --repo <root> --base <ref>`. Conditions: C1, C2, C3, C4, C5.
  - Write `find_drivers.spec.py` first, red. Then `find_drivers.py`: read the repo name from `origin`, list the diff paths against the base plus the working tree, search `<root>/.claude/skills/verify-<repo>-*/SKILL.md` and `~/.claude/skills/verify-<repo>-*/SKILL.md` (the home folder is an argument, so a test can give a temp folder), and print one driver path per line, or `no driver`. Then `verify/SKILL.md`: run the script, run each matched driver at the `verifier` role, and return the evidence paths or `no driver`. Add the skill to `skills/engineering/README.md` and to the composed-by table in `skills/engineering/CLAUDE.md`.
  - Done: `find_drivers.spec.py` covers C1 to C5 and passes. A user can run `/verify` on a branch and get `no driver` or a driver list.
- [x] **2. Create a driver.** Seam: `python3 skills/engineering/skills/create-verification-skill/scripts/check_driver.py <driver dir>`. Conditions: C6, C7, C8, C9.
  - Write `check_driver.spec.py` first, red. Then `check_driver.py`: frontmatter `name` and `app-paths`, the six `SKILL.md` sections, `features/README.md`, each feature file in the index, and the four H2s in each feature file. Each error names the file, the missing item, and the fix. Then `create-verification-skill/SKILL.md`, adapted from pstack, with the location rule and the check, and copy `references/feature-map-example/` in. Add the skill to the README.
  - Done: `check_driver.spec.py` covers C6 to C8 and passes, and the copied example feature map passes the feature part of the check.
- [x] **3. Run it.** Seam: `/create-verification-skill` on a scratch app. Conditions: C10.
  - Make a small CLI app in `/tmp/verify-demo`, a git repo whose `origin` owner is one that `~/.claude/AGENTS.md` names as the user's (no push). Follow `/create-verification-skill` there. Commit a change to the app, then run `find_drivers.py` on that diff. Record the commands and the results in Progress.
  - Done: the driver passes `check_driver.py` and its own proof run, its evidence survives its cleanup, and `find_drivers.py` prints its path from the diff.
- [x] **4. Maintain a driver.** Kind: docs.
  - `maintain-verification-skill/SKILL.md`, adapted from pstack: locate, index hygiene, source wave, reconcile, live pass, triage, ship or stop. The outcome is `clean`, `changed`, or `blocked`. It runs `check_driver.py`. The ship step follows the Spec Decision. Add the skill to the README.
  - Done: the skill holds every step and the three outcomes, and each relative path in it resolves.
- [x] **5. The callers.** Kind: docs.
  - `/test`: after `/happy-path`, run `/verify`, and on `no driver` write that in the plan's `Progress`. `/interrogate`: an adversary may prove a finding through `/verify`. `/blast-radius`: rung 5 runs `/verify`, and drop the sentence about no `/verify` skill. `/qa-screenshots`: when `/verify` has a driver, use it to reach each screen. `/retro`: a `no driver` line in `Progress` proposes `/create-verification-skill`. Add `verify` to the composed-by table.
  - Done: each of the five skills names `/verify`, and `grep -rn "no /verify skill" skills` finds nothing.
- [x] **6. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at HEAD 5bd14edc032ae66baa6c8bccfcc835f3cc706e5d. find_drivers 10 tests, check_driver 12, check_principles 11, map_units 14, rerun_findings 23, `.githooks/pre-commit` exit 0, `pre-commit_test.sh` and `commit-msg_test.sh` all ok.
- [ ] **7. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-11.md`. This step changes no code. Use `/engineering:mob-review`.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
- [ ] **8. Push.** Push the branch with `git push -u origin pstack-11_verify-drivers`. Push-only map: open no PR.
  - Done: the pushed SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-11.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-11.md`: one step per session, from the worktree.
- `/tdd`: steps 1 and 2.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-11_verify-drivers`.
- 2026-11-17: judgement calls that the unit does not decide:
  - The scope verdict came from the planner, with no `/scope-ticket` run. The unit is three skills, two scripts, and caller lines, which the map put in one unit.
  - The match and the layout check are scripts with tests, because both are deterministic and two skills depend on them (principle-encode-lessons-in-structure, map note r1.4).
  - `check_driver.py` lives in `create-verification-skill`. `maintain-verification-skill` runs it by a sibling path, so the check has one copy.
  - With no owner match, a driver goes in `~/.claude/skills/`. A wrong home folder costs a move, but a wrong repo folder commits a driver into a team repo.
  - The `benchmark` caller waits for unit 24, which adds that skill.
  - The proof run uses a scratch app in `/tmp`, because this repo has no app to drive.
- 2026-11-17: step 1 done in commit b92bcd1. `find_drivers.spec.py` has 10 tests and passes, and a mutation of the `*` glob made one test red. A driver with no `app-paths` key is named on stderr as `no app-paths: <path>`. `--home` sets the home skills folder. `verify/SKILL.md`, the README row, and the composed-by row are in. Callers join in step 5.
- 2026-11-17: step 2 done in commit be3d063. `check_driver.spec.py` has 12 tests and passes. A mutation that skips the section check made 6 tests red. The copied example feature map passes the check, and the check accepts any harness name in the `Driving it with` title. The README row is in. Next: step 3.
- 2026-11-17: step 3 done. No skill fix was needed. The scratch app is `/tmp/verify-demo` (a Python todo CLI, `TODO_FILE` sets the data file, `origin` is `git@github.com:xxKeefer/verify-demo.git`, no push). The owner rule put the driver in `/tmp/verify-demo/.claude/skills/verify-verify-demo-todo/` (committed there). Nothing went to `~/.claude/skills/`.
  - `check_driver.py <driver dir>`: `ok`, exit 0.
  - Proof run, from the repo root: Launch (`export TODO_FILE=$RUN/todo.json`, `python3 src/todo.py list` printed nothing, exit 0); Doctor (`scripts/doctor.sh` printed `doctor ok`, exit 0); Drive (`scripts/drive-add-list.sh /tmp/todo-verify-evidence/proof1` ran add, list, done, list, and every check passed); Cleanup (`rm -rf $RUN`, the run folder is gone). Evidence check after Cleanup: `transcript.txt` and `todo.json` (`[{"text": "buy milk", "done": true}]`) still exist in `/tmp/todo-verify-evidence/proof1`.
  - `find_drivers.py --repo /tmp/verify-demo --base main --home <empty temp folder>` on branch `change-app` (one commit to `src/todo.py`): printed `/tmp/verify-demo/.claude/skills/verify-verify-demo-todo/SKILL.md`. The same command on branch `docs-only` (one commit to `README.md`): printed `no driver`, exit 0.
  - Unproved by the stand-in: none, because the scratch app is the target.
- 2026-11-17: step 4 done in commit abedfd3. `maintain-verification-skill/SKILL.md` holds locate, index hygiene, source wave, reconcile, live pass, triage, and ship or stop, with the outcomes `clean`, `changed`, and `blocked`. It runs `check_driver.py` by a sibling path. A driver in the repo gets one commit and a draft PR through `/create-pr`. A driver in `~/.claude/skills/` gets an edit in place. The README row is in. Both relative paths resolve. The 7 gates that ran are green. Next: step 5.
- 2026-11-17: step 6 done. All gates green at 5bd14ed, no file changed except this plan. Next: step 7.
