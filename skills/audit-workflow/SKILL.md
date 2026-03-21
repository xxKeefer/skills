---
name: audit-workflow
description: Audit Claude Code workflow and suggest 3 optimizations. Use when user says "audit", "optimize workflow", "review setup", or wants to improve their Claude Code configuration, skills, or working patterns.
---

# Audit Workflow

Examine the current Claude Code setup, recent work patterns, and best practices to produce exactly **3 prioritized suggestions** for workflow improvement.

## Phase 0: Check Audit Backlog

Before any exploration, read `~/.claude/reference/up-for-audit.md`. If it exists and has items, **prioritize those items** in the Phase 1 agent prompts. After all findings are implemented, remove the actioned items from the file (keep unactioned items).

## Phase 1: Gather Data (parallel)

Launch up to 3 Explore subagents in a single message (incorporate Phase 0 items into agent prompts):

### Agent 1 - Configuration & Patterns

Read and analyze:
- `~/.claude/CLAUDE.md` and any `@`-referenced files
- All skills in `~/.claude/skills/` (read every SKILL.md)
- Memory files in the current project's `memory/` directory
- Recent plan files in `~/.claude/plans/` (read the 10 most recent)
- `AGENTS.md` files in the repo root and app directories

Look for: redundancy between CLAUDE.md and skills, missing memory entries, plan patterns that repeat, skill pipeline gaps, CLAUDE.md bloat (apply the "would removing this cause mistakes?" test to each line).

### Agent 2 - Codebase Health

Explore the codebase for:
- Convention drift (files not matching stated conventions in CLAUDE.md/AGENTS.md)
- Migration progress (legacy patterns remaining vs modern equivalents)
- Test infrastructure consistency
- TODO/FIXME density and staleness

Focus on quantifiable patterns with specific file counts and paths.

### Agent 3 - Best Practices

Search the web for current Claude Code best practices:
- CLAUDE.md authoring guidance
- Skill and subagent patterns
- Context management and efficiency tips
- Hook and automation patterns

Compare findings against the current setup.

## Phase 2: Synthesize

From the three agents' findings, select exactly **3 suggestions** using this priority order:

1. Simplifications that remove friction for the human
2. Efficiency gains for Claude (context, token usage, fewer repeated explorations)
3. Quality improvements (better code, fewer mistakes, stronger conventions)
4. Codebase health improvements (migration progress, consistency)

**Exclude** anything that is already well-handled or would add complexity without clear payoff.

## Phase 3: Present

For each finding, use this format:

### Finding N: `<title>`

**Problem:** What's wrong or suboptimal (1-2 sentences).

**Evidence:** Specific data - file counts, line numbers, plan references, or best practice citations.

**Recommendation:** Concrete action to take, with file paths.

**Effort / Impact:** Low/Medium/High for each.

---

After presenting all 3 findings, ask: "Want me to implement any of these?"

For detailed audit areas, see [CHECKLIST.md](CHECKLIST.md).
