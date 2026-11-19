# QA report

`happy-path` writes a manual QA checklist as an HTML report, in two modes: the happy path, and the
`sad` mode of [`SAD.md`](skills/happy-path/SAD.md). Both modes use this setup block and these
report inputs. Each mode adds its own setup rows and its own inputs.

## Setup block

The setup block is the state that the tester needs before item 1. Give one row for each part of
that state that applies:

- How to run the change: the command, and each flag or environment variable that the items need.
- Each account, token, role, or permission, and the items that use it.
- The data that must exist before the start, such as a record to edit, and the data that must not.
- The cleanup after the test, so that the system goes back to its first state.

Write no general steps in the setup block, such as how to install the tools or clone the repo.

## Report inputs

Write the checklist with `/write-report`. Give it these, and the inputs of the mode:

- `kind`: `qa`. A happy run and a sad run on the same branch write to the same file.
- `title`: `QA: {short description of changeset}`.
- `skill`: `/engineering:fix`.
- `track`: `["pass"]`. The user ticks pass to mark the items that they have done.
- `visuals`: one `table` with the question "What must be in place before you start?", the columns
  `Item` and `Initial state`, and one row for each part of the setup block. Do not fold it.
- `rows`: one row for each item, in the order of the mode. Each row has `ticks: ["pass", "fail"]`.

In chat, give the report path and the item count. Do not print the checklist.
