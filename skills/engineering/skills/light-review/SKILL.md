---
name: light-review
description: >
  Run the essential lanes of the review panel over a PR or branch: correctness, security,
  error-handling, code-quality, naming, test-design, test-quality, and architecture. Follows the
  mob-review steps, and writes the findings to the same HTML report through /write-report. On your
  own branch, it fixes each finding that has a fix, commits once, and reports what stays open. On
  someone else's, it drops the nits, and the ticks build a /engineering:post-review-comments
  prompt. It never pushes. Takes an optional handoff or spec path for the test-design
  check. Use when the user says "light review", "quick review", or wants a review with fewer
  lanes than /engineering:mob-review.
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
Each other line of those steps applies as written. The panel table of `mob-review` holds the guard
of each lane, and its Step 3 sets the model of each lane.

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
