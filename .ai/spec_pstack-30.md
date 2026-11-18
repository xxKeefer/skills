---
doctype: spec
ticket: none
status: confirmed
goal: "`/show-me` draws a flow that the check passes."
---

# Spec: text diagrams in `show-me`

## Intent

- Outcome: `primitives/show-me` gets a new view: hand-drawn box diagrams for a flow or a dependency graph. The view uses box-drawing characters and ASCII only, with no emoji, one route per line, and a label on each line. Mermaid stays for the HTML view.
- Outcome: a new script, `show-me/scripts/check_diagram.py`, checks a diagram: each character is one column wide, and the box corners line up.
- User: a reader who sees a flow or a dependency graph in a terminal or a markdown file, where Mermaid does not render.
- Why now: map unit 30.
- Success: `/show-me` draws a flow that the check passes.
- Constraint: the diagrams in the map are the examples of the view.

## Decisions

- The map names no Decision for this unit.

## Acceptance criteria

- [ ] **A.** Ask `/show-me` for a flow or a dependency graph in a text view → it draws a box diagram with box-drawing characters and ASCII only, no emoji, one route per line, and a label on each line. Mermaid stays the HTML view.
- [ ] **B.** Run `show-me/scripts/check_diagram.py` on a diagram → it passes when each character is one column wide and the box corners line up, and fails when either is false.
- [ ] **C.** Run `/show-me` on a flow, then run the check on its diagram → the check passes.
