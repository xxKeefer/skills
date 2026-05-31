# Checklist Rules

How to assemble the Today list from context sources.

## Structure

A single flat checklist under `## 📋 Today`. Groups are top-level checkboxes with indented
children.

## Section Mapping

Occasions from `occasions.md` map to checklist sections via their `Section` field:

| Section value | Checklist group |
|---|---|
| `chores` (default) | 🔄 Chores |
| `work` | 🧑‍💻 Work |
| `tasks` | 🎯 Tasks |

Items from all sources (occasions, user input, weekly goals, carries) merge into their
respective group. Within each group, sort by indentation -- parents first, then children.

## Chores Group

- `- [ ] 🔄 Chores` as parent
  - All items from "Chores (Daily Default)" as indented children
  - Day-specific chores from the "Chores (Day-Specific)" table matching today
  - Recurring Events with `section: chores` falling on today's date

## Work Group (weekdays only)

On weekdays (Mon-Fri), add a Work parent item:

- `- [ ] 🧑‍💻 Work` as top-level checkbox
  - Recurring Events with `section: work` falling on today's date
  - User's freeform input (standup, meetings, reviews, etc.)

Skip this group entirely on weekends (work-section occasions move to Tasks on weekends).

## Tasks Group

- `- [ ] 🎯` prefix for task items
  - Recurring Events with `section: tasks` falling on today's date
  - Goals pulled down from the weekly file
  - Carried items from yesterday (selected via multi-select carry-forward)
  - Ad-hoc tasks from user's freeform input
  - Use indented sub-items to break down larger tasks
