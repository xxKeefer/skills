# 0002 The domain map

**Status:** Accepted, 2026-10-28

## Context

The skill-suite clean-up retired, reworked, and refined skills one at a time. After that work,
some structure problems remained that no single skill could fix: shared text copied across
skills, a name clash, assets outside every plugin, and one domain rule that its own skill table
contradicts. Each domain was reviewed against one test from the skill rubric: split only when the
cut earns its load. A new install unit, model-invoked description, or user-invoked name must pay
for itself.

Counts on 2026-10-28:

| Domain | Skills | User-invoked |
| --- | --- | --- |
| primitives | 9 | 2 |
| developer | 16 | 7 |
| scribe | 11 | 6 |
| utility | 6 | 6 |
| meta | 7 | 6 |
| nix-manager | 6 | 4 |
| journal | 6 | 0 |
| omen | 11 | 0 |
| projects | 2 | 0 |
| experimental | 5 | 3 |
| deprecated | 9 | 9 |

## Decision

| Domain | Verdict |
| --- | --- |
| primitives | Keep all nine skills. The membership rule is "depends on no other domain". The old rule, "invoked by other skills, not typically by users", is false: five of the nine skills are invoked by the user, and they include `do-next` and `update-handoff`, the two most-used skills. |
| developer | Keep one domain. A split adds an install unit that no machine enables alone. Add no router skill: the user does not forget which skill to use. |
| scribe | No change. It is the home for prose work. The three lens skills (`asd-ste100`, `grices-maxims`, `orwells-six`) moved here from `experimental` in `d25d84b`, `8995221`, and `bf0586d`. |
| utility | The home for every installer skill. Each installed asset lives inside its installer's skill folder. `setup-tool-policy` lands in `utility`, not `experimental`, because the skill already exists and only its location is wrong. |
| journal, projects, omen, scribe | Share one model-invoked vault discovery skill. Its design and home domain are a separate decision. |
| nix-manager | Prefix all six skills with `nix-`: `nix-add`, `nix-remove`, `nix-rice`, `nix-refine`, `nix-debug`, and `nix-explain`. One prefix for the domain also stops later clashes with generic verbs. |
| omen | Make the six post-session skills user-invoked (`log-session`, `log-cannon`, `log-npcs`, `log-place`, `log-progression`, `make-summary`), and add one user-invoked router that names them in order. No skill invokes them. A merge into one skill was rejected for sprawl. |
| journal | Move the pull-down and carry-forward steps into one `CASCADE.md`, linked by relative path from each skill that uses them. Today the two steps are seven copies of one rule in `daily`, `weekly`, `monthly`, and `reflect`. |
| meta, projects | No change. |
| experimental, deprecated | No change. `deprecated` holds only user-invoked skills, and no skill outside it names one of its skills. |

## Consequences

- No skill moves between domains, so no change needs `/migrate-a-skill`.
- A `primitives` skill must not invoke a skill from another domain. `/do-next` breaks this today
  by sending every step to `/implement`.
- An installer must find its assets with `${CLAUDE_PLUGIN_ROOT}`, not with a path above its plugin
  root. A new hook holder goes inside `utility`.
- After the omen change, the agent no longer fires a post-session skill on its own. The user types
  the router or the skill name. `doctor-setting` must link the `log-cannon` file by path, because
  it can no longer load the skill.
- A rename in `nix-manager` changes what the user types.
