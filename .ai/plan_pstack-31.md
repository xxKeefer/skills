---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-31_findings-report
status: approved
goal: "`/diagnose` writes a findings file that passes the check."
spec: .ai/spec_pstack-31.md
builds_on: pstack-30
---

# Plan: pstack-31 `findings` and `report` layouts

## Goal

`primitives/write-to-file` gets a `findings` template and a findings check. `primitives/write-report` gets a check for the JSON `runs` block. `engineering/diagnose` and the `squash-bugs` subagent write findings files in the new layout. Scope: SCOPED, one PR: two scripts with their tests, one template, and three skill text edits.

## Spec

`.ai/spec_pstack-31.md`. This plan builds all of it, and adds AC F.

## Acceptance criteria

- [x] **A.** Ask `/write-to-file` for a `findings` file → it writes the file from a `findings` template, then runs the findings check and gives its result to the caller.
- [x] **B.** Run the findings check on a findings file → it passes a file in the template layout, and fails a file with a missing header key or section, with the line and a fix.
- [x] **C.** Run the report check on a report HTML file → it passes a file whose `runs` block has the `/write-report` shape, and fails a file whose block is missing, does not parse, or breaks the shape, with the problem and a fix.
- [x] **D.** Run `/diagnose` to the end of its hunt → it writes `findings_<KEY>.md` in the findings layout, not the old hunt layout.
- [x] **E.** Run `/diagnose` on a bug, then run the findings check on its file → the check passes.
- [x] **F.** A `squash-bugs` subagent writes its hunt doc → the file is in the findings layout, keeps its verdict line, and passes the findings check.

## Context

- Map: `.ai/map_pstack-program.md`, unit 31. Done line: `/diagnose` writes a findings file that passes the check.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-30_text-diagrams`, because the unit 20 to 30 PRs are not merged. The home machine sets the unit 31 PR base to that branch. Keep the unit 20 to 30 `.ai/` files.
- Intent: see the spec. A `findings` file holds a question, its answer, the evidence, and open points. It replaces the `hunt`, `spike`, `risks`, and `research` files.
- Decisions: File types (map). Five parsed layouts plus `scratch`. Each markdown layout keeps its header in YAML frontmatter. `report` is HTML with a JSON `runs` block, written by `/write-report`.
- Findings layout: header keys `doctype` (`findings`), `ticket`, and `status`. Status values: `open` (no proven answer yet), `answered`, and `consumed` (a fix or a plan used it). Required sections, in this order: `## Question`, `## Answer`, `## Evidence`, `## Open points`. Each required section has a body: text, or the word `none`. A writer can add more `## ` sections after `## Open points`, such as `## Ruled out` or `## Fix direction`. The file has no `goal` key, because the question is in the body.
- Findings check: `skills/primitives/skills/write-to-file/scripts/check_findings.py <path>`. It uses `layout.py`, as `check_spec.py` does. Each error prints as `<path>:<line>: <problem>. Fix: <fix>.` The last line is `open points: <n>`, the count of `- ` items under `## Open points`. A section whose body is only `none` counts 0. Exit 1 on any error, else 0. It checks the header keys, the doctype, the status, the four sections, their order, and an empty section body.
- Report check: `skills/primitives/skills/write-report/scripts/check_report.py <path>`. It prints `ok` and exits 0, or prints one line for each error, `<path>: <problem>. Fix: <fix>.`, and exits 1. It checks what `template.html` and the prompt readers use: the block exists and parses; top keys `title` (string), `path` (string), `skill` (string), `runs` (list); each run has an integer `run`, a string `title`, `date`, and `answer`; the run numbers are unique and in falling order; a run with rows has `columns`, each with `key` and `label`; each row has a string `id` that is unique in the file, and a `cells` object; `ticks`, when given, is a list of strings. It reuses the `BLOCK` pattern of `write_report.py` by copying the one regex line, because `write_report.py` runs `main()` on import.
- `write-report` Step 3 runs the report check after `write_report.py`. On exit 1, fix the temp JSON and run both again.
- `diagnose` Step 4: the template becomes the findings layout. Map the old sections: Report → `## Question` (the symptom, the confidence, and the reporter's read). Root Cause → `## Answer` (one-line root cause, location, what happens, why). Evidence → `## Evidence`. Then `## Open points` (what the hunt could not prove, and the blast radius items still to check). Keep `## Ruled out` and `## Fix direction` as added sections after `## Open points`. An unproven cause gets `status: open`, and its Answer starts with `Hypothesis:`. The fixer sets `status: consumed`, in place of deleting the file at once. Keep the rule that the consumer deletes the file: it marks it `consumed`, and `.ai/` clean-up deletes it. Drop the old `**Status:** active | consumed` line. Rename "hunt doc" and "Hunt Artifact" to "findings file" in `diagnose/SKILL.md`, including the description.
- `squash-bugs/BUG.md` step 6: the same layout. `**Verdict:** ...` stays as the first line of `## Answer`, so the parent check "holds the same verdict" still reads it. Symptom → `## Question`. Root cause → `## Answer`. The spec run and the code path → `## Evidence`. `## Open points` holds what a `decision` or `blocked` verdict needs. `## Fix`, `## Risk`, and `## Decisions` stay as added sections. Keep the words "hunt doc" in `squash-bugs`: they name the role, and the doctype is `findings`.
- `write-to-file/SKILL.md`: the `findings` row names `templates/findings.md`. Add the findings check beside the plan and spec checks, with the `open points: <n>` line in place of the open count. Add a `## Check a findings file` section, as `## Check a spec`. The `report` row says `/write-report` writes it and names its check.
- Defect hotspots: none recorded for this repo.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-31_findings-report`. Run no `gh` command.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`, `python3 skills/primitives/skills/write-to-file/scripts/check_findings.spec.py`, `python3 skills/primitives/skills/write-to-file/scripts/check_spec.spec.py`, `python3 skills/primitives/skills/write-report/scripts/check_report.spec.py`, and `python3 skills/primitives/skills/write-report/scripts/write_report.spec.py`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | `/write-to-file` writes a findings file from the template and runs the check | L | skill text and one template |
| B | the findings check passes a good file and fails a bad one | H | new logic, with section order and empty-body edge cases |
| C | the report check passes a written report and fails a bad block | H | new logic, and three skills parse the block it guards |
| D | `/diagnose` writes the findings layout | L | skill text |
| E | a `/diagnose` file passes the check | M | behaviour that an agent must follow. A text read cannot prove it. |
| F | a `squash-bugs` hunt doc is in the findings layout and keeps its verdict | M | the parent reads the verdict line, and the check now runs on the file |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | the template, filled, passes, and prints `open points: <n>` with the item count | EP | Unit | `test_template_layout_passes` |
| C2 | B | each missing header key, a wrong doctype, and a bad status fail with a line and a fix | EP | Unit | `test_header_errors` |
| C3 | B | a missing section, sections out of order, and an empty section body each fail with a line | EP | Unit | `test_section_errors` |
| C4 | B | an added section after `## Open points` passes, and `none` counts 0 open points | BVA | Unit | `test_added_section_and_none` |
| C5 | C | a report that `write_report.py` writes, with two runs, passes | EP | Unit | `test_written_report_passes` |
| C6 | C | no block, a block that does not parse, and a missing top key each fail | EP | Unit | `test_block_errors` |
| C7 | C | a duplicate row ID, a run number out of order, rows with no `columns`, and a row with no `cells` each fail | EP | Unit | `test_shape_errors` |
| C8 | E | a fresh agent follows `diagnose/SKILL.md` on a seeded bug, and the check passes on its file | EP | Manual | the live run in step 5 |
| C10 | C | a re-run on a report whose runs are stored oldest first writes the runs newest first, and the report check passes | EP | Unit | `test_rerun_sorts_runs_newest_first` |
| C9 | F | a fresh agent follows `BUG.md` step 6 on the same bug, and the check passes, with the verdict as the first line of `## Answer` | EP | Manual | the live run in step 5 |

### Not testing

- A, D: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The findings layout.** Seam: the `check_findings.py` command line. Conditions: C1, C2, C3, C4. Write the tests first and see them fail. Then write `templates/findings.md` and `scripts/check_findings.py` by the findings layout and the findings check in Context. Update `write-to-file/SKILL.md` as Context says.
  - Done: `check_findings.spec.py` adds the four tests in the Conditions table, and each passes. A and B hold.
- [x] **2. The report check.** Seam: the `check_report.py` command line. Conditions: C5, C6, C7. Write the tests first and see them fail. Then write `write-report/scripts/check_report.py` by the report check in Context. Add the check to `write-report` Step 3.
  - Done: `check_report.spec.py` adds the three tests in the Conditions table, and each passes. C holds.
- [x] **3. `diagnose` writes findings.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. Edit `diagnose/SKILL.md` as Context says. Update the `diagnose` row in `skills/engineering/CLAUDE.md` when its words change.
  - Done: D holds on a read, and the pre-commit test passes.
- [x] **4. `squash-bugs` writes findings.** Kind: docs. Edit `squash-bugs/BUG.md` step 6 as Context says.
  - Done: the step 6 template is in the findings layout, and the verdict is the first line of `## Answer`. The pre-commit test passes.
- [x] **5. Live run.** Kind: config. Conditions: C8, C9. In a temp git repo, seed a small bug with a clear root cause. Give one fresh agent `diagnose/SKILL.md` and the bug report, and tell it to stop after Step 4. Give a second fresh agent `BUG.md` step 6 and the same bug, with the verdict `fixed`. Run the findings check on each file. Copy the result in short form into this Done line.
  - Done: E and F hold. Each file passes the check.
  - Result: seeded bug: `cart.py` divides a discount by 10, not 100. A fresh agent on `diagnose/SKILL.md` wrote `findings_save15-charges-zero.md`, `status: answered`. The check printed `open points: 2`, exit 0. The agent also found that the seeded report gave the wrong charge (0.0, not -50.0), and logged it as an open point. A fresh agent on `BUG.md` step 6 wrote `findings_bug-1.md`. The check printed `open points: 0`, exit 0, and `**Verdict:** fixed` is the first line of `## Answer`. A re-run of the check in this thread gave the same results.
- [x] **6. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. All seven gates exit 0 on 33e8e8b.
- [x] **7. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-31.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: report `.ai/review_pstack-31_findings-report.html`, base 85bb3a5, reviewed head 8154bd2 (panel read c91c6aa). Four findings fixed, two open (a `consumed` setter in `fix`, and small test gaps).
- [x] **8. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. All seven gates exit 0 on c8d6ba4.
- [x] **9. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-31.md`. This step changes no code. Run `/engineering:light-review` with these lanes only: test-design, code-quality, and skills, which raised findings in run 1, and correctness, whose guard matches the scripts that 8154bd2 changed. Rows r1.1 (the `consumed` setter in `fix`) and r1.2 (small test gaps) stay open from run 1: do not raise them again, or a row that only repeats them.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: report `.ai/review_pstack-31_findings-report.html`, run 2, base 85bb3a5, reviewed head e620966 (panel read 0bf61e6). Three findings fixed, none open.
- [x] **10. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. All seven gates exit 0 on 67d5fec.
- [x] **11. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-31.md`. This step changes no code. Run `/engineering:light-review` with these lanes only: correctness and code-quality, which raised findings in run 2, and test-design, whose guard matches the spec file that e620966 changed. Rows r1.1 (the `consumed` setter in `fix`) and r1.2 (small test gaps) stay open from run 1: do not raise them again, or a row that only repeats them. This is the third review step: the build loop stops after it.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: report `.ai/review_pstack-31_findings-report.html`, run 3, base 85bb3a5, reviewed head c199831 (panel read 899d50f). Three findings fixed, none open.
- [ ] **12. Blast-radius fix: sort the runs.** Seam: the `write_report.py` command line. Conditions: C10. `write_report.py` keeps earlier runs in their stored order, and two real reports store them oldest first. A re-run then writes `[3, 1, 2]`, and the new report check fails on a block that the agent cannot fix from its temp JSON. Write the test first and see it fail: an existing report with runs 1 and 2, oldest first, gets a re-run, and the file then holds runs 3, 2, 1 and passes `check_report.py`. Then sort every run by `run`, newest first, in `write_report.py`. Keep each earlier run unchanged apart from its place.
  - Done: `write_report.spec.py` adds `test_rerun_sorts_runs_newest_first`, which fails before the fix and passes after it. The blast-radius proof script in Progress exits 0.
- [ ] **13. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **14. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-31.md`. This step changes no code. Run `/engineering:light-review` with the correctness and test-design lanes only, on the step 12 change to `write_report.py` and its spec. Rows r1.1 and r1.2 stay open from run 1: do not raise them again.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **15. Push.** Push-only map: run `git push -u origin pstack-31_findings-report`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-31.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-31.md`: one step per session, from the worktree.
- `/tdd`: steps 1 and 2.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-30_text-diagrams`, for the branch `pstack-31_findings-report`.
- Decision log: decisions_pstack-31.tsv
- 2026-11-18: playbook `map`, step 3: plan status `approved`, four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `check_findings.py`, its four tests, `templates/findings.md`, and the `write-to-file` text. Mutation check went red.
- 2026-11-18: step 2 done: `check_report.py`, its three tests, and the `write-report` Step 3 text. Mutation check went red.
- 2026-11-18: step 3 done: `diagnose/SKILL.md` Step 4 is the findings layout, and the `engineering/CLAUDE.md` row says findings file.
- 2026-11-18: step 4 done: `BUG.md` step 6 is the findings layout, with the verdict as the first line of `## Answer`.
- 2026-11-18: step 5 done: both live-run files pass the findings check. Next: step 6, the gates.
- 2026-11-18: step 6 done: the seven gates each exit 0. Next: step 7, review.
- 2026-11-18: step 7 done: light review, four fixes in 8154bd2, two open rows in the report. Next: step 8, push.
- 2026-11-18: build loop rule 7.2: review fix 8154bd2 changes how `check_findings.py` reads a section body, so steps 8 (Test) and 9 (Review) are a new round. Push is now step 10. Next: step 8.
- 2026-11-18: step 8 done: the seven gates each exit 0. Next: step 9, review round 2.
- 2026-11-18: step 9 done: light review round 2, three fixes in e620966, none open. Next: step 10, push.
- 2026-11-18: build loop rule 7.2: review fix e620966 changes how `check_findings.py` strips comments, so steps 10 (Test) and 11 (Review) are a third round, the last that the loop allows. Push is now step 12. Next: step 10.
- 2026-11-18: step 10 done: the seven gates each exit 0. Next: step 11, review round 3.
- 2026-11-18: step 11 done: light review round 3, three fixes in c199831, none open. The build loop stops here. Next: step 12, push.
- 2026-11-18: build loop stopped after the third review step (step 11). No row is open from runs 2 and 3. Rows r1.1 (Nit: no skill sets `status: consumed`) and r1.2 (Future: small test gaps) stay open from run 1. QA report `.ai/qa_pstack-31_findings-report.html` (ab32e68): 12 agent rows pass. Its push row is not run: the push is playbook step 6. Next: playbook step 5, `/blast-radius`.
- 2026-11-18: `/blast-radius`: verdict `risk`. Safety fact: every report that `write_report.py` writes passes `check_report.py`, because `write-report` Step 3 now runs the check after each write. Rung 4, and false. The check passed 42 of 44 real reports on the build machine. The 2 that fail store their runs oldest first (1, 2). A re-run keeps that order behind the new run (3, 1, 2), so the check fails, and the agent cannot fix earlier runs from its temp JSON. Confirmed risk: `skills/primitives/skills/write-report/scripts/write_report.py:56` (`data["runs"] = [new_run] + earlier`). Chance: medium, for each re-run on an old report. Cost: the report skill loops on a check that it cannot pass. Clear fix: sort the runs newest first in `write_report.py`, added as step 12. Cleared: `squash-bugs` still reads `**Verdict:**` and `## Decisions`, which the findings layout keeps (`BUG.md` step 6). Cleared: only `write-to-file` and `write-report` run the new checks. No hook and no CI runs `*.spec.py` by a glob. Cleared: an old hunt doc in flight is checked only after a write, and the writer then moves it to the new layout. Proof, from the repo root (exit 1 before step 12, exit 0 after it):
  ```
  python3 - <<'EOF'
  import json, os, subprocess, sys, tempfile
  d = "skills/primitives/skills/write-report/"
  tpl = open(d + "template.html").read()
  old = {"title": "R", "path": "", "skill": "", "runs": [
      {"run": n, "title": "Light run", "date": "2026-11-17", "answer": "a", "columns": [{"key": "k", "label": "K"}],
       "rows": [{"id": f"r{n}.1", "cells": {"k": "x"}}]} for n in (1, 2)]}
  tmp = tempfile.mkdtemp()
  rep = os.path.join(tmp, "review_x.html")
  open(rep, "w").write(tpl.replace('{"title": "Report", "path": "", "skill": "", "runs": []}', json.dumps(old)))
  run = os.path.join(tmp, "run.json")
  json.dump({"title": "R", "skill": "", "run": {"title": "Light run", "answer": "a", "columns": [{"key": "k", "label": "K"}], "rows": [{"cells": {"k": "y"}}]}}, open(run, "w"))
  w = subprocess.run(["python3", d + "scripts/write_report.py", rep, run], capture_output=True, text=True)
  c = subprocess.run(["python3", d + "scripts/check_report.py", rep], capture_output=True, text=True)
  print("write exit", w.returncode, "| check exit", c.returncode, "|", c.stdout.strip().split(": ", 1)[-1])
  sys.exit(c.returncode)
  EOF
  ```
  Output now: `write exit 0 | check exit 1 | run numbers are not unique and in falling order. Fix: number the runs, newest first.`, exit 1. Next: `/build` runs step 12.
