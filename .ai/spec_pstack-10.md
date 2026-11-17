---
doctype: spec
ticket: none
status: confirmed
goal: On a change, the blast-radius output names the rung reached and the command that proved it.
---

# Spec: blast-radius

Unit 10 of `.ai/map_pstack-program.md` (r1.3). The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: `engineering/blast-radius` finds what a change can break outside its diff. It proves by a run the one fact that makes the change safe, and lists what it cleared.
- User: the user, before a merge of a diff they do not trust, and `/work-on`, which runs it after the build loop and runs `/interrogate` when it reports risk.
- Why now: `persona-production-protector` reasons only from the static diff, so no review proves a safety claim by a run (r1.3).
- Success: on a change, the output names the rung reached and the command that proved it.
- Constraint: the skill applies no fix. The ladder has five rungs: said it, pointed at the line, walked it, ran it, saw it live.
- Out of scope: `/verify` (unit 11) and the comment ladder (unit 19). The text names `/verify` as it will be.

## Decisions

- Source: pstack `skills/blast-radius`, adapted to this repo. Its `arena` step goes, because `/work-on` runs `/interrogate` on risk, and `/interrogate` holds the panel.
- The skill is callable by the model, with no `disable-model-invocation`: `/work-on` calls it (map decision: the HITL line is on actions, not skills).
- The skill runs at the `prover` role of the `models` block: `opus` at high effort.
- Rung 5, "saw it live", runs through `/verify` when the repo has a driver. Until `/verify` exists, rung 4 is the top rung that the skill can reach.
- The verdict is one word. `risk`: a confirmed risk exists, or the safety fact is below rung 4. `clear`: the safety fact is at rung 4 or 5, and no confirmed risk exists.
- With a plan path, the skill records its result in the plan's `## Progress` through `/update-plan`: the verdict, the safety fact, the rung, the command, and each confirmed risk. With no plan, the result goes in the reply only. The skill writes no other file.

## Acceptance criteria

- [ ] **A.** Read `engineering/blast-radius` → it holds the five-rung ladder, finds the one safety fact, looks where a symbol search stops, and lists the confirmed and the cleared risks.
- [ ] **B.** Read the output step → it gives the verdict, the safety fact with its rung and the command that proved it, the risks, the cleared list, and the cheapest check before a merge. With a plan path, the result goes in the plan's Progress.
- [ ] **C.** Read the `/work-on` playbooks → the blast-radius step has no skip reason, and runs `/interrogate` on the verdict `risk`.
- [ ] **D.** Run `/blast-radius` on a change → the output names the rung reached and the command that proved it.
