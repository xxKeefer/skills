---
name: sad-path
description: >
  Generate a manual QA checklist that tries to break the current changeset, built from the test
  data of the edge-case personas. Each item names the exact input or key and cites a catalogue ID.
  It writes an HTML report, whose fail ticks build a /developer:fix prompt. Use when the user says
  "sad path", asks which edge cases to try by hand, or wants to break a form before closing out.
---

# Sad Path

Write a manual QA checklist of the inputs and keys that break the changed screens, as an HTML
report. It is the other half of `/happy-path`. The test data lives with the personas, so the
review panel and this checklist share one copy.

## Lanes

| Lane | Persona (read its Guard) | Fixtures | Catalogue |
|---|---|---|---|
| `form-behaviour` | [`persona-form-behaviour`](../persona-form-behaviour/SKILL.md) | [`fixtures.md`](../persona-form-behaviour/references/fixtures.md) | [`catalogue.md`](../persona-form-behaviour/references/catalogue.md) |
| `text-input` | [`persona-text-input`](../persona-text-input/SKILL.md) | [`fixtures.md`](../persona-text-input/references/fixtures.md) | [`catalogue.md`](../persona-text-input/references/catalogue.md) |

## Step 1: Read the Changeset

Find the changeset:

1. If `$ARGUMENTS` holds a commit range, use it.
2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
   `origin/<name>`. Fall back to `main`.
3. Off the default branch, diff against `git merge-base HEAD <default>`.
4. On the default branch, use the uncommitted diff, `git diff HEAD`.
5. If that diff is empty, ask the user for a range.

Read the `--stat`, then the diff of the non-test source files. If `$ARGUMENTS` holds resource
links, invoke `/look-up` for them.

**Done when:** you have the changed non-test source files and their hunks.

## Step 2: Pick the Lanes

For each lane, read only the Guard section of its persona. The rest of the persona is a code
review, and this skill writes a checklist.

A lane runs when a changed hunk in any non-test source file shows one of the Guard's code
signals, such as a form control, a schema rule, or a key handler. The Guard's path filter and
file types do not apply here. Its rule about hunks that do not count still applies.

For each lane that runs, list what the change touches: each form, each field by the label the
user sees, and each field's bounds and rules.

**Done when:** each lane is marked run, with the signal and the changed line, or skip.

## Step 3: Build the Items

For each lane that runs:

1. Read its fixtures file.
2. List the `###` headings of its catalogue. Each heading holds an ID and a short name. A
   catalogue is large, so read an item's full text only when Step 3.4 sends you to it.
3. For each changed form and field, take the fixture rows and smoke-script steps that fit it.
4. Take the expected result from the fixture, when it gives one, or from the schema or copy in
   the diff. Else read the catalogue item and take it from the Fix. Every expected result has one
   of these three sources.
5. Tag the item with the one catalogue ID that names the defect it probes. Use the ID that the
   fixture row cites, when it cites one. When an item only points at another ID, use that ID.
   The item goes under the lane whose catalogue holds its ID.
6. Rank the items: data saved wrong or work lost, then a wrong action, then a cosmetic fault.
   Keep the first 8. Merge items that send the same class of input to one field.

Then build the setup block: the state that the tester needs before item 1. Give one row for each
part of that state that applies:

- How to run the change: the command, and each flag or environment variable that the items need.
- How to reach each changed form: the route or the clicks from the start page.
- Each account, role, or permission, and the items that use it.
- The data that must exist before the start, such as a record to edit.
- Where to copy each fixture input, when an input holds invisible characters.
- The cleanup after the test, so that the system goes back to its first state.

**Done when:** each kept item names a field, an input or key, an expected result, and one
catalogue ID, no lane has more than 8 items, and the setup block names all the state that the
items need.

## Step 4: Write the Checklist

Write the checklist with `/write-report`. Give it these:

- `kind`: `qa`. A `/happy-path` run on the same branch writes to the same file.
- `title`: `QA: {short description of changeset}`.
- `skill`: `/developer:fix`.
- `track`: `["pass"]`. The user ticks pass to mark the items that they have done.
- The run title: `Sad path`.
- `meta`: `Lanes run` (each lane and its signal), `Skipped` (each lane), and `Cut by the cap`
  (each lane and its items past 8, or `none`).
- `answer`: one sentence on what the items try to break. Then: "Set up the state in the first
  table, then run the items in order. Tick pass or fail on each item. For a fail, write what
  happened in its note, then copy the prompt."
- `visuals`: one `table` with the question "What must be in place before you start?", the columns
  `Item` and `Initial state`, and one row for each part of the setup block. Do not fold it.
- `columns`: `lane`, `area` (the form or area), `step` (the action), `expect` (the expected
  result), and `catalogue` (mono, the catalogue ID).
- `rows`: one row for each item, lane by lane, in the Step 3 rank order. Each row has
  `ticks: ["pass", "fail"]`.

Rules:

- Each item is an action in the running app. A check of the code belongs to `/code-review:mob-review`.
- Quote each input byte-exact from the fixtures. When an input holds invisible characters, also
  name the fixture row and each invisible character, such as "T4 (zero-width space)", so the
  tester copies it from the fixtures file.
- No general steps in the setup table, such as how to install the tools or clone the repo.

In chat, give the report path, the item count, and the lanes that ran. Do not print the
checklist.

**Done when:** the new run has the setup table, each item that Step 3 kept is one row with a
catalogue ID, and the chat shows the report path and no checklist.
