---
name: fix
disable-model-invocation: true
description: Find and fix a broken behaviour from manual QA. Lighter than /diagnose, with no root-cause document.
---

# Fix

Resolve a broken behaviour reported from manual QA. Find the fault, fix it, prove it.

## Step 1: Understand the Problem

Parse `$ARGUMENTS` into **problem description** and **resource links** (if any).

Example: `fix the dropdown doesn't close when clicking outside` → problem is the full string.

Example: `fix ENG-123 submit button sends the wrong payload` → resource link is the ticket,
problem is the rest.

### Context sources (in order)

1. **Resource links in arguments** → invoke `/look-up`
2. **Recent git changes** (always) → read the `--stat` of the changeset, then its diff for the
   changed files, to understand what was just built. Find the changeset:
   1. If `$ARGUMENTS` holds a commit range, use it.
   2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
      `origin/<name>`. Fall back to `main`.
   3. Off the default branch, diff against `git merge-base HEAD <default>`.
   4. On the default branch, use the uncommitted diff, `git diff HEAD`.
   5. If that diff is empty, ask the user for a range.
3. **Conversation context** → any additional detail the user provided

**Exit early** if no problem is discernible. Ask:
> What's broken? Describe what you expected vs what actually happens.

## Step 2: Find the Fault

1. Trace the described behaviour through the recently changed code
2. Identify the minimal root cause — don't go broad, stay in the scope of recent work
3. If the cause isn't in recent changes, say so — this may need `/diagnose` instead

## Step 3: Fix and Prove

1. Write a failing test that captures the broken behaviour
2. Make the minimal fix to pass the test
3. Run affected tests — ensure nothing else broke
4. Run typecheck for affected projects
5. Commit following project git conventions
