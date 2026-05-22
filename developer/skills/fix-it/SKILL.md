---
name: fix-it
description: >
  Fix a functionally broken behaviour found during manual QA. Lighter than /hunt-it -- no formal
  root cause document, just find the fault and fix it. Use when user says "fix it", "this is
  broken", "X doesn't work", describes a bug they just found while testing, or gives a specific
  broken behaviour to resolve.
---

# Fix It

Resolve a broken behaviour reported from manual QA. Find the fault, fix it, prove it.

## Step 1: Understand the Problem

Parse `$ARGUMENTS` into **problem description** and **resource links** (if any).

Example: `fix-it the dropdown doesn't close when clicking outside` → problem is the full string.

Example: `fix-it ENG-123 submit button sends the wrong payload` → resource link is the ticket,
problem is the rest.

### Context sources (in order)

1. **Resource links in arguments** → invoke `/look-up`
2. **Recent git changes** (always) → read `git diff HEAD~3 --stat` then `git diff HEAD~3` for
   the changed files to understand what was just built
3. **Conversation context** → any additional detail the user provided

**Exit early** if no problem is discernible. Ask:
> What's broken? Describe what you expected vs what actually happens.

## Step 2: Find the Fault

1. Trace the described behaviour through the recently changed code
2. Identify the minimal root cause — don't go broad, stay in the scope of recent work
3. If the cause isn't in recent changes, say so — this may need `/hunt-it` instead

## Step 3: Fix and Prove

1. Write a failing test that captures the broken behaviour
2. Make the minimal fix to pass the test
3. Run affected tests — ensure nothing else broke
4. Run typecheck for affected projects
5. Commit following project git conventions
