---
name: refine-task
description: >
  Refine a thin Kanban card into a full, context-grounded task note in the project's tasks/ folder.
  Equal parts plan-it and task-it but corpus-agnostic -- it reads the project's MISSION, decisions,
  and corpus to ground the task, whatever the project is about. Use when the user says "refine task",
  "refine this card", "flesh out this card", "turn this card into a note", or wants a board card
  worked up into something executable.
argument-hint: "[project slug and/or card text; omit to be asked]"
---

# Refine Task

Take a one-line Kanban card and work it up into a full task note in `tasks/` -- the card is the
handle on the board, the note is where the detail lives. This is project-level backlog refinement:
`plan-it`'s context-gathering and decomposition, `task-it`'s observable acceptance criteria, written
for a cold picker-upper in the spirit of `update-handoff`. **Corpus-agnostic** -- the MISSION tells
you whether this is code, research, writing, or anything else; never assume a codebase.

The note is the durable state. Read the workspace format contracts before touching anything:
[NOTE-FORMAT.md](../new-project/NOTE-FORMAT.md), [BOARD-FORMAT.md](../new-project/BOARD-FORMAT.md).

## Step 1: Locate the Workspace and Resolve the Card

1. Discover the projects directory per the domain `CLAUDE.md` (scan the vault root for `*projects`;
   never hardcode).
2. Identify the project: a slug in `$ARGUMENTS`, else the only project with recent activity, else
   ask. Confirm the workspace directory exists (`<projects-dir>/<slug>/`).
3. Read the board (`<slug>.kanban.md`). Identify the target card:
   - Card text/title in `$ARGUMENTS` -> match it.
   - Nothing given -> list the open cards (Backlog / This Week / Doing) and ask which one.
4. Note the card's **entry state**:
   - **Plain card** (`- [ ] Some task`) -- no note yet; you'll create one and link it.
   - **Already linked** (`- [ ] [[Some task]]`) -- a stub note exists in `tasks/`; you'll refine it
     in place (update-handoff style: preserve structure, fold in detail).
   - Record the card's **column** -- it sets the note's `status` (Backlog/This Week -> `todo`,
     Doing -> `doing`, Done -> `done`).

**Done when:** you have one target card, its column, and its entry state.

## Step 2: Gather Project Context

Ground the task in the project, not in assumptions. Read what bounds it:

- **MISSION.md** -- the why, definition of done, constraints, out-of-scope. This also tells you
  **what kind of work the project is**, which shapes everything below.
- **decisions/** -- constraints and prior choices the task must respect. Don't relitigate them.
- **NOTES.md** and **sibling task notes** -- surrounding context, related work, shared vocabulary.
- **The corpus the card points at** -- whatever the project works over. Resolve any references the
  card or mission lean on via `/look-up`: code paths, vault notes, URLs, tracker tickets, docs.
  Corpus-agnostic -- follow the references that exist, don't invent code where there is none.

**Done when:** you can state, grounded in the workspace, why this task exists and what doing it
involves.

## Step 3: Assess Depth

Not every card needs a full note. A card is **trivial** when its outcome is self-evident, it's a
single obvious action, and there's nothing to decompose or decide. If so, say:

> This card is self-explanatory -- a full note would be busywork. Want a light note (context +
> done-criteria only), or leave it as a board card?

Otherwise it warrants full refinement -- continue.

**Done when:** you and the user agree on light vs full refinement (or the card is plainly
substantial).

## Step 4: Draft the Task Note

Compose the note per [NOTE-FORMAT.md](../new-project/NOTE-FORMAT.md):

- **Context** (mandatory) -- one short paragraph: why the task exists and how it serves the mission.
  If you can't write it, the card isn't scoped enough to start -- flag that instead of guessing.
- **Acceptance Criteria** -- the definition of done as **observable, verifiable outcomes**, not
  implementation steps. Durable: outcomes and contracts over file paths, in the project's own domain
  language. When all boxes check, the card moves to Done.
- **Notes** -- the approach: the ordered plan or key considerations a cold picker-upper needs to
  start. Reference decisions and resources by link; **don't duplicate** what already lives in the
  workspace. Keep implementation prescription light -- enough to start, not a script.

Set frontmatter from the template: `status` from the card's column, `project: "[[<slug>.kanban]]"`.
The note's filename must equal the card title exactly -- the board links to it by name.

If refining an existing stub note, **edit in place**: preserve its structure and any content already
there, fold in the detail, update stale claims. Don't replace it wholesale.

**Done when:** the note is drafted (in memory) against the format contract.

## Step 5: Checkpoint

Present, tersely:

> **Card:** `<card text>` (`<column>`, `<entry state>`)
> **Note:** `tasks/<Card Title>.md` (`create` / `update in place`)
> **Board change:** `- [ ] <text>` -> `- [ ] [[<Card Title>]]` (only if not already linked)
>
> {the drafted note body}

Wait for approval. The user may adjust scope, criteria, or the title. **Nothing is written before
they OK it** -- this is the hard gate.

**Done when:** the user has approved the note and any board change.

## Step 6: Write

On approval:

1. **Write the note** to `<projects-dir>/<slug>/tasks/<Card Title>.md` (matching the board's
   `new-note-folder`). Create from `_template.md` if new; edit in place if it exists.
2. **Link the card on the board** if it was a plain card: edit only that one line,
   `- [ ] <text>` -> `- [ ] [[<Card Title>]]`, replicating obsidian-kanban's "New note from card".
   Leave every other line, the column structure, and the `%% kanban:settings %%` block byte-for-byte
   intact. This is the one board write this skill makes; if the card is already linked, skip it.
3. **Never commit** -- the vault's git is the user's to manage.

**Done when:** the note exists in `tasks/` and the card links to it.

## Step 7: Confirm

Report:

> **Refined `<Card Title>`** -> `tasks/<Card Title>.md` ({created | updated})
> Card linked on the board. {one-line recap of the criteria count / scope}

**Done when:** the user has seen what was written and where.

## Principles

- **Corpus-agnostic.** MISSION decides the medium. Don't assume code, tests, or a repo.
- **The note is the state.** Write it for someone with none of this conversation's context.
- **Ground, don't invent.** Every claim in the note traces to the mission, a decision, or the corpus.
- **Reference, don't duplicate.** Link decisions and resources; don't copy them into the note.
- **One surgical board write.** Linking the card mirrors the plugin's own action -- nothing else on
  the board changes. Card management stays manual.
- **Checkpoint is a hard gate.** No file is written before the user approves.
- **Straight quotes only**; em dashes and emojis fine (vault rule).
