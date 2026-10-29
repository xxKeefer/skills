---
name: monthly
description: Generate the monthly file, with yearly goals, weekly links, and insights and themes from the weekly reflections.
disable-model-invocation: true
---

# Monthly

Generate the monthly file. Surface context from the year and the weeks.

## Step 1: Parse Input

`<user-input>` may contain:

- A **month** (e.g., "monthly june", "monthly 2026-06") -- target that month
- A **file path** -- update an existing monthly file
- **Nothing** -- target the current month

Determine the month and file name: `YYYY-MM-mon.md` (e.g., `2026-05-may.md`).

Find the journal directory with `/discover-vault-directory * holding occasions.md`.

Check if the monthly file already exists. If it does, read it and update rather than overwrite.

## Step 2: Read Context

Read these files from the journal directory:

- `YYYY.md` -- this year's goals (for pull-down)
- Previous month's file (if exists) -- check reflect section
- This month's weekly files (if any) -- for insights and theme detection
- `occasions.md` -- recurring events this month

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- This year's goals (what's active)
- Last month's reflect (what went well, friction, what's next)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Pull Down Yearly Goals

Follow **Pull-down** in [CASCADE.md](../../CASCADE.md), with this year's file as the parent.

Ask:

> Any additional goals for this month?

## Step 5: Assemble Events

Read `occasions.md` for recurring events falling within this month's date range. List them under
the Events section.

Ask:

> Any other events this month?

## Step 6: Build Weekly Overview Table

Generate the Overview table with wikilinks for each week that falls within this month. If weekly
files already exist, pull a short note from their goals or reflect. Otherwise leave Notes empty.

## Step 7: Collect Insights

If weekly files from this month (or the previous month if early in the month) exist, scan their
reflect sections for patterns:

- Recurring friction points
- Repeated wins or momentum areas
- Themes from "What is next" that keep appearing

Summarise findings in the Insights section. If nothing notable, leave it empty.

## Step 8: Detect Recurring Themes

Scan weekly files for recurring ideas or themes that appear in 2+ weeks' reflect or goals.

If found, suggest:

> These themes came up across multiple weeks:
> - {theme}
>
> Worth promoting any to a standalone note?

If nothing recurs, skip silently.

## Step 9: Carry Forward

Follow **Carry-forward** in [CASCADE.md](../../CASCADE.md) on the open goals in last month's file.

## Step 10: Write the Monthly File

Create or update `YYYY-MM-mon.md` in the journal directory using the format in
[templates/monthly.md](../../templates/monthly.md).

If updating an existing file, preserve any content already written. Only update sections that
need changes.

## Step 11: Done

> **{Month YYYY}** ready. {N} goals, {N} events, {N} weeks linked.
