---
name: daily
description: >
  Morning standup. Quick check-in: today's tasks from the sprint plan, chores from occasions,
  blockers. Produces or updates the day's file. Use when user says "daily", "standup", "what's
  today", "morning check-in", or starts their day.
---

# Daily

Morning standup. Quick, focused, <5 minutes. Be encouraging but direct.

## Step 1: Parse Input

`<user-input>` may contain:

- A **date** (e.g., "daily monday", "daily 2026-03-24") — target that day
- A **file path** — update an existing daily file
- **Nothing** — target today

Determine the day, week number, and file name: `YYYY-wkNN-day.md` (e.g., `2026-wk13-mon.md`).

Check if the file already exists in `10 - Sanctum/`. If it does, read it and update rather than
overwrite.

## Step 2: Read Context

Read these files for context:

- `10 - Sanctum/YYYY-wkNN-sprint.md` — this week's sprint plan (goals, habits, experiments)
- `10 - Sanctum/occasions.md` — chores and events for today
- Previous day's file (if exists) — check "What is next" from last reflect

## Step 3: Build the Day

Build a single flat checklist under `## Today`. Chores and tasks live in one list, organised by
single-level indent.

### Chores group

Pull from `occasions.md` and add as a top-level checkbox group within the Today list:

- `- [ ] Chores` as a parent item (no emoji)
  - All items from "Chores (Daily Default)" as indented children
  - Any day-specific chores from the "Chores (Day-Specific)" table that match today
  - Any events/reminders from "Recurring Events" that fall on today's date

### Work group (weekdays only)

On Monday--Friday, add a Work parent item:

- `- [ ] 🏢 Work` as a top-level checkbox
  - Indented children for standup, meetings, PR reviews, tickets, etc.
  - Populate from sprint plan work-related tasks if available

### Task items

Pull from the sprint plan and add as top-level checkboxes (same level as Chores/Work):

- Non-work tasks relevant to today from active domain goals
- Habit items for today
- Experiment actions if applicable
- Carried items from yesterday's "What is next" (if reflect was filled)
- Use indented sub-items to break down larger tasks

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

Create or update `10 - Sanctum/YYYY-wkNN-day.md`:

```markdown
---
type: sanctum/daily
tags:
  - sanctum
  - sanctum/daily
date: YYYY-MM-DD
up: '[[YYYY-wkNN-sprint]]'
prev: '[[YYYY-wkNN-prevday]]'
next: '[[YYYY-wkNN-nextday]]'
---

# Dayname — wkNN

## ☀️ Today

- [ ] Chores
  - [ ] Chore 1
  - [ ] Chore 2 {day-specific chores if applicable}
- [ ] Work {weekdays only}
  - [ ] standup
  - [ ] {work tasks}
- [ ] Task 1
- [ ] Task 2 {events/reminders if applicable}

## 🚧 Blockers

- (none) or blocker description

---

## 🤔 Reflect

<!-- Fill in the evening with /reflect -->

### What I learned

-

### What went well

-

### What is next

-

### ⚠ Friction

-
```

If updating an existing file, preserve any content already written (checked chores, completed tasks,
notes). Only update sections that need changes.

## Step 5: Send Off

> **{Dayname} — wkNN** ready. {N} tasks, {N} chores. {event note if applicable}
>
> Come back tonight with `/reflect`. Have a good one.
