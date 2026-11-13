---
name: light-review
description: >
  Run the eight essential lanes of the review panel over a PR or branch, into the same report as
  /engineering:mob-review. Use when the user says "light review" or "quick review", or wants fewer
  lanes than the full panel.
argument-hint: "[PR number or URL | branch] [handoff or spec path]"
---

# Light Review: the essential lanes of the panel

Run eight persona lanes over one diff, not the full panel. The steps, the guards, and the report
are those of `mob-review`. The other lanes do not run, so a clean light run is not a clean full
panel.

## The essential lanes

- `persona-correctness`
- `persona-security`
- `persona-error-handling`
- `persona-code-quality`
- `persona-naming`
- `persona-test-design`
- `persona-test-quality`
- `persona-architecture`

## Steps

Read [`mob-review`](../mob-review/SKILL.md), and follow its Steps 0 to 7 with the changes below.
Each other line of those steps applies as written. `mob-review/PANEL.md` holds the guard and the model of each
lane.

1. **Step 0.** Ask the user to `/clear` and run `/engineering:light-review` again, not `mob-review`.
2. **Step 2.** Match the changed files against the guards of the essential lanes only. Spawn no
   other persona and no project rubric. In the coverage table, list every other lane and the
   project rubric with the status `skipped (not in the light set)`.
3. **Step 3.** `persona-ac-check` does not run. So the `Handoff or spec:` line goes to the
   `persona-test-design` brief only.
4. **Step 5.** Set the run `title` to `Light run`, not `Panel run`. Write no `Spec` in `meta`. Add
   one sentence to the `answer`: this run covers the essential lanes only, and
   `/engineering:mob-review` runs the full panel. The key does not change, so a light run and a panel
   run of the same branch go to one file.
5. **Step 7.** A lane outside the light set is not a mis-guard. When a signal is about the lane
   list above, name `light-review` in the entry heading.

**Done when:** the report holds a `Light run`, and the chat shows what `mob-review` Step 5 and
Step 7 print. The coverage table lists each lane outside the light set as
`skipped (not in the light set)`.
