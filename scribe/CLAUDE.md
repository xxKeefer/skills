# Scribe

Capture and edit notes in the user's Obsidian vault. Skills in this domain run from the vault root.
"Vault" = the Obsidian vault.

The domain covers two jobs:

- **Capture** utilitarian procedures -- terse, repeatable how-tos for chores the user wants to
  offload and forget (distinct from `03-knowledge/` deep-dives and `04-notes/` fleeting thoughts).
- **Edit** existing notes -- structural and prose editing that preserves Obsidian syntax.

## Vault Conventions

### Procedures Directory

Procedure capture lives in the vault's procedures directory. Discover it by scanning the vault root
for a directory matching `*procedures` (e.g. `07-procedures/`). If none is found, ask the user where
procedures should live, create it, and store the path to memory. **Never hardcode the path** -- the
user may renumber or move it.

A procedure file is a small collection of related procedures for one area (e.g. `work.md`,
`nix.md`), not necessarily one procedure per file. Entry format is defined per skill.

### Editing

Preserve Obsidian-native syntax in every edit:

- **Frontmatter** (YAML between `---` fences) -- preserve exactly
- **Wikilinks** (`[[note]]`, `[[note|alias]]`) -- preserve exactly
- **Callouts** (`> [!type]`) -- preserve syntax
- **Tags** (`#tag/subtag`) -- preserve exactly
- **Embeds** (`![[file]]`) -- preserve exactly

## Dependencies

Scribe skills reference `/grill-it` from the `primitives` plugin for HITL coaching mechanics. Both
plugins must be installed.

## Skills

| Skill | Purpose |
|---|---|
| `/add-procedure` | Capture a just-solved task into the best-fit procedure file (or a new one) |
| `/edit-article` | HITL -- structural and prose editing for Obsidian notes |
