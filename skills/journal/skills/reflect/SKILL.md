---
name: reflect
description: >
  File-agnostic reflection and maintenance tool. Fills reflect sections, fixes prev/next links,
  bubbles themes to parent files, surfaces carry-forward items. Use when user says "reflect",
  "end of day", or wants to update any journal file's reflection.
---

# Reflect

File-agnostic reflection and maintenance tool. Three jobs: fill reflections, fix links, surface
carry-forward items.

## Step 1: Parse Input

`<user-input>` determines the target file:

| Argument | Target |
|---|---|
| (none) | Today's daily file |
| `yesterday` | Yesterday's daily file |
| `DD-MM-YYYY` | Specific daily file for that date |
| `week` | Current week file |
| `month` | Current month file |
| `year` | Current year file |
| A file path | That specific file |

Locate the journal directory per the journal domain's discovery convention, then find the target
file. If the file doesn't exist:

> No file found for {target}. Want me to create a minimal one?

Read the file. Check if the Reflect section is already filled -- if so:

> Reflection already exists for {target}. Update it, or leave it?

## Step 2: Fill Reflection

Walk through the reflect sections conversationally. Adapt to the file level.

### For daily files

Ask each section one at a time:

> What did you learn today?

> What went well?

> What's carrying into tomorrow?

> Any friction -- things that slowed you down or felt harder than they should?

Listen and record. Don't interrogate -- this should feel like a quick debrief.

### For weekly/monthly/yearly files

These are retrospective. Read the child files' reflect sections first, then present a summary:

> Here's what came up across your {dailies/weeklies/monthlies}:
> - Went well: {patterns}
> - Friction: {patterns}
> - What's next: {recurring themes}
>
> Anything to add or adjust?

One round of input, then write.

## Step 3: Write Reflection

Update the target file's reflect section with the conversation output. Match the template
format from `journal/templates/`.

Preserve all existing content in the file. Only write to the Reflect section (and Insights
for monthly files if applicable).

## Step 4: Fix Links

Scan the target file's frontmatter `prev` and `next` fields. Check whether the linked files
actually exist in the journal directory.

- If `prev` points to a non-existent file, find the nearest existing sibling before it and
  update the link
- If `next` points to a non-existent file, find the nearest existing sibling after it and
  update the link
- Also update the reciprocal link in the sibling file (their `next`/`prev` should point back)

This handles date gaps -- if you skip days or weeks, links stay navigable.

Report fixes silently unless the user passed `--verbose` or similar. Just fix them.

## Step 5: Bubble Up Themes

Check if the target file has a parent (via the `up` frontmatter field). If so, read sibling
files at the same level and look for recurring themes:

- Friction points mentioned in 2+ siblings
- Ideas or topics appearing across multiple files
- "What is next" items that keep reappearing without being addressed

If patterns are found, suggest updating the parent file:

> These themes came up across multiple {days/weeks/months}:
> - {theme}
>
> Want me to add them to the {weekly/monthly/yearly} file's insights or reflect?

If nothing recurs, skip silently.

## Step 6: Carry Forward

Scan the target file and its siblings for incomplete goals or tasks (unchecked `- [ ]` items
in Goals or Today sections).

If found, present as multi-select:

> These are still open -- select which to carry forward:
> - [ ] {item} (from {file})
> - [ ] {item} (from {file})
>
> Selected items carry into the next file at this level.
> Unselected items push up to the parent level.

No guilt, no pressure. Just surfacing information.

## Step 7: Done

> **{target}** reflected. {link fixes if any}. {carry-forward count if any}.
