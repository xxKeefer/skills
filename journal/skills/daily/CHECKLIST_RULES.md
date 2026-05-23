# Checklist Rules

How to assemble the Today list from context sources.

## Structure

A single flat checklist under `## 📋 Today`. Groups are top-level checkboxes with indented
children.

## Chores Group

Pull from `occasions.md`:

- `- [ ] 🔄 Chores` as parent
  - All items from "Chores (Daily Default)" as indented children
  - Day-specific chores from the "Chores (Day-Specific)" table matching today
  - Events/reminders from "Recurring Events" falling on today's date

## Work Group (weekdays only)

On weekdays (Mon-Fri), add a Work parent item:

- `- [ ] 🧑‍💻 Work` as top-level checkbox
  - Indented children for standup, meetings, reviews, tasks, etc.
  - Populate from user's freeform input if they mention work items

Skip this group entirely on weekends.

## Task Items

Pull from weekly goals and user input as top-level checkboxes (same level as Chores/Work):

- `- [ ] 🎯` prefix for task items
- Goals pulled down from the weekly file
- Carried items from yesterday's "What is next" (if reflect was filled)
- Ad-hoc tasks from user's freeform input
- Use indented sub-items to break down larger tasks
