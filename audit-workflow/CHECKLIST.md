# Audit Checklist

Structured areas to examine during a workflow audit. Not every area will produce a finding - focus on the highest-impact issues.

## CLAUDE.md Health

- [ ] Every line passes the "would removing this cause mistakes?" test
- [ ] No duplication between CLAUDE.md and skills or reference files
- [ ] Progressive disclosure: high-level rules in CLAUDE.md, details in `@`-referenced files
- [ ] File under 50 lines (global) / under 100 lines (project)
- [ ] `IMPORTANT:` or `YOU MUST` used only for rules Claude consistently ignores

## Skills Pipeline

- [ ] Skills chain logically (spike-it -> task-it -> plan-it -> do-it -> close-it)
- [ ] No gaps: frequent manual tasks that should be skills
- [ ] Descriptions include "Use when..." triggers with specific keywords
- [ ] `disable-model-invocation: true` on skills with side effects
- [ ] SKILL.md files under 100 lines; details split to reference files
- [ ] No stale skills referencing outdated patterns

## Memory

- [ ] MEMORY.md exists for the active project path
- [ ] Migration state is tracked (what's done, what's in progress)
- [ ] Common file paths and patterns are captured
- [ ] No stale entries contradicting current codebase state
- [ ] Topic files linked from MEMORY.md for detailed knowledge

## Plans (last 10-20)

- [ ] No recurring pattern appears in 3+ plans without being a skill or reference
- [ ] Verification blocks are consistent
- [ ] Plans reference existing utilities rather than reimplementing
- [ ] No plans that were blocked by the same issue repeatedly

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
