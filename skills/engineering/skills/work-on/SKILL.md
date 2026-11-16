---
name: work-on
description: >
  Take a ticket, an idea, or the next units of a map to draft PRs, through a playbook of ★
  commands, and stop only at the stops H0 to H5. Use when the user says "work on" with a ticket
  key, an idea, a map, or a plan to continue.
disable-model-invocation: true
argument-hint: "<ticket key> | <idea in a sentence> | @<map path> | @<plan path>"
---

# Work On

Run a playbook from start to end. A playbook is an ordered list of skill calls, the stop between
each pair, and a done line. This skill calls the ★ commands. It does not do their work, and it
does not copy their routing.

`$SKILL_DIR` is this skill's base directory.

## The stops

Stop only at these points. Between two stops, run with no input from the user.

| Stop | What | When |
| --- | --- | --- |
| H0 | The user approves the map. | Once per program. |
| H1 | The user says yes to the spec. | Once per change, when a spec exists. |
| H2 | The user approves the plan. | Once per change, or once per batch. |
| H3 | An open `Pending Decision` (a `D` entry) exists. | Only when the agent cannot decide. |
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

## Step 1: Pick the playbook

| `$ARGUMENTS` | Playbook |
| --- | --- |
| A ticket key or an idea | [`playbooks/new-ticket.md`](playbooks/new-ticket.md) |
| `@<map path>`: a file with doctype `map`, or with unit headings `### [ ] N. Title` | [`playbooks/map.md`](playbooks/map.md) |
| `@<spec path>`: a file with doctype `spec` | [`playbooks/new-ticket.md`](playbooks/new-ticket.md), from step 2. |
| `@<plan path>` | Continue. Read the plan's `## Progress` for the playbook and the last stop. Start at the playbook step after that stop. |
| Empty | Ask for a ticket key, an idea, a map, or a plan. |

Read the playbook from `$SKILL_DIR/playbooks/`.

**Done when:** you have the playbook and the step to start from.

## Step 2: Copy the steps into the todo list

Copy each playbook step into the todo list, in order, with its stop. Do not merge two steps, and
do not drop a step.

When you skip a step, keep it in the list. Mark it done, and add the reason, such as
`skipped: the ticket has a spec`.

**Done when:** the todo list holds every playbook step.

## Step 3: Run the steps

Run each step in order. Mark each todo when its step is done.

- Before an action on the pause list, stop (H4). A step that would do the action does not do it.
- When a step returns an open `D` entry, stop (H3).
- When a step fails and gives no `D` entry, stop, and show the failure as an H3 stop.

**Done when:** the playbook's done line holds, or the run is at a stop.

## Step 4: Stop

At each stop:

1. Write the plan with `/update-plan`. Record the playbook, the stop, and the next step in
   `## Progress`, so a fresh run can continue. Before a plan exists (H1), skip `/update-plan`.
   The command to continue is `/work-on @<spec path>`, or `/work-on <ticket key>` when
   `/refine-ticket` wrote the spec back to the ticket.
2. End the turn with one line that names the stop and the command to continue:

   ```
   H2: approve the plan at <plan path>. Continue: /work-on @<plan path>
   ```

Write no other text after the line.

**Done when:** the plan holds the stop, and the last line of the turn names the stop and the
command to continue.
