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

%% status: active | dormant | waiting | archived. Optional: until: YYYY-MM-DD %%

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
- **`status`** frontmatter is one of four values. `/broadsheet` reads it:

  | Value | Meaning | On `/broadsheet` |
  | --- | --- | --- |
  | `active` | in flight; the default | the board names its next card |
  | `dormant` | at rest by choice | silent |
  | `waiting` | blocked on a person, a date, or an event | one line, only when the project changed in the last 7 days |
  | `archived` | done or dropped; the folder moves to the vault's archive | gone |

- **`until`** frontmatter is optional: the date, `YYYY-MM-DD`, that a `waiting` or `dormant`
  project expects to be `active` again. `/broadsheet` shows it on a `waiting` line. Remove it when
  the status goes back to `active`.
- **Keep the `%%` status line** under the frontmatter, so the file says which values exist.
  Obsidian hides it in reading view.
