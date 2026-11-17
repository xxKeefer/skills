# 0017 A dated skill lifecycle, with no `experimental` domain

**Status:** Accepted, 2026-11-16.

## Context

A new skill landed in the `experimental` domain. When it proved its value, a human moved it to a
stable domain. When it fell out of use, a human moved it to `deprecated`, and later deleted it.

Each promotion needed a move, a README edit in two domains, and two version bumps.

A skill in `deprecated` had no date. Nothing told the user when a skill was ready to delete.

## Decision

- Remove the `experimental` domain. A new skill lands in the domain that it belongs to.
- Its skills moved: `retro`, `stand-up`, and `tidy-up` to `engineering`, `simulate` and
  `roleplay` to `primitives`, and `lobotomize` to `deprecated`.
- When a skill falls out of use, `/retire-a-skill` moves it to `deprecated` and writes
  `deprecated: <date>` into its frontmatter.
- `skills/meta/skills/retire-a-skill/scripts/due.py` lists each deprecated skill that is more than
  30 days old, with its count from the skill tally. The user deletes a listed skill with
  `/retire-a-skill`.
- Each move stays a human decision.

Options not chosen:

- Keep `experimental`, and add dates to it. A promotion still costs a move.
- Delete a skill with no `deprecated` stage. A skill that the user still needs is then lost
  without a warning period.

## Consequences

- A machine with `"experimental@xxkeefer-skills"` in `enabledPlugins` must delete that line, or
  Claude Code reports a missing plugin.
- A deprecated skill with no `deprecated:` key makes `due.py` exit 1, with an error line that
  names the file.
- The tally count helps the user decide. A count above 0 shows that the skill was used in the
  tally period.
