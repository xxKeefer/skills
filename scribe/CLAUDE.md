# Scribe

Knowledge work over a corpus -- primarily the user's Obsidian vault, but the context-curation
skills (`define-*`) work against any corpus, including code repos. Vault-bound skills run from the
vault root. "Vault" = the Obsidian vault.

The domain covers three jobs:

- **Capture** utilitarian procedures -- terse, repeatable how-tos for chores the user wants to
  offload and forget (distinct from `02-research/` deep-dives and `00-notes/` fleeting thoughts).
- **Edit** existing notes -- structural and prose editing that preserves Obsidian syntax.
- **Curate context** -- mine a corpus for its terminology and maintain a `CONTEXT.md` glossary
  (one file per context). Corpus-agnostic: code, vault, lore, or session logs.

## Vault Conventions

### Procedures Directory

Procedures are a kind of reference doc, so they live in the vault's reference directory. Discover it
by scanning the vault root for a directory matching `*reference` (e.g. `03-reference/`). If none is
found, ask the user where reference docs should live. **Never hardcode the path** -- the user may
renumber or move it.

A procedure file is a small collection of related procedures for one area (e.g. `git.md`,
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
| `/define-concept` | Mine a corpus for one concept's terms, verify term-by-term, write a CONTEXT.md |
| `/define-term` | Add a single term to a CONTEXT.md under a user-specified section |
| `/define-language` | Compare a conversation against a CONTEXT.md, propose restrained edits/additions |
| `/triage-notes` | HITL -- triage one fleeting inbox note: promote, taskify, or archive on approval |
| `/take-a-note` | Capture something from the conversation: append to a given note (style-matched) or drop a fresh note in vault 00-notes/ |
| `/teach` | Teach a topic over multiple sessions in a stateful workspace |
