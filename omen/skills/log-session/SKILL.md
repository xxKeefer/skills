---
name: log-session
description: >
  Log a game session to the campaign's session index. Takes a session log file, extracts date, game
  type, and summary, then appends a row to log.md. Use when user says "log session", "add session",
  "update the log", or has just finished a game and wants to record it.
---

# Log Session

Record a completed or in-progress session in the campaign's `log.md` index.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md:

1. Scan `02-omen/` in the vault for directories containing `log.md` and `lore/_cannon.md`
2. If multiple campaigns found, ask which one
3. If none found, ask the user where the campaign lives

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a session log file -- use it directly
- A session number -- find the matching file in the campaign's `logs/` directory
- Nothing -- list existing logs and ask which session to log, or ask if this is a new session

Read the session log file. If it doesn't exist yet, ask:
> Is this a new session? I'll create the log file -- what number is it?

## Step 3: Extract Session Details

From the session log file (or user input for new sessions), determine:

- **Date** -- from frontmatter, file content, or ask the user. Format: `DD-MM-YYYY`
- **Session reference** -- wikilink to the log file, e.g. `[[omen-crown_season_two-3]]`
- **Game type** -- one of: Transition, Continuation, Fork, Climax, Reflect. Infer from content or ask
- **Summary** -- one sentence capturing the key narrative beat. Keep it punchy and spoiler-aware

If any detail can't be inferred, ask. Don't guess game types -- they matter for canon weight.

## Step 4: Read the Current Log Index

Read the campaign's `log.md`. It contains a markdown table:

```markdown
| Date       | Session       | Type         | Summary                          |
| ---------- | ------------- | ------------ | -------------------------------- |
| 01-01-2026 | [[example-1]] | Transition   | The adventurers set out          |
```

## Step 5: Append the Entry

Add a new row to the table in `log.md` maintaining the existing column alignment. Place it after
the last populated row but before any trailing empty row.

## Step 6: Update Session Log Frontmatter

If the session log file exists, ensure its frontmatter has correct `prev`/`next` links:

- Set `prev` to the previous session's wikilink
- Update the previous session's `next` to point to this one

## Step 7: Confirm

> **Logged.** {session reference} added to {campaign} log -- {type}: {summary}

If this was a new session and the log file doesn't exist yet, offer to create it:
> Want me to scaffold the session log file too?
