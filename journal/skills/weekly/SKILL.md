---
name: weekly
description: >
  Generate weekly file. Pulls monthly goals, assembles events from occasions, creates daily links
  table. Detects recurring themes across daily files. Use when user says "weekly", "plan my week",
  "what's this week", or it's Monday.
---

# Weekly

Generate the weekly file. Surface context, don't apply pressure.

## Step 1: Parse Input

`<user-input>` may contain:

- A **week number** (e.g., "weekly wk14") -- plan that specific week
- A **file path** -- update an existing weekly file
- **Nothing** -- plan the current/next week

Determine the week dates (Monday -> Sunday) and the file name: `YYYY-wkNN-week.md`.

Locate the journal directory per the journal domain's discovery convention.

## Step 2: Read Context

Read these files from the journal directory:

- `YYYY-MM-mon.md` -- this month's goals (for pull-down)
- `occasions.md` -- recurring events this week
- Previous week's file (if exists) -- check reflect section
- This week's existing daily files (if any) -- for theme detection

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- This month's goals (what's active)
- Last week's reflect (what went well, friction, what's next)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Pull Down Monthly Goals

Read the current monthly file's Goals section. Present them:

> This month's goals:
> - [ ] Goal 1
> - [ ] Goal 2
>
> Pull any into this week?

Add selected goals to the weekly Goals section. Don't pressure -- if they skip, that's fine.

Ask:

> Any additional goals for this week?

## Step 5: Assemble Events

Read `occasions.md` for recurring events falling within this week's date range. List them under
the Events section.

Ask:

> Any other events this week?

## Step 6: Build Daily Links Table

Generate the Days table with wikilinks for each day of the week (Mon-Sun). If daily files already
exist, pull a short note from them. Otherwise leave the Notes column empty.

## Step 7: Detect Recurring Themes

If daily files from the previous week exist, scan their "Thoughts and Ideas" and reflect sections
for recurring themes or ideas that appear 2+ times.

If found, suggest:

> These themes came up multiple times last week:
> - {theme}
>
> Worth promoting any to a standalone note?

If nothing recurs, skip this step silently.

## Step 8: Carry Forward

Check the previous week's file for incomplete goals. Surface them:

> These are still open from last week:
> - {item}
>
> Carry forward or drop?

## Step 9: Write the Weekly File

Create or update `YYYY-wkNN-week.md` in the journal directory using the format in
`journal/templates/weekly.md`.

## Step 10: Done

> **Week {NN}** ready. {N} goals, {N} events.
