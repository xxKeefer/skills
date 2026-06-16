# Procedure File Format

A procedure file collects related how-tos for one area. Terse by default; offloaded so the brain
can forget the steps and recall them from the vault.

## File frontmatter

A new procedure file starts with:

```yaml
---
tags:
  - procedure/<area>
created: <YYYY-MM-DD>
source: conversation
---
```

- `<area>` -- the file's slug (e.g. `work`, `nix`, `homelab`).
- `source: conversation` when mined from an agent session; drop or change if captured from notes.
- Appending to an existing file leaves its frontmatter untouched.

## Entry format -- terse (default)

Most procedures are short. One `##` heading per procedure:

```markdown
## <Title>

*When/why: one line of context (optional).*

1. First step
2. Second step
3. ...

> [!warning] Gotcha worth flagging (optional)
```

Rules:

- Title is a plain imperative ("Deploy a branch version", "Reset a stuck migration").
- Steps are numbered when ordered, bullets when not. Commands in backticks/code fences.
- Gotchas, warnings, and "don't do this" notes go in `> [!warning]` / `> [!note]` callouts.
- Reference-only entries (connection strings, label tables) skip the steps and just hold the block.
- No filler. Every line is something the user would actually re-read mid-task.

## Entry format -- long-form (complex captures)

When the captured task is large (a multi-phase migration, a first-time setup with a mental model),
use the extended shape. Sub-headings are `###` under the entry's `##` title:

```markdown
## <Title>

Short framing paragraph -- what this is and when you'd do it.

### Mental model

The one idea that makes the rest make sense.

### Phase A -- <name>

1. ...

### Phase B -- <name>

1. ...

### Known issues

- Symptom -> fix.

### Lessons

- What you'd do differently next time.
```

Use long-form only when terse genuinely can't hold it. Default to terse.
