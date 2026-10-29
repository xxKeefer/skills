# Journal -- Personal Planner

Cascading goal/reflection system for Obsidian. All artifacts live in the **journal directory**
within the user's Obsidian vault. Skills find it with
`/discover-vault-directory * holding occasions.md`.

## Design Principles

- **Secretary/PA tone**: Surface information, don't apply pressure. No coaching, no accountability
  partner, no agile language.
- **Cascading goals**: Yearly goals feed monthly, monthly feed weekly, weekly feed daily. Each
  level is a backlog for the level below. No lock-in, no forced commitments.
- **Obsidian-native**: Valid YAML frontmatter (type, tags, prev/next/up wikilinks). No Dataview
  dependency. Compatible with Bases.
- **Template-portable**: Every file structure is simple enough to port to Obsidian Templater.
  Skills add value over templates by reading parent goals, detecting patterns, and fixing links.
- **Templates are the contract**: `journal/templates/` contains the authoritative output format
  for each file type. Skills must read and write against these templates.
- **Flat file structure**: All organisation via file naming. No nested directories.

## File Naming

| Level | Pattern | Example |
|---|---|---|
| Daily | `YYYY-wkNN-day.md` | `2026-wk22-sat.md` |
| Weekly | `YYYY-wkNN-week.md` | `2026-wk22-week.md` |
| Monthly | `YYYY-MM-mon.md` | `2026-05-may.md` |
| Yearly | `YYYY.md` | `2026.md` |

## Frontmatter

All journal files use this shape:

```yaml
---
type: journal/<daily|weekly|monthly|yearly>
date: YYYY-MM-DD
tags: [journal, journal/<type>]
up: "[[parent-file]]"
prev: "[[previous-sibling]]"
next: "[[next-sibling]]"
---
```

- Every file links `up` to its parent (daily -> weekly, weekly -> monthly, monthly -> yearly)
- Every file links `prev`/`next` to siblings at the same level
- Gaps are valid -- if you skip a day, `prev`/`next` jump over the gap (maintained by `/reflect`)

## Cascade

[`CASCADE.md`](CASCADE.md) holds the pull-down and carry-forward rules, and each journal skill
that uses them links it. Claude Code does not load this `CLAUDE.md` when a skill runs, so put
each cascade rule in that file.

## Invocation

Every journal skill is user-invoked: you start each one by hand. See
`docs/adr/0007-journal-and-omen-invocation.md`.

## State Files

One long-lived mutable file. Skills must read-modify-write carefully (never overwrite).

- `occasions.md` -- configurable events, reminders, day-specific chores

## Cross-Skill Data Flow

```
/yearly -> yearly file
/monthly -> reads: yearly goals -> monthly file
/weekly -> reads: monthly goals + occasions.md -> weekly file
/daily -> reads: weekly goals + occasions.md + yesterday's reflect -> daily file
/reflect -> updates: any journal file's reflect section; fixes prev/next links
```

## At a Glance

Each file includes a blockquote summary under the heading. The skill generates this by reading
the parent file's goals and the previous sibling's reflection to give a quick context snapshot.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## Templater Fallback

The repo's `scripts/obsidian/` module provides compiled Templater scripts and templates
as manual redundancy for when agents aren't available. These produce files matching the journal
skill contract. See `scripts/obsidian/README.md` for setup instructions.

## Dependencies

Journal skills reference `/grill` from the `primitives` plugin for conversational mechanics, and
`/discover-vault-directory` to find vault folders. Both plugins must be installed for full functionality. Manual fallback templates in `templates/`
work without it.
