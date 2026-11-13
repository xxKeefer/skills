# 0013 One engineering domain, with lifecycle commands

**Status:** Accepted, 2026-11-13. Supersedes ADR 0009 and ADR 0010. ADR 0015 replaces its `build`
line.

## Context

ADR 0010 split the dev skills by theme: `developer` builds code, and `code-review` improves it.
Each domain required the other. `start-ticket` names the review skills, and `review-pr` and
`pickup` call `/claim`. So no machine loaded one without the other. ADR 0002 says that a split no
machine enables alone adds an install unit and gives nothing back.

ADR 0009 made the review domain because a skill cannot read a file in another plugin (ADR 0001).
In one plugin, that limit goes away.

The domain held 68 skills and no front door. The user had to know which of the 68 to start.
`addyosmani/agent-skills` puts nine lifecycle commands over its skills: `/spec`, `/plan`, `/build`,
`/test`, `/constraints`, `/review`, `/webperf`, `/code-simplify`, and `/ship`.

## Decision

- Merge `developer` and `code-review` into one domain, `engineering`, at version 1.0.0. Each skill
  keeps its name. Its prefix changes to `engineering:`.
- Add nine commands with those names. Each one has `disable-model-invocation: true`, and its
  description starts with `★ `, so the commands stand out in the terminal list.
- A command picks a skill below it and runs it by name. Six commands only route: `spec`, `plan`,
  `build`, `test`, `review`, and `ship`. Three hold their own steps, because no skill below them
  does the work: `constraints`, `webperf`, and `code-simplify`.
- `build` runs one step with `/do-next`. It has no `auto` mode. `/run-wave` runs every step. Two
  skills with one job each beat one skill with two modes.

Options not chosen:

- Keep two domains and put the commands in one of them. A call by name crosses plugins, so this
  works, but the dependency cycle stays.
- Rename `start-ticket` to `plan` and `do-next` to `build` in place of wrappers. `do-next` is a
  primitive that other domains use, and `start-ticket` is named after the tracker flow.

## Consequences

- Settings that list `developer@xxkeefer-skills` or `code-review@xxkeefer-skills` must list
  `engineering@xxkeefer-skills` instead.
- A prompt or a report that names `/developer:` or `/code-review:` must name `/engineering:`.
  Old HTML reports keep the old prefix in their copy prompts.
- `/review` and `/plan` share a name with a built-in command. Type `/engineering:review` or
  `/engineering:plan` when the bare name opens the built-in.
- The North Star exception for personas now names `engineering`.
