---
name: plan
description: >
  ★ Plan: turn a ticket or a spec into a claimed worktree and an approved plan in vertical
  slices, through /start-ticket. Use when the user says "plan", or asks to plan a ticket key or a
  spec after /spec.
argument-hint: "<ticket key> | @<spec path> [map path, plan name, branch name]"
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
  - `check_spec.py` exits 1. Give each error line, and tell the user to fix the spec or run
    `/spec` again.

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
- `$ARGUMENTS` is a spec file, and the caller also gives a map path, a plan name, and a branch
  name: this is a map unit. `/work-on` gives these. Run the spec route above, with these changes:
  - Name the plan with the plan name from the caller.
  - Claim no branch and no worktree. Set `worktree` to the current worktree, and `branch` to the
    branch name from the caller. The caller makes the branch before the build.
  - Put the map path and the last AC, which is the unit's `Done:` line, in the plan's Context.
  - Skip the plan gate of `/start-ticket`. Write the plan with `status: approved`, and put
    `Approval: the map (H0).` in Context. The user approved the map, and that approval covers
    each unit plan.
  - On a SPLIT verdict, take path 2 and ask no question. Run no `/split-ticket`, because a map
    unit has no tracker. Write no plan. Return the slices to the caller, each with its goal and its
    ACs. The caller writes them into the map.
  - On a CLARIFY verdict, run no `/refine-ticket`, because a map unit has no ticket. Write no
    plan. Return each open question to the caller as a `D` entry.
- `$ARGUMENTS` is empty: ask for a ticket key or a spec path.

**Done when:** `/start-ticket` ran with a ticket or a spec.

## Step 2: Hand on

Return what `/start-ticket` returns. The plan has the layout of the `/write-to-file` plan
template, and the plan check of `/write-to-file` passed on it. When it wrote a plan, give
the next command:
`/build @<plan path>`, or `/implement @<plan path>` for one step. When it split the ticket,
give its wave 1 commands.

**Done when:** the user has the next command.
