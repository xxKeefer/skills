---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-10_blast-radius
status: approved
goal: On a change, the blast-radius output names the rung reached and the command that proved it.
spec: .ai/spec_pstack-10.md
---

# Plan: pstack-10 blast-radius

## Goal

Add `engineering/blast-radius`: find what a change can break outside its diff, prove by a run the
one fact that makes it safe, and give a one-word verdict. `/work-on` runs it after the build loop,
and runs `/interrogate` on the verdict `risk`. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-10.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read `engineering/blast-radius` → it holds the five-rung ladder, finds the one safety fact, looks where a symbol search stops, and lists the confirmed and the cleared risks.
- [ ] **B.** Read the output step → it gives the verdict, the safety fact with its rung and the command that proved it, the risks, the cleared list, and the cheapest check before a merge. With a plan path, the result goes in the plan's Progress.
- [ ] **C.** Read the `/work-on` playbooks → the blast-radius step has no skip reason, and runs `/interrogate` on the verdict `risk`.
- [ ] **D.** Run `/blast-radius` on a change → the output names the rung reached and the command that proved it.

## Context

- Map: `.ai/map_pstack-program.md`, unit 10. Done line: on a change, the output names the rung reached and the command that proved it.
- Approval: the map (H0).
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-10_blast-radius`. The home machine opens the PR into `pstack-inspired`.
- Spec Intent: find what a change can break outside its diff, prove the one safety fact by a run, and list what was cleared. The skill applies no fix. Out of scope: `/verify` (unit 11) and the comment ladder (unit 19).
- Spec Decisions:
  - Source: pstack `skills/blast-radius`. Its `arena` step goes, because `/interrogate` holds the panel.
  - No `disable-model-invocation`, because `/work-on` calls the skill.
  - The skill runs at the `prover` role of the `models` block: `opus` at high effort.
  - Rung 5 runs through `/verify` when the repo has a driver. Until `/verify` exists, rung 4 is the top rung.
  - Verdict `risk`: a confirmed risk exists, or the safety fact is below rung 4. Verdict `clear`: the safety fact is at rung 4 or 5, and no confirmed risk exists.
  - With a plan path, the result goes in the plan's `## Progress` through `/update-plan`. With no plan, it goes in the reply only. The skill writes no other file.
- Production gate: none. The skill runs only when the user types it or `/work-on` calls it.
- Commit convention: conventional commits with the domain as scope, such as `feat(engineering): ...`. No Claude attribution line, by the user's global rule.
- Gates: `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, `python3 skills/engineering/skills/interrogate/scripts/rerun_findings.spec.py`, and `.githooks/pre-commit`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the ladder and the search past grep | M | prose, but a weak ladder gives proofs that are only said |
| B | the output and the verdict | M | `/work-on` branches on the verdict word |
| C | the `/work-on` step | L | prose, a two-line change |
| D | a live run names the rung and the command | H | the done line of the unit |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A, B | the ladder, the safety fact, the risks, the verdict rule, and the plan write | review | Manual | the review step |
| C2 | C | both playbooks run `/interrogate` on `risk`, with no skip reason | review | Manual | the review step |
| C3 | D | a run of the skill on the unit 9 change names the rung and the command, and the command exits 0 on a re-run | use case | Manual | step 3 |

### Not testing

- No unit test. The skill adds no script, so the closest real check is a live run (C3), by the TDD skip rule.

## Steps

- [x] **1. The blast-radius skill.** Kind: docs.
  - Add `skills/engineering/skills/blast-radius/SKILL.md`, adapted from pstack. Steps: read the change, find the one safety fact, look where a symbol search stops, rate each risk, prove the safety fact by a run, give the verdict, then write the output. The ladder has the five rungs. Name **principle-prove-it-works** with its sibling path. Add the skill to `skills/engineering/README.md` and to the composed-by table in `skills/engineering/CLAUDE.md`.
  - Done: `SKILL.md` holds every Spec Decision, the README and the composed-by table list `blast-radius`, and each principle path resolves.
- [x] **2. The `/work-on` step.** Kind: docs.
  - In `work-on/playbooks/new-ticket.md` and `work-on/playbooks/map.md`, remove the skip reason from the blast-radius step, and run `/interrogate` when the verdict is `risk`.
  - Done: both playbooks name the verdict `risk`, and neither holds `skipped: no /blast-radius skill`.
- [x] **3. Run it.** Seam: `/blast-radius` on the unit 9 change, `git diff 428f956 7e49a7f -- skills/engineering/skills/interrogate/scripts/rerun_findings.py`. Conditions: C3.
  - Follow the skill with no plan path. Record the verdict, the safety fact, the rung, and the command in Progress, then run the command again.
  - Done: Progress names the rung and the command, and the command exits 0 on a re-run.
- [ ] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-10.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **6. Push.** Push the branch with `git push -u origin pstack-10_blast-radius`. Push-only map: open no PR.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-10.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-10.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-10_blast-radius`.
- 2026-11-17: judgement calls that the unit does not decide:
  - The scope verdict came from the planner, with no `/scope-ticket` run. The unit is one skill and two playbook lines.
  - The skill adds no script. The verdict rule is two lines, and a script for it would add a layer with one caller (principle-laziness-protocol). The proof is a live run in step 3 (principle-prove-it-works).
  - The output goes in the plan's Progress, not in a new `findings` file, so `/interrogate` reads it from the plan that it already takes, and `.ai/` gets no extra file.
  - The `arena` step of pstack goes, because `/work-on` runs `/interrogate` on `risk`.
- 2026-11-17: step 1 done in 1b89ccc. Added `blast-radius/SKILL.md`, the README row, and the composed-by row. Gates green.
- 2026-11-17: step 2 done in 158a4c9. Dropped the skip sentence from both playbooks, and they run `/interrogate` when the verdict is `risk`. Gates green.
- 2026-11-17: step 3 done. Live run of `/blast-radius` on `git diff 428f956 7e49a7f -- skills/engineering/skills/interrogate/scripts/rerun_findings.py` (the unit 9 re-run script), with no plan path.
  - Verdict: `risk`, because one confirmed risk exists.
  - Safety fact: `rerun_findings.py` keeps a finding only when its command exits non-zero on re-run and its evidence text is in the output. It drops every other finding, and it exits 0.
  - Rung: 4 (ran it). The proof script `/tmp/br-proof/prove.py` calls the real script with 7 findings (fail with evidence, pass, evidence missing from output, no evidence field, no command, bad cwd, timeout). It exits 1 unless only the first finding is kept. A mutant (`proc.returncode == 0` check removed) made it exit 1.
  - Command: `python3 /tmp/br-proof/prove.py skills/engineering/skills/interrogate/scripts/rerun_findings.py` (run from the repo root). First run: exit 0. Re-run: exit 0.
  - Confirmed risk R1: the `--timeout` is not enforced when a command leaves a child in a new session (`setsid`) that holds the output pipe. `proc.communicate()` in the timeout branch (`rerun_findings.py`, after `os.killpg`) waits for EOF on the pipe, and `killpg` does not reach the child. A command with `--timeout 1` took 8 s. A child that never exits hangs `/interrogate`. Chance: low (a finding command seldom daemonises). Cost: a stuck run. Check: run the script on a finding whose command forks a `setsid` child with `sleep 8`, and time it.
  - Cleared: callers (only `interrogate/SKILL.md` lines 21 and 71); the file has no change after 7e49a7f; a malformed findings file (exits 1 with a message); a negative exit code from a signal (counts as a failure, correct); output encoding (`errors="replace"`).
  - Follow-up (not fixed in this unit): R1. Close the pipe or use `communicate(timeout=...)` with a kill of the whole tree, or do not wait on the pipe after the kill, in `rerun_findings.py`.
