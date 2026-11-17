# `.ai/`

Working files for work in flight: maps, specs, plans, findings, reports, and decision logs. Git
tracks this folder, and the repo is public. Keep it small. A file earns its place only while an
open unit of work reads it.

## What stays

- A map with at least one unit that has no tick.
- The spec, plan, findings, and decision log of a unit whose PR is not merged.
- A report whose rows the user has not ticked yet.

Everything else goes.

## When to clean up

- **At the start of each unit**, before its first commit: delete each file of a unit whose PR is
  merged. Make the deletion the first commit on the new branch.
- **Before each push**: delete every `scratch` file. A scratch file never reaches the remote.
- **When a report is acted on**: delete it. Its fixes are in the commits.
- **When a map has a tick on every unit**: delete the map in the same PR as its last unit.
- **When the user asks for a groom**: apply every rule above to the whole folder at once.

Delete with no stop. Each file here is the agent's own working output, and git history is the
archive. List the deleted files in the reply.

## Before you delete

Move a fact that must outlive the work out of `.ai/` first:

- A decision about the repo: an ADR in `docs/adr/`.
- A term: `CONTEXT.md`.
- A lesson about a skill: `/retro`, so that it becomes a skill edit.

## Rules for each file

- One file for one piece of work. Edit it in place. Never keep a copy, a `-v2`, or an old version.
- No employer names, ticket keys, or other work facts. The scrub hook checks this folder too.
- No secrets, tokens, or machine-only paths that a reader on another machine cannot use.
