---
name: sync-docs
disable-model-invocation: true
description: Update every doc, README, type, and config that the current code changes put out of sync.
---

# Sync Docs

Analyze code changes, find every documentation surface that needs updating, and fix them.

## Step 1: Gather the Changes

Find the changeset:

1. If `$ARGUMENTS` holds a commit range or a file path, scope to it.
2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
   `origin/<name>`. Fall back to `main`.
3. Off the default branch, diff against `git merge-base HEAD <default>`.
4. On the default branch, use the uncommitted diff, `git diff HEAD`.
5. If that diff is empty, use **AskUserQuestion**: "What changes should I document? Give me a file, commit range, or branch."

Build a list of:

- **Files modified** — what changed and how
- **Functions/types added, changed, or removed** — signature changes, new exports, removed APIs
- **Behaviour changes** — anything that alters what the code does from a caller's perspective

**Done when:** the list covers every file in the changeset.

## Step 2: Identify Documentation Surfaces

For each change, check whether any of these surfaces need updating:

### Reference docs

- READMEs, guides, API docs, architecture docs, changelogs
- Search for references to changed functions, types, endpoints, or concepts
- Check if examples in docs still reflect reality

### Type signatures and interfaces

- Do exported type definitions match the actual shape of the data?
- Are deprecated fields or methods marked as such?

### Configuration and infrastructure

- Do config files, environment variable docs, or setup guides reflect the changes?
- Are new dependencies documented where expected?

**Done when:** every change from Step 1 is checked against every surface.

## Step 3: Present Findings

Group findings by category and present:

> **Documentation audit for `{scope}`**
>
> **Reference docs** ({N} updates)
> - `path/to/README.md` — {what needs changing}
>
> **Types** ({N} updates)
> - `TypeName` in `path/to/file` — field added/removed but type not updated
>
> Apply all, or pick specific items?

Wait for user approval. They may want to skip certain categories.

**Done when:** the user has picked the items to apply, or none.

## Step 4: Apply Changes

For each approved item:

1. Make the change
2. If updating docs, preserve the existing style and voice

**Done when:** every approved item is applied.

## Step 5: Verify

After applying changes:

1. Run the project's linter and typecheck
2. Summarise what was updated
3. Commit the changes with a message that follows the project's git conventions

**Done when:** the linter and typecheck pass, the changes are committed, and the user has the summary and the commit hash.
