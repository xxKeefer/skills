---
doctype: spec
ticket: none
status: confirmed
goal: "`/why` on a line returns its history with citations."
---

# Spec: `/why`

## Intent

- Outcome: a new skill, `engineering/why`, answers why a line, a block, or a file is the way it is. It builds the answer from the commits and the PR threads that touched the target. It cites the author of each source, and it says what the record does not answer.
- User: an engineer who reads code that they did not write, and must know the reason before they change it.
- Why now: map unit 29 (r1.22). `explain` builds its why layer from reasoning, not from the history of the code.
- Success: `/why` on a line returns its history with citations.
- Constraint: everything-agnostic. The skill names the code host as a tool role, not a product. Credit the pstack source (`why`) in one line of prose in the skill. User note (r1.22): name the skill `why`.
- Out of scope: a change to `primitives/explain`. The research row suggested the explain why layer, but the map puts the skill in `engineering` as `why`.

## Decisions

- The map names no Decision for this unit.

## Acceptance criteria

- [ ] **A.** Read `engineering/why` → it is a new skill that answers why from the commits and the PR threads of the target.
- [ ] **B.** Read `engineering/why` → it cites the author of each source, and says what the record does not answer.
- [ ] **C.** Run `/why` → the skill name is `why`.
- [ ] **D.** Run `/why` on a line → it returns the history of the line, with a citation for each claim.
