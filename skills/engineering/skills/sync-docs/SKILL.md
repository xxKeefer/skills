---
name: sync-docs
disable-model-invocation: true
description: Update every doc, README, code comment, and name that the current code changes put out of sync.
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

### Code comments

- **Stale comments** — comments that describe behaviour that no longer matches the code. Update or remove.
- **Missing context** — complex logic, non-obvious decisions, or workarounds that lack explanation.
- **Redundant comments** — comments that restate what the code obviously does. Remove.

### Naming

- **Functions** — does the name accurately describe what it does after the change?
- **Variables** — do names reflect their current purpose?
- **Files/modules** — does the file name still match its contents?

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
> **Comments** ({N} updates)
> - `path/to/file:L42` — stale comment, behaviour changed
> - `path/to/file:L87` — missing context for non-obvious logic
>
> **Naming** ({N} candidates)
> - `oldName` → `suggestedName` in `path/to/file` — {why}
>
> **Types** ({N} updates)
> - `TypeName` in `path/to/file` — field added/removed but type not updated
>
> Apply all, or pick specific items?

Wait for user approval. They may want to skip renames or certain categories.

**Done when:** the user has picked the items to apply, or none.

## Step 4: Apply Changes

For each approved item:

1. Make the change
2. If renaming, update all references across the codebase
3. If updating docs, preserve the existing style and voice

### Rules

- **Add a comment only where the code cannot show the intent**, and say why.
- **Add a docstring only where the name and signature do not explain the function.**
- **Prefer better names over comments** — a well-named function needs no explanation

**Done when:** every approved item is applied, and no reference to an old name is left.

## Step 5: Verify

After applying changes:

1. Run the project's linter and typecheck to catch any breakage from renames
2. Run tests if renames touched source code
3. Summarise what was updated
4. Suggest a commit message

**Done when:** the linter and typecheck pass, any tests you ran pass, and the user has the summary and the commit message.
