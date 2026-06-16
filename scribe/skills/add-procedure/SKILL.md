---
name: add-procedure
description: >
  Capture a just-solved task into the vault's procedures directory as a terse, repeatable how-to.
  Mines the current conversation for the steps, picks the best-fit procedure file (or starts a new
  one), and writes a consistent entry. Use when the user says "add procedure", "record this",
  "save this how-to", "runbook this", "I'll need to do this again", or just solved a fiddly task
  worth capturing.
---

# Add Procedure

Offload a chore into the vault: capture the steps once so the task is repeatable and the brain can
forget it. Procedures are utilitarian -- distinct from `03-knowledge/` deep-dives and `04-notes/`
fleeting thoughts.

## Step 1: Discover the Procedures Directory

Find the vault's procedures directory per the convention in the domain `CLAUDE.md`: scan the vault
root for a directory matching `*procedures` (e.g. `07-procedures/`). If none is found, ask the user
where procedures should live, create it, and store the path to memory. **Never hardcode the path.**

**Done when:** you have the procedures directory path.

## Step 2: Gather the Procedure

Get the content of the task being captured:

- **Default -- mine the conversation.** If this session just solved a task, reconstruct it: the
  goal, the ordered steps actually taken, the commands run, and any gotchas or dead-ends hit along
  the way. Strip false starts; keep what a future run needs.
- **Fall back -- ask.** If there's no session to mine (fresh context, or the user invoked cold),
  ask them to paste or describe the procedure.

Resolve any links the procedure references via `/look-up` so captured commands/URLs are accurate.

**Done when:** you have the goal, the steps, and the gotchas for one procedure.

## Step 3: Assign a File

Scan the procedures directory. For each existing procedure file, read its title and `##` headings to
model what area it covers. Then decide placement:

- **Best-fit file found** -- append the new entry to it. No prompt.
- **No good fit** -- propose a new procedure file (`<area>.md`, slug derived from the topic) and
  confirm with a **single yes/no**. Never ask the user to define an area's boundary or scope.

If the user rejects the proposed name, take their alternative and proceed.

**Done when:** you know the target file (existing or newly named) and whether it's an append or a
new file.

## Step 4: Write the Entry

Format the entry per [PROCEDURE-FORMAT.md](PROCEDURE-FORMAT.md):

- **Terse by default** -- title, optional one-line *when/why*, numbered steps, gotchas as callouts.
- **Long-form** only when the capture is genuinely complex (mental model, phases, known issues,
  lessons).
- **New file** -- add the frontmatter from the template, then the entry.
- **Append** -- add the `##` entry under the existing content; leave frontmatter untouched.

Match the terseness of the user's existing entries. Do not pad.

**Done when:** the entry is written to the target file.

## Step 5: Confirm

Report what was captured and where:

> **Captured `<Title>`** -> `<file>` (`<new file>` / appended)
>
> {one-line recap of the entry}

If a new file was created, mention it so the user knows a new area now exists.

**Done when:** the user has seen what was written and where.
