# Utility

Dev-environment setup skills — one-shot configuration tasks that prepare a repo or machine for
agent-assisted work. Kept separate from `developer` (which is day-to-day engineering workflow) so
the setup skills are easy to find, maintain, or retire on their own.

## Skills

| Skill | Purpose |
|---|---|
| `/setup-pre-commit` | Detect language/toolchain and configure pre-commit hooks (format, type-check, test) |
| `/setup-git-guardrails` | Block dangerous git commands via a Claude Code hook |

## Design Principles

- **One-shot, not recurring**: these run once when setting up a project, not in the daily loop.
- **Deterministic feedback loops**: they install guard rails agents cannot bypass.
