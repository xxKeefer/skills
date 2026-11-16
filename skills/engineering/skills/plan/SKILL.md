---
name: plan
description: >
  ★ Plan: turn a ticket or a spec into a claimed worktree and an approved plan handoff in vertical
  slices, through /start-ticket. Use when the user says "plan", or asks to plan a ticket key or a
  spec after /spec.
argument-hint: "<ticket key> | @<spec path>"
---

# Plan

Turn the output of `/spec` into a plan handoff that `/build` runs. `/start-ticket` does the work.
This command picks its input.

## Step 1: Route

- `$ARGUMENTS` is a ticket key: run `/start-ticket` with the key.
- `$ARGUMENTS` is a spec file: run `/start-ticket` with the spec in place of the ticket:
  - The spec's lettered ACs are the ticket's ACs. The spec has no tracker state, so skip each step
    that reads or writes the tracker.
  - Name the handoff after the spec's slug. Set `ticket: none` and `spec: <spec path>` in its
    header.
  - Claim the current branch, or ask for a branch name when the current branch is the default
    branch.
- `$ARGUMENTS` is empty: ask for a ticket key or a spec path.

**Done when:** `/start-ticket` ran with a ticket or a spec.

## Step 2: Hand on

Return what `/start-ticket` returns. The plan handoff has the layout of the `/write-to-file` plan
template, and the plan check of `/write-to-file` passed on it. When it wrote a plan handoff, give
the next command:
`/build @<handoff path>`, or `/implement @<handoff path>` for one step. When it split the ticket,
give its wave 1 commands.

**Done when:** the user has the next command.
