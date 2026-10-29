# Utility

Dev-environment setup skills — one-shot configuration tasks that prepare a repo or machine for
agent-assisted work. Kept separate from `developer` (which is day-to-day engineering workflow) so
the setup skills are easy to find, maintain, or retire on their own.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## Design Principles

- **One-shot, not recurring**: these run once when setting up a project, not in the daily loop.
- **Deterministic feedback loops**: they install guard rails agents cannot bypass.
- **Self-contained**: each installer keeps the files it installs in its own skill folder and finds
  them with `${CLAUDE_SKILL_DIR}`, so it works from any install.
