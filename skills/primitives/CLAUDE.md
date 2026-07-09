# Primitives

Foundational skills that other domains compose. These are cross-cutting building blocks, not
opinionated workflows. Every other domain in this marketplace depends on primitives being
installed.

## Design Principles

- **Composable**: Primitives are invoked by other skills, not typically by users directly
- **Domain-agnostic**: No assumptions about what kind of work is being done
- **Minimal**: Each primitive does one thing well

## Skills

| Skill | Purpose | Used by |
|---|---|---|
| `/grill` | Relentless questioning until shared understanding | spike, research, write-a-skill, experimental:diagnose |
| `/write-to-file` | Write output files to `.ai/` for `@`-reference | to-plan, research, scratch docs |
| `/look-up` | Fetch and ingest resources (files, web, tracker tickets, wiki pages) | spike, research, to-plan, to-tickets |
| `/explain` | Layered what/how/why explanation of any target | developer:explain-reasoning, nix-manager:explain |
| `/caveman` | Ultra-compressed communication mode (~75% fewer tokens) | invoked directly by the user |
| `/handoff` | Compact the conversation into a handoff doc for a fresh agent | invoked directly by the user |
| `/update-handoff` | Update a handoff/plan doc in place with current progress | invoked directly by the user |
| `/do-next` | Cold-start from a handoff/plan doc and execute the next step | invoked directly by the user |
| `/tabular-analysis` | Compare concepts in a markdown table with the user's exact columns, one row each | invoked directly by the user; composes look-up, write-to-file |
