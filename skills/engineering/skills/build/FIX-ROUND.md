# Fix Round

Read this file when the arguments of `/build` hold a review report and row IDs. Add the fix round
before you do Step 1 item 2 of [`SKILL.md`](SKILL.md).

1. Parse the JSON in the `<script type="application/json" id="runs">` block of the report. Find
   each ticked row in its run. Read the plan path from the `Plan` key of the run's
   `meta`. With no `Plan` key, stop, and name `/engineering:apply-review`.
2. Before the push step, add one step for each ticked row:
   `**<n>. Review fix <row ID>.** <issue> at <where>. Report: <report path>.` Its done line is
   the row's recommendation, with the row's note when it has one.
3. After the fix steps, decide if the round needs a new round of test and review. It needs one
   when a ticked row changes runtime behaviour, or when the round has more than three fix steps.
   A row that changes only tests, comments, names, or file locations does not change behaviour.
   If the round needs one, add a new round as the section
   below says. If the round does not
   need one, add no round. Write that choice into the plan as a recorded decision.
4. Write the unticked row IDs of the run into the plan as a recorded decision, at the new
   review step. With no new review step, write them at the first step after the fix steps. Add
   the reason for each row when the report gives one.
5. Delete the `D` entry that names this report. The ticks are its answer.

## Add a new round

Read this section each time `SKILL.md` adds a new round: Step 1 item 7, or Step 2 item 7.2.

To add a new round, add a new test step and a new review step after the last review step. Copy
the text of the last test step and the last review step. In the new review step, add the row
IDs that stay open in the last report. Tell the panel not to raise those rows again, and not to
raise any row that only repeats them. Also name the lanes to run: each lane that raised a
finding in the last run, and each lane whose guard matches a file that changed after the last
reviewed head. A clean lane whose files did not change does not run again.
