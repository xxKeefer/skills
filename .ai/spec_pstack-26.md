---
doctype: spec
ticket: none
status: confirmed
goal: "A grill looks up a fact instead of asking it."
---

# Spec: the fork rule

## Intent

- Outcome: `grill`, `spec`, and `plan` classify each question before they ask it. An observable fact goes to a lookup or a prototype, not to the user. Only a decision goes to the user.
- User: the user, who answers fewer questions about facts that the agent can find.
- Why now: map unit 26 (r1.18).
- Success: a grill looks up a fact instead of asking it.
- Constraint: everything-agnostic. Credit the pstack source (`poteto-mode`, its fork rule) in one line of prose.
- Out of scope: the pause list. Unit 1 already put it in the `pause-list.md` rule.

## Decisions

- The HITL line is on actions, not on skills (map Decision "Autonomy and the HITL line"). The pause list stays in the `pause-list.md` rule, and this unit does not change it.

## Acceptance criteria

- [ ] **A.** Read `grill`, `spec`, and `plan` → each classifies a question before it asks: an observable fact goes to a lookup or a prototype, and only a decision goes to the user.
- [ ] **B.** Run a grill on a plan that turns on a fact in the corpus → the grill looks up the fact and does not ask it.
