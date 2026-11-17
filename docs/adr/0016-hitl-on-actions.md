# 0016 HITL on actions, not on skills

**Status:** Accepted, 2026-11-16. Replaces the flag line of ADR 0013.

## Context

ADR 0013 gave each command `disable-model-invocation: true`. Many workflow skills had the same
flag. So only the user could start them. A router or another skill could not call `/plan` after
`/spec`, and the user typed each step of the work from idea to PR.

The flag put the human stop on the skill. But most steps of a workflow skill make output that only
the user or the agent reads. The steps that need the user are the actions that another person
sees, such as a merge or a posted comment. A skill-level flag stops too much and guards too
little. It stops a test round, and it does not guard a merge inside a skill that has no flag.

## Decision

- The HITL line moves from skills to actions.
- The workflow skills lose `disable-model-invocation`. These are the skills that do a step of the
  work from idea to PR. The router and other skills can call them, and the user can still type
  each one. The commands keep the `★ ` prefix.
- **The pause rule:** an action stops for the user when another person reads its output. An action
  whose output only the user or the agent reads runs with no stop.
- **The pause list:** mark a PR ready for review, merge, force-push to a branch that another person
  uses, deploy, delete data or a branch that is not merged, post a comment, a review, or a ticket
  update as the user, write a ticket, and send a message to a person.
- These run with no stop: the end of a ★ skill, a test round or a review round, a push to the
  agent's own branch, and a draft PR.
- When the agent cannot tell if another person reads the output, it stops.
- The rule `pause-list.md` in `install-rules` holds the pause rule and the pause list. It has no
  `paths:` key, so it loads in each session.
- Skills whose job needs the user's judgement keep the flag. Examples are `retro`, `roleplay`, the
  journal skills, the `meta` skills that change the marketplace, the `persona-*` lanes, and the
  `utility` installers.

Options not chosen:

- Keep the flag on the workflow skills, and add a router that tells the user which command to type
  next. The user still types each step, and a flagged skill still guards no action.
- Remove the flag from every skill. A skill whose whole job is the user's judgement, such as
  `retro`, has no use when the agent starts it.

## Consequences

- One request can run `/spec`, then `/plan`, then `/build`, with no typed command between them.
- The agent stops only at an action on the pause list, or at an open `D` entry in a handoff.
  `/plan` also stops on a spec with `status: draft` or an open question, because the confirmed
  spec is the one stop before the plan.
- A machine with no installed `pause-list.md` rule has no guard on these actions. Run
  `/install-rules` on each machine.
- The HITL row in `CONTEXT.md` names the pause list, not the frontmatter flag, as the human stop.
