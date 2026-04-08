---
name: check-in
description: >
  Adhoc mid-day micro-reflection. Appends a timestamped entry to today's daily file between the
  todo list and the reflect section. Use when user says "check-in", "log this", "note this",
  "quick update", or wants to capture a thought, observation, or progress note during the day.
---

# Check-in

Adhoc micro-reflection. No questions, no ceremony — just capture and go.

## Step 1: Find the Daily File

Locate the sanctum directory per the journal domain's discovery convention, then find today's `YYYY-wkNN-day.md` within it.

If the file doesn't exist:
> No daily file for today. Run `/daily` first, or should I create a minimal one?

## Step 2: Capture the Entry

`<user-input>` is the check-in content. If empty, ask:
> What's on your mind?

## Step 3: Append to Daily File

Find the `---` separator that sits between the Today/Blockers/Check-ins sections and the Reflect section.
Insert or append to a `## 📌 Check-ins` section just above that separator.

If the section doesn't exist yet, create it. If it does, append to it.

Format:
```markdown
## 📌 Check-ins
- **HH:MM** — {user's check-in content}
```

Use the current local time for the timestamp.

## Step 4: Confirm

> **Logged.** {brief acknowledgement — 1 sentence max}

That's it. No questions, no follow-up. Get out of the way.
