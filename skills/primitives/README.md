# Primitives

Foundational skills that other domains compose. Always install this domain.

## Skills

| Skill | Purpose |
|---|---|
| `/grill` | Relentless questioning until shared understanding is reached |
| `/write-to-file` | Write output files to `.ai/`, or the user's folder for the doctype, for later `@`-reference |
| `/write-report` | Write an HTML report whose ticks build a prompt to copy, and return its `file://` URL. A re-run adds a run to the same file |
| `/look-up` | Fetch and ingest resources (files, web, tracker tickets, wiki pages) |
| `/explain` | Layered what/how/why explanation of any target |
| `/show-me` | Show a topic or a diff as the smallest visual that makes the point |
| `/caveman` | Ultra-compressed communication mode (~75% fewer tokens) |
| `/update-plan` | Update a plan doc in place with current progress |
| `/do-next` | Cold-start from a plan doc and execute the next step |
| `/checkpoint` | Stop at a safe point: one `wip:` commit and a resume note in the plan |
| `/sitrep` | Show the open decisions, the choices made alone, the skipped steps, and the follow-ups of a plan |
| `/tabular-analysis` | Compare concepts in a markdown table with the user's exact columns, one row each |
| `/discover-vault-directory` | Find a folder in the Obsidian vault by glob and marker files |
| `/roleplay` | Play a narrative scene in character from `🎬 ACTION! 🥸` to `OK_STOP`, then debrief what the play surfaced |
| `/simulate` | Stand in for a technical system from `⚙️ RUNNING! 🧪` to `OK_STOP`, then debrief where the render cheated |
| `/sharpen` | Rewrite a prompt to go deeper, not wider, with the same task |

## Installation

```json
{
  "enabledPlugins": {
    "primitives@xxkeefer-skills": true
  }
}
```

This domain is a prerequisite for all other domains in the marketplace.
