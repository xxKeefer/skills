# Agent Brief Template

How to write durable agent briefs for AFK (fully autonomous) issues.

## Template

```markdown
## Agent Brief

**Category:** bug | enhancement
**Summary:** one-line description

**Current behavior:** what happens now
**Desired behavior:** what should happen after

**Key interfaces:**
- `TypeName` -- what needs to change and why
- `functionName()` -- current vs desired return

**Acceptance criteria:**
- [ ] Specific, testable criterion

**Out of scope:**
- Thing that should NOT be changed
```

## Principles

- **Durability over precision** -- no file paths, no line numbers. Describe behaviours and
  contracts, not locations. Paths go stale; behaviours survive refactors.
- **Behavioural, not procedural** -- describe *what*, not *how*. The agent picks the approach.
- **Complete acceptance criteria** -- agent must know when it's done without asking.
- **Explicit scope boundaries** -- prevent gold-plating. "Out of scope" is mandatory.
- **Domain language** -- use the project's ubiquitous language (check `UBIQUITOUS_LANGUAGE.md`
  if it exists). Avoid internal jargon the agent won't know.

## When to Write One

An agent brief is added as a comment when an issue transitions to `ready-for-agent` state
(via `/triage-it`). Not every issue needs one -- only AFK issues where an autonomous agent
will pick up the work without human guidance.
