---
doctype: spec
ticket: none
status: confirmed
goal: "A loop on a small metric stops at the predicate, with one log row per try."
---

# Spec: `loop-until`

## Intent

- Outcome: a new `engineering/loop-until` improves one measured number to a stated predicate. Each try is one change and one measure, then keep or revert. The harness is proven able to fail, then frozen. A plateau means a new approach. Each try writes one row to the decision log.
- User: the user, who wants a number moved to a target. `/build` loops test and review, but no skill loops to a metric target.
- Why now: map unit 22 (r1.9).
- Success: one loop on a small metric stops when the predicate holds, and the decision log has one row for each try.
- Constraint: adapt pstack's hillclimb and autonomous-run playbooks. Credit them in one line of prose. Everything-agnostic: no language, framework, or tool beyond the agent and git.
- Out of scope: a wake mechanism for an unattended run, parallel tries in worktrees, and a change to `/webperf`, which keeps its own steps.

## Decisions

- Source: pstack `poteto-mode/playbooks/hillclimb.md` and `autonomous-run.md`. Keep: a repro case first, one metric with a direction, a predicate with a target and a floor on tries, a harness proven to separate cases and then frozen, a baseline and a green regression gate before any change, one change per try, keep only past noise with the gate green, revert in full, one commit per kept try, a pivot on a plateau, and never relax the predicate. Drop: the hillclimb model name, the wake mechanism, and parallel worktrees.
- The decision log: the existing `decisions_<KEY>.tsv`, written through `/update-plan`, so that `/sitrep` and `/retro` read the tries. A loop with no plan first writes one with `/write-to-file`, doctype `plan`. The plan holds the frame: the metric, the harness command, the predicate, and the baseline.
- Each try runs in a fresh subagent at the `worker` role. The main thread measures, and keeps or reverts.
- Model-invoked, so the user can type it and a playbook can call it.

## Acceptance criteria

- [ ] **A.** Read `engineering/loop-until` → before any change, it names a repro case, one metric, the direction that is better, and a predicate with a target and a floor on tries.
- [ ] **B.** Read `engineering/loop-until` → it proves that the harness separates a contrast case from the target case, records the baseline and a green gate, then freezes the harness.
- [ ] **C.** Read `engineering/loop-until` → each try makes one change and measures it with the frozen harness. It keeps the change as one commit only past noise with the gate green, else reverts in full. Each try logs one row either way.
- [ ] **D.** Read `engineering/loop-until` → a run of rejected tries makes it change approach, it stops only on the predicate or a surfaced dead end, and it never relaxes the predicate.
- [ ] **E.** Run `loop-until` on a small metric → it stops at the predicate, with one log row per try.
