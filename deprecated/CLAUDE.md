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
| `/bootstrap-ubiquitous-language` | Bootstrap a glossary for a brownfield project by mining the codebase for domain terms |
| `/design-it` | Generate multiple radically different interface designs via parallel sub-agents |
| `/improve-it` | Find architectural improvements by deepening shallow modules |
| `/learn-it` | Extract repeatable patterns from a conversation into a new skill |
| `/optimise-skill` | Harden a skill for durability, agnosticism, and size |
| `/qa-it` | Interactive bug intake session that files GitHub issues |
| `/refactor-it` | Interview-driven refactor planning, filed as a GitHub issue |
| `/research-it` | Pre-spike research producing a decision artifact (superseded by developer version) |
| `/teach-it` | Codify repeated user feedback into persistent guidance |
| `/triage-it` | Label-based state machine for triaging GitHub issues |
| `/ubiquitous-language` | Extract domain terminology from conversations into a glossary |
