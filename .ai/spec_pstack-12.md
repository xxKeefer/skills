---
doctype: spec
ticket: none
status: confirmed
goal: After a /build, /sitrep lists the choices the agent made alone.
---

# Spec: the decision log and /sitrep

Unit 12 of `.ai/map_pstack-program.md` (r1.8, r1.26). The user approved the map at H0, so this
spec is confirmed.

## Intent

- Outcome: each choice that the agent makes during a build with no user goes into a decision log, `decisions_<KEY>.tsv`, beside the plan. `/sitrep` shows the open decisions, the choices made alone, the skipped steps, and the follow-ups.
- User: the user, during a run and after it. `/retro` also reads the log after the PR.
- Why now: a choice that the agent makes alone is now only prose in `Progress`, if anywhere. No skill collects these choices, so the user cannot check them in one view (r1.8).
- Success: after a `/build`, `/sitrep` lists the choices that the agent made alone.
- Constraint: `primitives` depends on no other domain. Engineering skills ask a primitive by name and never run a primitives script by path.
- Out of scope: `/checkpoint` (unit 13). Model escalation entries (unit 20). A new doctype in `/write-to-file`.

## Decisions

- Name: `decisions_<KEY>.tsv` beside the plan. `<KEY>` is the plan file name after `plan_`, so `plan_pstack-12.md` gives `decisions_pstack-12.tsv`.
- Columns: decision, reason, evidence, result, with one header row. A tab or a newline in a field becomes a space, so each row stays one line.
- Writer: `scripts/log_decision.py` appends each row. It lives in `primitives/update-plan`, because `/update-plan` already records each step, and engineering skills reach primitives only by skill name.
- `build` writes the log: each step subagent gives `/update-plan` each choice that the plan does not record, and `/build` gives its own recorded decisions. `/update-plan` adds one `Progress` line that links the log, the first time it writes a row.
- `primitives/sitrep` (new) reads the plan and the log with a script. It shows every open entry under `Pending Decisions`, each row of the log, each skipped step, and each `Follow-ups` item. For each item it gives the evidence, the risk, and the agent's pick.
- Name (r1.26): `sitrep`.
- `/sitrep` has no `disable-model-invocation`, so another skill can call it. It writes no file. It only reads.
- `/retro` reads the log, compares each decision with its result, and proposes a skill edit for a decision whose result went wrong (map flow).

## Acceptance criteria

- [ ] **A.** Run `log_decision.py` on a plan with no log → it makes `decisions_<KEY>.tsv` beside the plan with the header row, appends the row, and prints the log path.
- [ ] **B.** Read `build` and its step brief → each step gives `/update-plan` each choice that the plan does not record, `/update-plan` appends each one with `log_decision.py`, and the plan's `Progress` links the log.
- [ ] **C.** Read `primitives/sitrep` → it lists every pending decision with the evidence, the risk, and the agent's pick, from the log, `Pending Decisions`, skipped steps, and `Follow-ups`.
- [ ] **D.** Run `/build` on a plan, then `/sitrep` → it lists the choices that the agent made alone.
