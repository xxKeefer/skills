---
doctype: spec
ticket: none
status: confirmed
goal: "`proof-read` flags a tell by its ID."
---

# Spec: `UNSLOP.md`

## Intent

- Outcome: `scribe/UNSLOP.md` is a numbered catalogue of AI tells. Each tell has a stable ID that a skill can cite. `proof-read` cites the catalogue, and names each tell that it flags by its ID.
- User: the user, who reads a proof-read finding and can look up the tell by its ID.
- Why now: map unit 28 (r1.20). The scribe skills have plain-word rules, but no list of AI vocabulary and tells.
- Success: `proof-read` flags a tell by its ID.
- Constraint: everything-agnostic. Credit the pstack source (`unslop`) in one line of prose in `UNSLOP.md`. An ID never changes or gets reused after it ships.
- Out of scope: the other proof-read lenses (`grices-maxims`, `asd-ste100`, `orwells-six`), and the output style.

## Decisions

- The map names no Decision for this unit.

## Acceptance criteria

- [ ] **A.** Read `scribe/UNSLOP.md` → it is a numbered catalogue of AI tells, each with a stable ID, and `proof-read` cites it.
- [ ] **B.** Run `proof-read` on a text that holds a catalogued tell → the finding names the tell by its ID.
