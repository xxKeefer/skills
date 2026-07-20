# Domain docs

This repo is **single-context**.

- **Glossary**: `CONTEXT.md` at the repo root — the shared terminology for the marketplace,
  its domains, and their concepts. Read it before working; propose additions via the scribe
  skills rather than editing ad hoc.
- **ADRs**: `docs/adr/` — does not exist yet; create it when the first architectural decision
  record is written. One decision per file, `NNNN-slug.md`.

## Consumer rules

- Skills that need domain language (`/improve-codebase-architecture`, `/diagnose`, `/tdd`,
  `/triage`) read `CONTEXT.md` first and use its terms verbatim.
- Respect ADRs in the area you're changing; record new decisions rather than silently
  reversing old ones.
