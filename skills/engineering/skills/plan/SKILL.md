---
name: plan
description: >
  ★ Plan: turn a ticket or a spec into a claimed worktree and an approved plan in vertical
  slices, through /start-ticket. Use when the user says "plan", or asks to plan a ticket key or a
  spec after /spec.
argument-hint: "<ticket key> | @<spec path>"
---

# Plan

Turn the output of `/spec` into a plan that `/build` runs. `/start-ticket` does the work.
This command picks its input.

## Step 1: Route

- `$ARGUMENTS` is a ticket key: run `/start-ticket` with the key.
- `$ARGUMENTS` is a spec file: read it. It has the layout of the `/write-to-file` spec template.
  Stop when one of these holds, and tell the user to answer or delete each item first:
  - The frontmatter has `status: draft`.
  - `check_spec.py` prints `open questions: <n>` with `<n>` above 0. Ask `/write-to-file` to
    check the spec.

  Then run `/start-ticket` with the spec in place of the ticket:
  - The goal is the frontmatter `goal`.
  - The ACs are the lettered lines of `## Acceptance criteria`, with their letters. They are the
    ticket's ACs.
  - The `## Intent` and `## Decisions` sections, and `## Out of scope` when it exists, go into
    the plan's Context.
  - The spec has no tracker state, so skip each step that reads or writes the tracker.
  - Name the plan after the spec's slug. Set `ticket: none` and `spec: <spec path>` in its
    header.
  - Claim the current branch, or ask for a branch name when the current branch is the default
    branch.
- `$ARGUMENTS` is empty: ask for a ticket key or a spec path.

**Done when:** `/start-ticket` ran with a ticket or a spec.

## Step 2: Hand on

Return what `/start-ticket` returns. The plan has the layout of the `/write-to-file` plan
template, and the plan check of `/write-to-file` passed on it. When it wrote a plan, give
the next command:
`/build @<plan path>`, or `/implement @<plan path>` for one step. When it split the ticket,
give its wave 1 commands.

**Done when:** the user has the next command.
