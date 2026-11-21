---
name: act-on-broadsheet
description: >
  Apply the rows that the user chose on a broadsheet page to the vault: move, archive, or delete a
  note, set a project's status, tick or carry a goal, edit a template, or add to a want list. Writes
  each veto and snooze to the broadsheet memory. Asks before each delete, and reports each change. Use when the user pastes the prompt that a
  broadsheet page builds.
disable-model-invocation: true
argument-hint: "<prompt from the broadsheet page>"
---

# Act on Broadsheet

Apply the choices that the user made on a `/broadsheet` page, from its vault maintenance prompt.
The choices are the approval, so this skill asks no question, except before a delete. The page's
skill suite prompt is not for this skill: it goes to `/engineering:spec`.

Write as a secretary: do what each row says, and report it. No coaching. Commit nothing in the
vault.

## Step 1: Parse the prompt

`$ARGUMENTS` holds the prompt that the page builds:

```text
/journal:act-on-broadsheet
Edition: <paper name> · <date>
Rows (id | choice | section | row | comment):
- letters:<inbox folder>/<note>.md | do | letters | <note title> 3 days Why: a recipe. Do: move the note to <folder>.
- the-board:<project> | comment | the-board | <project> ... | comment: set it to waiting until March
```

1. With no row line, stop. Say to pick a choice or write a comment on a broadsheet page, and paste
   the prompt that its bar copies.
2. For each line that starts with `- `, drop the `- `. Split the rest on ` | ` only three times:
   the first three fields are the `id`, the `choice`, and the `section`. The rest is the row text.
   If the rest holds ` | comment: `, the text after its first match is the `comment`, and the text
   before it is the row text. Row text that holds ` | ` stays whole.
3. The `id` is `<section>:<target>`. The target is the part after the first `:`. Decode the
   target: `%20` is a space and `%7C` is a `|`. Find the note by the decoded target. Keep the `id`
   as written, encoded, for the memory in Step 5.
4. The `choice` is one of `do`, `veto`, `snooze`, `done`, or `comment`, which means the row has a
   comment and no choice.

**Done when:** each row line gives an id, a target, a choice, a section, the row text, and a
comment or none.

## Step 2: Find the vault

1. Find the journal folder with `/discover-vault-directory * holding occasions.md`. The vault root
   is its parent.
2. Find each folder that a row needs, by glob and never by a fixed path: the archive with
   `/discover-vault-directory *archive`, the projects folder with
   `/discover-vault-directory *projects`, and the templates with
   `/discover-vault-directory *meta/templates`.
3. Read the page: the `*-broadsheet.html` file in the journal folder whose `<title>` matches the
   `Edition` line. Find each row by its `data-id`, and read its full `Do:` text and its links.
   With no page, use the row text in the prompt.

**Done when:** you have the vault root, each folder that the rows need, and the full action of
each row.

## Step 3: Sort the rows

Sort each row by its choice:

| Choice | What to do |
| --- | --- |
| `do` | Apply the row's `Do:` action. A comment changes or narrows it |
| `comment` | Apply the comment as the action for the row's target |
| `done` | The user did it already. Only the ledger and the board offer it. Tick the goal or the card that the row names, if it is open. Else change nothing |
| `veto` | Write the row to the memory in Step 5. Change nothing else |
| `snooze` | Write the row to the memory in Step 5, until the date in the comment. With no date in the comment, until 4 weeks from today. Change nothing else |

When a row and its comment leave a choice between two actions, ask the user which, and wait. When
a row's action names no file in the vault, such as a change to the routine, change nothing and say
so in the report.

**Done when:** each row has one action, or no change and its reason.

## Step 4: Ask before a delete

List each row whose action deletes a note, with its path and its reason:

> These notes go for good:
> 1. `<path>`: 400 days in the archive, no link from outside it
>
> Delete them? `all`, `none`, or numbers.

Delete only the notes that the user names. A note that the user keeps gets no change. With no
delete row, ask nothing.

**Done when:** each delete row has a yes or a no from the user, or there is no delete row.

## Step 5: Apply the rows

Apply each row in prompt order. Read each file before you edit it, and edit only the lines that
the action names.

- **Move** a note: move it to the folder that the action names. Make the folder if it does not
  exist.
- **Archive** a note: move it into the archive folder, under the same path that it had below the
  vault root.
- **Delete** a note: delete it, only after the yes of Step 4.
- After a move, an archive, or a delete, search the vault for links that name the note by its path,
  and fix each one. A link by name alone still works after a move.
- **Folder change** from the floor plan, such as a merge, a rename, or new subfolders: make the
  change, and fix the links as for a move.
- **Project status:** set `status:` in the project's `MISSION.md` frontmatter to `active`,
  `dormant`, `waiting`, or `archived`. Set `until:` when the action or the comment gives a date,
  and remove it when the status is `active`.
- **Goal** from the ledger: tick it, carry it to the next file at its level, or drop it, as the
  action says. Follow [`CASCADE.md`](../../CASCADE.md).
- **Template edit** from the editorial: edit the template that the action names in the templates
  folder.
- **Want list:** add the item to the end of the list in the note.
- **Veto** or **snooze**: append one line to `broadsheet-memory.md` in the journal folder. Make the
  file if it does not exist. Change no other line in it. The line is `<id> | veto`, or
  `<id> | snooze until <YYYY-MM-DD>`, with the full `id` of the row, encoded as the prompt gives
  it. `/broadsheet` then leaves out the row: for good after a veto, and to the end date after a
  snooze. A comment that gives a day without a year gives the next such day.

When an action fails, such as a missing note, change nothing for that row, and give the reason in
the report.

**Done when:** each row is applied, or has a reason that it is not.

## Step 6: Report

Reply with one line for each row, in prompt order:

```text
- letters:<path> | do | moved <old path> -> <new path>, fixed 2 links
- the-morgue:<path> | do | kept: you said no to the delete
- the-board:<project> | comment | set status to waiting, until 2027-03-01
- editorial:<slug> | do | no change: the action names no file
- stale-shelf:<path> | veto | muted for good in broadsheet-memory.md
- letters:<path> | snooze | muted until 2026-12-20 in broadsheet-memory.md
```

End with the count of notes moved, archived, deleted, and edited, and of rows muted.

**Done when:** each row of the prompt has one line in the report.
