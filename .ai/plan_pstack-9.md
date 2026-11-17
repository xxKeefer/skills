---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-9_interrogate
status: approved
goal: On a branch with a planted bug, the interrogate report keeps the proven finding and drops an unproven one.
spec: .ai/spec_pstack-9.md
---

# Plan: pstack-9 interrogate

## Goal

Add `engineering/interrogate`: adversaries try to break a change, a script re-runs each finding's
command, and only a proven finding stays in the report. `/work-on` runs it after the build loop
when `blast-radius` finds risk. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-9.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `engineering/interrogate` → it frames the scope and the intent, fans out panel adversaries in their own worktrees, and gives each one the break-this brief.
- [ ] **B.** Run `rerun_findings.py` on a findings file → a finding whose command fails with its evidence line is kept, each other finding is dropped with its reason, and only commands that can be run again are kept.
- [ ] **C.** Read the report step → kept findings are rows with the command, the output, the intent they break, and the adversaries that found them. The Dropped list gives a count and a reason for each adversary.
- [ ] **D.** Read the `/work-on` playbooks → `/interrogate` runs after the build loop when `blast-radius` finds risk, with the panel models.
- [ ] **E.** Run `/interrogate` on a branch with a planted bug → the report keeps the proven finding and drops an unproven one.

## Context

- Map: `.ai/map_pstack-program.md`, unit 9. Done line: on a branch with a planted bug, the report keeps the proven finding and drops an unproven one.
- Approval: the map (H0).
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-9_interrogate`. The home machine opens the PR into `pstack-inspired`.
- Spec Intent: adversaries try to break a change, and a finding stays only when a re-run of its command proves it. The re-run check is a script (r1.4 user note). The skill applies no fix. Out of scope: `blast-radius` (unit 10) and `/verify` (unit 11). The text names them as they will be.
- Spec Decisions:
  - Source: pstack `skills/interrogate`, MIT licence. pstack's `arena` phases go inline. `skills/engineering/PSTACK-LICENSE` already holds the notice.
  - No `disable-model-invocation`, because `/work-on` calls the skill.
  - Adversaries use the `panel` role: `opus` high, `sonnet` high, and the session model.
  - Each adversary works in its own git worktree, with the scope's uncommitted changes copied in.
  - An adversary returns findings as JSON: `title`, `command`, `evidence`. No command means dropped.
  - `scripts/rerun_findings.py` keeps a finding when its command exits non-zero and the output holds the evidence line. It drops the rest with a reason.
  - The agent then drops a kept finding that does not break the intent, and merges findings with one root cause.
  - One `/write-report` report, kind `interrogate`. Rows are the kept findings, and ticks build a `/engineering:fix` prompt. The Dropped list has a count and a reason for each adversary.
  - `/work-on` runs `/interrogate` after the build and before `/ship`, when `/blast-radius` reports risk. Until `/blast-radius` exists, the step is skipped with that reason.
- Production gate: none. The skill runs only when the user types it or `/work-on` calls it, and the `/work-on` step is skipped until `/blast-radius` exists.
- Commit convention: conventional commits with the domain as scope, such as `feat(engineering): ...`. No Claude attribution line, by the user's global rule.
- Gates: `python3 skills/engineering/skills/interrogate/scripts/rerun_findings.spec.py`, `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, and `.githooks/pre-commit`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill frames, fans out, and briefs | M | prose, but a wrong brief gives unproven findings |
| B | the re-run keeps or drops each finding | H | the whole value of the skill rests on this check |
| C | the report shape | L | `/write-report` owns the layout |
| D | the `/work-on` step | L | prose, skipped until unit 10 |
| E | a planted bug is kept, an unproven finding is dropped | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a command that exits non-zero with the evidence line in its output is kept | EP | Unit | `rerun_findings.spec.py` |
| C2 | B | a command that exits 0 is dropped with reason `passed on re-run` | EP | Unit | `rerun_findings.spec.py` |
| C3 | B | a non-zero exit without the evidence line is dropped with reason `evidence not in output` | EP | Unit | `rerun_findings.spec.py` |
| C4 | B | a finding with no command or no evidence is dropped with reason `no command` or `no evidence`, and a command over the timeout is dropped with `timed out` | BVA | Unit | `rerun_findings.spec.py` |
| C5 | E | in a temp git repo with a planted bug, a failing-test finding is kept and a finding whose test passes is dropped | use case | Integration | `rerun_findings.spec.py` |
| C6 | A, C | the brief, the panel, the worktrees, and the report shape | review | Manual | the review step |
| C7 | E | a live `/interrogate` run on a planted-bug branch | use case | Manual | the user, after the trial |

### Not testing

- D: prose. The review step reads it.
- C7 needs a live panel of subagents. A subagent build cannot spawn the panel, so the user checks it in the trial. C5 proves the keep and drop rule on the same shape.

## Steps

- [x] **1. The re-run script.** Seam: `python3 skills/engineering/skills/interrogate/scripts/rerun_findings.py <findings.json>`, which prints JSON `{"kept": [...], "dropped": [...]}` and exits 0, or exits 1 with one error line for a malformed file. Conditions: C1, C2, C3, C4, C5.
  - Write `rerun_findings.spec.py` first, with fixtures in a temp folder, then `rerun_findings.py`. Input: a JSON list of findings, each with `adversary`, `title`, `command`, `evidence`, and `cwd`. The script runs each command through the shell in its `cwd`, with a timeout (`--timeout`, default 120 seconds). A kept finding gets its `output` and `exit`. A dropped finding gets its `reason`. C5 builds a temp git repo with a planted bug and its tests.
  - Done: `rerun_findings.spec.py` covers C1 to C5 and passes, and a user can run the script on a findings file.
  - Recorded decision: a finding whose `cwd` folder does not exist is dropped with the reason `cwd not found`, so that the script never stops on one bad finding.
- [x] **2. The interrogate skill.** Kind: docs.
  - Add `skills/engineering/skills/interrogate/SKILL.md`, adapted from pstack. Steps: frame the scope and the intent, fan out the panel adversaries in their own worktrees with the brief, collect each adversary's findings JSON, run `rerun_findings.py`, drop a kept finding that does not break the intent and merge findings with one root cause, write the report with `/write-report` (kind `interrogate`, `skill` `/engineering:fix`), then remove the worktrees. Name **principle-prove-it-works** and **principle-separate-before-serializing-shared-state** with sibling paths. Add the skill to `skills/engineering/README.md`.
  - Done: `SKILL.md` holds every Spec Decision, the README lists `interrogate`, and each principle path resolves.
  - Recorded decision: the first line of `PSTACK-LICENSE` now names the `interrogate` skill too, because it named only the principles.
- [x] **3. The `/work-on` step.** Kind: docs.
  - Add a step to `work-on/playbooks/new-ticket.md` after `/build`, and to `work-on/playbooks/map.md` between the build and `/ship`: run `/interrogate @<plan path>` when `/blast-radius` reports risk. When `/blast-radius` does not exist, mark the step skipped with that reason. Its stop: H3, only when a kept finding has no fix step.
  - Done: both playbooks hold the step, and the step numbers in each playbook and in `work-on/SKILL.md` still match.
  - Recorded decision: `skills/engineering/CLAUDE.md` gets an `interrogate` row in the composed-by table, and the `fix` row names the `interrogate` report as a caller.
- [x] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. At `633666d`: `rerun_findings.spec.py` 15 tests OK, `check_principles.spec.py` 11 tests OK, `map_units.spec.py` 14 tests OK, `.githooks/pre-commit` exit 0.
- [ ] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-9.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
- [ ] **6. Push.** Push the branch with `git push -u origin pstack-9_interrogate`. Push-only map: open no PR.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-9.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-9.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:mob-review`: the review step.
- `/create-pr`: not in a push-only map.

## Progress

- 2026-11-17: plan written on `pstack-9_interrogate`.
- 2026-11-17: judgement calls that the unit does not decide:
  - The scope verdict came from the planner, with no `/scope-ticket` run. The unit is one skill, one script, and two playbook lines.
  - The keep rule is mechanical: a non-zero exit and the evidence line in the output. The intent check stays with the agent, because a script cannot judge intent (principle-build-the-lever).
  - The `/work-on` step names `/blast-radius` as it will be, and is skipped until unit 10 lands.
  - The report ticks build a `/engineering:fix` prompt, because interrogate applies no fix.
  - The cleanup commit `0a4b4b8` deletes the unit 8 files and fixes three stale map lines, at the user's request.
- 2026-11-17: `/build` ran steps 1 to 4. Commits: `d4cd57b` (step 1, TDD: 15 tests red, then green, and a mutation check on the exit and evidence rules), `6ea2a53` (step 2), `633666d` (step 3). Step 4 changed no file.
