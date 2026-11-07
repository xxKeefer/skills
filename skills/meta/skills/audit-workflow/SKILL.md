---
name: audit-workflow
description: Audit the Claude Code setup and the token spend of recent sessions, then suggest 3 optimizations ranked by saving.
disable-model-invocation: true
---

# Audit Workflow

Examine the current Claude Code setup, the token spend of recent sessions, recent work patterns, and best practices. Produce exactly **3 suggestions**, ranked by estimated saving against effort, and save them as a report.

`$SKILL_DIR` is this skill's base directory, shown when the skill loads. The window is the last 7 days, unless the user gives another number of days.

## Phase 1: Gather Data (parallel)

In one message, run the token audit and launch up to 3 Explore subagents.

### Token audit

Run `python3 "$SKILL_DIR/scripts/token_audit.py" --days <days>`. It reads the session transcripts under `~/.claude/projects` and prints a markdown report:

| Section | What it shows |
|---|---|
| Totals | The spend, the cost per request, and the cache-read share |
| Baseline | The input of the first request of each session, and the cost of 1,000 baseline tokens over the window |
| By session, By skill | Where the money goes |
| By tool, Context debt | The tool results that later turns keep reading again: result tokens × turns after × the cache-read price |
| Friction | Hook denials, other denials, declines, and failed tool calls |

The prices are a dated table in the script. When the date is more than 3 months old, check the table against the pricing page that the report names before you quote a dollar figure.

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

From the token audit and the findings of the three agents, select exactly **3 suggestions**. Give each one an estimated saving per week and an effort (S, M, or L). Rank them by saving against effort. When two are close, prefer them in this order:

1. Shrink the baseline. Every request of every session pays for it.
2. Remove turns. Each turn reads the whole context again, so a friction row or a repeated command sequence costs a full turn.
3. Trim bytes. A smaller tool result cuts its context debt.

Size each saving from the token audit, and show the arithmetic:

- Baseline: the tokens cut ÷ 1,000 × the cost of 1,000 baseline tokens.
- Turns: the turns removed × the cost per request.
- Bytes: the share of the context debt that the change removes.

Scale a window figure to a week: × 7 ÷ the days in the window. Label each figure as an estimate. A finding that the token audit cannot size, such as a codebase-health finding, ranks after the sized ones. A suggestion to use a cheaper model follows the [Subagent models](../writing-great-skills/SKILL.md#subagent-models) rule.

**Exclude** anything that is already well handled, anything the data does not support, and anything that adds complexity with no clear saving.

## Phase 3: Present

For each suggestion, use this format:

### Suggestion N: `<title>`

**Problem:** What is wrong or suboptimal (1-2 sentences).

**Evidence:** Figures from the token audit, file counts, line numbers, use counts, or best-practice citations.

**Recommendation:** The concrete action to take, with file paths.

**Saving / Effort:** The estimated saving per week with its arithmetic, and S, M, or L.

---

After the 3 suggestions, add an **Already good** section: what the data shows is lean, so the user knows what not to change.

Transcripts hold secrets and customer data. Quote only the command shapes and the figures that the token audit prints. Never copy a command argument or a transcript line.

## Phase 4: Save the report

Write the report through `/write-to-file`, with doctype `report` and the name `audit-workflow-<YYYY-MM-DD>.md`. Put the 3 suggestions and Already good first, then the token audit output. Then ask: "Want me to implement any of these?"

For detailed audit areas, see [CHECKLIST.md](CHECKLIST.md).
