# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill-it`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed. Ticket-creating skills (`research-it`, `spike-it`, `task-it`, `plan-it`) target
the project's tracker — GitHub via `gh` by default, or whatever the repo's CLAUDE.md declares (e.g.
Jira via the Atlassian MCP). Some skills (`hunt-it`, `qa-it`, `triage-it`) are still GitHub-specific.

## Workflow

```
research-it -> spike-it -> task-it -> plan-it -> do-it (uses tdd)
                              ^
                          design-it (explore APIs)
                          hunt-it (track bugs -> issue)
                          refactor-it (improve existing code -> issue)

Triage: triage-it (label state machine, agent briefs)
QA: qa-it (interactive bug intake -> issues)

Anytime: explain-it, document-it, improve-it
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
| `/hunt-it` | Trace a bug from report to root cause, file GitHub issue with TDD fix plan |
| `/resolve-it` | Critically assess code review feedback |
| `/resolve-conflicts` | Resolve git merge/rebase conflicts using history; HITL on complex cases, follows test/refactor links |
| `/design-it` | Generate multiple radically different interface designs |
| `/document-it` | Sync documentation to code changes |
| `/improve-it` | Find architectural improvement opportunities |
| `/explain-it` | Unpack agent reasoning transparently |
| `/triage-it` | Label-based state machine for GitHub issue triage |
| `/qa-it` | Interactive bug intake session, files GitHub issues |
| `/refactor-it` | Interview-driven refactor planning with tiny commits |

## References

| File | Purpose |
|---|---|
| `references/AGENT-BRIEF.md` | How to write durable agent briefs for AFK issues |
| `references/OUT-OF-SCOPE.md` | How the `.ai/.out-of-scope/` knowledge base works |
