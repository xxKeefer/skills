---
doctype: spec
ticket: none
status: confirmed
goal: "/tidy-up shows the table and deletes nothing until a pick."
---

# Spec: The `tidy-up` audit table

## Intent

- Outcome: `/tidy-up` shows a read-only audit table of the repo's working state first: size, merged, dirty, PR state, and last used for each item. It deletes only the rows that the user picks.
- User: the user who cleans up after finished work, and wants to see what each item is before it goes.
- Why now: map unit 17 (r1.25).
- Success: a run lists every item in one table, changes nothing, and waits. After a pick, only the picked rows change.
- Constraint: subtract before you add. Change the existing steps in place. Add no script and no new step.
- Out of scope: a change to what counts as stale, and any action on the remote.

## Decisions

- The table replaces the checkpoint table of Step 3. It holds one numbered row for each item: item, work, size, merged, dirty, PR state, last used, proposed action, reason. A column that does not apply to an item shows `-`.
- The user picks rows by number, `all`, or `none`. The skill applies only the picked rows. There is no single yes for the whole table.
- Remove the bypass that applies the cleanup at once when the user asked for it by name. A pick is always needed.
- No script: each column comes from one git command or the code host, and the agent already runs those in Step 1. A script would add a file to keep in step with no gain.
- Remove the repeated word in the opening list ("plans, plans").

## Acceptance criteria

- [ ] **A.** Run `/tidy-up` on a repo with a merged worktree and a dirty one → one table shows size, merged, dirty, PR state, and last used for each row.
- [ ] **B.** Read the skill → it deletes and fixes nothing until the user picks rows, and applies only the picked rows.
- [ ] **C.** Run `/tidy-up`, then pick no rows → no file, branch, or worktree changes.
