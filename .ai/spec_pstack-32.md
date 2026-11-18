---
doctype: spec
ticket: none
status: confirmed
goal: "The script audit report exists, with rows to tick."
---

# Spec: Script audit

## Intent

- Outcome: one report lists each skill step where a script saves time or tokens, or makes a result deterministic, such as report schema checks, the version bump, and the skill table sync.
- Outcome: the same report lists each existing script that does neither.
- User: the repo owner, who ticks the rows to build or delete later.
- Why now: map unit 32.
- Success: the report exists, with rows to tick.
- Constraint: the audit changes no script and no skill. It only writes the report.

## Decisions

- Scripts (map): a script earns its place only when it saves time or tokens, or when its result must be deterministic. A judgement that a model already makes well gets no script. Each row names which of the two a script gives, or says it gives neither.
- File types (map): `report` is HTML with a JSON `runs` block and rows to tick, written by `/write-report`.

## Acceptance criteria

- [ ] **A.** Read the audit report → it has one row for each skill step where a new script saves time or tokens, or makes a result deterministic, and each row names which of the two it gives.
- [ ] **B.** Read the audit report → it has one row for each existing script that gives neither, with the reason, so the user can tick it for deletion.
- [ ] **C.** Run the report check on the audit report → it passes, and each row has a tick box.
