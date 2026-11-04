@CONTEXT.md

# xxkeefer-skills

A marketplace of personal skills for working with AI agents. Every skill is framework-agnostic,
language-agnostic, and tool-agnostic -- pure best-practice principles expressed as markdown
workflows.

## Domains

| Domain | Purpose | Always required? |
|---|---|---|
| `primitives` | Foundational skills other domains compose | Yes |
| `implement-code` | Engineering workflows -- ticket to PR | No |
| `dev-personas` | Persona code reviewers, the `mob-review` panel that runs them, `update-personas`, `self-improve`, and the `sad-path` checklist | No |
| `journal` | Personal planner -- cascading goal/reflection system | No |
| `projects` | Long-running, goal-oriented project management -- workspaces, Kanban, journal bridge | No |
| `meta` | Skills about skills -- writing, auditing, lifecycle management | No |
| `omen` | Creative -- TTRPG, worldbuilding, narrative | No |
| `scribe` | Capture procedures, edit notes, curate glossaries, teach topics | No |
| `nix-manager` | NixOS config management -- add, remove, rice, refine | No |
| `utility` | Dev-environment setup -- pre-commit hooks, machine setup | No |
| `experimental` | Skills on probation -- promote when usage justifies, else demote | No |
| `deprecated` | Skills awaiting a keep/kill decision before deletion | No |

## Architecture

Each domain is an independent plugin in the `xxkeefer-skills` marketplace. Domains are versioned
separately and can be enabled/disabled independently. The `primitives` domain is a prerequisite
for all others -- it provides foundational skills (like `/grill`) that other domains compose.

Top-level layout:

| Path | Holds |
|---|---|
| `skills/` | The domain plugins (one directory per domain). Sources in `marketplace.json` point here (`./skills/<domain>`). Installable assets, such as hooks, the status line, output styles, and rules, live inside their `utility` installer skill, so they ship with the plugin. |
| `scripts/` | Supporting tooling a skill depends on but doesn't ship inline (e.g. `obsidian/` -- the journal's Templater scripts and templates). |
| `.claude-plugin/` | The marketplace registry (`marketplace.json`). |
| `.githooks/` | The scrub check: a pre-commit hook, its public pattern file, and its tests (`sh .githooks/pre-commit_test.sh`). |

The root owns only the registry, the commit hook, and shared documentation (`README.md`,
`CLAUDE.md`, `CONTEXT.md`).
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

There are two exceptions: the rules that `/install-rules` ships, and the `dev-personas` reviewers.
A rule is an opinionated convention for one file type, and a persona reviews one lane of a diff,
so both name languages, frameworks, and tools. Neither names employer or client code.

A skill does not restate an employer's internal docs, even with the names removed. No regex
checks this rule, so it binds whoever imports a skill. The pre-commit hook checks only the names.

## Agent skills

### Issue tracker

Issues are cards on the `agentic-skills` Obsidian Kanban board in the vault. See
`docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one `CONTEXT.md` at the repo root; ADRs go in `docs/adr/`. See
`docs/agents/domain.md`.
