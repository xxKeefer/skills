# Omen -- TTRPG Campaign Management

Creative skills for TTRPG campaign logging, lore management, and session planning. All artifacts
live in **setting directories** within the user's Obsidian vault.

## Setting Format

The run-time contract lives in
[skills/scaffold-setting/SETTING-FORMAT.md](skills/scaffold-setting/SETTING-FORMAT.md): campaign
discovery, folder structure, frontmatter, game types, lore templates, wikilinks, tone, and file
templates. Omen skills link it. Claude Code does not load this `CLAUDE.md` when a skill runs, so
put every rule that a skill needs at run time in the format file.

## Skills

| Skill | Purpose |
|---|---|
| `/log-session` | Log a game session to the session index |
| `/log-cannon` | Extract canon events from a session log |
| `/log-npcs` | Catalog NPCs from a session log |
| `/log-place` | Catalog places from a session log |
| `/log-progression` | Update character arcs from a session log |
| `/make-lore` | Spin off a heading into a standalone lore file |
| `/make-blurb` | Generate hype blurb from session planning |
| `/make-summary` | Narrative summary from a completed session |
| `/plan-session` | Plan a new session by game type |
| `/scaffold-setting` | Bootstrap a new campaign setting with standard structure |
| `/doctor-setting` | Migrate an existing campaign to the standard structure |

## Dependencies

- `primitives` -- `/discover-vault-directory` to find the omen folder and each campaign.
