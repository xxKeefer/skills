---
name: work-on
description: >
  Take a ticket, several tickets at once, an idea, or the next units of a map to draft PRs,
  through a playbook of ★ commands, and stop only at the stops H0 to H5. Use when the user says
  "work on" with ticket keys, an idea, a map, or a plan to continue.
argument-hint: "<ticket key>... | <idea in a sentence> | @<map path> | @<plan path>..."
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
| H3 | An open `Pending Decision` (a `D` entry) exists. | Only when no option has a reason to recommend it. The agent takes a recommended option and logs it, with no stop. |
| H4 | An action is on the pause list. | Each time another person reads the output. |
| H5 | The user picks the skill edits from `/retro`. | After a unit. |

H4 holds each action on the pause list in the `pause-list.md` rule:

- Mark a PR ready for review.
- Merge.
- Force-push to a branch that another person uses.
- Deploy.
- Delete data, or delete a branch that is not merged.
- Post a comment, a review, or a ticket update as the user.
- Write a ticket.
- Send a message to a person.

The end of a ★ command is not a stop. A test round, a review round, a push to the agent's own
branch, and a draft PR are not stops. In the user's own build loop, a review report row is not a
stop: the review fixes each row with no stop.

## Principles

The 24 principles are skills with `disable-model-invocation: true`. They add no context until you
read one. A principle lives at `$SKILL_DIR/../<name>/SKILL.md`. The user can also type it, such as
`/principle-fix-root-causes`.

- **Read it first.** Before you apply a principle, read its `SKILL.md` in full in this session. Do not apply one from memory of the index.
- **Name it in the reply.** The reply names each principle that shaped a choice, and says what the choice was. Cite a principle only when you read its file in this session. Name none when none applied.

**Core**

- `principle-laziness-protocol`. Refactoring, sizing a diff, or about to add an abstraction, a layer, or a signal that threads through the code. Prefer deletion and the smallest change.
- `principle-foundational-thinking`. Before you write logic: core types, data structures, scaffold before feature, and what concurrent actors share.
- `principle-redesign-from-first-principles`. A new requirement fits into an existing design. Redesign as if it had been a base assumption.
- `principle-attack-the-premise`. Two or more fixes that share one premise have failed the same gate. Write the premise down and test it before the next fix.
- `principle-subtract-before-you-add`. Ordering an addition, a refactor, or a rewrite. Remove dead weight first, then build on the simpler base.
- `principle-minimize-reader-load`. Code that is hard to trace. Count the layers and the hidden state, collapse one-caller wrappers, and shrink mutable scope.
- `principle-outcome-oriented-execution`. A planned rewrite or migration with phase boundaries. Converge on the target, and keep no throwaway compatibility state.
- `principle-experience-first`. A product, UX, or feature-scope tradeoff. Choose user delight over implementation convenience.
- `principle-exhaust-the-design-space`. A new interaction or architecture decision with no precedent. Build two or three prototypes and compare them.
- `principle-build-the-lever`. Any non-trivial work. Build a tool only when it saves time or tokens, or when the result must be deterministic.

**Architecture**

- `principle-model-the-domain`. Stateful logic, or code that branches a lot or repeats a shape assumption. Encode the domain in a structure, not in conditionals.
- `principle-boundary-discipline`. Wiring validation, error handling, or framework adapters. Guard at system boundaries, trust internal types, keep business logic pure.
- `principle-type-system-discipline`. Designing types or a signature in a typed language. Make illegal states impossible to represent, and parse external data at the boundary.
- `principle-make-operations-idempotent`. Commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- `principle-migrate-callers-then-delete-legacy-apis`. A new internal API while old callers exist. Migrate and delete in one wave.
- `principle-separate-before-serializing-shared-state`. Concurrent actors might write the same file, branch, key, or object. Remove the sharing first.

**Verification**

- `principle-prove-it-works`. After a task, before you say it is done. Check the real artifact, not a proxy.
- `principle-fix-root-causes`. Debugging. Trace each symptom to the first place the system went wrong, and fix it there.
- `principle-sequence-verifiable-units`. Multi-step work, and how you stack commits and PRs. Small units that each end in a check.
- `principle-test-behavior-not-implementation`. Writing, changing, or keeping a test. Assert what the users of the code can observe.
- `principle-explain-the-number`. Before you trust, report, or act on a measured number. Find what limits it, and rule out that it measured something else.

**Delegation**

- `principle-guard-the-context-window`. Context is filling up: large outputs, long files, repeated reads. Send bulk work to subagents, and keep summaries in the main thread.
- `principle-never-block-on-the-human`. About to ask whether to do something on reversible work. Proceed and present the result. Stop only at the pause list.

**Meta**

- `principle-encode-lessons-in-structure`. You write the same instruction a second time. Fix it at the highest rung of the ladder that works, with docs last.

## Step 1: Pick the playbook

| `$ARGUMENTS` | Playbook |
| --- | --- |
| Two or more ticket keys, or two or more plan paths | [`playbooks/parallel.md`](playbooks/parallel.md) |
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
