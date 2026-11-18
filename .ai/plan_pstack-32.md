---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-32_script-audit
status: approved
goal: "The script audit report exists, with rows to tick."
spec: .ai/spec_pstack-32.md
builds_on: pstack-31
---

# Plan: pstack-32 Script audit

## Goal

One HTML report lists each skill step where a new script saves time or tokens, or makes a result deterministic, and each existing script that does neither. The user ticks the rows to build or delete in a later unit. Scope: SCOPED, one PR: one report file. No script and no skill changes.

## Spec

`.ai/spec_pstack-32.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read the audit report → it has one row for each skill step where a new script saves time or tokens, or makes a result deterministic, and each row names which of the two it gives.
- [x] **B.** Read the audit report → it has one row for each existing script that gives neither, with the reason, so the user can tick it for deletion.
- [x] **C.** Run the report check on the audit report → it passes, and each row has a tick box.

## Context

- Map: `.ai/map_pstack-program.md`, unit 32. Done line: the report exists, with rows to tick.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-31_findings-report`, because the unit 20 to 31 PRs are not merged. The home machine sets the unit 32 PR base to that branch. Keep the unit 20 to 31 `.ai/` files.
- Decisions: Scripts (map). A script earns its place only when it saves time or tokens, or when its result must be deterministic. A judgement that a model already makes well gets no script. The unit 19 comment scanner is the example: the reviewer read the diff better, so the scanner went. `principle-build-the-lever` holds the same test.
- Decisions: File types (map). `report` is HTML with a JSON `runs` block and rows to tick, written by `/write-report`.
- Report: `/write-report`, kind `audit`, key `pstack-32_script-audit`, so the file is `.ai/audit_pstack-32_script-audit.html`. The repo's Working files rule puts every doctype in `.ai/` of this worktree, so the report travels with the branch to the home machine. `skill` is `/engineering:spec`, because a ticked row is the input to a later spec. Each row has `ticks: ["build"]` (a new script) or `ticks: ["delete"]` (an existing script).
- Report columns: `kind` (`Build` or `Delete`), `where` (mono: the skill step as `<path>:<line>`, or the script path), `what` (the script to build, or what the script does now), `gives` (`time or tokens`, `deterministic`, both, or `neither`), `why` (the evidence: the repeated work, the callers, or why a model does the job as well), and `cost` (S, M, or L for a build row).
- Actionable only: the report lists no keep row. An existing script that earns its place gets no row. The run `answer` gives the counts: scripts read, delete rows, skill steps read, build rows. One folded `table` visual lists the scripts kept, with the one word that earns each its place, so the user can check the coverage.
- Existing scripts: each `*.py`, `*.sh`, and `*.js` under `skills/` and `.githooks/`, outside `deprecated/`, that is not a test (`*.spec.py`, `*_test.py`, `*_test.sh`). A delete row needs a read of the script and a search for its callers in every Markdown file and hook. A script with no caller is a delete row only when no skill names its path.
- Build candidates: a skill step that repeats the same mechanical work on each run, such as a parse, a count, a version bump, a table sync, a schema check, or a file move, where a model wastes tokens or can give a different result each time. The map names three examples: report schema checks, the version bump, and the skill table sync. A step that needs judgement is not a candidate. Read `skills/engineering/skills/principle-build-the-lever/SKILL.md` before the sweep.
- Fan-out: the sweep reads about 180 `SKILL.md` files and 30 scripts. Send read-only subagents, one for each domain and one for the scripts. Each returns rows in the column shape above, with `file:line` for each claim. The step thread checks each delete row's caller search itself before it writes the row.
- Defect hotspots: none recorded for this repo.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. The unit adds one `.ai/` file. No skill loads it.
- Push-only map: the push step runs `git push -u origin pstack-32_script-audit`. Run no `gh` command.
- Commit convention: conventional commits with the domain as scope, `docs(ai)` for `.ai/`. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`, and `python3 skills/primitives/skills/write-report/scripts/check_report.py .ai/audit_pstack-32_script-audit.html`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | each build row names a real repeated step and what a script gives | M | a judgement over 180 files. A missed step or a weak row costs a later unit, not a break. |
| B | each delete row is a script that gives neither | M | a wrong row invites the deletion of a script that a skill runs |
| C | the report passes the check, and each row has a tick box | L | `/write-report` runs the check |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | each delete row names its caller search and its result, and a re-run of that search in the step thread gives the same result | EP | Manual | the caller search in step 1 |
| C2 | A, B | the run answer counts match the rows, and every existing script is in a delete row or in the kept table | EP | Manual | a count in step 1 |
| C3 | C | `check_report.py` prints `ok`, and every row has a `ticks` list | EP | Integration | the report check gate |

### Not testing

- A: the quality of each build row. The review step reads each row against the Scripts decision.

## Steps

- [x] **1. The script audit report.** Kind: docs. Conditions: C1, C2, C3. Read `principle-build-the-lever` and the Scripts decision. Send the fan-out in Context. Check each delete row's caller search in this thread. Write the report with `/write-report` as Context says.
  - Done: `.ai/audit_pstack-32_script-audit.html` exists, `check_report.py` prints `ok`, and the counts in the run answer match the rows. A, B, and C hold.
  - Result: `.ai/audit_pstack-32_script-audit.html`, run 1. 13 build rows and 1 delete row (`prompt_boolean.js`), each with a tick. The kept table lists 42 scripts, so 43 scripts in total. The four sweeps read 63 skill files. `check_report.py` prints `ok`. A re-run of the `prompt_boolean` caller search in this thread found the same six hits and no caller.
- [x] **2. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. All four gates exit 0 on c6e1ab0.
- [ ] **3. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-32.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **4. Push.** Push-only map: run `git push -u origin pstack-32_script-audit`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-32.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-32.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-31_findings-report`, for the branch `pstack-32_script-audit`.
- Decision log: decisions_pstack-32.tsv
- 2026-11-18: playbook `map`, step 3: plan status `approved`, four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 ran in the build thread, not in a step subagent, because its fan-out needs subagents and no agent starts an agent of its own. The sweep added `scripts/obsidian/scripts/*.js` to the existing scripts, because they are scripts in the repo outside `skills/`. Next: step 2, the gates.
- 2026-11-18: step 2 done: the four gates each exit 0. Next: step 3, review.
