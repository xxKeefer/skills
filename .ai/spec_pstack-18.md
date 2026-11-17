---
doctype: spec
ticket: none
status: confirmed
goal: "A repeated mistake gets a fix at the highest rung that works."
---

# Spec: The correct ladder

## Intent

- Outcome: a repeated agent mistake gets its fix at the highest rung of one ordered ladder: architecture, then types, then a lint whose error names the fix, then a test, and docs last. `constraints` and `self-improve` both apply it.
- User: the user whose agents make the same mistake twice, and who wants it made impossible, not written down again.
- Why now: map unit 18 (r1.6). `constraints` proves each rule fails, but does not order the fix levels.
- Success: `constraints` backs a new rule at the highest rung that works, and `self-improve` routes a repeated theme the same way.
- Constraint: subtract before you add. Write the ladder once, and point to it. Add no script and no new step.
- Out of scope: a memory of past mistakes in `constraints`, and a change to how `self-improve` groups themes.

## Decisions

- The ladder lives in `principle-encode-lessons-in-structure`, which already says to encode a repeated rule as structure. Its unordered list becomes the ordered ladder, with "a mistake class counts after two times". One definition, so the two skills cannot drift apart.
- `constraints` Step 4 and `self-improve` Step 3 read the principle by path and apply the ladder. Neither copies it.
- `self-improve` already counts a theme at two or more fixes of one kind. That is the two-times count, so its threshold stays.
- The route row for a theme specific to the codebase picks its target by the ladder, so the agent file comes last, not first.

## Acceptance criteria

- [ ] **A.** Read `principle-encode-lessons-in-structure` → it orders the fix rungs as architecture, types, a lint whose error names the fix, a test, then docs, and counts a mistake class after two times.
- [ ] **B.** Read `constraints` → when it writes a rule, it backs the rule at the highest rung of the ladder that works, and reads the principle by path for the ladder.
- [ ] **C.** Read `self-improve` → a codebase-specific theme goes to the highest rung that works, with the agent file last, and the step reads the principle by path.
- [ ] **D.** Run `python3 skills/engineering/skills/work-on/scripts/check_principles.py .` → exit 0, and no skill outside the principle restates the ladder.
- [ ] **E.** Feed a repeated mistake through either skill → its fix lands at the highest rung that works.
