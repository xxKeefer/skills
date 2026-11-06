---
name: happy-path
description: >
  Generate a manual QA test plan for the current changeset. Reads recent git changes to understand
  what was built, then writes a concise checklist as an HTML report, whose fail ticks build a
  /developer:fix prompt. Use when user says "happy path", "qa plan", "test plan", "what should I
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
- No setup instructions the human already knows
- No automated-test-level detail — this is for eyes-on-screen verification
- Keep it under 15 items total. To stay under the cap, merge related changes into one item.

**Done when:** every user-visible change in the diff maps to an item.

## Step 3: Write the Checklist

Write the checklist with `/write-report`. Give it these:

- `kind`: `qa`. A `/review:sad-path` run on the same branch adds its run to the same file.
- `title`: `QA: {short description of changeset}`.
- `skill`: `/developer:fix`.
- The run title: `Happy path`.
- `meta`: `Range`, the changeset from Step 1, such as `main...HEAD` or `uncommitted`.
- `answer`: one sentence on what changed. Then: "Tick each item that fails, write what happened in
  its note, then copy the prompt."
- `columns`: `area`, `step` (the action), and `expect` (the expected result).
- `rows`: one row for each item, area by area. Each row has `ticks: ["fail"]`.

In chat, give the report path and the item count. Do not print the checklist.

**Done when:** each item is one row in the new run, and the chat shows the report path and no
checklist.
