# Scribe

Capture and edit notes in the user's Obsidian vault. Skills in this domain run from the vault root.
"Vault" = the Obsidian vault.

The domain covers two jobs:

- **Capture** utilitarian procedures -- terse, repeatable how-tos for chores the user wants to
  offload and forget (distinct from `03-knowledge/` deep-dives and `04-notes/` fleeting thoughts).
- **Edit** existing notes -- structural and prose editing that preserves Obsidian syntax.

## Vault Conventions

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
| `/edit-article` | HITL -- structural and prose editing for Obsidian notes |
