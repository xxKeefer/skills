# Journal -- Life Coach Skill Suite

Agile-inspired personal growth system for Obsidian. All artifacts live in the **sanctum directory**
within the user's Obsidian vault.

## Sanctum Discovery

Skills must never hardcode the sanctum path. Instead:

1. Scan the vault for a directory containing journal state files (`occasions.md`, `backlog.md`,
   `north-stars.md`, `kaizen.md`).
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

## Kaizen

Kaizen -- continuous tiny improvement -- is a first-class principle. North stars set direction;
kaizen sets cadence. The aim is to be 1% better every day, not to chase heroic rewrites.

- **One-Day PDCA:** Each day is a micro Plan-Do-Check-Act loop. `/daily` plans a near-zero-friction
  improvement; the day executes it; `/reflect` checks the outcome and acts (capture, adjust, or
  drop).
- **Standards lifecycle:** Experiments are proposed in `/ponder`, tried for one sprint, and
  graduated to Standards in `kaizen.md` when kept. Standards become locked-in baselines that
  `/weekly` carries into the next sprint by default.
- **5 Whys on recurring friction:** When the same friction shows up across multiple days,
  `/reflect` runs a 5 Whys mini-dialogue and records the root cause to `kaizen.md`.
- **Kaizen-shrink over abandonment:** A habit failing for 2+ sprints gets shrunk to a near-zero
  floor (e.g. "run 3x/week" -> "put running shoes on 3x/week") rather than dropped. The shrink is
  logged to Active Calibrations.

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

Four long-lived mutable files. Skills must read-modify-write carefully (never overwrite).

- `north-stars.md` -- active + achieved SMART goals, one per domain
- `backlog.md` -- single backlog, domain-tagged, north stars wikilinked
- `occasions.md` -- configurable events, reminders, day-specific chores
- `kaizen.md` -- standards (locked-in baselines), improvement log, active calibrations, 5 Whys log

## Cross-Skill Data Flow

```
/smart-goal -> north-stars.md -> /quest -> quest-<domain>.md
/vault -> backlog.md <-> north-stars.md
/weekly -> reads: previous ponder + backlog + north-stars + kaizen.md (Standards) -> sprint plan
/daily -> reads: sprint plan + occasions.md + kaizen.md (Standards) -> day file (with kaizen intent)
/check-in -> appends to: day file (between today + reflect)
/reflect -> appends to: day file; appends to: kaizen.md (Improvement Log, 5 Whys)
/ponder -> reads: week's day files + kaizen.md (Improvement Log) -> retro file;
           writes: kaizen.md (Standards on graduation, Active Calibrations on shrink)
/chronicle -> reads: period's ponders + kaizen.md -> arc file (Kaizen Arc)
```

`kaizen.md` producers: `/reflect` (Improvement Log, 5 Whys), `/ponder` (Standards, Calibrations).
`kaizen.md` consumers: `/daily`, `/weekly`, `/ponder`, `/chronicle`.

## WIP Limits

- 3 active domains per sprint (default)
- 4th domain requires explicit stretch-goal override -- coach blocks by default
- Dormant domains stay in backlog, challenged after 3+ sprints

## Skills

| Skill | Purpose |
|---|---|
| `/weekly` | Monday sprint planning ceremony |
| `/daily` | Morning standup and day file |
| `/check-in` | Adhoc mid-day micro-reflection |
| `/reflect` | Evening reflection |
| `/ponder` | Sprint retro |
| `/chronicle` | Monthly or yearly progress arc |
| `/vault` | Manage the life backlog and north stars |
| `/smart-goal` | SMART goal setting for any life domain |
| `/quest` | Map an actionable route to achieve a north star |

## Dependencies

Journal skills reference `/grill-it` from the `primitives` plugin for conversational coaching
mechanics. Both plugins must be installed for full functionality. Manual fallback templates work
without it.
