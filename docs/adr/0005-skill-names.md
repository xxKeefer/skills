# 0005 Each skill name is unique

**Status:** Accepted, 2026-10-29

## Context

A user types a skill by its name, and the skill tally counts uses by name. Two skills with one name
cannot be told apart in either place.

On 2026-10-29 one name was used twice in this repo: `explain`, in `primitives` and `nix-manager`.
The tally merged their uses. No name in this repo was also used in the owner's private overlay, a
second skills repo that is installed beside this one.

`nix-manager` named all six of its skills with bare verbs: `add`, `remove`, `rice`, `refine`,
`debug`, and `explain`. Its skills work on one tool, NixOS, but the names do not say so. ADR 0002
chose the `nix-` prefix for all six skills.

## Decision

- **Unique.** A skill name is unique across this repo and the private overlay.
- **Tool prefix.** A domain bound to one tool prefixes every skill with the name of that tool:
  `nix-add`, `nix-remove`, `nix-rice`, `nix-refine`, `nix-debug`, and `nix-explain`.
- Workflow verbs in tool-agnostic domains stay bare, for example `developer:fix` and
  `primitives:grill`.
- `/write-a-skill` searches for the new name before it drafts a skill.
- A rename that removes a name the user types is a breaking change. It takes a major version bump.
  `nix-manager` goes from 2.1.0 to 3.0.0, as the `*-it` rename did in `0b7b916`.

Options not chosen:

- A domain prefix on every generic verb. It also covers `developer:fix`, `tweak`, `implement`,
  `diagnose`, `scribe:teach`, and `primitives:grill` and `explain`, so it needs renames or a list
  of exceptions.
- Uniqueness only. The `nix-` prefix then rests on ADR 0002 alone, and a later tool domain gets no
  rule.
- A minor version bump, as parent rule 3 of the skill-suite handoff gives for other changes.

## Consequences

- `primitives:explain` keeps its name, and `nix-manager:nix-explain` composes on it.
- A user types `/nix-add` in place of `/add`. The old names no longer exist.
- Uses that the tally recorded under the old names stay under the old names.
- A skill that another skill invokes changes its name only when every caller changes in the same
  commit. All callers of `nix-debug` and `nix-refine` are inside `nix-manager`.
