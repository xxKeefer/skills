# Decisions Format

Decision records live in `decisions/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`,
etc. Create the directory lazily -- only when the first decision is written.

They are the project equivalent of ADRs: they capture **why a non-obvious choice was made** so future
sessions (and collaborators) don't relitigate it or quietly reverse it.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what was decided, and why it matters. State the alternative that was rejected and
the reason, when it's not obvious.}
```

That is the whole format. A decision record can be a single paragraph. The value is recording *that*
the choice was made and *why* -- not filling out sections.

## Optional sections

Only when they add genuine value:

- **Status** frontmatter (`active | superseded by NNNN`) -- when a later decision reverses this one.
- **Context** -- the situation that forced the choice, when non-obvious.
- **Consequences** -- what this locks in or rules out downstream.

## Numbering

Scan `decisions/` for the highest existing number and increment by one.

## When to write a decision record

Write one when any of these is true:

1. **A non-obvious choice was made** that someone might later question or reverse -- a vendor,
   a layout, a sequencing call, a scope cut.
2. **The mission shifted** -- record the change here and update `MISSION.md`.
3. **A constraint was discovered** that reshapes the plan -- a budget, a deadline, a dependency.

### What does *not* qualify

- Routine task progress. That's the board's job.
- Anything already obvious from the mission or the board.

## Supersession

When a later record reverses an earlier one, mark the old one `Status: superseded by NNNN` rather
than deleting it. The history of how the project's thinking evolved is itself useful.
