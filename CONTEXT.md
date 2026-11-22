# xxkeefer-skills — Context

**Last updated:** 2026-11-16

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

A foundational skill in the `primitives` domain that other domains compose. Named as a
straight descriptive kebab-case verb, like every skill in this repo.

## Concepts & conventions

| Term | Definition |
| --- | --- |
| **HITL** | Human-in-the-loop. An action that needs a yes from the user before it runs. The pause list in the `pause-list.md` rule marks the human stop: each action whose output another person reads. A skill can call a workflow skill with no stop (ADR 0016). `disable-model-invocation: true` now marks only the skills whose whole job needs the user's judgement, such as `retro`. (Formerly signalled on the skill by that flag, and before that by a `*-it` name suffix, dropped 2026-07.) |
| **AFK** | Away-from-keyboard. A task fully specified for autonomous agent execution without human interaction. |
| **Vertical slice** | A unit of work that cuts through all layers end-to-end and is demo-able or verifiable on its own. |
| **Progressive disclosure** | Decomposing complex skills into composable primitives, so users engage at the level of abstraction they need. |
| **Everything-agnostic** | The north star: skills encode how to think about problems, not how to use specific frameworks, languages, or tools. |
| **Tool role** | A kind of tool that a skill needs, such as the tracker, the code host, or the browser. A skill names the role, and the repo's `## Agent skills` block or the machine's `## Tools on this machine` block names the product. |
| **Principle** | One of the 24 pstack `principle-*` skills in `engineering`, each a short rule with `disable-model-invocation: true`. `/work-on` indexes them in five groups. The agent reads a principle by path before it applies it, and names it in the reply. |
| **Durability** | Issue content must survive radical codebase changes -- no file paths, domain language, behavioural criteria. |

## Domain terms

| Term | Definition |
| --- | --- |
| **Vault** | The user's Obsidian vault. Vault-bound scribe skills run from the vault root. |
| **Cascading goals** | Journal-domain mechanic: yearly goals feed monthly, monthly feed weekly, weekly feed daily. Each level is a backlog for the level below. |
| **Journal directory** | The vault directory containing `occasions.md` and all journal files. Discovered by scanning, never hardcoded. |
| **Projects directory** | The vault directory holding project workspaces (e.g. `04-projects/`). Discovered by scanning for `*projects`, never hardcoded. |
| **Project workspace** | A stateful per-project directory (MISSION, Kanban board, decisions log, notes), modelled on the `teach` skill. The workspace is the state. |
| **Project board** | A per-project obsidian-kanban file (`<slug>.kanban.md`): headings as columns, checkboxes as cards. Skills edit the board surgically — add, move, or tag a card, never reorder other cards or touch the settings block. The task notes behind the cards are fully skill-managed; `/do-next` and `/update-plan` already treat them as plans. |
| **Plan** | The working document that a fresh agent cold-starts from: steps with done lines, and a Progress section. `/do-next` runs its next step, and `/update-plan` records the run. In the vault, the task note (`tasks/{Card Title}.md`) that `/promote-card` writes from a card is a plan. It holds the grilled spec and a phased plan. (Formerly "handoff".) |
| **Handoff** | The act of writing `Progress` into a plan, so that a fresh agent can continue the work. `/checkpoint` does it when a session stops, and writes a plan when none exists. The word does not name the document. (The `/handoff` skill was deprecated 2026-11-17.) |
| **Phased plan** | The Plan section of a vault plan: numbered phases, each a vertical slice with a done line. `/do-next` runs one phase per session, and `/update-plan` records it in Progress. Every vault plan has one, even with a single phase. |
