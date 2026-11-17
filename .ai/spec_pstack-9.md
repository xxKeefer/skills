---
doctype: spec
ticket: none
status: confirmed
goal: On a branch with a planted bug, the interrogate report keeps the proven finding and drops an unproven one.
---

# Spec: interrogate

Unit 9 of `.ai/map_pstack-program.md` (r1.1). The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: `engineering/interrogate` sends adversaries to break a change. A finding stays in the report only when a re-run of its command proves it. Each other finding goes to a Dropped list.
- User: the user, who gets only proven findings, and `/work-on`, which runs the skill after the build loop when `blast-radius` finds risk.
- Why now: every persona lane is read-only, so no review finding is proven by a run (r1.1).
- Success: on a branch with a planted bug, the report keeps the proven finding and drops an unproven one.
- Constraint: the re-run check is a script, not agent judgement (r1.4 user note). The skill applies no fix.
- Out of scope: `blast-radius` (unit 10) and `/verify` (unit 11). The text names them as they will be.

## Decisions

- Source: pstack `skills/interrogate`, MIT licence, adapted to this repo. pstack's `arena` phases go inline, because this repo has no `arena` skill.
- The skill is callable by the model, with no `disable-model-invocation`: `/work-on` calls it (map decision: the HITL line is on actions, not skills).
- The adversaries use the `panel` role of the `models` block: one adversary each on `opus` high, `sonnet` high, and the session model.
- Each adversary works in its own git worktree, with the scope's uncommitted changes copied in (`principle-separate-before-serializing-shared-state`).
- An adversary returns each finding as JSON: a title, a command, and an evidence line from the output of its own run. A finding with no command is dropped.
- `scripts/rerun_findings.py` re-runs each command in the adversary's worktree. It keeps a finding when the command exits non-zero and its output holds the evidence line. It drops the rest, each with a reason.
- After the script, the agent drops a kept finding whose failure does not break the intent, and merges kept findings that share a root cause.
- The report is one `/write-report` report, kind `interrogate`. Its rows are the kept findings, with ticks that build a `/engineering:fix` prompt. The Dropped list holds the count and the reason for each adversary.
- `/work-on` runs `/interrogate` after the build, before `/ship`, when `/blast-radius` reports risk. Until `/blast-radius` exists, the step is skipped with that reason.

## Acceptance criteria

- [ ] **A.** Read `engineering/interrogate` → it frames the scope and the intent, fans out panel adversaries in their own worktrees, and gives each one the break-this brief.
- [ ] **B.** Run `rerun_findings.py` on a findings file → a finding whose command fails with its evidence line is kept, each other finding is dropped with its reason, and only commands that can be run again are kept.
- [ ] **C.** Read the report step → kept findings are rows with the command, the output, the intent they break, and the adversaries that found them. The Dropped list gives a count and a reason for each adversary.
- [ ] **D.** Read the `/work-on` playbooks → `/interrogate` runs after the build loop when `blast-radius` finds risk, with the panel models.
- [ ] **E.** Run `/interrogate` on a branch with a planted bug → the report keeps the proven finding and drops an unproven one.
