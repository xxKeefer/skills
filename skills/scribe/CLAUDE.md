# Scribe

Knowledge work over a corpus -- primarily the user's Obsidian vault, but the context-curation
skills (`define-*`) work against any corpus, including code repos. Vault-bound skills run from the
vault root. "Vault" = the Obsidian vault.

The domain covers three jobs:

- **Capture** utilitarian procedures -- terse, repeatable how-tos for chores the user wants to
  offload and forget (distinct from `*research` deep-dives and `*notes` fleeting thoughts).
- **Edit** existing notes -- gated proof-reading passes over structure and prose that preserve
  Obsidian syntax.
- **Curate context** -- mine a corpus for its terminology and maintain a `CONTEXT.md` glossary
  (one file per context). Corpus-agnostic: code, vault, lore, or session logs.

## Vault Conventions

### Procedures Directory

Procedures are a kind of reference doc, so they live in the vault's reference directory.
`/add-procedure` finds it with `/discover-vault-directory *reference`.

A procedure file is a small collection of related procedures for one area (e.g. `git.md`,
`nix.md`), not necessarily one procedure per file. Entry format is defined per skill.

### Editing

The rules for every edit, starting with Obsidian syntax, live in [`HARD-RULES.md`](HARD-RULES.md).
The four proof-read skills link that file. Change a shared rule there, not in a skill.

## Dependencies

Scribe skills reference `/grill` from the `primitives` plugin for HITL coaching mechanics, and
`/discover-vault-directory` to find vault folders. Both plugins must be installed.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.
