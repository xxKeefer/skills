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

````markdown
## <Title>

> When/why: one sentence of context (optional).

1. First step:
   ```bash
   <one command>
   ```
2. Second step
3. ...

> [!warning] Short title (optional)
> One or two lines: what goes wrong, and what to do instead.

### Reference (optional)

- [<Link name>](<url>)

```<value-name>
<value>
```
````

Rules:

- Title is a plain imperative ("Deploy a branch version", "Reset a stuck migration").
- Steps are numbered when ordered, bullets when not.
- One command per code fence, so that click-to-copy copies one runnable command. An alternative
  command gets its own fence. Indent each fence under its step so that the list numbers hold.
- Put the explanation of a command in the step text, outside the fence, so that a copy holds only
  the command.
- One value per fence for credentials, hosts, and IDs. Name the value in the fence's info string,
  for example ```` ```password ````.
- Gotchas, warnings, and "don't do this" notes go in `> [!warning]` / `> [!note]` callouts. Give
  each callout a short title line, then a `>` body line.
- Links, values, tables, and connection strings that the steps use go in a `### Reference`
  sub-section at the end of the entry, so that the material sits with the steps that use it.
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

### Reference

- Links, values, and tables the phases use.
```

Use long-form only when terse genuinely can't hold it. Default to terse.
