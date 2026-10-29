# Out-of-Scope Knowledge Base

Institutional memory for rejected feature requests. Prevents re-triaging the same ideas and
gives context to anyone who asks "why don't we...?"

## Structure

Create an `.ai/.out-of-scope/` directory at the project root (following the `/write-to-file`
convention). One markdown file per **concept** (not per issue).

```
.ai/.out-of-scope/
  real-time-sync.md
  custom-themes.md
  mobile-app.md
```

## File Format

```markdown
# {Concept Name}

**Decision:** wontfix | deferred
**Last reviewed:** YYYY-MM-DD

## Why Not

1-3 sentences explaining the decision.

## Related Issues

- #N -- {title} ({date})
- #N -- {title} ({date})

## Conditions for Revisiting

What would need to change for this to be reconsidered.
```

## Rules

- **One file per concept** -- multiple issues requesting the same thing get grouped under one file
- **Only rejected enhancements** -- bugs are never out-of-scope, they're just low priority
- **Check during triage** -- before triaging a new enhancement, search `.ai/.out-of-scope/` for prior art
- **Living documents** -- update "Related Issues" when new requests for the same thing arrive
- **Include revisit conditions** -- prevents permanent dismissal without reasoning
