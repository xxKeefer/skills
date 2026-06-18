# Journal -- Personal Planner

Cascading goal/reflection system for Obsidian. All artifacts live in the **journal directory**
within the user's Obsidian vault.

## Journal Directory Discovery

Skills must never hardcode the journal path. Instead:

1. Scan the vault for a directory containing `occasions.md`.
2. If found, use that directory for all reads and writes.
3. If not found, ask the user where journal files live and store the path to memory.

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

## Cascading Goal Pull-Down

The core mechanic:

```
yearly goals
  -> prompted into monthly goals
    -> prompted into weekly goals
      -> prompted into daily tasks
```

Each level serves as a backlog for the level below. When generating a file, the skill reads the
parent's goals and asks: "Want to pull any of these down?" No lock-in, no forced commitments.

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

| Skill | Purpose |
|---|---|
| `/daily` | Generate daily file with tasks and reflection sections |
| `/weekly` | Generate weekly file with goals, events, and daily links |
| `/monthly` | Generate monthly file with goals and weekly overview |
| `/yearly` | Generate yearly file with aspirations and monthly overview |
| `/reflect` | File-agnostic reflection and link maintenance tool |
| `/update-occasions-config` | Sync vault `occasions.md` into `vault_occasions.js` for Templater |

## Templater Fallback

The repo's `scripts/obsidian/` module provides compiled Templater scripts and templates
as manual redundancy for when agents aren't available. These produce files matching the journal
skill contract. See `scripts/obsidian/README.md` for setup instructions.

## Dependencies

Journal skills reference `/grill-it` from the `primitives` plugin for conversational mechanics.
Both plugins must be installed for full functionality. Manual fallback templates in `templates/`
work without it.
