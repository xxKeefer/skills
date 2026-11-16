@CONTEXT.md

# xxkeefer-skills

A marketplace of personal skills for working with AI agents. Every skill is framework-agnostic,
language-agnostic, and tool-agnostic -- pure best-practice principles expressed as markdown
workflows.

## Architecture

Each domain is an independent plugin in the `xxkeefer-skills` marketplace. Domains are versioned
separately and can be enabled/disabled independently. The `primitives` domain is a prerequisite
for all others -- it provides foundational skills (like `/grill`) that other domains compose.

Installable assets, such as hooks, the status line, output styles, and rules, live inside their
`utility` installer skill, so they ship with the plugin. The root owns only the registry, the commit
hook, and shared documentation. No skills live at root -- they all live under `skills/`.

`.githooks/` holds the scrub check: a pre-commit hook, its public pattern file, and its tests
(`sh .githooks/pre-commit_test.sh`).

## Skill Lifecycle

A skill has a dated lifecycle ([ADR 0017](docs/adr/0017-dated-skill-lifecycle.md)). Each move is a
human decision:

- **Add:** a new skill lands in the domain that it belongs to.
- **Deprecate:** when a skill falls out of use, run `/retire-a-skill`. It moves the skill to
  `deprecated` and writes `deprecated: <date>` into its frontmatter.
- **Delete:** run `skills/meta/skills/retire-a-skill/scripts/due.py`. It lists each deprecated
  skill that is more than 30 days old, with its count from the skill tally. Delete a listed skill
  with `/retire-a-skill`. Git history is the archive.

## North Star

Everything-agnostic. Skills encode *how to think about problems*, not how to use specific tools.
A skill should work equally well whether you're writing Rust, TypeScript, Python, or anything
else. No framework lock-in, no language assumptions, no tool dependencies beyond the agent itself.

There are two exceptions: the rules that `/install-rules` ships, and the `engineering` personas.
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
