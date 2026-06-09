---
name: migrate-a-skill
description: >
  Move a skill from one domain to another within a skills marketplace repo, keeping docs,
  versions, and git history in sync. Usage: migrate-a-skill <skill-name> <to-domain>. Use when
  the user says "migrate a skill", "promote this skill", "move <skill> to <domain>", or
  "demote <skill> to deprecated".
argument-hint: "<skill-name> <to-domain>"
---

# Migrate a Skill

Move a skill cleanly between domains: relocate the directory, fix every doc that references it,
bump both domain versions, and land it as a single commit. Assumes a marketplace repo laid out
like this one — domains as plugin dirs, each with `skills/`, `README.md`, `CLAUDE.md`, and
`.claude-plugin/plugin.json`.

## Step 1: Resolve inputs

Parse `<skill-name>` and `<to-domain>` from the arguments.

- **Locate the skill.** Find `*/skills/<skill-name>/` under the repo root. That parent is the
  **source domain**.
  - Not found → stop, report it.
  - Found in more than one domain → ask the user which source domain to migrate from.
- **Validate the target.** `<to-domain>/.claude-plugin/plugin.json` must exist.
  - Missing → stop, report it. Do not invent a new domain here.
- **No-op guard.** Source domain == target domain → stop, nothing to do.

**Done when:** you have a confirmed source domain, target domain, and skill path.

## Step 2: Read what you're moving

- Read the skill's `SKILL.md` frontmatter — capture `name` and the `description`.
- Distil a one-line **Purpose** for the doc tables (≈10 words, present tense). Reuse the wording
  already in the source domain's skill table if it has a row for this skill.

**Done when:** you have the skill's display name (`/<name>`) and its Purpose line.

## Step 3: Move the directory

Use `git mv <source-domain>/skills/<skill-name> <to-domain>/skills/<skill-name>` so history is
preserved. If the skill ships supporting files (references, templates, scripts), they move with
the directory — confirm nothing the skill depends on lives outside its own folder.

**Done when:** the skill directory exists only under the target domain.

## Step 4: Update the docs

In **both** the source and target domains, edit `README.md` **and** `CLAUDE.md`:

- **Source domain** — remove the skill's row from the `## Skills` table.
- **Target domain** — add a row `| `/<name>` | <Purpose> |` to the `## Skills` table, keeping the
  table's existing ordering style.

Notes:
- If a doc has no skill table, skip that file and flag it in the summary rather than inventing one.
- A domain with no skills shows a `_None yet._` placeholder under `## Skills`. When adding the
  first row, replace the placeholder with the table; when removing the last row, restore it.
- Leave the root `CLAUDE.md` / `README.md` alone — they list domains, not skills.
- If the source-domain README has migration notes (e.g. experimental's "Migrated in from…"
  blurb) that named this skill, prune the stale reference.

**Done when:** no doc in the source domain still lists the skill, and both target docs do.

## Step 5: Bump versions

Minor-bump the `version` in `.claude-plugin/plugin.json` for **both** domains — the target gained
a skill, the source lost one (e.g. `1.2.0` → `1.3.0`).

**Done when:** both `plugin.json` versions are incremented.

## Step 6: Confirm, then commit

Show the user a summary before committing:

- Skill moved: `<skill-name>`, `<source>` → `<target>`
- Docs edited (list files)
- Version bumps (old → new for each domain)
- Proposed commit message (see below)

Pick the commit `type` from the direction of the move:

| Move | Type |
|---|---|
| into a stable domain (esp. from `experimental`) — a promotion | `feat` |
| into `deprecated` — a demotion | `chore` |
| any other lateral move | `refactor` |

Message shape — scope is both domains, lower-cased imperative subject, body explains the why:

```
<type>(<source>,<target>): migrate <skill-name> from <source> to <target>

<one or two lines: what the skill does and why it's moving>. Bump <source> to
<new>, <target> to <new>.
```

On confirmation, `git add` the moved directory, both READMEs, both CLAUDE.mds, and both
plugin.jsons, then commit. Do not push.

**Done when:** a single commit captures the move, doc edits, and version bumps.
