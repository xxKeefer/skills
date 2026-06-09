---
name: teach-it
description: >
  Correct repeated undesired agent behaviour by codifying user feedback into persistent guidance.
  Writes feedback to memory first, then updates relevant skills or reference docs at global scope,
  then at project scope. Use when the user says "teach it", "remember this", "stop doing X",
  "always do Y", "I keep telling you", or is correcting the same behaviour for the second time.
---

# Teach It

Turn user corrections into durable guidance so the same mistake never repeats.

## Step 1: Capture the Feedback

`$ARGUMENTS` may contain:

- **A direct correction** — "stop doing X", "always do Y instead of Z"
- **A pattern description** — "every time I ask for X you do Y wrong"
- **A reference to earlier in the conversation** — "that thing you just did"

If `$ARGUMENTS` is empty or unclear, use **AskUserQuestion**:

> What behaviour do you want me to correct? Describe what I keep getting wrong and what you
> want instead.

Restate the feedback back to the user in this format:

```
## Feedback Captured

**Bad behaviour:** <what the agent does wrong>
**Desired behaviour:** <what the agent should do instead>
**Why:** <the reason this matters — ask if not obvious>
**Scope:** Global | Project | Both
```

Ask the user to confirm before proceeding. If scope is unclear, ask:

> Should this apply everywhere, or just in this project?

## Step 2: Write to Memory

Save a feedback memory file. This is the first and most important step — memory persists across
conversations regardless of whether docs get updated.

Write to the appropriate memory directory:

- **Global:** `~/.claude/projects/{project-path}/memory/`
- Follow the memory file format with `type: feedback` frontmatter

The memory should lead with the rule, then include **Why:** and **How to apply:** lines so future
conversations know when the guidance is relevant.

Confirm to the user that memory has been saved.

## Step 3: Update Global Scope

Check if the feedback warrants changes to global configuration:

1. **Read `~/.claude/CLAUDE.md`** — does an existing rule need strengthening, clarifying, or adding?
2. **Check global reference docs** — are there reference files linked from global CLAUDE.md that
   should reflect this feedback?
3. **Check skills** — does this feedback affect how a skill in the user's skill directories behaves?

For each relevant file:

- **Existing rule covers it** — tighten the wording or add specificity
- **New rule needed** — add it to the appropriate section
- **Skill needs updating** — modify the skill's SKILL.md (principles, steps, or guardrails)
- **No global change needed** — skip and say so

Present each proposed change before making it:

> **Global update:** `~/.claude/CLAUDE.md` — add rule to Code Style section:
> `{proposed text}`
>
> Apply?

Wait for approval on each change.

## Step 4: Update Project Scope

Repeat the same process for project-local configuration:

1. **Read the project's `CLAUDE.md`** — does a rule need adding or updating?
2. **Check project reference docs** — any linked reference files to update?
3. **Check project skills** — does this feedback affect a project-specific skill?

Same approval flow — present each change, wait for confirmation.

If the feedback is global-only (Step 1 scope), skip this step.

## Step 5: Verify Coverage

Summarise what was changed:

```
## Changes Applied

**Memory:** <memory file path>
**Global docs:** <list of files changed, or "none">
**Project docs:** <list of files changed, or "none">
**Skills updated:** <list of skills changed, or "none">
```

Ask:

> Anything else to adjust, or is that captured?

## Guiding Principles

- **Memory first, docs second.** Memory is the safety net — even if doc updates are skipped or
  wrong, memory ensures the feedback persists.
- **Minimal, precise edits.** Add the tightest rule that captures the feedback. Don't rewrite
  sections or restructure documents.
- **Ask before writing.** Every file change gets user approval. The user is teaching — they need
  to see what's being learned.
- **Preserve existing voice.** Match the tone and format of the document being edited. Don't
  impose a different style.
- **One correction per invocation.** If the user has multiple corrections, handle them one at a
  time. Each gets its own memory entry and doc updates.
