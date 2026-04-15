---
name: intake-raw
description: >
  Batch-process all notes in 00-raw/, classify each note, and route to the correct vault location.
  Knowledge notes are absorbed into existing docs or used to create new ones via the absorb-and-split
  algorithm. Low-confidence and work-related notes are routed to 00-raw/hitl/ for human triage.
  Use when the user says "intake", "process raw", "process inbox", or wants to batch-process
  their raw notes folder.
---

# Intake Raw

Batch-process `00-raw/` -- classify, route, and absorb.

## Step 1: Scan Raw Folder

List all files in `00-raw/` (excluding `hitl/` subdirectory). For each file:

- Read the full content
- Note the filename, any frontmatter, headings, and body text

If `00-raw/` is empty (excluding `hitl/`), report and stop:

> **No raw notes to process.** `00-raw/` is empty.

## Step 2: Classify Each Note

For each raw note, determine the classification:

| Classification | Criteria |
|---|---|
| **Knowledge** | Reference material, factual content, how-to, concepts, technical information |
| **Fleeting/personal** | Shower thoughts, quick ideas, personal observations, stream of consciousness |
| **Project-related** | Tied to a specific project, contains action items or deliverables |
| **Work-related** | Employer-specific, work meetings, work tasks -- **always route to HITL** |
| **Low confidence** | Cannot confidently classify -- **route to HITL** |

Bias toward `00-raw/hitl/` when uncertain. False negatives (missed HITL) are worse than false
positives (unnecessary HITL).

## Step 3: Route Non-Knowledge Notes

For each note that is NOT classified as knowledge:

- **Fleeting/personal** -- move to `04-notes/` root
- **Project-related** -- move to `05-projects/` root
- **Work-related** -- move to `00-raw/hitl/`
- **Low confidence** -- move to `00-raw/hitl/`

## Step 4: Absorb Knowledge Notes

For each note classified as knowledge, apply the absorb-and-split algorithm (see CLAUDE.md):

1. Search `03-knowledge/` for the most relevant existing doc
2. If found -- insert content under the most relevant heading
3. If the section exceeds ~500 lines -- split the largest subsection into a new doc
4. If no match -- create a new knowledge doc with a declarative name
5. Apply recursively if splits produce oversized docs
6. If overall doc exceeds ~2000 lines -- split the largest L1/L2 heading

For new knowledge docs:

- Generate fresh canonical frontmatter (see CLAUDE.md spec)
- Use declarative, descriptive filenames following existing naming conventions in `03-knowledge/`
- Add a `## Sources` section at the bottom

## Step 5: Post-Intake Cleanup

For each processed raw note:

- **Fully absorbed** -- delete the raw file
- **Partially absorbed or un-absorbable** -- move to `98-archive/`

## Step 6: Report

Summarise the batch:

> **Intake complete**
>
> | Action | Count |
> |---|---|
> | Absorbed into knowledge | {N} |
> | New knowledge docs created | {N} |
> | Filed to notes | {N} |
> | Filed to projects | {N} |
> | Routed to HITL | {N} |
> | Archived | {N} |
> | Splits performed | {N} |
>
> **Knowledge docs modified:** {list}
> **New docs created:** {list}
