# 0007 Journal and omen invocation

**Status:** Accepted, 2026-10-29

## Context

ADR 0002 decided two changes for these domains: one `CASCADE.md` for the journal pull-down and
carry-forward steps, and a user-invoked router for the six omen post-session skills. It left the
details open. Facts on 2026-10-29:

- All six journal skills were model-invoked, and most of their triggers were bare words: "daily",
  "weekly", "monthly", "yearly", and "reflect". The journal plugin loads in every session on the
  machine where it runs. So a code session about a "daily standup" can fire `/daily`.
- No skill in this repo or the owner's private overlay invokes a journal skill or one of the six
  omen post-session skills. `doctor-setting` cites the `/log-cannon` criteria, but it does not
  invoke the skill.
- The cascade rule had eight copies. Pull-down was in `daily`, `weekly`, and `monthly`.
  Carry-forward was in `daily`, `weekly`, `monthly`, and `reflect`. `yearly` held a shorter
  carry-forward with no push-up, because a year has no parent level. ADR 0002 counted seven copies.
- The omen post-session skills each triggered "after logging a session". `/log-cannon` reads
  `_npcs.md` and `_places.md` so that its wikilinks use known names, but the omen `README.md`
  listed it before `/log-npcs` and `/log-place`.

## Decision

- **Journal skills are user-invoked.** All six skills set `disable-model-invocation: true` and have
  a one-line description. The user starts each one by hand, so the journal domain loads no
  description.
- **One cascade file.** `skills/journal/CASCADE.md`, at the plugin root, holds the pull-down and
  carry-forward rules for all four levels, and a table of where each level keeps its items.
  `daily`, `weekly`, `monthly`, `yearly`, and `reflect` link it as `../../CASCADE.md`, the pattern
  of ADR 0003. The journal `CLAUDE.md` links the file in place of its own description of the
  mechanic.
- **Yearly joins the cascade.** At the yearly level, carry-forward drops each unselected item.
- **The router is `/debrief-session`.** It is user-invoked. Its name pairs with `/plan-session`,
  which runs before a game, and with `/log-session`. It names the six skills in data order:
  `log-session`, `log-npcs`, `log-place`, `log-cannon`, `log-progression`, `make-summary`. The
  NPC and place indexes are current before `/log-cannon` links them, and `/make-summary` reads the
  canon entries of this session. The omen `README.md` table uses the same order.
- **The six omen post-session skills are user-invoked**, as ADR 0002 decided, with a one-line
  description each. `doctor-setting` links the `log-cannon` `SKILL.md` for its canon criteria.

Options not chosen:

- Narrow the `/daily` trigger to phrases such as "daily note" and "plan my day". False fires
  become less frequent, but the description still loads every turn.
- Make only `/daily` user-invoked, or only the four generators. `/update-occasions-config` was the
  weakest case for the change: with model invocation, the agent can offer a sync after the user
  edits `occasions.md`.
- Keep the `yearly` carry-forward as its own text. It is the same rule with no parent, so a
  separate copy can drift.
- Name the router `/after-session`, which says when to run it and not what it does, or
  `/wrap-session`, where "wrap" has several meanings.
- Keep the old `README.md` order in the router.
- Amend ADR 0002, or record no ADR. The journal invocation choice is new, and ADR 0002 does not
  cover it.

## Consequences

- The agent cannot start a journal skill or an omen post-session skill on its own. No other skill
  can invoke them. A skill that needs their rules must link a file.
- After an edit to `occasions.md`, the user runs `/update-occasions-config` by hand.
- A change to the cascade rule edits `CASCADE.md` only.
- Five omen skills stay model-invoked: `scaffold-setting`, `doctor-setting`, `plan-session`,
  `make-blurb`, and `make-lore`.
