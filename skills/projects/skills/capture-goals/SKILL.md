---
name: capture-goals
description: >
  Facilitate a planning sit-down for a project. Grills the participants, takes their thought dump,
  and organises it into discrete, actionable cards on the Kanban board. The conversational heartbeat
  of a project -- mirrors the journal's daily skill. Use when the user says "capture goals", "plan the
  project", "let's plan", "brain dump", or wants to turn loose planning thoughts into tasks.
---

# Capture Goals

Sit down with the people who own the project, draw out everything in their heads, and turn the mess
into a clean set of actionable cards. This is the recurring planning session -- run it whenever
thinking has outpaced the board.

## Step 1: Identify the Project and Read State

Check `$ARGUMENTS` for a slug or name. Otherwise discover the projects directory and list active
projects; ask which one.

Read `MISSION.md` (so tasks serve the goal) and the current board per
[BOARD-FORMAT.md](../new-project/BOARD-FORMAT.md) (so you don't duplicate existing cards).

## Step 2: Facilitate the Dump

There may be **more than one person in the room** (e.g. the user and a partner). Address the room,
capture every voice. Invoke `/grill-it` to draw thoughts out and pressure-test them -- but tuned for
*elicitation*, not interrogation. Keep it conversational:

- "What needs to happen for this to move forward?"
- "What's worrying you / what's blocked?"
- "What did we say last time that hasn't been done?"
- "Anything dated -- deadlines, appointments, hard dates?"

Let it run loose. Capture raw thoughts verbatim as they come; don't organise yet. Stop when the room
is empty of ideas.

## Step 3: Organise into Tasks

Turn the raw dump into discrete cards. Each card must be:

- **Actionable** -- starts with a verb, names one concrete thing to do.
- **Atomic** -- one card, one task. Split compound thoughts ("sort finance and book the inspection"
  -> two cards).
- **Non-duplicate** -- check it against existing board cards; merge rather than repeat.
- **Dated when a date surfaced** -- attach `@{YYYY-MM-DD}` per BOARD-FORMAT.

Drop pure venting and anything already done. Group nothing yet -- a flat list is the output here.

## Step 4: Confirm the List

Present the organised cards back to the room before writing:

> From that session, here are the cards:
> - [ ] {task}
> - [ ] {task} @{date}
>
> Add, drop, reword, or split anything?

One round of refinement, then write. This is the moment for human judgement -- don't skip it.

## Step 5: Write to the Board

**Read-modify-write** `<slug>.kanban.md` -- never overwrite the file. Append the confirmed cards to
the **Backlog** column.

Then triage near-term work:

> Pull any of these into **This Week**?
> - [ ] {card}
> - [ ] {card}

Move selected cards from Backlog to This Week. Leave the rest in Backlog. No pressure to schedule.

## Step 6: Surface Milestones

If any card carries a hard date that belongs in the journal (a deadline, not just a target), offer:

> {N} of these are dated milestones. Push them to the journal via `/schedule-goals`?

Hand off to `/schedule-goals` for the ones the user picks.

## Step 7: Confirm

> Captured **{n}** cards for **{Project}**:
> - Backlog: {n}
> - This Week: {n}
> - Milestones to journal: {n or "none"}
>
> Worth a decision record? (if the session shifted direction, write one per DECISIONS-FORMAT.)
