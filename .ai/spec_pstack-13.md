---
doctype: spec
ticket: none
status: confirmed
goal: /checkpoint mid-step leaves a clean tree, and /do-next or /work-on resumes from the plan.
---

# Spec: /checkpoint

Unit 13 of `.ai/map_pstack-program.md` (r1.24). The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: `primitives/checkpoint` stops work at a safe point. It finishes or backs out the current step, makes one `wip:` commit, and writes the resume note as a `Progress` entry.
- User: the user, when a session must end before a step is done. The agent, when its context window is close to full.
- Why now: no skill owns a clean stop. `/update-plan` records progress but leaves edits uncommitted, so a fresh session can lose them (r1.24).
- Success: `/checkpoint` mid-step leaves a clean tree, and `/do-next` or `/work-on` resumes from the plan.
- Constraint: subtract before you add. `/checkpoint` adds no script and no template. It calls `/update-plan` for the note, and `/handoff` when no plan exists.
- Out of scope: a change to `/do-next` or `/work-on`. The retirement of `/handoff` or `/do-next` (the map defers moves to after the trial).

## Decisions

- Thin skill: `/checkpoint` owns only the stop and the `wip:` commit. `/update-plan` writes the note, because it already owns `Progress`.
- One trigger, one skill: the "context is about to blow out" trigger moves from the `/update-plan` description to `/checkpoint`.
- Dead fallback: `principle-guard-the-context-window` drops "If `/checkpoint` is not installed", because `engineering` depends on `primitives`.
- No push and no PR: a pause takes no action that another person reads (the pause rule).
- Name: `/checkpoint` (map, Domains and lifecycle).

## Acceptance criteria

- [ ] **A.** Read `/update-plan` and `principle-guard-the-context-window` → the context trigger is only in `/checkpoint`, and the fallback line is gone.
- [ ] **B.** Read `primitives/checkpoint` → it finishes or backs out the step, makes one `wip:` commit, writes the note through `/update-plan`, and pushes nothing.
- [ ] **C.** Run `/checkpoint` mid-step on a plan, then `/do-next` on the same plan → the tree is clean after `/checkpoint`, and `/do-next` continues the same step from the note.
