# Audit Checklist

Structured areas to examine during a workflow audit. Not every area will produce a finding - focus on the highest-impact issues.

## CLAUDE.md Health

- [ ] Every line passes the "would removing this cause mistakes?" test
- [ ] No duplication between CLAUDE.md and skills or reference files
- [ ] Progressive disclosure: high-level rules in CLAUDE.md, details in `@`-referenced files
- [ ] File under 50 lines (global) / under 100 lines (project)
- [ ] `IMPORTANT:` or `YOU MUST` used only for rules Claude consistently ignores

## Skills Pipeline

- [ ] Skills chain logically (`idea -> grill -> handoff -> implement (uses tdd)`)
- [ ] No gaps: frequent manual tasks that should be skills
- [ ] Model-invoked descriptions include "Use when..." triggers with specific keywords
- [ ] Skills are user-invoked (`disable-model-invocation: true`) unless the agent or another skill must reach them
- [ ] SKILL.md files under 100 lines; details split to reference files
- [ ] No stale skills referencing outdated patterns

## Memory

- [ ] MEMORY.md exists for the active project path
- [ ] Migration state is tracked (what's done, what's in progress)
- [ ] Common file paths and patterns are captured
- [ ] No stale entries contradicting current codebase state
- [ ] Topic files linked from MEMORY.md for detailed knowledge

## Codebase Conventions

- [ ] Convention drift: files not matching CLAUDE.md/AGENTS.md stated patterns
- [ ] Migration progress: count of files still using legacy patterns
- [ ] Test consistency: single testing paradigm per project
- [ ] Stale TODOs/FIXMEs (older than 6 months)

## Claude Code Configuration

- [ ] Hooks automate deterministic rules (vs advisory CLAUDE.md instructions)
- [ ] Permission allowlist covers common read-only operations
- [ ] Session naming used for multi-day tickets (`--resume`)
- [ ] Context management: `/compact` and `/clear` used between unrelated tasks
