# Start Ticket: optional inputs

`SKILL.md` links each section from the step that needs it. Only some runs read this file.

## No questions

When the user says to ask no questions, a gate that asks for a yes takes its
default and continues. Write the AC letters (Step 8), move the ticket (Step 4), and write the plan
without the approval (Step 6). Put `Approval: none, the user waived questions.` in Context, and
list each assumption there. A SPLIT or CLARIFY verdict still stops, because the
user picks the path. Name each skipped gate in the Step 9 return.

## A spec

When `/plan` gives a spec in place of the key, take the goal from its frontmatter `goal` and the
ACs from its `## Acceptance criteria` section. Skip Step 1 items 2 to 4.

## A sub-task map

If the ticket is a sub-task, find the map of its parent: `map_<PARENT>.md`, in the folder that
`/write-to-file` picks for doctype `map`, or in a subfolder of it. `/split-ticket` wrote it.
Read the unit of this sub-task: its `Done:` line, its `merge` value, and its `builds_on` value.
With no map, continue without them.

## Defect hotspots

Step 5 reads the defect hotspots of this repo before it rates the ACs, if
`/engineering:self-improve` wrote them:
`${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/<repo key>/defect-hotspots.md`. The repo key is
`<owner>--<repo>` from the `origin` URL, else `local--<main worktree folder name>`. A file that the
plan changes, in or under one of its Hotspots areas, is a hotspot. Raise its likelihood one step,
only once, and name the area in the Why column. Derive the conditions for the area's Usually missed
escape types first.

## Split at the plan gate

In Step 6, on SPLIT path 2, the plan steps become the slices:

1. Write each step as a slice in the format of
   [`scope-ticket`](../../scope-ticket/SKILL.md) Step 4. Give it its files, its parent
   ACs, its size, its points, and the slices that it builds on.
2. Run `/split-ticket` with the key, the slices, and the ticket text.
3. Write no plan, and stop. Return the `/split-ticket` result. Say that the worktree from Step 3
   has no use, and give its path.
