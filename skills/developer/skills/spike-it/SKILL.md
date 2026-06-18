---
name: spike-it
description: >
  Deep-dive investigation of a feature, bug, or technical problem. Accepts tracker tickets,
  wiki pages, or a plain description — delegates to /grill-it for clarification until the problem is
  fully understood, then creates a ticket in the project's tracker capturing the spike. Use when the user says "spike it",
  "spike this", "investigate this", "flesh this out", "hydrate ticket", "improve ticket", "research
  this", "feasibility study", or wants to fully understand a problem before committing to implementation.
---

# Spike It

This is the PRD skill. It produces the specification that feeds `/task-it`.

Build a complete understanding of a problem, then create a ticket in the project's tracker that captures it.

> **Tracker:** "the project's tracker" means whatever issue system the repo's CLAUDE.md declares — a
> GitHub issue via `gh`, a Jira ticket via the Atlassian MCP, etc. Read it to learn which tracker is
> in use and how to create and reference tickets. Default to GitHub issues via `gh` if nothing is
> declared.

## Step 1: Parse Inputs

`$ARGUMENTS` may contain any combination of:

- **Tracker tickets** — references in the project's tracker; fetch via `/look-up`
- **Wiki/documentation URLs** — fetch the page content
- **Free-text description** — anything that isn't a tracker ticket or documentation URL

If `$ARGUMENTS` is empty, use **AskUserQuestion**:

> What are we spiking? Give me a ticket reference, documentation link, description, or any combination.

Gather everything provided. For each ticket, fetch its content via `/look-up`. For each documentation page, fetch the content. Summarise all gathered context back to the user in bullet points.

## Step 2: Relentless Clarification

Invoke `/grill-it` to fully understand the problem before producing anything. Pass it the gathered context from Step 1 and these spike-specific areas to probe (skip what's already clear):

- **Problem clarity** — Can you state the problem in one sentence? If not, ask.
- **User impact** — What changes from the end user's perspective?
- **Scope boundaries** — What is explicitly in and out of scope?
- **Error states** — What can go wrong and how should it behave?
- **Permissions / roles** — Does behaviour vary by user type?
- **Existing behaviour** — What must be preserved?
- **Proposed approach** — Does the team have a direction, or is this open-ended?
- **New dependencies** — Libraries, APIs, patterns being considered?
- **Constraints** — Feature flags, backwards compatibility, performance, timeline?
- **Designs** — Mockups, wireframes, design links?
- **Related work** — Other tickets, prior art?

**All questions must be resolved before proceeding.** If `/grill-it` surfaces questions that cannot
be answered in-session, flag them as blockers and ask the user how to resolve them — do not carry
unresolved questions into the output.

## Step 3: Research

Based on the clarified understanding, do the research needed to fill gaps. This may include:

- **Codebase exploration** — find existing patterns, similar implementations, relevant files. Use Explore subagents for broad searches.
- **Dependency comparison** — if new libraries are being evaluated, compare bundle size, maintenance health, framework compatibility, API ergonomics, stack fit. Use WebFetch/WebSearch.
- **Pattern analysis** — if new patterns are proposed, find existing code that would be affected. Assess migration cost.
- **API surface** — if backend APIs are involved, document the expected contract.

Summarise key findings to the user before writing. Ask if anything is missing.

## Step 4: Create the Tracker Ticket

Compose the ticket body using the [issue template](ISSUE_TEMPLATE.md) as a starting structure but **adapt it to the investigation**:

- Drop sections that aren't relevant
- Add sections the investigation warrants (e.g. "Migration Path", "Performance", "Security")
- Every section earns its place — if it adds no value, cut it

### Writing guidelines

- Lead with the conclusion/recommendation, then evidence
- Bullet points over paragraphs, tables over prose
- `> blockquote` for one-line section summaries
- Tables for comparisons, checkboxes for scope items
- Horizontal rules (`---`) between major sections
- Reference tickets using the tracker's identifier convention (`#N` for GitHub, `ENG-123` for Jira, …)
- Code snippets only to illustrate an API surface or pattern — not implementation
- Acceptance criteria: each item = one observable, testable behaviour

Create the ticket in the project's tracker (per the repo's CLAUDE.md — `gh issue create` for GitHub,
the Atlassian MCP for Jira, etc.) using a `spike:` title prefix.

## Step 5: Present and Offer Next Steps

Show the ticket URL/key and a brief summary of what the spike covers.

Ask the user which (if any) they want:

1. **Adjust** — revise the ticket
2. **Create tickets** — hand off to `/task-it`
3. **Plan implementation** — hand off to `/plan-it`
4. **Done** — leave the ticket as-is
