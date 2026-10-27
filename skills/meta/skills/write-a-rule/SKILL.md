---
name: write-a-rule
description: Write a path-scoped Claude Code rule for one directory. Takes a directory path.
disable-model-invocation: true
---

# Write a Rule

A rule is a quality contract for one directory. It loads when an agent touches a matching file and
says nothing otherwise. Every line is a **contract term**: something the code in that directory
must keep true, or a name it must use. Mine the directory for evidence, draft, verify, then put
the judgement calls to the user.

## Step 1: Resolve the Target

`$ARGUMENTS` holds one directory path, and optionally the word `global`.

1. Confirm the directory exists. If not, stop and say so.
2. Derive the rule path:
   - **Project** (default): `<repo root>/.claude/rules/<workspace>/<module>.md`. `<workspace>` is
     the segment after `apps/` or `libs/`. `<module>` is the last segment. Outside a monorepo, use
     `<module>.md` alone.
   - **Global**: `~/.claude/rules/<module>.md`.
3. Show the derived path. One yes/no. Take an alternative if offered.
4. If the file already exists, this run is a **refresh**. Otherwise it is a **create**.

**Done when:** the target directory, rule path, and mode are known.

## Step 2: Mine the Directory

Read the code, not the docs. Existing prose in the directory is not an input.

- **Layout** from the file tree. Record only what deviates from the repo's defaults, or what a new
  file in this directory must follow.
- **Patterns** from the source files. For each recurring way of doing things, name one exemplar
  file. A pattern with no exemplar is not a pattern.
- **Invariants** from spec names. A good test name is an invariant. Collect them as numbered,
  testable statements.
- **Strays**: search the repo for the module's name outside the directory. List each hit.
- **Gotchas** from the conversation, if this session worked in the directory. Observed mistakes
  only.

On a **refresh**, also load the existing rule and mark every exemplar path that no longer exists
and every invariant with no matching spec.

**Done when:** a draft of Layout, Patterns, Invariants, and Strays exists, each line traceable to
a file.

## Step 3: Interview

Draft first, ask second. Put the judgement calls to the user one at a time, with a recommended
answer each:

1. **Language.** The core model in one sentence, then each term with its definition and the words
   to avoid. The code cannot supply avoid-words.
2. **Confirm or strike** each drafted Layout, Pattern, and Invariant line. On a refresh, ask only
   about the marked and new lines.
3. **Strays.** For each hit outside the directory, offer two exits: add a glob, or move the code
   under the directory. Recommend the move when the stray is module logic.

**Done when:** every line in the draft has been accepted, edited, or struck by the user.

## Step 4: Verify

- Every exemplar path exists.
- Every invariant maps to at least one spec, or the user has accepted it as untested.
- Every Pattern has an exemplar. Strike any that do not.
- Globs: one best-guess glob per owning directory. The user widens later if needed.
- Word count. Over about 600 words means the directory holds two modules. Say so and offer a
  split.

**Done when:** all checks pass or the user has accepted each exception.

## Step 5: Write

Write the file per [TEMPLATE.md](TEMPLATE.md). Section order is fixed. Empty sections are
removed, not left as headings. The canary line is always last.

Report:

> **Rule written** -> `<path>` (`create` / `refresh`)
>
> Globs: `<glob>`. Sections: `<list>`. Words: `<n>`.
> Rules load at session start. Open a new session, touch a file in the directory, and check for the
> canary.

**Done when:** the file is on disk and the report is shown.
