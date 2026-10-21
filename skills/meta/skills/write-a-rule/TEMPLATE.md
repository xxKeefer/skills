# Rule Template

```markdown
---
paths:
  - "<owning dir>/**"
---

# <Module>

<One-line purpose.>

## Language

> **<Core model in one sentence.>**

| Term | Definition | Avoid |
|---|---|---|
| **<Term>** | <What it is, in the module's words.> | <Words that mean the same thing but are not used here.> |

## Layout

- `<path>/` <what lives here and why it is separate>.

Only deviations from the repo default, or what a new file must follow.

## Patterns

- **<Pattern name>.** <One sentence.> Exemplar: `<path/to/file>`.

Cite a file, never paste code. Code blocks rot.

## Invariants

1. <Testable statement the code must keep true.>

## Gotchas

- <Observed mistake and the correct move.>

Optional. Observed mistakes only.

State `🧭 <module>` on your first reply after this rule loads.
```

## Rules of the template

- Section order is fixed. Remove an empty section, do not leave a bare heading.
- Soft cap about 600 words. Over the cap, the directory probably holds two modules.
- One glob per owning directory. Devs widen it later as the escape hatch.
- The canary line is always last. Remove it once the rule is trusted.
