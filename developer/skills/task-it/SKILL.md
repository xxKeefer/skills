---
name: task-it
description: >
  Turn a /spike-it output into tracker tickets ready for /plan-it or /do-it. Decomposes the spike into
  demo-able blocks of work, gets user approval, resolves the epic, then creates the tickets in the
  issue tracker. Use when the user says "task it", "create tickets", "break into tickets", "make the
  tickets", or wants to turn a spike or feature breakdown into tracked issues.
---

# Task It

Decompose a `/spike-it` output into tickets, get approval, then create them under an epic.

## Step 1: Parse Input

`$ARGUMENTS` may contain:

- **Spike file path** (e.g. `.ai/spike_TICKET-123.md`) — read the file
- **Ticket key** of the spike ticket — fetch from the issue tracker
- **Nothing** — check the current conversation for a `/spike-it` output

If no spike context is found, use **AskUserQuestion**:

> What are we breaking into tickets? Give me a spike file path, ticket key, or description.

Read the spike document. Extract:

- **Scope items** (the "In scope" checklist)
- **Acceptance criteria**
- **Technical considerations**
- **Approach / broad strokes**
- **Open questions** (unresolved ones may block tickets — flag them)

Summarise what you found back to the user.

## Step 2: Decompose into Tickets

Break the spike into tickets. Each ticket should be a **demo-able block of work** — something worth showing at the end of a sprint. `/plan-it` handles the fine-grained decomposition within a ticket; `/task-it` defines the deliverable units.

For each ticket, draft:

```
### Ticket N: {summary}

**Type:** feat | fix | refactor | chore
**Summary:** 1 sentence
**Description:** 2-4 sentences — what changes from the user's perspective
**Acceptance Criteria:**
- [ ] Testable behaviour 1
- [ ] Testable behaviour 2
**Depends on:** Ticket N (if any)
**Labels:** [relevant labels from spike, e.g. migration, tech-debt]
```

### Sizing guidance

- Each ticket should be **completable in 1-3 days** by a developer with agent tooling
- A ticket is too big if it touches more than one feature area that could be demoed independently
- A ticket is too small if it has no visible or testable outcome on its own
- Order tickets by dependency — note which ones block others
- Flag unresolved open questions from the spike if they block a ticket

## Step 3: Present for Approval

Show the full ticket list:

> **{N} tickets from spike `{spike name}`:**
>
> 1. **{summary}** — {type} — {1-line description}
> 2. **{summary}** — {type} — {1-line description}
> ...
>
> Dependency order: 1 → 2 → 3 (4 and 5 independent)

Ask: **"Adjust any tickets, or approve to create?"**

Iterate until the user approves. They may want to merge, split, reorder, or drop tickets.

## Step 4: Resolve the Epic

Use **AskUserQuestion**:

> Which epic should these tickets go under? Give me an epic key (e.g. `ENG-10000`), or say "find one" and I'll suggest the most likely match.

### If the user provides an epic key

Fetch it from the issue tracker to confirm it exists and show the summary.

### If the user says "find one" or doesn't know

Search for candidate epics:

1. If the spike references a parent epic or linked tickets, check those first
2. Search the issue tracker for epics in the same project, sorted by most recently updated
3. Present the top 3-5 most relevant epics based on name/description similarity to the spike

Ask: **"Use one of these, or create a new epic?"**

### If no epic fits

Propose a new epic:

```
Summary: {suggested epic title}
Description: {1-2 sentences from the spike's problem statement}
```

Ask: **"Create this epic, or adjust?"**

If approved, create the epic in the issue tracker.

## Step 5: Create the Tickets

For each approved ticket, create it in the issue tracker:

1. Set fields:
   - **project:** extracted from the epic key or spike ticket
   - **type:** Use your tracker's equivalent of Story (for feat), Task (for refactor/chore), Bug (for fix)
   - **summary:** the ticket summary
   - **description:** the description + acceptance criteria
   - **labels:** from the ticket draft

2. Link each ticket to the epic

3. If tickets have dependencies, create dependency links (e.g. "Blocks" relationships)

After creating all tickets, present:

> **Created {N} tickets under epic `{EPIC-KEY}`:**
>
> 1. [`{KEY}`](TICKET_URL) — {summary}
> 2. [`{KEY}`](TICKET_URL) — {summary}
> ...
>
> Pick one to `/plan-it` or `/do-it`?
