---
name: codebase-news
description: >
  Summarise the notable changes in the current repo over a time period as a table with the columns
  app/lib, topic and summary. Reads the changelogs first and the commit history where they fall
  short. Usage: codebase-news [time-period], default last 24 hours. Use when the user says "codebase news", "what changed
  while I was away", "catch me up on the repo", or is back from leave.
---

# Codebase News

Turn a window of repo history into one table that a returning developer can scan in a minute. One
row per theme, not one per commit. The repo is the current working directory.

## Step 1: Resolve the window

- Take `<time-period>` in any form that `git log --since` reads: `2 weeks`, `2026-10-07`,
  `last monday`. A range such as `2026-10-01..2026-10-14` also sets `--until`.
- No argument: use the last 24 hours (`--since="24 hours ago"`).
- Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. Remove the
  `origin/` prefix to get `<default>`.
- Fetch it (`git fetch origin <default>`). Read everything from `origin/<default>`, not from the
  working tree. The checkout can be a feature branch or out of date.
- If the fetch fails, use the local default branch and say so in Step 6.
- Find the base commit: `git rev-list -1 --before=<start> origin/<default>`.

**Done when:** you have a start date, an end date, a base commit and the branch to read.

## Step 2: Read the changelogs

1. List the tracked changelogs: `git ls-files | grep -iE '(^|/)CHANGELOG\.md$'`.
2. Read each one from the branch (`git show origin/<default>:<path>`).
3. Keep only the release entries dated inside the window.
4. Collect the breaking changes, features and fixes, each with its scope, ticket key and commit hash.
5. Remove duplicates across files. A release tool lists one commit under every package it touches,
   so attribute each entry to the scope in its commit subject, not to the file it sits in.

**Done when:** you have each in-window changelog entry once.

## Step 3: Fill the gaps from the commit history

Changelogs cover only the packages that release. Go to the commit history when a row below applies:

| Condition | What to read |
| --- | --- |
| The repo has no changelog | `git log <base>..origin/<default> --no-merges`, minus release commits |
| A changed package has no changelog | `git log <base>..origin/<default> --no-merges -- <package-path>` |
| An entry is too thin to summarise (empty release heading, bare subject) | That commit's body and `git show --stat` |
| A change sits outside every package: root scripts, CI, shared config, agent guidance (`AGENTS.md`, `CLAUDE.md`, `.claude/`) | `git diff --stat <base> origin/<default> -- <paths>`, then the diff if the stat is not clear |
| A package or app was added | `git diff --name-status <base> origin/<default>`, filtered for added manifests |

To find packages with no changelog, compare the package directories in
`git diff --name-only <base> origin/<default>` against the changelog list.

Always collect the breaking-change footers: `git log <base>..origin/<default> --grep='BREAKING'`.

Read a diff only when the subject and body do not say what changed. Never write a summary from a
ticket key alone.

**Done when:** every changed package and every root-level change has a source.

## Step 4: Group into rows

One row per theme. Order the rows by how much they affect a developer with open branches:

1. Breaking changes in shared packages. One row per change, with its migration (old name → new name).
2. New packages, lint rules, agent guidance and dev tooling.
3. Feature work, grouped by epic or product theme. A product that landed in three apps is one row.
4. Smaller changes, one row per app.

Leave out release commits, version bumps, formatting, and dependency bumps that are not security
fixes.

**Done when:** each collected change is in one row, or the rule above drops it.

## Step 5: Build the table

The columns are fixed:

```markdown
| # | app/lib | topic | summary |
```

- `#`: the row number, from 1, so the user can refer to "row 3".
- `app/lib`: the packages that the row touches, separated by commas. Use the package name for a
  library.
- `topic`: a short name for the theme. Add `(breaking)` when the row has a breaking change.
- `summary`: what changed, in short phrases, with ticket keys in parentheses. For anything removed,
  name its replacement.
- An empty cell gets `—`, never a guess.

**Done when:** every row has a value or `—` in every column.

## Step 6: Present

1. Above the table, write one paragraph that reads like a short news article, at most six
   sentences:
   - The lead sentence gives the biggest story, such as a major version jump in a shared library.
     It also gives the window and the number of non-merge commits.
   - The next sentences cover the other main themes, in order of importance, by product or feature
     name.
   - Use plain prose. No bullets, no ticket keys and no row numbers, because the table has them.
   - Report facts only. No hype words.
2. Show the table.
3. Below the table, write at most two lines:
   - The user's own PRs that merged in the window. Match `git config user.name` and
     `git config user.email` against the commit authors.
   - The sources you used: changelogs only, or changelogs and commit history. Say if the fetch
     failed.

If the user asks to keep the table, delegate to `/write-to-file`.

## Principles

- **Themes, not commits.** Fifty commits on one epic make one row.
- **Breaking changes first.** The first question of a returning developer is "what breaks my
  branch?".
- **Evidence only.** Every cell traces to a changelog entry, a commit or a diff.
- **Read the remote.** The local checkout is not the source of truth.
