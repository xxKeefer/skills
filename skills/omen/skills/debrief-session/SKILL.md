---
name: debrief-session
description: List the post-session skills in the order to run them after a game.
disable-model-invocation: true
---

# Debrief Session

Point the user through the debrief of a finished game. The post-session skills are user-invoked,
so this skill cannot run them: it names each one, in order, for the user to type.

## Step 1: Show the Order

Take the session from `$ARGUMENTS`: a path, a wikilink, or a session number. Show this table, with
`{session}` replaced by that value. If `$ARGUMENTS` is empty, remove `{session}`, and each skill
asks for the session itself.

| # | Run | Writes |
| --- | --- | --- |
| 1 | `/log-session {session}` | A row in `log.md` |
| 2 | `/log-npcs {session}` | `lore/_npcs.md` |
| 3 | `/log-place {session}` | `lore/_places.md` |
| 4 | `/log-cannon {session}` | Canon events in `lore/_cannon.md`, linked to the NPCs and places from rows 2 and 3 |
| 5 | `/log-progression {session}` | Each character file in `characters/` |
| 6 | `/make-summary {session}` | A story retelling in `lore/_cannon.md`, after the events from row 4 |

Then say why the order matters: `/log-cannon` links the names that rows 2 and 3 add, and
`/make-summary` reads the canon events that row 4 adds.

**Done when:** the user has the table, with each command ready to copy.
