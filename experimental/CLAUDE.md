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
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/patch-doctor` | Diagnose and fix drift between a skill's current output contract and the artifacts it already produced |
| `/debrief` | Human-readable session debrief dropped into vault 00-raw/: done, next steps, teach-yourself |
| `/take-a-note` | Capture something from the conversation: append to a given note (style-matched) or drop a fresh note in vault 00-raw/ |
