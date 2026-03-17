# PR Template

Generate the PR body from this structure. Remove empty sections. Delete unchecked items. Preserve emoji formatting. Insert generated QA test plan under the Manual Test Plan heading.

---

```markdown
## 📝 Description

_<brief summary of changes>_

## 📸 Screenshots

_<suggested screenshots to capture>_

## 📦 Dependency Updates

- [ ] ➕ Added new dependencies
- [ ] ➖ Removed dependencies
- [ ] 🔼 Upgraded dependencies
- [ ] 🔽 Downgraded dependencies

## 🧪 Testing Details

- [ ] 🧪 Unit tests
- [ ] 🧩 Integration tests
- [ ] 🧑‍🔬 End-to-End tests
- [ ] 🙅 No tests necessary

If this change breaks the End-to-End tests, please provide a link to the relevant pull request here or as a separate comment.

### Manual Test Plan

_<generated QA test plan — one bullet per behaviour, action → expected result>_

## ✅ Checklist

- [ ] I have performed a self-review of my own code.
```
