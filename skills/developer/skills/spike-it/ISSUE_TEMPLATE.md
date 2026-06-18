# Issue Template

Use this as a starting structure for the GitHub issue body. Drop irrelevant sections. Add new
sections if the investigation warrants them. Every section must earn its place.

---

```markdown
# {Spike Title}

## The Problem

> One-line summary of why this investigation exists.

- Context bullet points
- What pain or gap prompted this spike

---

## Approach

> One-line summary of the proposed approach.

**Broad Strokes:**

- High-level steps the implementation would take
- Keep to 3-6 bullets

---

## Scope

**Related:** #N, #N _(links to related issues, spikes)_
**Designs:** [link](url) _(if applicable)_
**Feature flag:** `flag_name` _(if applicable)_

**In scope:**

- [ ] Scoped item 1
- [ ] Scoped item 2

**Not in scope:**

- Item explicitly excluded and why

---

## Acceptance Criteria

- [ ] [Single testable assertion a non-technical QA person can manually verify]
- [ ] [Another testable assertion]
- [ ] [Cover happy path, error states, and edge cases]

---

## Dependency Comparison

> Only include if new libraries/dependencies are being evaluated.

| Criteria | Option A | Option B |
|---|---|---|
| Bundle size | | |
| Maintenance (last release, open issues) | | |
| Framework compatibility | | |
| TypeScript support | | |
| API ergonomics | | |
| Community / adoption | | |
| Fits existing stack | | |

**Recommendation:** Which option and why in 1-2 sentences.

---

## Technical Considerations

- Architecture, integration, and implementation concerns
- How this fits (or doesn't) with existing patterns
- Migration cost if introducing new patterns
- API contracts or schema considerations
- Performance implications

---

## Future Work

- Items discovered during the spike that are worth doing but not part of initial scope
```
