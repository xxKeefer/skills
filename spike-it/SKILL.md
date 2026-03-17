---
name: spike-it
write-to: "{plans_dir}/spike_{TICKET}.md"
description: >
  Deep-dive investigation of a feature, bug, or technical problem. Accepts issue tracker tickets,
  wiki pages, or a plain description — then relentlessly asks clarifying questions until the problem is
  fully understood before producing a terse output document. Use when the user says "spike it",
  "spike this", "investigate this", "flesh this out", "hydrate ticket", "improve ticket", "research
  this", "feasibility study", or wants to fully understand a problem before committing to implementation.
---

# Spike It

Build a complete understanding of a problem, then produce a terse document that captures it.

## Step 1: Parse Inputs

`$ARGUMENTS` may contain any combination of:

- **Ticket keys** (e.g. `ENG-29019`, `PLAT-1234`) — fetch from the issue tracker
- **Wiki/documentation URLs** — fetch the page content
- **Free-text description** — anything that isn't a ticket key or documentation URL

If `$ARGUMENTS` is empty, use **AskUserQuestion**:

> What are we spiking? Give me a ticket key, documentation link, description, or any combination.

Gather everything provided. For each ticket, fetch summary, description, acceptance criteria, linked tickets, and comments. For each documentation page, fetch the content. Summarise all gathered context back to the user in bullet points.

## Step 2: Relentless Clarification

Your job is to **fully understand the problem before producing anything**. Ask clarifying questions using **AskUserQuestion** until you can explain the problem, constraints, and scope back to the user and they agree you've got it.

Rules:

- Ask in batches of 2-4 targeted questions — not a wall of 20
- Adapt each batch based on previous answers — don't ask questions already answered
- Skip areas the source material already covers
- Keep going until there are no ambiguities left
- If the user says "that's enough" or equivalent, respect it and move on

Areas to probe (skip what's already clear):

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
- **Related work** — Backend spikes, other tickets, prior art?
- **Open questions** — Anything the user already knows is unresolved?

## Step 3: Research

Based on the clarified understanding, do the research needed to fill gaps. This may include:

- **Codebase exploration** — find existing patterns, similar implementations, relevant files. Use Explore subagents for broad searches.
- **Dependency comparison** — if new libraries are being evaluated, compare bundle size, maintenance health, framework compatibility, API ergonomics, stack fit. Use WebFetch/WebSearch.
- **Pattern analysis** — if new patterns are proposed, find existing code that would be affected. Assess migration cost.
- **API surface** — if backend APIs are involved, document the expected contract.

Summarise key findings to the user before writing. Ask if anything is missing.

## Step 4: Produce the Document

Write the output to the path specified by `write-to` in this skill's frontmatter. Resolve `{plans_dir}` using the "Plans Directory" convention in the user's global CLAUDE.md. If no convention is configured, use **AskUserQuestion** to ask where to write.

Use the [output template](OUTPUT_TEMPLATE.md) as a starting structure but **adapt it to the investigation**:

- Drop sections that aren't relevant
- Add sections the investigation warrants (e.g. "Migration Path", "Performance", "Security")
- Every section earns its place — if it adds no value, cut it

### Writing guidelines

- Lead with the conclusion/recommendation, then evidence
- Bullet points over paragraphs, tables over prose
- `> blockquote` for one-line section summaries
- Tables for comparisons, checkboxes for scope items
- Horizontal rules (`---`) between major sections
- Link tickets as `[TICKET-XXXXX](TICKET_URL)`
- Code snippets only to illustrate an API surface or pattern — not implementation
- Acceptance criteria: each item = one observable, testable behaviour

## Step 5: Present and Offer Next Steps

Show the file path and a brief summary of what the document covers.

Ask the user which (if any) they want:

1. **Adjust** — revise the document
2. **Publish to project wiki** — ask for the target location, then create the page
3. **Update the source ticket** — push description and acceptance criteria to the ticket
4. **Create tickets** — hand off to `/task-it`
5. **Plan implementation** — hand off to `/plan-it`
6. **Done** — leave the document as-is
