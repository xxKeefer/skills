---
name: why
description: >
  Answer why a line, a block, or a file is the way it is, from its commits and PR threads, with a
  citation for each claim. Use when the user says "why" about code, or must know the reason before
  they change it.
argument-hint: "<file>[:<line>[-<line>]]"
---

# Why

Answer why a target is the way it is. The record is the commits and the PR threads that touched it.
The skill only reads. It writes no file and posts nothing. Adapted from the pstack `why` skill.

## Step 1: Resolve the target

1. Take `<file>`, `<file>:<line>`, or `<file>:<start>-<end>`. A pasted block: find its file and
   lines with a search.
2. A file with no range: use the whole file.
3. Read the current lines, so that you know what you explain.

**Done when:** you have a file, a line range, and the text of those lines.

## Step 2: Read the history

Read these sources in order:

1. `git blame -w -M -C --porcelain -L <start>,<end> -- <file>` gives the commit of each line.
2. `git log -L <start>,<end>:<file> --no-patch --format='%h %an %ad %s'` gives the history of the
   range, with renames followed.
3. `git show --no-patch --format='%h %an%n%B' <sha>` gives the message of each commit. Read the
   diff only when the message does not say why.
4. Find the PR that merged each commit. The first line of
   `git log --merges --ancestry-path --reverse --format='%h %s' <sha>..HEAD` is the merge that
   brought the commit in. Read the PR number from its subject. A later merge is not this PR. Else
   ask the code host.
5. Read the description and the review threads of each PR through the code host tool role. Find
   the tool as the engineering `CLAUDE.md` says.

A source that you cannot read goes into the unanswered part, with the reason. Examples: no code
host tool, a squashed commit with no PR number, a PR that you cannot reach.

**Done when:** every commit in the range has its message read, and every PR has been read or has a
reason in the unanswered list.

## Step 3: Answer

Write in this order:

1. **Answer.** One to three sentences: why the target is this way now.
2. **History.** From oldest to newest, one bullet for each change that matters. State what the
   change did and why.
3. **Unanswered.** What the record does not say, and each source that you could not read.

Rules:

- Cite each claim with a short SHA or a PR number, and the author of that source:
  `(a1b2c3d, Alex)` or `(PR 42, Sam)`.
- A claim with no source is not a claim. Put it in Unanswered, or leave it out.
- Say "the record does not say" when it is silent. Never guess a reason from the code.
- Quote a commit message or a thread line only when the exact words matter.
