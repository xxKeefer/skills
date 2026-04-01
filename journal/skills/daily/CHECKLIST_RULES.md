# Checklist Rules

How to assemble the Today list from context sources.

## Structure

A single flat checklist under `## Today`. Groups are top-level checkboxes with indented children.

## Chores Group

Pull from `occasions.md`:

- `- [ ] Chores` as parent (no emoji)
  - All items from "Chores (Daily Default)" as indented children
  - Day-specific chores from the "Chores (Day-Specific)" table matching today
  - Events/reminders from "Recurring Events" falling on today's date

## Work Group (weekdays only)

On weekdays, add a Work parent item:

- `- [ ] Work` as top-level checkbox
  - Indented children for standup, meetings, reviews, tasks, etc.
  - Populate from sprint plan work-related tasks if available

## Task Items

Pull from the sprint plan as top-level checkboxes (same level as Chores/Work):

- Non-work tasks relevant to today from active domain goals
- Habit items for today
- Experiment actions if applicable
- Carried items from yesterday's "What is next" (if reflect was filled)
- Use indented sub-items to break down larger tasks
