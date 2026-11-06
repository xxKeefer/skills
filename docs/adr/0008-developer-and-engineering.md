# 0008 Developer and engineering

**Status:** Accepted, 2026-11-06. ADR 0009 moves the personas and the review skills to `review`.

## Context

ADR 0002 kept `developer` as one domain, because a split adds an install unit that no machine
enables alone. After a merge of new workflow skills, `developer` held 63 skills. It fit neither of
the owner's two uses:

- Work at an employer needs the full ticket-to-PR flow, the review panel, and its process steps.
- Personal side projects need a lighter flow with the owner's own opinions.

One domain that serves both uses is a compromise that serves neither one well.

## Decision

Split by use, not by skill type:

- `engineering` is the domain for work at an employer. It starts as a copy of `developer` at
  version 1.0.0.
- `developer` is the domain for personal side projects. It keeps its name and version.

Each domain then changes on its own. A skill can exist in both domains with the same name, because
Claude Code puts the plugin name in front of each skill name (`developer:tdd`, `engineering:tdd`).

The agnostic bar binds both domains. `engineering` names no employer or client code, and the
pre-commit hook checks it like every other domain.

## Consequences

- At the start, the two domains hold the same 63 skills. Each edit to a shared skill must go to
  one domain, to the other, or to both. Nothing keeps them in sync.
- When both domains are on in one session, each skill name exists twice. The model-invoked
  descriptions load twice, and a bare `/tdd` has two targets. Turn on one domain per context.
