# Apply fixes (own code only)

`mob-review` Step 6 sends you here when the branch is your own. Never push. The push is the
user's action, or a later step of the handoff.

## 1. Sort the findings

Judge each finding on **size and certainty**, not on its severity tier. A `change-requested` can
be a one-liner and a `nit` can be a redesign.

**Small**: the fix is mechanical or local, and there is one obvious right answer:

- Deleting a redundant wrapper, duplicated mapping, or vacuous assertion
- Extracting a shared helper or test fixture already duplicated verbatim
- Adding a test case for an uncovered branch that the existing harness already supports
- Renames, missing `readonly`/`as const`, tightening a loose type, i18n key extraction

**Leave for the user**. Report with a recommendation instead:

- Anything that changes public API, a component contract, or an exported type
- Anything touching behaviour the tests don't pin down, or needing a product/design call
- Refactors spanning several files, or that would restructure a module
- Anything where two reasonable fixes exist and picking one is a judgment call the author should
  make
- Anything a persona itself flagged as `future` and framed as its own ticket

Mark each small finding **mechanical** (the code does the same thing after the fix) or
**behaviour** (the fix changes what the code does).

## 2. Ask once

Print the small findings as one numbered list, with the persona, the `file:line`, and the fix. Ask
once which to apply. Change nothing until the user answers. With no small findings, skip the
question.

Under `/auto-handoff` (you follow its `STEP.md`), you cannot ask. Take every small finding as a
pick.

## 3. In a handoff: add fix steps, fix nothing

Do this when Step 1 got a handoff. Change no code.

1. Add the picks as steps before the push step, the step that pushes or opens a PR. With no push
   step, add them at the end. Use the handoff's own step format. Use IDs that leave every existing
   ID unchanged, such as `6a` and `6b` after review step `6`.
2. Put every mechanical pick in one step. Its done line: the gates pass, and each added test goes
   red when you break the code it targets.
3. Give each behaviour pick its own step, test-first. The step names the failing test to write
   first, from the finding's counterexample. Its done line names that test.
4. Under `/auto-handoff`, also write a `D` entry in the `STEP.md` form. It lists the fix steps and
   asks which to keep: all, only the ones the user names, or none. Its `Blocks` line lists the fix
   steps and the push step.
5. Tick the review step. Write the base and head SHAs from the Step 5 report into its done line.

The fix commits come after the reviewed head. The push step finds them as drift and asks whether
to review them again.

## 4. Outside a handoff: apply the picks

1. **Prove each fix.** Fix a behaviour pick test-first: write the failing test, see it go red,
   then fix. For an added test, mutate the source it targets, confirm the new test goes red, and
   restore. A test that passes either way covers nothing. For a refactor, the existing specs must
   stay green.
2. Run the repo's typecheck, lint, format check, and the affected tests, at the smallest scope
   that proves the change, per the repo's `CLAUDE.md` / `AGENTS.md`.
3. Commit as one commit per the repo's commit convention, body listing what changed and why. For
   uncommitted work (Step 1), leave the fixes in the working tree.
4. Say that no panel read the fixes. The head SHA in the report is the last reviewed head.

## 5. Summarise

In the final summary, mark every finding `applied`, `fix step <id>`, or `left for you`, so the
report stays a complete account of the panel's output.
