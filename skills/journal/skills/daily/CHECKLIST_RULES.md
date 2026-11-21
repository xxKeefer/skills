# Checklist Rules

How to assemble the Today list from context sources.

## Structure

A single flat checklist under `## 📋 Today`. Groups are top-level checkboxes with indented
children.

## Section Mapping

The items come from the output of `occasions.py` for the day (see Step 2 of the skill). Each key
of `due` maps to one checklist group:

| `due` key | Checklist group |
|---|---|
| `chores` | 🔄 Chores |
| `work` | 🧑‍💻 Work |
| `tasks` | 🎯 Tasks |

Items from all sources (occasions, user input, weekly goals, carries) merge into their
respective group. Within each group, sort by indentation -- parents first, then children.

## Chores Group

- `- [ ] 🔄 Chores` as parent
  - Each line of `daily` as an indented child, with its own nesting kept
  - Each item of `due.chores`

## Work Group (weekdays only)

On weekdays (Mon-Fri), add a Work parent item:

- `- [ ] 🧑‍💻 Work` as top-level checkbox
  - Each item of `due.work`
  - User's freeform input (standup, meetings, reviews, etc.)

Skip this group entirely on weekends (`due.work` items move to Tasks on weekends).

## Tasks Group

- `- [ ] 🎯` prefix for task items
  - Each item of `due.tasks`
  - Goals pulled down from the weekly file
  - Carried items from yesterday (selected via multi-select carry-forward)
  - Ad-hoc tasks from user's freeform input
  - Use indented sub-items to break down larger tasks
