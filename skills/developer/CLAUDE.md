# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed. `code-review` (adopted from Matt Pocock's set, MIT, v1.1.0) reads the
repo's `docs/agents/issue-tracker.md`, written once by `/set-up-dev-workflow-skills` in the
`utility` domain.

## Workflow

```
idea -> grill -> handoff -> implement (uses tdd)
  projects:promote-card = vault-native on-ramp for a bare board card with no code context yet --
  grills it into a spec and tickets, when the tracker is an Obsidian Kanban board

After implementation: code-review (standards + spec, since a fixed point)

After implementation: happy-path (manual QA checklist)
                        -> fix (broken behaviour found in QA)
                        -> diagnose (non-obvious root cause) -> fix
                        -> tweak (small polish edits)

Closure: resolve-feedback (review feedback), resolve-conflicts (merge/rebase conflicts)

Anytime: sync-docs
```

Environment setup (pre-commit hooks) lives in the `utility` domain.

## Skills

| Skill | Purpose |
|---|---|
| `/grill-with-docs` | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Build a throwaway prototype to answer a design question |
| `/implement` | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Red-green-refactor loop |
| `/tweak` | Apply small, focused edits to recently built work |
| `/diagnose` | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Fix a broken behaviour found during manual QA -- lighter than a full bug hunt |
| `/happy-path` | Generate a manual QA test plan for the current changeset |
| `/code-review` | Two-axis review of changes since a fixed point: standards and spec |
| `/resolve-feedback` | Critically assess code review feedback |
| `/resolve-conflicts` | Resolve git merge/rebase conflicts using history; HITL on complex cases, follows test/refactor links |
| `/sync-docs` | Sync documentation to code changes |
| `/domain-modeling` | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Deep-module vocabulary the architecture skills compose |
| `/improve-codebase-architecture` | Scan for deepening opportunities, HTML report, grill through picks |
