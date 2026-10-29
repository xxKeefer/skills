# Cascade

Goals cascade down the journal levels: each level is a backlog for the level below. Open items
move along their level or up to its parent. The journal skills follow the two rules below. Show
each choice, and accept a skip without comment.

## Levels

| Level | File | Open items in | New items go to | Parent |
| --- | --- | --- | --- | --- |
| Yearly | `YYYY.md` | `## 🎯 Goals` | `## 🎯 Goals` | none |
| Monthly | `YYYY-MM-mon.md` | `## 🎯 Goals` | `## 🎯 Goals` | yearly |
| Weekly | `YYYY-wkNN-week.md` | `## 🎯 Goals` | `## 🎯 Goals` | monthly |
| Daily | `YYYY-wkNN-day.md` | `## 📋 Today` | the `🎯 Tasks` group in `## 📋 Today` | weekly |

An open item is an unchecked `- [ ]` item.

## Pull-down

A skill that generates a file with a parent reads the parent's `## 🎯 Goals` and offers them:

> {Parent period}'s goals:
> - [ ] Goal 1
> - [ ] Goal 2
>
> Pull any into {this period}?

Add each selected goal where new items go in this file. The yearly level has no parent, so it has
no pull-down.

## Carry-forward

A skill that finds open items in a file offers them as a multi-select:

> These are still open from {period} -- select which to keep {next period}:
> - [ ] {item 1}
> - [ ] {item 2}
>
> Selected items go into {next period}'s list. Unselected items push up to the {parent} file.

- Put each selected item where new items go in the next file at the same level.
- Put each unselected item where new items go in the parent file.
- At the yearly level, drop each unselected item. Say so in the prompt in place of the push-up
  line.
