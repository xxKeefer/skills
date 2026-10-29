---
name: audit-workflow
description: Audit the Claude Code setup and suggest 3 optimizations.
disable-model-invocation: true
---

# Audit Workflow

Examine the current Claude Code setup, recent work patterns, and best practices to produce exactly **3 prioritized suggestions** for workflow improvement.

## Phase 1: Gather Data (parallel)

Launch up to 3 Explore subagents in a single message:

### Agent 1 - Configuration & Patterns

Read and analyze:
- `~/.claude/CLAUDE.md` and any `@`-referenced files
- All skills in `~/.claude/skills/` (read every SKILL.md)
- All plugin skills. Read `~/.claude/plugins/installed_plugins.json`. Take the `installPath` of each entry with scope `user`, and of each entry whose `projectPath` is the working directory. Read every `skills/*/SKILL.md` under each path.
- `~/.claude/skill-tally.json`, if it exists: the use count of each skill
- Memory files in `~/.claude/projects/<project>/memory/`, where `<project>` is the folder for the working directory
- `AGENTS.md` files in the repo root and app directories

Look for: redundancy between CLAUDE.md and skills, missing memory entries, skills with few or no uses in the tally, skill pipeline gaps, CLAUDE.md bloat (apply the "would removing this cause mistakes?" test to each line).

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

**Evidence:** Specific data - file counts, line numbers, use counts, or best practice citations.

**Recommendation:** Concrete action to take, with file paths.

**Effort / Impact:** Low/Medium/High for each.

---

After presenting all 3 findings, ask: "Want me to implement any of these?"

For detailed audit areas, see [CHECKLIST.md](CHECKLIST.md).
