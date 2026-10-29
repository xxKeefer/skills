# Scribe

Knowledge work over a corpus -- primarily the user's Obsidian vault, but the context-curation
skills (`define-*`) work against any corpus, including code repos. Vault-bound skills run from the
vault root. "Vault" = the Obsidian vault.

The domain covers three jobs:

- **Capture** utilitarian procedures -- terse, repeatable how-tos for chores the user wants to
  offload and forget (distinct from `02-research/` deep-dives and `00-notes/` fleeting thoughts).
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

| Skill | Purpose |
|---|---|
| `/add-procedure` | Capture a just-solved task into the best-fit procedure file (or a new one) |
| `/proof-read` | HITL -- four gated passes over one document (structure, Grice, STE, Orwell), ends with an edit table |
| `/asd-ste100` | Proof-read one document against ASD-STE100 Simplified Technical English, in a chosen mode |
| `/grices-maxims` | Proof-read one document against Grice's maxims: what it says, leaves out, and implies |
| `/orwells-six` | Proof-read one document against Orwell's six rules from "Politics and the English Language" |
| `/define-concept` | Mine a corpus for one concept's terms, verify term-by-term, write a CONTEXT.md |
| `/define-term` | Add a single term to a CONTEXT.md under a user-specified section |
| `/define-language` | Compare a conversation against a CONTEXT.md, propose restrained edits/additions |
| `/triage-notes` | HITL -- triage one fleeting inbox note: promote, taskify, or archive on approval |
| `/take-a-note` | Capture something from the conversation as a fresh note in vault 00-notes/ |
| `/teach` | Teach a topic over multiple sessions in a stateful workspace |
