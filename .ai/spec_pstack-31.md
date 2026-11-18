---
doctype: spec
ticket: none
status: confirmed
goal: "`/diagnose` writes a findings file that passes the check."
---

# Spec: `findings` and `report` layouts

## Intent

- Outcome: `primitives/write-to-file` gets a template and a check for the `findings` doctype.
- Outcome: `primitives/write-report` gets a check for the JSON `runs` block of a `report`.
- Outcome: `engineering/diagnose` writes its hunt as a `findings` file in the new layout.
- User: an agent or a person who reads a findings file or a report, and a skill that parses one.
- Why now: map unit 31.
- Success: `/diagnose` writes a findings file that passes the check.
- Constraint: a `findings` file holds a question, its answer, the evidence, and open points, as the map's File types decision says. Its header is YAML frontmatter.

## Decisions

- File types (map): five parsed layouts plus `scratch`. `findings` holds a question, its answer, the evidence, and open points. Its writers are `/diagnose` and spike work. `findings` replaces `spike`, `hunt`, `risks`, and `research` markdown files. Each markdown layout keeps its header in YAML frontmatter.
- File types (map): `report` is HTML with a JSON `runs` block and rows to tick, written by `/write-report`.

## Acceptance criteria

- [ ] **A.** Ask `/write-to-file` for a `findings` file → it writes the file from a `findings` template, then runs the findings check and gives its result to the caller.
- [ ] **B.** Run the findings check on a findings file → it passes a file in the template layout, and fails a file with a missing header key or section, with the line and a fix.
- [ ] **C.** Run the report check on a report HTML file → it passes a file whose `runs` block has the `/write-report` shape, and fails a file whose block is missing, does not parse, or breaks the shape, with the problem and a fix.
- [ ] **D.** Run `/diagnose` to the end of its hunt → it writes `findings_<KEY>.md` in the findings layout, not the old hunt layout.
- [ ] **E.** Run `/diagnose` on a bug, then run the findings check on its file → the check passes.
