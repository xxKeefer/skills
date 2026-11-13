---
name: happy-path
description: >
  Generate a manual QA test plan for the current changeset. Reads recent git changes to understand
  what was built, then writes a concise checklist as an HTML report, whose fail ticks build a
  /engineering:fix prompt. Use when user says "happy path", "qa plan", "test plan", "what should I
  test", or wants to manually verify before closing out.
---

# Happy Path

Write a manual QA checklist for the current changeset as an HTML report.

## Step 1: Read the Changeset

Find the changeset:

1. If `$ARGUMENTS` holds a commit range, use it.
2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
   `origin/<name>`. Fall back to `main`.
3. Off the default branch, diff against `git merge-base HEAD <default>`.
4. On the default branch, use the uncommitted diff, `git diff HEAD`.
5. If that diff is empty, ask the user for a range.

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
  items in order. Tick pass or fail on each item. For a fail, write what happened in its note,
  then copy the prompt."
- `visuals`: one `table` with the question "What must be in place before you start?", the columns
  `Item` and `Initial state`, and one row for each part of the setup block. Do not fold it.
- `columns`: `area`, `step` (the action), and `expect` (the expected result).
- `rows`: one row for each item, area by area. Each row has `ticks: ["pass", "fail"]`.

In chat, give the report path and the item count. Do not print the checklist.

**Done when:** the new run has the setup table, each item is one row in the new run, and the chat
shows the report path and no checklist.
