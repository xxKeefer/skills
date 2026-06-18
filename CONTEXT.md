# xxkeefer-skills — Context

**Last updated:** 2026-06-16

Shared terminology for the xxkeefer-skills marketplace. This is the repo-wide glossary; per-domain
concepts still live here rather than in their own `CONTEXT.md` files for now.

## The core model

> **A marketplace groups domains; each domain is a plugin that holds skills.**

The marketplace is the registry. Each domain inside it is an independently versioned plugin, and a
domain's value is the skills it ships. The `primitives` domain is special: its skills are the
foundation the others compose.

## Core Terms

### Marketplace

The top-level registry (`xxkeefer-skills`) that groups all domains. Configured as a local directory
source in Claude Code settings.

### Domain

A self-contained plugin within the marketplace. Has its own version, skills, and documentation, and
maps 1:1 to a plugin directory. Enabled and disabled independently of the others.

### Plugin

The Claude Code concept a domain maps to. Each domain directory carries a
`.claude-plugin/plugin.json`.

### Skill

A markdown-defined workflow in a domain's `skills/` directory, invoked via `/skill-name`.

### Primitive

A foundational skill in the `primitives` domain that other domains compose. Model-invocable and
named without the `*-it` suffix.

## Concepts & conventions

| Term | Definition |
| --- | --- |
| **HITL** | Human-in-the-loop. A skill or task that needs human judgment, design review, or an architectural decision. Signalled by the `*-it` suffix. |
| **AFK** | Away-from-keyboard. A task fully specified for autonomous agent execution without human interaction. |
| **Vertical slice** | A unit of work that cuts through all layers end-to-end and is demo-able or verifiable on its own. |
| **Progressive disclosure** | Decomposing complex skills into composable primitives, so users engage at the level of abstraction they need. |
| **Everything-agnostic** | The north star: skills encode how to think about problems, not how to use specific frameworks, languages, or tools. |
| **Durability** | Issue content must survive radical codebase changes -- no file paths, domain language, behavioural criteria. |
| **Triage state** | Label-based state for GitHub issues: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. |
| **Agent brief** | A structured comment on AFK issues describing current/desired behaviour, key interfaces, acceptance criteria, and scope boundaries. |

## Domain terms

| Term | Definition |
| --- | --- |
| **Vault** | The user's Obsidian vault. Vault-bound scribe skills run from the vault root. |
| **Cascading goals** | Journal-domain mechanic: yearly goals feed monthly, monthly feed weekly, weekly feed daily. Each level is a backlog for the level below. |
| **Journal directory** | The vault directory containing `occasions.md` and all journal files. Discovered by scanning, never hardcoded. |
| **Projects directory** | The vault directory holding project workspaces (e.g. `05-projects/`). Discovered by scanning for `*projects`, never hardcoded. |
| **Project workspace** | A stateful per-project directory (MISSION, Kanban board, decisions log, notes), modelled on the `teach` skill. The workspace is the state. |
| **Milestone** | A dated project event written into the `occasions.md` Projects section so the journal surfaces it. Year-guarded, single-fire. Distinct from a goal. |
| **Project board** | A per-project obsidian-kanban file (`<slug>.kanban.md`): headings as columns, checkboxes as cards. Edited manually; skills only read it. |
| **Projects-to-journal bridge** | The one-way v1 interface: projects push milestones into `occasions.md`; the journal stays unaware of project schema. |
