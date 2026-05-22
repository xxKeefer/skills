---
name: tweak-it
description: >
  Apply small, focused edits to recently built work. Designed for fresh-context sessions after
  /do-it. Rebuilds context from recent git changes by default, accepts resource links for
  additional context. Use when user says "tweak it", "fix the alignment", "polish this", or
  gives a small targeted instruction after implementation is mostly done.
---

# Tweak It

Small, focused edits. One tweak per invocation.

## Step 1: Build Context

Parse `$ARGUMENTS` into **tweak request** and **resource links** (if any).

Example: `tweak-it align the text left in the center card` → tweak request is the full string,
no resource links.

Example: `tweak-it plans/plan_ENG-123.md make the error toast dismissable` → resource link is
the plan file, tweak request is the rest.

### Context sources (in order)

1. **Resource links in arguments** → invoke `/look-up`
2. **Recent git changes** (always) → read `git diff HEAD~3 --stat` then `git diff HEAD~3` for
   the changed files to understand what was just built
3. **Conversation context** → any additional detail the user provided

**Exit early** if no tweak request is discernible. Ask:
> What needs tweaking? Describe the change in one sentence.

## Step 2: Apply the Tweak

1. Identify the minimal set of files to touch
2. Make the edit
3. Run affected tests — fix if broken
4. Run typecheck for affected projects
5. Commit following project git conventions
