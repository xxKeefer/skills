---
name: happy-path
description: >
  Write a manual QA checklist for the current changeset as an HTML report. Use when the user says
  "happy path" or "test plan", or asks what to test by hand before closing out. The `sad` mode tries
  to break the changed forms and fields: use it when the user says "sad path", asks which edge
  cases to try by hand, or wants to break a form.
argument-hint: "[sad] [commit range | resource links]"
---

# Happy Path

Write a manual QA checklist for the current changeset as an HTML report.

**Sad mode.** When the arguments hold `sad`, or the user asks for the sad path, for edge cases to
try by hand, or to break a form, read [`SAD.md`](SAD.md) and follow it in place of the steps
below. Otherwise run the happy path.

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
- Give each item a runner. `agent`: a command shows the result, such as a push, a CI status, log
  text, or an API reply. `you`: the result needs eyes on a UI or a dashboard.
- Take each push or PR item from the plan's push step, when a plan exists. When that step is
  done, or says to open no PR, write no item for it.
- On a branch in a stack (`gh stack view` succeeds), write each push as `gh stack push` and each
  rebase as `gh stack rebase`. A step that drops a commit resets the branch, then runs
  `gh stack push`. That command force-pushes with a lease and keeps the stack in order.

Then build the setup block of [`QA-REPORT.md`](../../QA-REPORT.md), with this row too, when it
applies: what the tester must not touch, when a step can change live or shared state.

**Done when:** every user-visible change in the diff maps to an item, and the setup block names all
the state that the items need.

## Step 3: Write the Checklist

Give `/write-report` the report inputs of [`QA-REPORT.md`](../../QA-REPORT.md), and these:

- The run title: `Happy path`.
- `meta`: `Range`, the changeset from Step 1, such as `main...HEAD` or `uncommitted`.
- `answer`: one sentence on what changed. Then: "Set up the state in the first table, then run the
  items in order. The agent runs the `agent` items and reports each result. You run the `you`
  items. Tick pass or fail on each item. For a fail, write what happened in its note, then copy
  the prompt."
- `columns`: `area`, `by` (`agent` or `you`), `step` (the action), and `expect` (the expected
  result).
- `rows`: area by area.

**Done when:** the new run has the setup table, each item is one row in the new run, and the chat
shows the report path and no checklist.
