---
name: new-project
description: >
  Scaffold a stateful project workspace for long-running, goal-oriented work in Obsidian. Grills for
  the mission, then creates the directory with a MISSION file, an obsidian-kanban board, and a
  decisions log. Use when the user says "new project", "start a project", "scaffold a project", or
  wants to begin tracking a long-running goal.
---

# New Project

Bootstrap a stateful project workspace. The workspace is the state -- a mission, a board, and a
decisions log that persist across sessions, modelled on the `teach` skill.

## Step 1: Discover the Projects Directory

Find the vault's projects directory per the convention in the domain `CLAUDE.md`: scan the vault
root for a directory matching `*projects` (e.g. `05-projects/`). If none is found, ask the user where
projects live and store the path to memory. Never hardcode the path.

## Step 2: Clarify the Mission

Check `$ARGUMENTS` for a project name and any seed description. Then invoke `/grill-it` to pin down
the mission before scaffolding -- a vague mission produces a useless project. Probe only what's
unclear:

- **Why** -- the concrete real-world outcome. Push past "sort out X" to the actual result.
- **Definition of done** -- the observable conditions that make this complete.
- **Constraints** -- deadline, budget, dependencies, people involved.
- **Out of scope** -- adjacent work this project will not do.
- **Seed tasks** -- any tasks already known, to seed the board's Backlog.

Resolve everything in-session. Do not carry open questions into the workspace.

Derive a **slug** (kebab-case) from the project name for the directory and board filename.

## Step 3: Confirm Structure

Present what will be created:

> **Scaffolding: {Project Name}**
>
> ```
> {projects-dir}/{slug}/
>   MISSION.md
>   {slug}.kanban.md
>   decisions/
>   tasks/
>     _template.md
>   NOTES.md
> ```
>
> Proceed?

If a directory for the slug already exists, stop -- this is an existing project. Offer
`/project-status` instead.

## Step 4: Create the Workspace

Create `{projects-dir}/{slug}/` and write each file against its format contract:

- `MISSION.md` -- per [MISSION-FORMAT.md](MISSION-FORMAT.md), filled from the grill.
- `{slug}.kanban.md` -- per [BOARD-FORMAT.md](BOARD-FORMAT.md). Seed the Backlog with any known
  tasks; leave This Week / Doing / Done empty (Done keeps its `**Complete**` marker). Set
  `new-note-folder` to `{projects-dir-from-vault-root}/{slug}/tasks` and `new-note-template` to
  `{projects-dir-from-vault-root}/{slug}/tasks/_template.md` in the `%% kanban:settings %%` block.
- `decisions/` -- create the directory empty (records are added later as choices arise). If the
  grill surfaced a foundational decision, write `decisions/0001-*.md` per
  [DECISIONS-FORMAT.md](DECISIONS-FORMAT.md).
- `tasks/` -- create the directory and write `tasks/_template.md` per [NOTE-FORMAT.md](NOTE-FORMAT.md).
  This is where obsidian-kanban drops new notes created from cards.
- `NOTES.md` -- an empty scratchpad with a `# {Project Name} -- Notes` heading.

## Step 5: Confirm and Offer Next Steps

Report what was created and the board's seeded tasks. Then ask:

> Workspace ready. Want to:
> 1. **Schedule goals** -- push milestones into the journal via `/schedule-goals`
> 2. **Add tasks** -- you fill the board manually in Obsidian
> 3. **Done** -- start later

Do not write to the board after scaffolding -- card management is manual from here.
