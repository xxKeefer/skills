---
name: triage-it
description: >
  Label-based state machine for triaging GitHub issues. Supports overview, specific issue triage,
  quick state override, and resumable sessions. References AGENT-BRIEF.md and OUT-OF-SCOPE.md.
  Use when the user says "triage", "triage it", "triage issues", "review issues", or wants to
  process the issue backlog.
---

# Triage It

Process GitHub issues through a label-based state machine. The maintainer (you, the human) drives
all transitions -- this is a HITL skill.

## Labels

### Category labels

- `bug` -- something is broken
- `enhancement` -- new feature or improvement

### State labels (mutually exclusive)

- `needs-triage` -- default for new issues, not yet reviewed
- `needs-info` -- waiting on reporter for clarification
- `ready-for-agent` -- fully specified, an AFK agent can pick it up
- `ready-for-human` -- requires human judgment (HITL)
- `wontfix` -- rejected, with reasoning

## Step 1: Parse Input

`$ARGUMENTS` may contain:

- **Nothing** -- show triage overview
- **Issue reference** (e.g. `#42`) -- triage that specific issue
- **Label override** (e.g. `#42 ready-for-agent`) -- quick state transition
- **`resume`** -- pick up where the last triage session left off

## Step 2: Overview Mode (no specific issue)

Fetch open issues and group by state:

```bash
gh issue list --state open --label "needs-triage" --json number,title,labels,createdAt
gh issue list --state open --label "needs-info" --json number,title,labels,createdAt
```

Present:

> **Triage overview:**
>
> **Needs triage ({N}):**
> - #N -- {title} ({age})
> - #N -- {title} ({age})
>
> **Needs info ({N}):**
> - #N -- {title} ({age})
>
> Pick an issue to triage, or I'll start from the oldest.

## Step 3: Triage a Specific Issue

Fetch the full issue:

```bash
gh issue view {number} --json number,title,body,labels,comments,author,createdAt
```

### 3a: Assess the Issue

Read the issue body and comments. Determine:

- **Category:** bug or enhancement?
- **Clarity:** is the problem well-defined? Reproduction steps? Expected vs actual?
- **Scope:** does this touch one concern or many?
- **Prior art:** check `.ai/.out-of-scope/` for previously rejected similar requests
  (see [OUT-OF-SCOPE.md](../references/OUT-OF-SCOPE.md))

### 3b: Decide the State Transition

Present your assessment and recommendation:

> **Triage: #{N} -- {title}**
>
> **Category:** bug | enhancement
> **Clarity:** Clear | Partial | Vague
> **Prior art:** none | references `.ai/.out-of-scope/{file}`
>
> **Recommendation:** {state} -- {reasoning}

Wait for the user to confirm or override.

### 3c: Apply the Transition

Based on confirmed state:

**needs-info:**
- Add a comment asking specific questions (2-3 max, targeted)
- Apply `needs-info` label, remove `needs-triage`

**ready-for-agent:**
- Apply `ready-for-agent` label, remove `needs-triage`
- Add an agent brief comment (see [AGENT-BRIEF.md](../references/AGENT-BRIEF.md))
- Use `/grill-it` if you need to flesh out acceptance criteria with the user

**ready-for-human:**
- Apply `ready-for-human` label, remove `needs-triage`
- Add a triage note explaining what human judgment is needed

**wontfix:**
- Apply `wontfix` label, remove `needs-triage`
- Add a comment with reasoning
- If enhancement: create or update the relevant `.ai/.out-of-scope/` file via `/write-to-file`
- Close the issue

## Step 4: Bug Reproduction (bugs only)

For bugs marked `ready-for-agent` or `ready-for-human`, attempt to verify the reproduction:

1. Read the reproduction steps from the issue
2. Trace the code path to confirm the described behaviour exists
3. Note findings in the agent brief or triage note

If the bug cannot be reproduced from the description, transition to `needs-info` instead.

## Step 5: Session Continuity

After each issue is triaged, offer to continue:

> **Triaged #{N} -> {state}.**
> **Remaining:** {N} needs-triage, {N} needs-info
>
> Next issue, or done for now?

If the user stops mid-session, the label state on each issue captures progress -- the session is
inherently resumable. Running `/triage-it resume` just fetches the current overview.

## Guiding Principles

- **Maintainer drives transitions** -- never auto-transition without confirmation
- **Durability in agent briefs** -- no file paths, domain language, behavioural criteria
- **Out-of-scope is institutional memory** -- check it before triaging enhancements
- **Prefer ready-for-agent** -- if an issue can be fully specified for AFK execution, do that
- **Two questions max for needs-info** -- targeted questions, not open-ended "tell me more"
