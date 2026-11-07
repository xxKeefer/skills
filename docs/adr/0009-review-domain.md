# 0009 The review domain

**Status:** Accepted, 2026-11-06. Renamed `code-review` on 2026-11-07, so the `review:` prefix below is now `code-review:`. ADR 0010 merges `engineering` into `developer` and supersedes "How engineering loads".

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
`/code-review:mob-review`. A call by name can cross plugins. A path cannot.

`review` requires `primitives` and `developer`, because `review-pr` and `pickup` call `/claim`.
`engineering` requires `primitives`, `developer`, and `review`.

Options not chosen:

- One copy of the personas in each domain. Each persona edit and each calibration entry must go
  to two copies, and nothing keeps them in sync.
- The personas in one domain, and the other domain reads them by path. The path breaks in a
  copied install (ADR 0001).
- The personas at the repo root. A path above a plugin root also breaks in a copied install.

## How engineering loads

`developer` and `review` load in every session, from `enabledPlugins` in the user settings.
`engineering` loads in work sessions only. The user settings do not list it. Instead, the main
checkout of each work repo turns it on in its `.claude/settings.local.json`:

```json
"enabledPlugins": { "engineering@xxkeefer-skills": true }
```

Git ignores that file, so the entry stays on one machine and changes no team file. These facts
support the choice. The docs and tests on 2026-11-06, with Claude Code 2.1.319, showed them:

- `enabledPlugins` merges key by key. For each plugin, the most specific source that names it
  wins, so a local file can turn on a plugin that the user settings do not list
  (https://code.claude.com/docs/en/plugins/loading.md, "Find where a plugin is enabled").
- Claude Code reads `.claude/settings.local.json` at the git root of the session. A session in a
  worktree reads the file in the main checkout. In a test, a worktree with no local file loaded
  `engineering` from the main checkout's file. So each worktree gets `engineering` with no setup.
- Claude Code reads no settings from a parent folder. In a test, a session in a child git repo,
  and one in a plain subfolder, did not load `engineering` from the parent's local file.
- A relative-path plugin needs no install record (loading.md). In a test, a local settings entry
  alone loaded `engineering`, so `claude plugin install` is not necessary.

Options not chosen:

- `engineering` on in the user settings. Each home session then loads the ticket and PR skills.
- One local file in the parent folder that holds the work repos. It does not reach the repos.
- A shell function that adds `--settings` in the work folder. It applies only to the terminal,
  and not to the desktop app or an IDE.
- No setting turns a plugin on by path or glob. `--settings` and `--plugin-dir` apply to one
  session only.

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
- A home session loads `developer` and `review`. A work session loads all three domains. See "How
  engineering loads". Each skill name lives in one domain, so no session lists a name twice.
- Each new work repo needs the `engineering` entry once, in its main checkout. A work session
  started in a folder that is not a git repo reads that folder's own `.claude/settings.local.json`,
  so that folder needs the entry too.
