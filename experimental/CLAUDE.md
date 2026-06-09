# Experimental

Personal skills on probation. A holding domain for recently-created skills whose long-term home
and value aren't yet decided.

> Named `experimental` here; the work marketplace uses `new` for the same role so the two plugins
> don't collide when both marketplaces are installed.

## Lifecycle

- **Entry**: any freshly-authored personal skill lands here first.
- **Promotion**: once a skill proves its worth in real use (a manual call — see root CLAUDE.md),
  move it into the appropriate stable domain (`primitives`, `developer`, `meta`, …).
- **Demotion**: if a skill stops being used or proves low-value, move it to `deprecated`.

## Skills

| Skill | Purpose |
|---|---|
| `/define-concept` | Mine a concept's terminology, verify term-by-term, write a glossary section |
| `/define-term` | Add a single term to the glossary under a user-specified concept |
| `/update-language` | Audit a conversation against the glossary, propose restrained edits |
| `/tabular-analysis` | Compare/contrast concepts in a markdown table with exactly the user's pipe-split columns |

The glossary three are a cohort — they reference each other by name and share the glossary-location lookup.
Migrated from the work marketplace's `maintain` plugin (generic, no Megaport coupling). Promote them
together into a stable domain (likely `maintain`-equivalent or `meta`) once they earn it.
