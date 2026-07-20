# Triage labels

The five canonical triage roles and the tag strings this repo's kanban board uses for them.
Apply exactly these strings as inline card tags; a card carries at most one state tag at a time.

| Canonical role | Board tag | Meaning |
|---|---|---|
| needs-triage | `#needs-triage` | maintainer needs to evaluate |
| needs-info | `#needs-info` | waiting on reporter |
| ready-for-agent | `#afk` | fully specified, an agent can pick it up with no human context |
| ready-for-human | `#hitl` | needs human implementation |
| wontfix | `#wontfix` | will not be actioned; card moves to the archive |

`#afk` and `#hitl` follow this repo's glossary (see `CONTEXT.md`): AFK = away-from-keyboard
(autonomous agent work), HITL = human-in-the-loop.
