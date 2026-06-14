# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill-it`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed. Ticket-creating skills (`research-it`, `spike-it`, `task-it`, `plan-it`) target
the project's tracker — GitHub via `gh` by default, or whatever the repo's CLAUDE.md declares (e.g.
Jira via the Atlassian MCP).

## Workflow

```
research-it -> spike-it -> task-it -> plan-it -> do-it (uses tdd)

After implementation: happy-path (manual QA checklist)
                        -> fix-it (broken behaviour found in QA)
                        -> hunt-it (non-obvious root cause) -> fix-it / plan-it
                        -> tweak-it (small polish edits)

Closure: resolve-it (review feedback), resolve-conflicts (merge/rebase conflicts)

Anytime: explain-it, document-it
```

Environment setup (pre-commit hooks, git guardrails) lives in the `utility` domain.

## Skills

| Skill | Purpose |
|---|---|
| `/research-it` | Pre-spike research producing decision artifacts that steer spike sessions |
| `/spike-it` | Deep-dive investigation of a problem (PRD process) |
| `/task-it` | Decompose a spike into vertical-slice tracker tickets with HITL/AFK classification |
| `/plan-it` | Break a task into ordered, atomic steps |
| `/do-it` | Execute a plan step-by-step via /tdd |
| `/tdd` | Red-green-refactor loop |
| `/tweak-it` | Apply small, focused edits to recently built work |
| `/hunt-it` | Trace a non-obvious bug to proven root cause, hand off to /fix-it or /plan-it |
| `/fix-it` | Fix a broken behaviour found during manual QA -- lighter than a full bug hunt |
| `/happy-path` | Generate a manual QA test plan for the current changeset |
| `/resolve-it` | Critically assess code review feedback |
| `/resolve-conflicts` | Resolve git merge/rebase conflicts using history; HITL on complex cases, follows test/refactor links |
| `/document-it` | Sync documentation to code changes |
| `/explain-it` | Unpack agent reasoning transparently |

## References

| File | Purpose |
|---|---|
| `references/AGENT-BRIEF.md` | How to write durable agent briefs for AFK issues |
| `references/OUT-OF-SCOPE.md` | How the `.ai/.out-of-scope/` knowledge base works |
