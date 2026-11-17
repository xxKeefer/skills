---
doctype: spec
ticket: none
status: confirmed
goal: "A branch with an added comment gets a finding with the replacement, and a hack gets a step or a follow-up."
---

# Spec: No comments

## Intent

- Outcome: no comment lands in code that the user or the agent writes. On the user's own branch, `persona-comments` turns each added comment into a finding whose fix is a rung of the comment ladder. A comment that marked a hack becomes a plan step or a Follow-up.
- User: the user, who can ask a model what any line does, so a comment adds nothing they cannot get another way (r1.21).
- Why now: map unit 19 (r1.21). `persona-comments` still keeps a comment that "explains why", and the `coding` block says nothing on comments.
- Success: a review of the user's branch finds each added comment and names its replacement; a hack comment ends as a plan step or a Follow-up; the `coding` block states the rule.
- Constraint: subtract before you add. Cut the rules the own-branch lens does not need from the hot path of `persona-comments` before adding the lens. Add no script and no new skill.
- Out of scope: a change to the rules on another person's PR, a sweep of comments that already exist, and a ticket for a Follow-up.

## Decisions

- Two lenses, from the map Comments decision. On the user's own branch, each added comment is a finding, except a tool directive whose reason a check enforces and a comment that the repo's lint requires. On another person's PR, the current rules stay.
- The lens comes from the ownership check that `mob-review` Step 1 already makes (own code: every commit is by the current git user). The persona reads it; it does not make its own check.
- Subtract first: the current numbered rules, their severity list, and the e2e JSDoc exception serve only the other-PR lens. They move out of `SKILL.md` into one reference file that only that lens reads. The three existing reference files stay as they are, and that file points to them. The description shrinks to the two lenses.
- No script. The persona reads the added lines of the diff, and tells a comment from a string. A per-line scan missed a comment on each new quote shape that review found (D1, 2026-11-17).
- The comment ladder (a better name, a type, a test whose title states the fact, a check that fails with the fix in its error, delete it) lives once, in `persona-comments`. Each own-lens finding names the rung and the replacement in its `suggestion`.
- A hack: the persona marks the finding as a hack and names the architectural fix. `mob-review` `FIX.md` applies the rung now, then runs `/blast-radius` on the architectural fix. A small fix inside the change's scope becomes a new plan step; a fix too big or outside the scope becomes a `Follow-ups` entry in the plan. No stop.
- `Follow-ups` already exists in the plan layout (unit 4), and `/sitrep` already shows it. `create-pr` adds the plan's Follow-ups to the PR body, so the PR's notes show them. The user decides whether a ticket is written.
- The `coding` block of `install-agents-md` gets the rule: "No comments. Two exceptions: tool directives and comments that lint requires."
- `PANEL.md`: the `persona-comments` row's trigger becomes a changed source, script, or config file in any language.

## Acceptance criteria

- [ ] **A.** Read `persona-comments` → its Guard and Scope find each added comment line by reading the diff, in any language, and no script runs.
- [ ] **B.** Read `persona-comments` on the user's own branch → each added comment is a finding whose `suggestion` names a ladder rung and the replacement, except the two exceptions; the other-PR rules are not in `SKILL.md`.
- [ ] **C.** Read `persona-comments` on another person's PR → it reads the reference file and applies the current rules unchanged.
- [ ] **D.** Read `mob-review` `FIX.md` → a hack finding runs `/blast-radius` on the architectural fix, and becomes a new plan step when small and in scope, else a `Follow-ups` entry.
- [ ] **E.** Read `create-pr` → the PR body lists the plan's Follow-ups, and removes the section when there are none.
- [ ] **F.** Run `install_agents_md.py` against a scratch home → the `coding` block holds "No comments. Two exceptions: tool directives and comments that lint requires."
- [ ] **G.** Review a branch with an added comment → it gets a finding with the replacement, and a hack gets a step or a follow-up.
