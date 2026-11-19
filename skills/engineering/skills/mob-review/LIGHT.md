# Light mode

The light mode runs the lanes that the Light column of [`PANEL.md`](PANEL.md) marks, not the full
panel. The steps, the guards, and the report are those of [`SKILL.md`](SKILL.md). The other lanes
do not run, so a clean light run is not a clean full panel.

Follow Steps 0 to 7 of `SKILL.md` with the changes below. Each other line of those steps applies as
written.

1. **Step 0.** Ask the user to `/clear` and run `/engineering:mob-review light` again.
2. **Step 1.** Drop `light` from the arguments. Then read the target and the plan or spec path
   from the arguments that are left.
3. **Step 2.** Match the changed files against the guards of the light lanes only. Spawn no other
   persona and no project rubric. In the coverage table, list every other lane and the project
   rubric with the status `skipped (not in the light set)`. When no light lane matches, match the
   guards of every panel lane, and run each lane that matches. Mark each one
   `ran (no essential lane matched)` in the coverage table, and say so in the `answer`. A run with
   no lane reviews nothing.
4. **Step 3.** `persona-ac-check` does not run. So the `Plan or spec:` line goes to the
   `persona-test-design` brief only.
5. **Step 5.** Set the run `title` to `Light run`, not `Panel run`. Write no `Spec` in `meta`. Add
   one sentence to the `answer`: this run covers the light lanes only, and `/engineering:mob-review`
   with no `light` runs the full panel. The key does not change, so a light run and a panel run of
   the same branch go to one file.
6. **Step 7.** A lane outside the light set is not a mis-guard. When a signal is about the Light
   column, name the light mode of `mob-review` in the entry heading.

**Done when:** the report holds a `Light run`, and the chat shows what Step 5 and Step 7 print. The
coverage table lists each lane outside the light set as `skipped (not in the light set)` or
`ran (no essential lane matched)`. At least one lane ran, or no panel lane matches the diff.
