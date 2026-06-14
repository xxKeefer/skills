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

## One Off Events - YYYY
| Occasion | Date/Rule | Type | Section |
|---|---|---|---|
| 💒 A Wedding | Oct 12 | event | tasks |

Fire once on the date, then prune the row manually. Year-guarded (the `- YYYY` suffix scopes them to that year). Default section `tasks`.

## Projects
| Occasion | Date/Rule | Type | Section |
|---|---|---|---|
| 🏗 Project Name: milestone | Jul 3 | event | tasks |

Written by the `projects` domain's `/schedule-goals`; removed by `/close-project`. Dated, year-guarded, single-fire. Default section `tasks` so milestones surface in the daily/weekly Tasks group with no template change.
