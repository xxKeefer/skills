# Daily Template

Output format for the daily file.

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

# Dayname -- wkNN

## Today

- [ ] Chores
  - [ ] Chore 1
  - [ ] Chore 2 {day-specific chores if applicable}
- [ ] Work {weekdays only}
  - [ ] standup
  - [ ] {work tasks}
- [ ] Task 1
- [ ] Task 2 {events/reminders if applicable}

## Blockers

- (none) or blocker description

---

## Reflect

<!-- Fill in the evening with /reflect -->

### What I learned

-

### What went well

-

### What is next

-

### Friction

-
```
