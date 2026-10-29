# Primitives

Foundational skills that other domains compose. These are cross-cutting building blocks, not
opinionated workflows. Every other domain in this marketplace depends on primitives being
installed.

## Design Principles

- **Base layer**: Depends on no other domain
- **Domain-agnostic**: No assumptions about what kind of work is being done
- **Minimal**: Each primitive does one thing well

## Skills

`Used by` lists every skill in this repo whose `SKILL.md` names the primitive as `/<name>`.

| Skill | Purpose | Used by |
|---|---|---|
| `/grill` | Relentless questioning until shared understanding | do-next, developer:diagnose, developer:grill-with-docs, developer:improve-codebase-architecture, meta:write-a-hook, meta:write-a-skill, projects:new-project, projects:promote-card, deprecated:spike, deprecated:triage, deprecated:wayfinder |
| `/write-to-file` | Write output files to `.ai/`, or the user's folder for the doctype, for `@`-reference | handoff, tabular-analysis, developer:codebase-news, developer:diagnose, meta:write-a-skill, utility:set-up-dev-workflow-skills |
| `/look-up` | Fetch and ingest resources (files, web, tracker tickets, wiki pages) | tabular-analysis, developer:diagnose, developer:fix, developer:happy-path, developer:resolve-conflicts, developer:tweak, scribe:add-procedure, scribe:triage-notes, deprecated:spike |
| `/explain` | Layered what/how/why explanation of any target | nix-manager:explain, deprecated:explain-reasoning |
| `/caveman` | Ultra-compressed communication mode (~75% fewer tokens) | the user only |
| `/handoff` | Compact the conversation into a handoff doc for a fresh agent | the user only |
| `/update-handoff` | Update a handoff/plan doc in place with current progress | do-next |
| `/do-next` | Cold-start from a handoff/plan doc and execute the next step | projects:promote-card |
| `/tabular-analysis` | Compare concepts in a markdown table with the user's exact columns, one row each | experimental:lobotomize |
| `/discover-vault-directory` | Find a folder in the Obsidian vault by glob and marker files | projects:new-project, scribe:add-procedure, scribe:take-a-note, scribe:triage-notes |
