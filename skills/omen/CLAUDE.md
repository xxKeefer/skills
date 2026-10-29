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

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## Dependencies

- `primitives` -- `/discover-vault-directory` to find the omen folder and each campaign.
