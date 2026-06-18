# MISSION.md Format

`MISSION.md` lives at the project workspace root. It captures **why this project exists** and **what
done looks like**. Every status report, sprint summary, and decision should trace back to it. It is
the project's compass -- when scope drifts, this is what you check against.

## Template

```md
---
type: project/mission
status: active
tags: [project]
---

# Mission: {Project Name}

## Why
{1-3 sentences. The concrete outcome this project delivers. What changes when it's done? Avoid
abstract framings -- push for the real-world result.}

## Definition of done
- {A specific, observable condition that must be true for the project to be complete}
- {Another}
- {...}

## Constraints
- {Budget, deadline, dependencies, people involved, anything that bounds the approach}

## Out of scope
- {Adjacent work this project explicitly will not do -- protects focus}
```

## Rules

- **One mission per project.** Two unrelated goals are two projects.
- **Concrete over abstract.** "Move into the new house by {month}" beats "sort out housing."
- **Definition of done is a checklist, not a vibe.** Each item must be observably true or false.
- **Push back on vagueness.** If the user can't say why the project exists, grill them before writing.
- **Revise when reality shifts.** Missions change. Update this file and record the shift in a
  decision (see [DECISIONS-FORMAT.md](DECISIONS-FORMAT.md)). Don't leave a stale mission steering work.
- **Keep it short.** Past a screen, it has stopped being a compass and become a plan -- that belongs
  on the board.
- **`status`** frontmatter is `active` while in flight; `/close-project` sets it to `done`.
