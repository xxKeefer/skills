# 0009 The review domain

**Status:** Accepted, 2026-11-06

## Context

ADR 0008 split `developer` and `engineering`, and each domain started with the same 63 skills.
Both domains then held the 37 `persona-*` skills, `PERSONA-CONTRACT.md`, and the review skills.

`mob-review` reads each persona and the contract by path. `self-improve`, `update-personas`, and
`sad-path` also read persona files by path. A path above a plugin root does not resolve in a
copied install (ADR 0001). So a skill in one plugin cannot read a persona in another plugin, and
personas can be shared only inside one plugin.

The PRD plan for `engineering` adds `light-review`, a smaller panel that reads the same personas.
It also makes `mob-review` read `post-review-comments`, and `pickup` read `resolve-feedback`, by
path.

## Decision

Make a `review` domain. It holds the 37 personas, `PERSONA-CONTRACT.md`, and these 8 skills:

- the panel and its upkeep: `mob-review`, `self-improve`, `update-personas`, and `sad-path`
- the PR review skills: `review-pr`, `post-review-comments`, `pickup`, and `resolve-feedback`

Each file that a review skill reads by path is in the `review` plugin. `developer` and
`engineering` call the review skills by name, with the plugin prefix, such as
`/review:mob-review`. A call by name can cross plugins. A path cannot.

`review` requires `primitives` and `developer`, because `review-pr` and `pickup` call `/claim`.
`engineering` requires `primitives` and `review`.

Options not chosen:

- One copy of the personas in each domain. Each persona edit and each calibration entry must go
  to two copies, and nothing keeps them in sync.
- The personas in one domain, and the other domain reads them by path. The path breaks in a
  copied install (ADR 0001).
- The personas at the repo root. A path above a plugin root also breaks in a copied install.

## Consequences

- `engineering` lost 45 skills and now holds 18.
- The North Star exception for personas names `review`. The agnostic bar and the rules for
  editing personas moved to the `review` `CLAUDE.md`.
- On 2026-11-06, the absorb plan deleted the copies that `developer` held of the 8 review skills,
  the personas, and the contract. Before that, a session with `developer` and `review` on loaded
  each review skill name twice.
- A skill names a review skill with the `review:` prefix, in its own text and in each prompt that
  it builds. The prefix stays valid after the absorb plan.
- A skill that moves into or out of `review` must not leave a path read across the plugin
  boundary. Change each such read into a call by name.
