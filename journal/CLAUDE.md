# Journal -- Life Coach Skill Suite

Agile-inspired personal growth system for Obsidian. All artifacts live in the **sanctum directory**
within the user's Obsidian vault.

## Sanctum Discovery

Skills must never hardcode the sanctum path. Instead:

1. Scan the vault for a directory containing journal state files (`occasions.md`, `backlog.md`,
   `north-stars.md`).
2. If found, use that directory for all reads and writes.
3. If not found, ask the user where journal files live and store the path to memory.

## Design Principles

- **Domain-agnostic**: Skills never reference hardcoded life domains. Users create domains freely
  via `#domain/<area>` tags. Skills discover active domains by reading `backlog.md` and
  `north-stars.md`.
- **Coach-driven, manually operable**: Claude generates all artifacts conversationally. Every file
  type has a manual fallback template in `journal/templates/`.
- **Obsidian-native**: Valid YAML frontmatter (type, tags, aliases, prev/next/up wikilinks). No
  Dataview dependency. Compatible with Bases.
- **Flat file structure**: All organisation via file naming. No nested directories.

## Coaching Tone

Blend of **blunt accountability partner** and **encouraging mentor**.

- Push back hard when the user overcommits (>3 active domains without stretch override)
- Push back hard on domains dormant 3+ sprints: "You said this mattered -- what changed?"
- Proactively surface patterns at sprint boundaries
- Celebrate achievements genuinely
- Suggest experiments for recurring friction (1-sprint trial, then evaluate)

## File Naming

| File type | Pattern | Example |
|---|---|---|
| Sprint plan | `YYYY-wkNN-sprint.md` | `2026-wk13-sprint.md` |
| Daily | `YYYY-wkNN-day.md` | `2026-wk13-mon.md` |
| Ponder (retro) | `YYYY-wkNN-ponder.md` | `2026-wk13-ponder.md` |
| Chronicle (monthly) | `YYYY-MM-chronicle.md` | `2026-03-chronicle.md` |
| Chronicle (yearly) | `YYYY-chronicle.md` | `2026-chronicle.md` |
| Quest | `quest-<domain>.md` | `quest-se.md` |
| State files | descriptive name | `north-stars.md`, `backlog.md`, `occasions.md` |

## State Files

Three long-lived mutable files. Skills must read-modify-write carefully (never overwrite).

- `north-stars.md` -- active + achieved SMART goals, one per domain
- `backlog.md` -- single backlog, domain-tagged, north stars wikilinked
- `occasions.md` -- configurable events, reminders, day-specific chores

## Cross-Skill Data Flow

```
/smart-goal -> north-stars.md -> /quest -> quest-<domain>.md
/vault -> backlog.md <-> north-stars.md
/weekly -> reads: previous ponder + backlog + north-stars -> sprint plan
/daily -> reads: sprint plan + occasions.md -> day file
/check-in -> appends to: day file (between today + reflect)
/reflect -> appends to: day file
/ponder -> reads: week's day files -> retro file
/chronicle -> reads: period's ponders -> arc file
```

## WIP Limits

- 3 active domains per sprint (default)
- 4th domain requires explicit stretch-goal override -- coach blocks by default
- Dormant domains stay in backlog, challenged after 3+ sprints

## Dependencies

Journal skills reference `/grill-it` from the `primitives` plugin for conversational coaching
mechanics. Both plugins must be installed for full functionality. Manual fallback templates work
without it.
