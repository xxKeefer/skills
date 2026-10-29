# 0006 One skill list per domain

**Status:** Accepted, 2026-10-29

## Context

Three files listed the skills of each domain: the domain `README.md`, the domain `CLAUDE.md`, and
the root `README.md`. A move between domains edited five files. On 2026-10-26 the root list missed
8 skills. `/write-a-skill` had no step that added a new skill to any list.

On 2026-10-29 all three lists matched the skill folders, but the copies differed in other ways:

- 18 rows used different words for the same skill in `CLAUDE.md` and `README.md`.
- `primitives/CLAUDE.md` had a `Used by` column, a hand copy of a grep. Each new caller edited and
  bumped `primitives`. On 2026-10-29, four commits bumped it for this column alone.
- `nix-manager/CLAUDE.md` had a `Mode` column, HITL or AFK, which copied each skill's
  `disable-model-invocation` flag.
- `scribe/CLAUDE.md` marked `proof-read` as HITL, but `proof-read` is model-invoked.
- `developer/CLAUDE.md` had a workflow diagram that omitted 6 of its 16 skills.
- The `utility` description in `marketplace.json` and `plugin.json` listed five of its seven
  skills.

## Decision

- **One table.** Each domain `README.md` holds the only table of its skills. Its rows stayed as
  written.
- **CLAUDE.md for maintainers.** Each domain `CLAUDE.md` keeps its rules for maintainers. Its
  `## Skills` section links the `README.md`.
- **Root lists domains.** The root `README.md` lists each domain with its purpose and a link to the
  domain `README.md`. It names no skills.
- **No `Used by` column.** Before a rename, a maintainer searches every Markdown file under
  `skills/` for `/<name>`. `primitives/CLAUDE.md` says so.
- **Frontmatter decides invocation.** The `Mode` column and the HITL marks are gone.
- **No workflow diagram.** The `Phase` column in `developer/README.md` gives the order of the
  developer skills.
- **Descriptions name a purpose.** The `utility` description names the kinds of asset its
  installers set up, not the skills.
- `/write-a-skill`, `/write-a-hook`, `/migrate-a-skill`, and `/retire-a-skill` edit the domain
  `README.md` table only. `/write-a-skill` gained a step that adds the row.

Options not chosen:

- Keep the three lists, and add a pre-commit check that compares each table with
  `ls skills/<domain>/skills/`. The duplication stays, and a script polices it.
- Keep the three lists with no check.
- Move the `Used by` column into the `README.md` table. Each new caller still edits `primitives`.
- Redraw the developer workflow diagram with all 16 skills, in either file. ADR 0002 found that the
  user does not forget which developer skill to use.

## Consequences

- A move between domains edits two `README.md` files and two `plugin.json` files.
- A new caller of a primitive does not edit `primitives`.
- A rename search must also cover format files, such as the omen `SETTING-FORMAT.md`, which calls
  `/discover-vault-directory` for nine omen skills. A search of every Markdown file covers them.
