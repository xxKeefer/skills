# 0004 One skill finds vault folders

**Status:** Accepted, 2026-10-29

## Context

Skills in four domains find a folder in the Obsidian vault, and each domain wrote its own rule:

- `journal`: scan the vault for the folder that holds `occasions.md`. If none, ask, and store the
  path in agent memory.
- `projects`: the `*projects` folder at the vault root.
- `scribe`: the `*reference` folder at the vault root for `add-procedure`. `take-a-note` and
  `triage-notes` search the home folder for `.obsidian/`, then use `00-notes/`.
- `omen`: a hardcoded `07-omen/`, then campaign folders that hold `log.md` and `lore/_cannon.md`.

ADR 0002 chose one shared, model-invoked discovery skill and left its design and home to this
decision. An earlier design stalled on persistence. The user rejected agent memory, which can be
lost or can hold a stale answer.

## Decision

`primitives:discover-vault-directory` finds vault folders for every domain.

- **Home.** `primitives`. All four callers already depend on it. The "Domain-agnostic" principle
  of `primitives` is a rule of thumb, so it stays as written.
- **No persistence.** The skill scans on every run and stores nothing.
- **Vault root.** The first folder that holds `.obsidian/`, in this order: `~/studio/notes`, the
  current folder or its nearest parent, then a search of the home folder.
- **Interface.** One glob relative to the vault root, plus optional marker files after `holding`.
  The glob sets the scan depth. The skill returns the absolute path.
- **Matches.** On one match, the skill uses it. On many, it asks which one. On zero, it asks
  where the folder is.

Options not chosen:

- A "Folders" table in the vault `CLAUDE.md`, or a router file in `99-meta/`. On 2026-10-29 each
  folder glob matched one folder, so a store would hold answers to a question that is never asked.
- A home in `scribe`. `journal`, `projects`, and `omen` would then depend on `scribe`.
- A generic `find-directory` that knows nothing about vaults. Each caller would still find the
  vault root itself.
- The vault path only in the user's own instructions. The user chose the fixed path first because
  it is the fastest check on every machine they use.
- A `scan_root` parameter beside the match. Omen would need two calls, and a nested glob such as
  `*omen/*` does the same job in one.

## Consequences

- The skill holds the personal path `~/studio/notes` in a public repo. On another machine the path
  does not exist, and the skill moves to the next check.
- A caller passes a glob, not a folder name, so a renamed or renumbered vault folder needs no skill
  edit.
- `journal`, `projects`, and `scribe` gain the many-match question. Before, they assumed one match.
- Each domain moves to the skill in its own commit. `scribe:add-procedure` moved first.
