---
type: sanctum/occasions
tags:
  - sanctum
aliases:
  - occasions
  - events
---

## Chores (Daily Default)
- [ ] Chore 1
- [ ] Chore 2

## Chores (Day-Specific)
| Day | Chore |
|---|---|
| Wednesday (even weeks) | Chore description |

## Recurring Events
| Occasion | Date/Rule | Type | Section |
|---|---|---|---|
| 🎂 Name | Mon DD | event | chores |
| 🎅 Holiday | Dec 25 | event | chores |
| 📋 Reminder | 1st Mon Month | reminder | chores |

Section values: `chores`, `work`, `tasks` -- maps the occasion into the matching checklist group in the daily file. Defaults to `chores` if omitted.
