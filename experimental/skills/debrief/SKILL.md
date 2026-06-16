---
name: debrief
description: >
  Produce a human-readable session debrief and drop it into 00-raw/ in the Obsidian vault.
  Covers what was done, next steps, and practical "next time" notes so the user doesn't have
  to faff around rediscovering the same things. The human counterpart to /handoff.
argument-hint: "Any topic to emphasise in the next-time notes?"
---

Write a session debrief for the human to read after the conversation ends. Save it as a markdown
note directly into the Obsidian vault's `00-raw/` folder so it's ready for `/wiki:intake-raw`
without any manual moving.

If the user passed arguments, treat them as a hint about which topic to focus the next-time
notes on.

## Step 1: Locate the Vault

Scan the home directory for a directory containing `.obsidian/`. Use the first match as the
vault root. If none is found, fall back to `/tmp/` and warn the user.

## Step 2: Generate the Note

Write a markdown file to `{vault}/00-raw/debrief-{YYYY-MM-DD}.md`.

Use this frontmatter:

```yaml
---
tags: ["debrief", "00-raw"]
date: {YYYY-MM-DD}
---
```

Then write the sections below in order. Do not duplicate content already captured in other
artifacts (PRDs, plans, ADRs, commits, diffs) — reference them by path or URL instead.

### What Was Done

Factual bullets. One per distinct outcome. Reference artifacts by path or URL, don't reproduce
them.

### Next Steps

Ordered, actionable verb phrases. Flag blocked steps and their dependency. Tag with `[agent]`
or `[human]` where relevant.

### Next Time

The core of the debrief. Practical notes that will save time when this kind of work comes up
again — the things the user would otherwise have to rediscover or ask an agent about. Think:
personal runbook entries, not lessons.

Include any of the following that are relevant:

- **Gotchas** — things that went wrong or nearly went wrong, and why
- **Shortcuts** — faster ways to do what was done, now that the lay of the land is known
- **Decisions made** — key calls and the reasoning, so they don't get relitigated
- **Commands / incantations** — exact commands, flags, or sequences worth preserving
- **Mental models** — the framing or analogy that made something click

Keep each entry terse. This is a reference, not an explanation.

### Go Deeper *(optional)*

Only include this section if there is a concept or skill from the session worth understanding
more formally — something where surface-level familiarity isn't enough for future work.

For each item (1–2 max):

- **What it is** — name and one-sentence definition
- **Why it's worth understanding** — what deeper knowledge would unlock
- **Where to start** — a canonical resource (official docs, well-known book). Do not invent
  URLs; describe the type of resource if unsure of a specific one

Omit this section entirely if the session was routine or the next-time notes cover everything.

## Step 3: Confirm

Print the full path of the file written and a one-line summary of each section's content.
