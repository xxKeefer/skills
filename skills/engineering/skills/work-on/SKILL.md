---
name: work-on
description: >
  Take a ticket, an idea, or the next units of a map to draft PRs, through a playbook of ★
  commands, and stop only at the stops H0 to H5. Use when the user says "work on" with a ticket
  key, an idea, a map, or a plan to continue.
argument-hint: "<ticket key> | <idea in a sentence> | @<map path> | @<plan path>"
---

# Work On

Run a playbook from start to end. A playbook is an ordered list of skill calls, the stop between
each pair, and a done line. This skill calls the ★ commands. It does not do their work, and it
does not copy their routing.

`$SKILL_DIR` is this skill's base directory.

Run at the `judgement` role of the `models` block in `~/.claude/AGENTS.md`. With no `models` block,
use the session model.

## The stops

Stop only at these points. Between two stops, run with no input from the user.

| Stop | What | When |
| --- | --- | --- |
| H0 | The user approves the map. | Once per program. |
| H1 | The user says yes to the spec. | Once per change, when a spec exists. |
| H2 | The user approves the plan. | Once per change. A map run has no H2 stop, because the map approval (H0) covers each unit plan. |
| H3 | An open `Pending Decision` (a `D` entry) exists. | Only when the agent cannot decide. |
| H4 | An action is on the pause list. | Each time another person reads the output. |
| H5 | The user picks the skill edits from `/retro`. | After a unit. |

H4 holds each action of the `pause-list.md` rule. The stop is on the action, not on the task.

Between stops, never block on the user. The user supervises later, not in the loop, and code
changes are reversible and reviewable.

- Proceed, then present. Do not ask "should I do X?" Do X, and say why.
- Reversible work runs with no stop. This covers code, notes, and splitting a task.
- Product direction comes from the user. Execution does not wait for it.
- When you see a problem, record it and fix it in the next round.
- When you cannot decide, write a `D` entry under `## Pending Decisions` in the plan, and continue
  with the steps that do not depend on it.

The end of a ★ command is not a stop. A test round, a review round, a push to the agent's own
branch, and a draft PR are not stops. In the user's own build loop, a review report row is not a
stop: the review fixes each row with no stop.

## Principles

The 14 principles are skills with `disable-model-invocation: true`. They add no context until you
read one. A principle lives at `$SKILL_DIR/../<name>/SKILL.md`. The user can also type it, such as
`/principle-fix-root-causes`.

- **Read it first.** Before you apply a principle, read its `SKILL.md` in full in this session. Do not apply one from memory of the index.
- **Name it in the reply.** The reply names each principle that shaped a choice, and says what the choice was. Cite a principle only when you read its file in this session. Name none when none applied.

**Core**

- `principle-redesign-from-first-principles`. A new requirement, rewrite, or migration meets an existing design.
- `principle-subtract-before-you-add`. Ordering an addition, refactor, or rewrite, or sizing a diff.
- `principle-minimize-reader-load`. Code that is hard to trace.
- `principle-experience-first`. A product, UX, or feature-scope tradeoff.
- `principle-build-the-lever`. Any non-trivial work.

**Architecture**

- `principle-model-the-domain`. Before logic, stateful logic, or code with many branches.
- `principle-type-system-discipline`. Types, signatures, validation, error handling, or adapters.
- `principle-make-operations-idempotent`. Commands or loops that run amid crashes and retries.
- `principle-separate-before-serializing-shared-state`. Concurrent actors might write the same target.

**Verification**

- `principle-prove-it-works`. Before you say a task is done.
- `principle-fix-root-causes`. Debugging, or two fixes on one premise failed.
- `principle-sequence-verifiable-units`. Multi-step work, and how you stack commits and PRs.

**Delegation**

- `principle-guard-the-context-window`. Context is filling up with large outputs or repeated reads.

**Meta**

- `principle-encode-lessons-in-structure`. You write the same instruction a second time.

## Step 1: Pick the playbook

| `$ARGUMENTS` | Playbook |
| --- | --- |
| A ticket key or an idea | [`playbooks/new-ticket.md`](playbooks/new-ticket.md) |
| `@<map path>`: a file with doctype `map`, or with unit headings `### [ ] N. Title` | [`playbooks/map.md`](playbooks/map.md) |
| `@<spec path>`: a file with doctype `spec` | [`playbooks/new-ticket.md`](playbooks/new-ticket.md), from step 2. |
| `@<plan path>` | Continue. Read the plan's `## Progress` for the playbook and the last stop. After H3 or H4, start at the step that stopped, because that step is not done. After H1, H2, or H5, start at the next step. |
| Empty | Ask for a ticket key, an idea, a map, or a plan. |

Read the playbook from `$SKILL_DIR/playbooks/`.

**Done when:** you have the playbook and the step to start from.

## Step 2: Copy the steps into the todo list

Copy each playbook step into the todo list, in order, with its stop. Do not merge two steps, and
do not drop a step.

When you skip a step, keep it in the list. Mark it done, and add the reason, such as
`skipped: the ticket has a spec`.

When the session has no todo tool, list the playbook steps once in the reply, with the same marks.
Then, as each step ends, write the step and its mark in the plan's `## Progress`, when a plan
exists.

**Done when:** the todo list, or the list in the reply, holds every playbook step.

## Step 3: Run the steps

Run each step in order. Mark each step done in the list when it is done.

- Before an action on the pause list, stop (H4). A step that would do the action does not do it.
- When a step returns an open `D` entry, stop (H3).
- When a step fails and gives no `D` entry, stop, and show the failure as an H3 stop.

**Done when:** each step ran the skill that it names, or is marked skipped with its reason in the
list, and the playbook's done line holds or the run is at a stop.

## Step 4: Stop

At each stop:

1. Write the plan with `/update-plan`. Record the playbook, the stop, and the next step in
   `## Progress`, so a fresh run can continue. When no plan exists yet, skip `/update-plan`.
   Then the command to continue is `/work-on @<map path>` in a map run, `/work-on @<spec path>`,
   or `/work-on <ticket key>` when `/refine-ticket` wrote the spec back to the ticket.
2. End the turn with one line that names the stop and the command to continue:

   ```
   H2: approve the plan at <plan path>. Continue: /work-on @<plan path>
   ```

Write no other text after the line.

**Done when:** the plan holds the stop, and the last line of the turn names the stop and the
command to continue.
