---
name: qa-it
description: >
  Interactive bug intake session. User reports problems conversationally, agent explores the
  codebase for domain context, then files GitHub issues directly. Light clarification only --
  2-3 questions max. Use when the user says "qa it", "report a bug", "something's broken",
  "file a bug", or wants to conversationally report issues they've found.
---

# QA It

Interactive bug intake. The user describes problems they've observed, you explore the codebase
for context, ask a few clarifying questions, and file durable GitHub issues.

## Step 1: Listen

Let the user describe what they found. They might report:

- A single bug
- Multiple related bugs discovered during a session
- Vague "something's off" observations

Do NOT interrupt with a full grilling. This is a quick intake, not `/grill-it`.

## Step 2: Light Clarification

Ask **at most 2-3 targeted questions** to fill gaps. Focus on:

- **What did you expect vs what happened?** (if not already stated)
- **Can you reproduce it consistently?** (if unclear)
- **Which part of the app / which flow?** (if ambiguous)

If the user's report is already clear, skip straight to Step 3.

## Step 3: Explore for Context

While the user talks (or after clarification), explore the codebase in the background:

- Search for the modules and behaviours the user is describing
- Understand the domain language the project uses
- Check if `UBIQUITOUS_LANGUAGE.md` exists and use its terminology
- Identify the contracts and interfaces involved
- Look for existing tests that cover (or should cover) the reported area

This context makes the filed issues durable and domain-accurate.

## Step 4: File the Issues

For each distinct bug, create a GitHub issue via `gh issue create`.

### Issue format

```markdown
## Problem

**Symptom:** one-line summary of what the user observed
**Expected behavior:** what should happen
**Actual behavior:** what happens instead
**Reproduction:** steps to reproduce (mandatory -- derive from user's report + your exploration)

## Context

Describe the affected behaviour using domain language. Reference modules and contracts,
not file paths or line numbers. Note any related behaviours that might be affected.

## Acceptance Criteria

- [ ] {specific observable fix -- what should the user see after the fix?}
- [ ] Existing behaviour in related flows is preserved
```

Label as `bug` and `needs-triage`.

### Multiple related bugs

If the user reports several issues in one session:

1. Separate them into distinct issues (one concern per issue)
2. Cross-reference related issues in the Context section
3. Create them all, then present the full list

## Step 5: Present and Continue

After filing:

> **Filed {N} issue(s):**
>
> - #N -- {title}
> - #N -- {title}
>
> Anything else to report, or done?

Keep the session open -- the user may have more to report. When they're done, summarise
everything filed.

## Guiding Principles

- **Quick intake, not interrogation** -- 2-3 questions max, then file
- **Durability** -- no file paths in issue bodies, domain language, behavioural descriptions
- **Reproduction is mandatory** -- derive steps from the user's report + codebase exploration
- **One concern per issue** -- split compound reports into separate issues
- **File first, triage later** -- issues get `needs-triage` label; `/triage-it` handles the rest
