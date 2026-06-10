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
| `/grill-it` | Relentless questioning until shared understanding | spike-it, research-it, write-a-skill, experimental:hunt-it |
| `/write-to-file` | Write output files to `.ai/` for `@`-reference | plan-it, research-it, scratch docs |
| `/look-up` | Fetch and ingest resources (files, web, tracker tickets, wiki pages) | spike-it, research-it, plan-it, task-it |
| `/explain` | Layered what/how/why explanation of any target | developer:explain-it, nix-manager:explain |
| `/caveman` | Ultra-compressed communication mode (~75% fewer tokens) | invoked directly by the user |
| `/handoff` | Compact the conversation into a handoff doc for a fresh agent | invoked directly by the user |
