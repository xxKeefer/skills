# Frontmatter Standardisation

Every triage standardises frontmatter on the surviving artifact. The inbox note arrives with the
`take-a-note` capture shape:

```yaml
---
source: {conversation | https://... | tool:name}
created: {YYYY-MM-DD}
---

#raw
```

## Rules

- **Drop the `#raw` tag** on promotion -- it marks "untriaged", which is no longer true.
- **Keep `created`** if present and accurate; otherwise set it from the file's own date or the
  capture date in the body. Don't invent precision you don't have.
- **Add `updated: {today}`** when you rewrite or move content.
- **Set real tags** that aid retrieval, per the vault's tag taxonomy (see vault `README.md`). Inbox
  notes rarely have these; supply them.
- **Carry `source` forward** -- provenance is worth keeping.

## Respect existing conventions

Some destinations already carry solid, schema-bound frontmatter -- journal files, project files,
campaign notes. **Do not flatten these.** When a task or note lands in such a file, match its
existing frontmatter shape; don't impose the capture shape on top of it.

When promoting a fleeting note into a folder that *doesn't* enforce a schema (`research`, `work`,
generic `reference`), the target shape is minimal:

```yaml
---
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
source: {original source}
tags: [retrieval, tags, here]
---
```

## Archive

Archived notes keep their frontmatter and gain a marker:

```yaml
archived: {YYYY-MM-DD}
```

Add it; don't strip the rest. `98-archive/` is soft-delete, so the note must stay legible for the
monthly review.
