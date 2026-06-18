---
name: close-project
description: >
  Close out a completed project. Marks the mission done, removes the project's milestone rows from
  occasions.md so it stops surfacing in the journal, and archives the workspace. Use when the user
  says "close project", "archive project", "we're done with X", or a long-running project has reached
  its goal.
---

# Close Project

End a project cleanly. The goal is reached (or abandoned) -- stop it cluttering the journal and tuck
the workspace away, intact, for the record.

## Step 1: Identify the Project

Check `$ARGUMENTS` for a slug or name. Otherwise discover the projects directory and list active
projects; ask which one.

Read `MISSION.md`. Show the definition of done and confirm:

> Closing **{Project}**. Done criteria:
> - {item} {met? / unmet?}
>
> Close it out? (use `abandoned` instead of `done` if it's being dropped, not finished)

Don't block on unmet criteria -- the user may close early. Just surface the gap.

## Step 2: Mark the Mission

Set `MISSION.md` frontmatter `status: done` (or `abandoned`). Append a one-line closing note with
the date under the mission body.

## Step 3: Strip Journal Injection

Discover the journal directory (scan for `occasions.md`). **Read-modify-write.** Remove this
project's rows from the `## Projects` section (match by the project label prefix). If that leaves the
Projects section empty, remove the section heading and its table too.

Then offer to run `/update-occasions-config` so the removed milestones drop out of
`vault_occasions.js`. Until that runs, already-generated journal files are unaffected -- which is
correct; closing a project shouldn't rewrite history.

## Step 4: Archive the Workspace

Move the project directory to an archive location within the projects directory:

```
{projects-dir}/{slug}/  ->  {projects-dir}/_archive/{slug}/
```

Create `_archive/` if it doesn't exist. Move, don't delete -- the workspace is the record.

## Step 5: Confirm

> Closed **{Project}** (`{done|abandoned}`):
> - Mission marked `{status}`
> - {n} milestone rows removed from `occasions.md`
> - Archived to `_archive/{slug}/`
> - {Ran / skipped} `/update-occasions-config`
