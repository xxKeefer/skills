---
doctype: spec
ticket: none
status: confirmed
goal: "`/sharpen` on a prompt returns a deeper version."
---

# Spec: `sharpen`

## Intent

- Outcome: a new skill, `primitives/sharpen`, rewrites a prompt to go deeper, not wider. It asks what a top professional would do, the rawest material they would start from, their methods and tools, and what outside proof would show the result is right. Then it rewrites the prompt to ask for exactly that.
- User: the user, before they hand a task to an agent. The skill is user-only.
- Why now: map unit 25 (r1.15).
- Success: `/sharpen` on a prompt returns a deeper version of that prompt.
- Constraint: everything-agnostic. The skill is short, about ten lines of method, and names no tool product. Credit the pstack source in one line of prose.
- Out of scope: a call from any other skill, and a change to `grill`.

## Decisions

- Adapt pstack's `sharpen`: its four questions and its rewrite rule. The rewritten prompt asks the agent to prototype a choice that an experiment can settle, and leaves product or preference choices to the user.
- The skill is user-only: it keeps `disable-model-invocation: true`, as pstack has it and as the map unit says.
- The skill lens differs from `grill`. `grill` asks the user questions about a plan. `sharpen` rewrites a prompt with no questions to the user.

## Acceptance criteria

- [ ] **A.** Read `primitives/sharpen/SKILL.md` → it is a new user-only skill with `disable-model-invocation: true`, and it rewrites a prompt to go deeper, not wider.
- [ ] **B.** Run `/sharpen` on a prompt → it returns a deeper version of the prompt.
