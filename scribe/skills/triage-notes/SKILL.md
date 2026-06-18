---
name: triage-notes
description: >
  Triage a fleeting note out of the vault inbox: read it, decide whether it should be promoted to a
  stable note, turned into a task, or archived, then execute the move on your approval. Takes an
  optional note path; with no path it picks one inbox note at random. Use when the user says
  "triage notes", "triage my inbox", "process 00-notes", "clear the inbox", or hands you a note to
  sort.
argument-hint: "[optional path to a note; omit to pick one inbox note at random]"
---

# Triage Notes

Process one note out of the inbox. The inbox (`00-notes/`) is the user's -- this skill assists
their triage, it does not auto-promote. **Nothing moves without explicit approval at the
checkpoint (Step 4).** One note per run by design; run it again to take the next.

## Step 1: Locate the Inbox and Resolve the Target

1. Find the vault root: scan the home directory for a folder containing `.obsidian/`; first match
   wins. If none, warn and stop.
2. Find the inbox: the vault's fleeting-capture folder, conventionally `00-notes/`. Scan for it;
   never hardcode. If absent, ask the user where fleeting notes live.
3. Resolve the target:
   - **Path given in `$ARGUMENTS`** -- triage that note.
   - **No path** -- list `*.md` in the inbox, exclude `README.md` and any index files, pick **one
     at random**, and announce which one you drew.

**Done when:** you have exactly one note file to triage.

## Step 2: Read and Analyse

1. Read the **full** note.
2. Resolve any links it leans on via `/look-up` so the value judgement is based on real content,
   not a dangling reference.
3. Characterise it -- answer in one line each:
   - **What is it?** durable knowledge, a how-to, a term/concept, an actionable task, a half-formed
     thought, or noise.
   - **Is it still true / still wanted?** stale captures get archived, not promoted.
   - **What's the single most valuable thing in it?** if the note is mostly dross around one good
     nugget, the nugget is what gets promoted -- the rest goes.

**Done when:** you can state what the note is and what (if anything) is worth keeping.

## Step 3: Decide the Disposition

Pick exactly one. Routing is by what the note *is*:

| Disposition | When | Where it lands |
|---|---|---|
| **Promote -- stable note** | Durable knowledge worth consulting later | best-fit folder (Step 5) |
| **Promote -- task** | An action the user needs to do | a journal file or a project board |
| **Archive** | Stale, superseded, or no lasting value | `98-archive/` |
| **Leave** | Genuinely not ready to triage yet | stays in the inbox, untouched |

For **promote -- stable note**, prefer delegating to the scribe skill that fits, so the content
lands formatted to that home's conventions:

| Note is... | Delegate to | Typical home |
|---|---|---|
| A repeatable how-to / solved chore | `/add-procedure` | `*reference/` |
| Prose worth keeping as an article | `/edit-article` (after the move) | `*research/`, `*work/` |
| Terminology around a concept | `/define-concept` or `/define-term` | a `CONTEXT.md` |

If nothing fits, **extract the most valuable information** and do a plain move to the best-fit
folder (Step 5). Folders, by intent (match against the vault's actual numbered folders, don't
hardcode names):

- learning / tutorial / course capture -> `*research/`
- distilled lookup or runbook -> `*reference/`
- work scratch or living work doc -> `*work/`
- structured course material -> `*lessons/{course}/`
- TTRPG / campaign content -> `*omen/{campaign}/`
- project-specific -> `*projects/{project}/`

**Done when:** you have one disposition and a concrete destination.

## Step 4: Checkpoint (hard gate)

Present, tersely:

> **Note:** `<filename>`
> **It is:** {one-line characterisation}
> **Disposition:** {promote-note | promote-task | archive | leave} -> `<destination>`
> **Via:** {delegated skill, or "plain move", or "extract: <the nugget>"}
> **Why:** {one line}

Wait for the user. They approve, redirect (different disposition/destination), or skip. **Do not
proceed without an explicit go.**

**Done when:** the user has approved a disposition (or told you to leave/skip it).

## Step 5: Execute

On approval, carry out the move. **Standardise frontmatter every time** -- on whichever artifact
survives (the moved note, or the file it lands in). See [FRONTMATTER.md](FRONTMATTER.md).

- **Promote via delegated skill** -- invoke it (`/add-procedure`, `/edit-article`,
  `/define-concept`, `/define-term`) with the note's content, then delete the inbox note once the
  content has safely landed.
- **Promote via plain move** -- move the file (or just the extracted nugget) to the destination
  folder. Standardise its frontmatter to the destination's convention: drop the `#raw` inbox tag,
  set real tags, keep/repair `created`, add `updated: {today}`. Respect folders that already carry
  solid frontmatter (e.g. journal files) -- don't flatten them.
- **Promote -- task** -- append the action to the relevant journal backlog or project board,
  matching that file's exact existing format (read it first), then delete the inbox note. These
  files are normally human-owned; the user's approval at Step 4 is what authorises the write.
- **Archive** -- move the file to `*archive/`, add `archived: {today}` to its frontmatter.
- **Leave** -- do nothing.

Move, don't copy: a triaged note leaves the inbox (unless **Leave**). Never commit -- the vault's
git is the user's to manage.

**Done when:** the note is in its new home (or deliberately left) and frontmatter is standardised.

## Step 6: Confirm

Report:

> **Triaged `<filename>`** -> {destination} ({how})
> {one-line recap; note count remaining in inbox if you counted in Step 1}

**Done when:** the user has seen what moved where.

## Principles

- **Assist, don't auto-triage.** The inbox is the user's. Step 4 is a hard gate.
- **One note, one run.** No batch sweeps -- keeps each decision deliberate and cheap.
- **Salvage the nugget.** A bad note with one good fact is a promote of that fact, not the note.
- **Standardise frontmatter on every triage**, respecting the destination's conventions.
- **Straight quotes only**; em dashes and emojis fine (vault rule).
