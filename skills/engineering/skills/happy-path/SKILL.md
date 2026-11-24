---
name: happy-path
description: >
  Write a manual QA checklist for the current changeset as an HTML report. Use when the user says
  "happy path" or "test plan", or asks what to test by hand before closing out.
---

# Happy Path

Write a manual QA checklist for the current changeset as an HTML report.

## Step 1: Read the Changeset

Find the changeset as [`CHANGESET.md`](../../CHANGESET.md) says.

Read the `--stat` of the changeset to identify changed files, then its diff to understand what
changed. If `$ARGUMENTS` contains resource links, invoke `/look-up` for additional context.

## Step 2: Build the Items

Build a flat list of items, grouped by feature or area. Each item is a concrete action and an
expected result that the user can check in under a minute.

Rules:
- Happy path first, obvious edge cases only if high risk
- No general steps, such as how to install the tools or clone the repo
- No automated-test-level detail — this is for eyes-on-screen verification
- Keep it under 15 items total. To stay under the cap, merge related changes into one item.
- When the plan or the ticket has acceptance criteria, tag each item with the AC that it proves,
  and word its expected result from that AC. An expected result that asks for more than its AC is
  new behaviour: leave it out, or tag it `beyond AC`.
- Give each item a runner. `agent`: a command shows the result, such as a push, a CI status, log
  text, or an API reply. `you`: the result needs eyes on a UI or a dashboard.
- Take each push or PR item from the plan's push step, when a plan exists. When that step is
  done, or says to open no PR, write no item for it.
- On a branch in a stack (`gh stack view` succeeds), write each push as `gh stack push` and each
  rebase as `gh stack rebase`. A step that drops a commit resets the branch, then runs
  `gh stack push`. That command force-pushes with a lease and keeps the stack in order.

Then build the setup block: the state that the tester needs before item 1. Give one row for each
part of that state that applies:

- How to run the change: the command, and each flag or environment variable that the items need.
- Each account, token, role, or permission, and the items that use it.
- The data that must exist before the start, and the data that must not.
- What the tester must not touch, when a step can change live or shared state.
- The cleanup after the test, so that the system goes back to its first state.

**Done when:** every user-visible change in the diff maps to an item, and the setup block names all
the state that the items need.

## Step 3: Write the Checklist

Write the checklist with `/write-report`. Give it these:

- `kind`: `qa`. A `/engineering:sad-path` run on the same branch adds its run to the same file.
- `title`: `QA: {short description of changeset}`.
- `skill`: `/engineering:fix`.
- `track`: `["pass"]`. The user ticks pass to mark the items that they have done.
- The run title: `Happy path`.
- `meta`: `Range`, the changeset from Step 1, such as `main...HEAD` or `uncommitted`.
- `answer`: one sentence on what changed. Then: "Set up the state in the first table, then run the
  items in order. The agent runs the `agent` items and reports each result. You run the `you`
  items. Tick pass or fail on each item. For a fail, write what happened in its note, then copy
  the prompt."
- `visuals`: one `table` with the question "What must be in place before you start?", the columns
  `Item` and `Initial state`, and one row for each part of the setup block. Do not fold it.
- `columns`: `area`, `ac` (the AC ID, `beyond AC`, or empty with no ACs), `by` (`agent` or `you`), `step` (the action), and `expect` (the expected
  result).
- `rows`: one row for each item, area by area. Each row has `ticks: ["pass", "fail"]`.

In chat, give the report path and the item count. Do not print the checklist.

**Done when:** the new run has the setup table, each item is one row in the new run, and the chat
shows the report path and no checklist.
