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

## Step 2: Identify Documentation Surfaces

For each change, check whether any of these surfaces need updating:

### Reference docs

- READMEs, guides, API docs, architecture docs, changelogs
- Search for references to changed functions, types, endpoints, or concepts
- Check if examples in docs still reflect reality

### Code comments

- **Stale comments** — comments that describe behaviour that no longer matches the code. Update or remove.
- **Missing context** — complex logic, non-obvious decisions, or workarounds that lack explanation. Add a comment only if the code can't speak for itself.
- **Redundant comments** — comments that restate what the code obviously does. Remove.

### Naming

- **Functions** — does the name accurately describe what it does after the change?
- **Variables** — do names reflect their current purpose?
- **Files/modules** — does the file name still match its contents?
- Flag rename candidates but do NOT rename without presenting to the user first — renames have a blast radius.

### Type signatures and interfaces

- Do exported type definitions match the actual shape of the data?
- Are deprecated fields or methods marked as such?

### Configuration and infrastructure

- Do config files, environment variable docs, or setup guides reflect the changes?
- Are new dependencies documented where expected?

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

## Step 4: Apply Changes

For each approved item:

1. Make the change
2. If renaming, update all references across the codebase
3. If updating docs, preserve the existing style and voice

### Rules

- **Don't add comments to obvious code** — `i++; // increment i` is noise
- **Don't add docstrings to every function** — only where the name and signature aren't self-explanatory
- **Prefer better names over comments** — a well-named function needs no explanation
- **Match existing doc style** — if the project uses terse bullet READMEs, don't write prose paragraphs
- **Comments explain WHY, not WHAT** — the code shows what, comments should capture intent, constraints, or non-obvious reasoning

## Step 5: Verify

After applying changes:

1. Run the project's linter and typecheck to catch any breakage from renames
2. Run tests if renames touched source code
3. Summarise what was updated
4. Suggest a commit message
