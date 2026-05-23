---
name: yearly
description: >
  Generate yearly file. Goals and aspirations dump, monthly plan table, reflection sections.
  Lightest-touch skill -- mostly an organising structure. Use when user says "yearly",
  "plan my year", or at the start of a new year.
---

# Yearly

Generate the yearly file. Lightest-touch skill -- a goals dump and organising structure.

## Step 1: Parse Input

`<user-input>` may contain:

- A **year** (e.g., "yearly 2027") -- target that year
- A **file path** -- update an existing yearly file
- **Nothing** -- target the current year

Determine the file name: `YYYY.md` (e.g., `2026.md`).

Locate the journal directory per the journal domain's discovery convention.

Check if the yearly file already exists. If it does, read it and update rather than overwrite.

## Step 2: Read Context

Read these files from the journal directory:

- Previous year's file (if exists) -- check reflect section and goals
- `occasions.md` -- recurring yearly events

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- Last year's reflect (what went well, friction, what's next)
- Last year's goals (what was achieved, what carried over)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Set Goals

If a previous year's file exists, surface its incomplete goals:

> Last year's open goals:
> - {item}
>
> Carry any forward?

Then ask:

> What are your goals and aspirations for {YYYY}?

This is freeform -- big-picture stuff. Holidays, projects, life changes, learning goals. No
structure enforced beyond a checklist.

## Step 5: Assemble Events

Read `occasions.md` for notable yearly events. List them under the Events section.

Ask:

> Any other events or milestones planned for this year?

## Step 6: Build Monthly Plan Table

Generate the Monthly Plans table with wikilinks for all 12 months. If monthly files already
exist, pull a short note from their goals. Otherwise leave Notes empty.

## Step 7: Write the Yearly File

Create or update `YYYY.md` in the journal directory using the format in
`journal/templates/yearly.md`.

If updating an existing file, preserve any content already written. Only update sections that
need changes.

## Step 8: Done

> **{YYYY}** ready. {N} goals set.
