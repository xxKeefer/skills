# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed. `spike` targets the project's tracker — GitHub via `gh` by default, or
whatever the repo's CLAUDE.md declares (e.g. Jira via the Atlassian MCP). The skills adopted from
Matt Pocock's set (`wayfinder`, `to-spec`, `to-tickets`, `triage`, `code-review` — MIT, v1.1.0)
instead read the repo's `docs/agents/issue-tracker.md`, written once by
`/set-up-dev-workflow-skills` in the `utility` domain.

## Workflow

```
idea -> to-spec -> to-tickets -> implement (uses tdd)
  wayfinder = large-effort on-ramp; spike = deep-dive investigation feeding implement
  triage = keep the tracker's issues/PRs agent-ready

After implementation: code-review (standards + spec, since a fixed point)

After implementation: happy-path (manual QA checklist)
                        -> fix (broken behaviour found in QA)
                        -> diagnose (non-obvious root cause) -> fix
                        -> tweak (small polish edits)

Closure: resolve-feedback (review feedback), resolve-conflicts (merge/rebase conflicts)

Anytime: explain-reasoning, sync-docs
```

Environment setup (pre-commit hooks, git guardrails) lives in the `utility` domain.

## Skills

| Skill | Purpose |
|---|---|
| `/grill-with-docs` | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Build a throwaway prototype to answer a design question |
| `/spike` | Deep-dive investigation of a problem (PRD process) |
| `/wayfinder` | Decision-mapping for large-scale work (fog-of-war, HITL/AFK tickets) |
| `/to-spec` | Turn an idea or conversation into a published spec |
| `/to-tickets` | Break a spec into tracer-bullet vertical-slice tickets |
| `/triage` | Move issues and external PRs through the triage state machine, write agent-ready briefs |
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
| `/explain-reasoning` | Unpack agent reasoning transparently |
| `/domain-modeling` | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Deep-module vocabulary the architecture skills compose |
| `/improve-codebase-architecture` | Scan for deepening opportunities, HTML report, grill through picks |

## References

| File | Purpose |
|---|---|
| `skills/triage/AGENT-BRIEF.md` | How to write durable agent briefs for AFK issues |
| `skills/triage/OUT-OF-SCOPE.md` | How the `.ai/.out-of-scope/` knowledge base works |
