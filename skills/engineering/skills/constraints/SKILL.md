---
name: constraints
description: "★ Constraints: write the project's quality bar to CONSTRAINTS.md, with a command behind each rule, then check each branch against it and catch a lowered bar."
argument-hint: "[path to check, default the branch diff]"
disable-model-invocation: true
---

# Constraints

Decide the quality bar once, write it down, and stop an agent from quietly lowering it. The first run
sets up `CONSTRAINTS.md`. Each later run checks the branch against it.

The interview needs a live user. In a run with no user, apply the floor in Step 5 only, and say so.

## Step 1: Route

- No `CONSTRAINTS.md` at the repo root: go to Step 2.
- `CONSTRAINTS.md` exists: go to Step 5.

## Step 2: Detect

Read what you can before you ask. Find the language and stack, the test runner, the linters and the
type checker, the coverage output, the CI workflows, and the agent files (`CLAUDE.md`, `AGENTS.md`).
Report what you found in two lines.

**Done when:** the user has the two lines.

## Step 3: Ask four questions

Ask one at a time. Each question carries your guess and a default, so "I do not know" still gives a
working bar. Stop at four.

1. Which dimensions beyond the floor to enforce: coverage of changed lines, security scans,
   performance budgets, accessibility, architecture boundaries. Say what each one costs. A
   performance or accessibility check needs a running URL.
2. Whether a failed check blocks the agent mid-task or only warns. Default: block on the floor, warn
   on the rest.
3. Whether the user has target numbers, or wants today's values measured and held. Default: measure
   and hold. Each held value may get better and may not get worse.
4. The slowest check that may run before the agent hands work back. Default: 90 seconds.

**Done when:** you have four answers or four defaults.

## Step 4: Write and wire the bar

1. Write `CONSTRAINTS.md` with four sections:
   - **Floor**: the rules in Step 5, always on.
   - **Enforced**: a table with columns Dimension, Rule, Checked by (the exact command), and Runs at
     (edit, task end, or CI). A rule with no command is not a constraint. Leave it out.
   - **Measured, not enforced**: the metric, today's value, and the direction it must not move.
   - **Exceptions**: ID, rule, path, reason, owner, and expiry date.
2. Add each command to the project's own scripts, so that it runs without an agent. Use the tools
   that the project already has. Add a new tool only for a dimension that the user picked.
3. Prove each enforced row. Run its command against a planted violation and against clean code. The
   violation must fail, and the clean code must pass. Remove the planted violation.
4. Show the user the line to add to the project's agent file: "Read CONSTRAINTS.md before you write
   code. Do not weaken it to make a change pass." Add it only after a yes, because the agent file
   may be a team file.

**Done when:** `CONSTRAINTS.md` exists, each enforced row failed on a violation and passed on clean
code, and the user has answered about the agent file.

## Step 5: Check the branch

Read the branch diff against its base, or the path in `$ARGUMENTS`. Find each place where the change
lowers the bar:

- **Floor**: a new suppression (`@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`, and the
  same for the stack in use). A skipped, deleted, or emptied test. A removed assertion. A stub that
  throws "not implemented". An empty catch. A secret in source. An edit that weakens
  `CONSTRAINTS.md` or a check config.
- **Enforced**: run each command whose Runs at value is task end or edit.
- **Measured**: compare each value with the held value.
- **Exceptions**: flag each exception past its expiry date.

Report each finding as a row: rule, file and line, and what to do. A finding with a reason in its
commit message is still a finding. The user decides if it stays, and adds it to Exceptions.

**Done when:** the user has every finding, or a line that says the branch keeps the bar.
