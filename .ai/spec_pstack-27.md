---
doctype: spec
ticket: none
status: confirmed
goal: "A design-it-twice run shows the rubric and the grafts."
---

# Spec: the design-it-twice rubric

## Intent

- Outcome: `codebase-design/DESIGN-IT-TWICE.md` writes a rubric before the fan-out. It sketches the caller's usage first, picks a base design by the rubric, grafts the strong parts of the other designs onto the base, and scraps a design on a known tell.
- User: the user, who gets one scored design with named grafts, not a menu of designs.
- Why now: map unit 27 (r1.19). Design-it-twice has fixed briefs, but no rubric, no graft, and no scrap trigger.
- Success: a design-it-twice run shows the rubric and the grafts.
- Constraint: everything-agnostic. Credit the pstack source (`arena` and `architect`) in one line of prose.
- Out of scope: the deepening flow in `DEEPENING.md`, and `improve-codebase-architecture`.

## Decisions

- The map names no Decision for this unit.

## Acceptance criteria

- [ ] **A.** Read `DESIGN-IT-TWICE.md` → it writes a rubric before the fan-out, sketches the caller's usage first, picks a base, grafts the strong parts of the other designs, and scraps a design on a known tell.
- [ ] **B.** Run design-it-twice on a module → the output shows the rubric, the score of each design, the base, and each graft.
