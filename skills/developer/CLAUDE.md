# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed. Ticket-creating skills (`research`, `spike`, `to-tickets`, `to-plan`) target
the project's tracker — GitHub via `gh` by default, or whatever the repo's CLAUDE.md declares (e.g.
Jira via the Atlassian MCP).

## Workflow

```
research -> spike -> to-tickets -> to-plan -> implement (uses tdd)

After implementation: happy-path (manual QA checklist)
                        -> fix (broken behaviour found in QA)
                        -> diagnose (non-obvious root cause) -> fix / to-plan
                        -> tweak (small polish edits)

Closure: resolve-feedback (review feedback), resolve-conflicts (merge/rebase conflicts)

Anytime: explain-reasoning, sync-docs
```

Environment setup (pre-commit hooks, git guardrails) lives in the `utility` domain.

## Skills

| Skill | Purpose |
|---|---|
| `/research` | Pre-spike research producing decision artifacts that steer spike sessions |
| `/grill-with-docs` | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Build a throwaway prototype to answer a design question |
| `/spike` | Deep-dive investigation of a problem (PRD process) |
| `/to-tickets` | Decompose a spike into vertical-slice tracker tickets with HITL/AFK classification |
| `/to-plan` | Break a task into ordered, atomic steps |
| `/implement` | Execute a plan step-by-step via /tdd |
| `/tdd` | Red-green-refactor loop |
| `/tweak` | Apply small, focused edits to recently built work |
| `/diagnose` | Trace a non-obvious bug to proven root cause, hand off to /fix or /to-plan |
| `/fix` | Fix a broken behaviour found during manual QA -- lighter than a full bug hunt |
| `/happy-path` | Generate a manual QA test plan for the current changeset |
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
| `references/AGENT-BRIEF.md` | How to write durable agent briefs for AFK issues |
| `references/OUT-OF-SCOPE.md` | How the `.ai/.out-of-scope/` knowledge base works |
