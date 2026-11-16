---
doctype: map
---

# Map: fixture

## Units

### [x] 1. ADR 0016, the pause list, callable workflow skills

- Done: the agent runs `/plan` after `/spec` when asked, and stops at an action on the pause list.

### [x] 2. Remove `experimental`

- Done: no skill lives in `experimental`, and `due.py` lists `lobotomize` after 30 days.

### [x] 3. Rename "handoff" to "plan"

- Done: `grep -ri handoff skills docs CONTEXT.md` finds only the act of handing off.

### [x] 4. The plan layout (r1.4, r1.17)

- Done: `/plan` on a ticket writes a plan that passes the check, and a broken plan fails with the line to fix.

### [x] 5. The spec layout

- Done: `/spec` then `/plan` with no hand edits between them.

### [x] 6. `/work-on`, the "new ticket" playbook, and the map playbook (r1.16)

- Done: `/work-on <ticket>` takes a ticket to a draft PR and stops only at H1, H2, H3, and H4. `/work-on @<map>` builds the next batch of units as stack layers, with one stop for the plans.

### [ ] 7. `install-agents-md` and the models block (r1.10)

- Done: a run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a second run changes nothing.

### [ ] 8. Principles and the TDD skip rule (r1.2)

- Done: `/work-on` on a task names the principle that shaped a choice, and the principle's file was read in that session.

### [ ] 9. `interrogate` (r1.1)

- Done: on a branch with a planted bug, the report keeps the proven finding and drops an unproven one.

### [ ] 10. `blast-radius` (r1.3)

- Done: on a change, the output names the rung reached and the command that proved it.

### [ ] 11. `/verify` and the drivers (r1.5)

- Done: `/create-verification-skill` on a small app writes a driver that passes its own proof run, and `/verify` finds it from a diff.

### [ ] 12. The decision log and `/sitrep` (r1.8, r1.26)

- Done: after a `/build`, `/sitrep` lists the choices the agent made alone.

### [ ] 13. `/checkpoint` (r1.24)

- Done: `/checkpoint` mid-step leaves a clean tree, and `/do-next` or `/work-on` resumes from the plan.

### [ ] 14. Stacks in `claim` and `stand-up`

- Done: `claim` on a branch inside a stack returns the stack's worktree, synced.

### [ ] 15. `ship` with gh-stack, and the map layout (r1.11)

- Done: `/ship` on a rebased stack layer accepts the old review when the patch-id matches.

### [ ] 16. `babysit` and the status line chips (r1.12)

- Done: a CI change on a watched PR shows a notification and the right chip, and leading spaces survive in the real status line.

### [ ] 17. The `tidy-up` audit table (r1.25)

- Done: `/tidy-up` shows the table and deletes nothing until a pick.

### [ ] 18. The correct ladder (r1.6)

- Done: a repeated mistake gets a fix at the highest rung that works.

### [ ] 19. No comments (r1.21)

- Done: a branch with an added comment gets a finding with the replacement, and a hack gets a step or a follow-up.

### [ ] 20. Two failures and model escalation (r1.13)

- Done: a third fix attempt starts with a written premise and a higher effort.

### [ ] 21. `eval-skill` (r1.23)

- Done: one run compares two versions of a skill and reports a winner or "no difference".

### [ ] 22. `loop-until` (r1.9)

- Done: a loop on a small metric stops at the predicate, with one log row per try.

### [ ] 23. TypeScript rules (r1.14)

- Done: `/install-rules` installs the rule.

### [ ] 24. `benchmark` (r1.7)

- Done: `webperf` reports a verdict with its limiter, or "inconclusive".

### [ ] 25. `sharpen` (r1.15)

- Done: `/sharpen` on a prompt returns a deeper version.

### [ ] 26. The fork rule (r1.18)

- Done: a grill looks up a fact instead of asking it.

### [ ] 27. Design-it-twice rubric (r1.19)

- Done: a design-it-twice run shows the rubric and the grafts.

### [ ] 28. `UNSLOP.md` (r1.20)

- Done: `proof-read` flags a tell by its ID.

### [ ] 29. `/why` (r1.22)

- Done: `/why` on a line returns its history with citations.

### [ ] 30. Text diagrams in `show-me`

- Done: `/show-me` draws a flow that the check passes. The diagrams in this map are the examples.

### [ ] 31. `findings` and `report` layouts

- Done: `/diagnose` writes a findings file that passes the check.

### [ ] 32. Script audit

- Done: the report exists, with rows to tick.

### [ ] 33. Retire list and version bumps

- Done: each changed domain has one new version, and only this unit changed a `plugin.json`.
