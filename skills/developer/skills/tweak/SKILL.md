---
name: tweak
disable-model-invocation: true
description: Make one small, focused edit to work from a recent /implement. Takes optional resource links for context.
---

# Tweak

Small, focused edits. One tweak per invocation.

## Step 1: Build Context

Parse `$ARGUMENTS` into **tweak request** and **resource links** (if any).

Example: `tweak align the text left in the center card` → tweak request is the full string,
no resource links.

Example: `tweak plans/plan_ENG-123.md make the error toast dismissable` → resource link is
the plan file, tweak request is the rest.

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

**Exit early** if no tweak request is discernible. Ask:
> What needs tweaking? Describe the change in one sentence.

## Step 2: Apply the Tweak

1. Identify the minimal set of files to touch
2. Make the edit
3. Run affected tests — fix if broken
4. Run typecheck for affected projects
5. Commit following project git conventions
