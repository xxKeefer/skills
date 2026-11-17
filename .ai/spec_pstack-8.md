---
doctype: spec
ticket: none
status: confirmed
goal: /work-on on a task names the principle that shaped a choice, and the principle's file was read in that session.
---

# Spec: principles and the TDD skip rule

Unit 8 of `.ai/map_pstack-program.md` (r1.2). The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: the 24 pstack `principle-*` skills live in `engineering`, `/work-on` indexes them, and `engineering/tdd` has the skip rule.
- User: the user, who can type a principle on a smell, and the agent, which reads a principle before it cites it.
- Why now: the map orders this unit after `/work-on` and the models block, which the index and the skip rule build on.
- Success: a `/work-on` reply names the principle that shaped a choice, and that principle's `SKILL.md` was read in the same session.
- Constraint: the principles stay skills with `disable-model-invocation: true`, not a rule file, so they cost no context (r1.2 user note).
- Out of scope: the `/verify` router and its drivers (unit 11), and `/checkpoint` (unit 13). The adapted principles name them as they will be.

## Decisions

- Take all 24 pstack `principle-*` skills, with pstack's names, into `engineering`: the map's Principles decision.
- Each principle keeps `disable-model-invocation: true`: it costs no context, and the user can type it on a smell.
- `/work-on` holds an inline index in pstack's five groups (Core, Architecture, Verification, Delegation, Meta), with one "when it applies" line each: the map's Principles decision.
- The agent reads a principle's `SKILL.md` by path when it applies it. A skill that runs without the router names its principles in bold, with a sibling path such as `../principle-fix-root-causes/SKILL.md`.
- The reply names each principle that shaped a decision, and cites only a principle it read in this session.
- Adapt two: `principle-never-block-on-the-human` points at the pause list, and `principle-guard-the-context-window` points at subagents and `/checkpoint`.
- TDD by default. Skip a test only when it would be expensive, integration-heavy, or unclear, and use the closest real check instead (`/verify` when the repo has a driver). A skip is never silent: the plan step stays, marked skipped with its reason, and `/sitrep` shows it: the map's TDD decision.

## Acceptance criteria

- [ ] **A.** List the `principle-*` skills in `engineering` → 24 skills with pstack's names, each with `disable-model-invocation: true`, and the two adapted principles point at the pause list, and at subagents and `/checkpoint`.
- [ ] **B.** Read `/work-on` → an inline index in the five groups, one "when it applies" line per principle, the reply rule, and the "read it first" rule.
- [ ] **C.** Read `engineering/tdd` → the skip rule: the three skip reasons, the closest real check, and a skipped step that stays in the plan with its reason.
- [ ] **D.** Type `/principle-fix-root-causes` → the skill runs, and no rule file holds the principles.
- [ ] **E.** Run `/work-on` on a task → the reply names the principle that shaped a choice, and the principle's file was read in that session.
