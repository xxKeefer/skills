@CONTEXT.md

# xxkeefer-skills

A marketplace of personal skills for working with AI agents. Every skill is framework-agnostic,
language-agnostic, and tool-agnostic -- pure best-practice principles expressed as markdown
workflows.

## Domains

| Domain | Purpose | Always required? |
|---|---|---|
| `primitives` | Foundational skills other domains compose | Yes |
| `developer` | Engineering workflows -- investigation to closure | No |
| `journal` | Personal planner -- cascading goal/reflection system | No |
| `projects` | Long-running, goal-oriented project management -- workspaces, Kanban, journal bridge | No |
| `meta` | Skills about skills -- writing, auditing, lifecycle management | No |
| `omen` | Creative -- TTRPG, worldbuilding, narrative | No |
| `scribe` | Capture procedures, edit notes, curate glossaries, teach topics | No |
| `nix-manager` | NixOS config management -- add, remove, rice, refine | No |
| `utility` | Dev-environment setup -- pre-commit hooks, git guardrails | No |
| `experimental` | Skills on probation -- promote when usage justifies, else demote | No |
| `deprecated` | Skills awaiting a keep/kill decision before deletion | No |

## Architecture

Each domain is an independent plugin in the `xxkeefer-skills` marketplace. Domains are versioned
separately and can be enabled/disabled independently. The `primitives` domain is a prerequisite
for all others -- it provides foundational skills (like `/grill-it`) that other domains compose.

Top-level layout:

| Path | Holds |
|---|---|
| `skills/` | The domain plugins (one directory per domain). Sources in `marketplace.json` point here (`./skills/<domain>`). |
| `hooks/` | Claude Code hook holders (e.g. `tool-policy`) -- installable guardrails, not skills. |
| `scripts/` | Supporting tooling a skill depends on but doesn't ship inline (e.g. `obsidian/` -- the journal's Templater scripts and templates). |
| `output-styles/` | Claude Code output styles (e.g. `Terse.md`). |
| `.claude-plugin/` | The marketplace registry (`marketplace.json`). |

The root owns only the registry and shared documentation (`README.md`, `CLAUDE.md`, `CONTEXT.md`).
No skills live at root -- they all live under `skills/`.

## Skill Maturity

New skills land in `experimental` and earn their way into a stable domain, or fall through to
`deprecated` and eventual deletion. **All moves are manual** — a deliberate human decision, not an
automated rule:

- **Promote** (`experimental` → stable domain): when a skill has proven its worth in real use, move
  it into the domain it belongs to and bump that domain's version.
- **Deprecate** (any domain → `deprecated`): when a skill has gone cold or its value is in doubt,
  move it here rather than deleting outright.
- **Delete** (`deprecated` → gone): once you're confident the skill is genuinely unused. Git history
  is the archive.

## North Star

Everything-agnostic. Skills encode *how to think about problems*, not how to use specific tools.
A skill should work equally well whether you're writing Rust, TypeScript, Python, or anything
else. No framework lock-in, no language assumptions, no tool dependencies beyond the agent itself.
