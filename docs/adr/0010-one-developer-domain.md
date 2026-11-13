# 0010 One developer domain

**Status:** Superseded by ADR 0013, 2026-11-13. Accepted 2026-11-07. Supersedes ADR 0008. Supersedes "How engineering loads" in ADR
0009.

## Context

ADR 0008 split `developer` and `engineering` by use: work at an employer, and personal side
projects. ADR 0009 then moved code review out to its own domain, and each skill name came to live
in one domain only. After that, the split was by name, not by use. `engineering` held 7 skills, and
it needed `developer` for every build, debug, and QA step.

## Decision

Merge `engineering` into `developer`. Split the dev skills by theme instead:

- `developer` implements code, broadly: ticket, plan, build, debug, QA, and PR.
- `code-review` improves code: the personas, the review panels, and PR review. ADR 0009 named it
  `review`. It took the name `code-review` on 2026-11-07.

The 7 skills keep their names. Their prefix changes from `engineering:` to `developer:`.
`TEST-APPROACH.md` moves to `developer`. `developer` drops its duplicate of `STE.md`.

## Consequences

- A home session now loads the ticket and PR skills too.
- Each work repo that has `"engineering@xxkeefer-skills": true` in its local settings must drop
  the entry. The marketplace has no `engineering` plugin now.
- `developer` requires `code-review`, because `start-ticket` names the review skills. `code-review`
  requires `developer`, because `review-pr` and `pickup` call `/claim`. Both calls go by name, so
  the cycle crosses no path.
- `improve-codebase-architecture` moves to `code-review`, because it improves code. It calls
  `/codebase-design` and `/domain-modeling` by name, so they stay in `developer`.
