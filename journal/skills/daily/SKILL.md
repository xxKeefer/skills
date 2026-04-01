---
name: daily
description: >
  Morning standup. Quick check-in: today's tasks from the sprint plan, chores from occasions,
  blockers. Produces or updates the day's file. Use when user says "daily", "standup", "what's
  today", "morning check-in", or starts their day.
---

# Daily

Morning standup. Quick, focused, <5 minutes. Be encouraging but direct.

**Input:** optional date or file path, plus freeform notes (ad-hoc tasks, work context, extra chores).
**Output:** daily file (`YYYY-wkNN-day.md`) in the sanctum directory.

## Step 1: Parse Input

`<user-input>` may contain:

- A **date** (e.g., "daily monday", "daily 2026-03-24") -- target that day
- A **file path** -- update an existing daily file
- **Freeform notes** -- ad-hoc tasks, work context, or extra chores to fold into the checklist
- **Nothing** -- target today

Determine the day, week number, and file name: `YYYY-wkNN-day.md` (e.g., `2026-wk13-mon.md`).

Locate the sanctum directory per the journal domain's discovery convention.

Check if the daily file already exists. If it does, read it and update rather than overwrite.

## Step 2: Read Context

Read these files from the sanctum directory for context:

- `YYYY-wkNN-sprint.md` — this week's sprint plan (goals, habits, experiments)
- `occasions.md` — chores and events for today
- Previous day's file (if exists) — check "What is next" from last reflect

## Step 3: Build the Day

Build the Today checklist. See [CHECKLIST_RULES.md](CHECKLIST_RULES.md) for assembly rules.

### Confirm

Ask the user:

> Here's what I've pulled from your sprint plan and yesterday's reflect. Anything to add, drop, or
> adjust for today?

Keep it brief -- this should be a quick confirmation, not a planning session.

### Blockers

Ask:

> Anything blocking you today?

If they mention blockers, note them. If a blocker is recurring (appeared in previous dailies), flag
it: "This has come up before -- is it time to address it directly?"

## Step 4: Write the Daily File

Create or update `YYYY-wkNN-day.md` in the sanctum directory using the format in
[DAILY_TEMPLATE.md](DAILY_TEMPLATE.md).

If updating an existing file, preserve any content already written (checked chores, completed tasks,
notes). Only update sections that need changes.

## Step 5: Send Off

> **{Dayname} — wkNN** ready. {N} tasks, {N} chores. {event note if applicable}
>
> Come back tonight with `/reflect`. Have a good one.
