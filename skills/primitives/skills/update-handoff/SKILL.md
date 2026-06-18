---
name: update-handoff
description: >
  Update an existing handoff/plan document in place with the current state of progress, so a
  fresh agent can cold-start from it. Takes one argument: the @-tagged file path to update.
  Use when the user says "update handoff", "update the plan", or context is about to blow out.
argument-hint: "@path/to/handoff-or-plan.md"
---

Update the @-tagged file with the current state of progress, for the purpose of bootstrapping a
fresh agent for a cold start.

- Edit the file in place. Preserve its existing structure and headings — fold progress into the
  document it already is, don't replace it with a fresh handoff.
- Mark what's done, what's in progress, and what's next. Update stale claims to match reality.
- Don't duplicate content already captured in other artifacts (PRDs, ADRs, issues, commits,
  diffs) — reference them by path or URL.
- Redact anything sensitive (keys, passwords, PII).

The reader is a cold agent with none of this conversation's context. Write so it can pick up
and continue without asking.
