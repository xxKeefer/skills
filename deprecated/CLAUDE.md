# Deprecated

Personal skills awaiting a keep/kill decision. A holding domain for skills that are rarely used or
possibly low-value, kept around until you decide whether the use case is genuinely rare (keep) or
the skill has no value (delete).

> Named `deprecated` here; the work marketplace uses `old` for the same role so the two plugins
> don't collide when both marketplaces are installed.

## Lifecycle

- **Entry**: a skill that's gone cold or whose value is in doubt moves here from its domain.
- **Revival**: if the use case turns out to matter, move it back to a stable domain.
- **Deletion**: after a grace window with no use, delete it — git history is the archive.

Disable this whole domain when you don't want deprecated skills loaded.

## Skills

| Skill | Purpose |
|---|---|
| `/design-it` | Generate multiple radically different interface designs via parallel sub-agents |
| `/improve-it` | Find architectural improvements by deepening shallow modules |
| `/research-it` | Pre-spike research producing a decision artifact (superseded by developer version) |
| `/intake-raw` | AFK batch -- process all notes in `00-raw/`, classify, route, absorb-and-split (from wiki) |
| `/intake-it` | HITL single note -- process one `00-raw/hitl/` note with human guidance (from wiki) |
| `/standardise-frontmatter` | AFK -- normalise knowledge note frontmatter to canonical shape (from wiki) |
| `/rebuild-index` | AFK -- generate or rebuild INDEX.md for a given directory (from wiki) |
