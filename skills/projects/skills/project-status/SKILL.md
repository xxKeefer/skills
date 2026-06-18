---
name: project-status
description: >
  PM-persona check-in on a project. Reads the Kanban board and mission, then summarises state: what's
  done, what's in progress, what's stalled, the next actions, and upcoming milestones. Use when the
  user says "project status", "where are we on X", "check in on the project", or wants a read on a
  long-running project.
---

# Project Status

A competent project manager reading you the state of play. Informative and terse -- no pressure, no
agile ceremony, no coaching. Just: where things stand and what's next.

## Step 1: Identify the Project

Check `$ARGUMENTS` for a slug or name. Otherwise discover the projects directory and list active
projects; ask which one.

## Step 2: Read the Workspace

Read, in this order:

- `MISSION.md` -- the goal and definition of done. Everything is judged against this.
- `<slug>.kanban.md` -- the board. Parse columns and cards per
  [BOARD-FORMAT.md](../new-project/BOARD-FORMAT.md): `Backlog`, `This Week`, `Doing`, `Done`, and any
  custom columns. Note `- [x]` (complete) vs `- [ ]` (open) and any `@{YYYY-MM-DD}` date tags.
- `decisions/` (if present) -- the latest record or two, for recent direction.

## Step 3: Assess State

Work out:

- **Progress** -- count done vs total; which definition-of-done items are met.
- **In flight** -- what's in `Doing` right now.
- **Stalled** -- cards in `Doing` with no movement, or `This Week` items whose dates have passed.
  Flag overdue `@{date}` tags explicitly.
- **Next actions** -- the most sensible cards to pull from `Backlog`/`This Week`, given the mission.
- **Upcoming** -- milestones with future `@{date}` tags, soonest first.

## Step 4: Report

Lead with the headline, then the detail. Keep it scannable:

> **{Project}** -- {one-line state, e.g. "on track" / "stalled on finance" / "blocked"}
>
> - **Done:** {n}/{total} -- {what's complete that matters}
> - **Doing:** {cards in progress}
> - **Stalled / overdue:** {cards + why, or "none"}
> - **Next up:** {1-3 recommended cards}
> - **Upcoming dates:** {milestone -- date, soonest first, or "none"}

If the board has drifted from the mission (lots of cards unrelated to the definition of done, or a
definition-of-done item with no cards), say so plainly -- that's the most useful thing a PM surfaces.

Do not modify the board. This skill only reports.
