---
name: research-it
description: >
  Pre-spike research producing a decision artifact that steers future spike sessions. Investigates
  tech stacks, library choices, approaches, and anti-approaches. Output is a durable research
  document that provides fast context to agents and humans entering a spike cold. Use when the user
  says "research it", "research this", "explore options", "what stack", "compare libraries", or
  wants to make meta-level decisions before writing a PRD.
---

# Research It

Investigate options and produce a research artifact before committing to a spike. The output
is a decision document that pre-steers `/spike-it` sessions and gives fast context to any agent
or human picking up the work later.

## Step 1: Understand the Problem Space

`$ARGUMENTS` may contain:

- **Topic** -- "auth library for Next.js", "state management approach", "deployment strategy"
- **Issue reference** (e.g. `#42`) -- fetch context from GitHub via `gh`
- **Constraints** -- "must be OSS", "no vendor lock-in", "runs on edge"

If unclear, use **AskUserQuestion**:

> What are we researching? Give me a topic, constraints, or problem description.

## Step 2: Clarify Scope

Invoke `/grill-it` to nail down:

- **What decision needs to be made?** -- one sentence
- **What are the constraints?** -- budget, timeline, team skill, licensing, infra
- **What's already decided?** -- things that are locked in and not up for debate
- **What's been tried or rejected before?** -- prior art, known dead ends
- **What does success look like?** -- how will you evaluate options?

All questions resolved before proceeding.

## Step 3: Research

Investigate the option space. For each viable approach:

1. **What is it?** -- one-line description
2. **Why consider it?** -- what problem does it solve well
3. **Trade-offs** -- what you gain vs what you lose
4. **Ecosystem fit** -- how it plays with existing stack and constraints
5. **Maturity** -- maintenance health, community size, release cadence
6. **Evidence** -- links, benchmarks, community sentiment, prior experience

Use web search for current ecosystem data. Use codebase exploration to understand existing
patterns and constraints.

### Anti-approaches

Equally important: document approaches that were considered and **rejected**, with clear
reasoning. This prevents future agents or team members from re-investigating dead ends.

## Step 4: Present Findings

Present a summary for discussion:

> **Research: `{topic}`**
>
> **Options:**
> 1. **{Option A}** -- {one-line trade-off summary}
> 2. **{Option B}** -- {one-line trade-off summary}
> 3. **{Option C}** -- {one-line trade-off summary}
>
> **Rejected:**
> - **{Option X}** -- {why it was eliminated}
>
> **Recommendation:** {which and why}
>
> Discuss before I write the artifact?

Iterate until the user is satisfied with the analysis.

## Step 5: Write the Research Artifact

Use `/write-to-file` to write `.ai/research_{terse-description}.md`.

### Artifact structure

```markdown
# Research: {Topic}

> {One-sentence decision to be made}

**Researched:** {date}
**Status:** active | consumed | stale

## Context

What prompted this research. Constraints. What's already locked in.

## Options

### Option 1: {Name}

**Summary:** one-line
**Trade-offs:** what you gain vs lose
**Ecosystem fit:** how it integrates
**Maturity:** maintenance, community, releases
**Evidence:** links, benchmarks, experience

### Option 2: {Name}

...

## Rejected Approaches

### {Approach Name}

**Why rejected:** clear reasoning
**When to revisit:** conditions that would change this decision (or "never")

## Decision

**Chosen approach:** {name}
**Rationale:** why this over the alternatives
**Open risks:** what could go wrong, what to watch for

## Steering Notes

Guidance for the `/spike-it` session and any agent picking this up:

- {directive -- e.g. "use library X for auth, not Y"}
- {directive -- e.g. "avoid approach Z because..."}
- {directive -- e.g. "prototype needed for X before committing"}
```

## Step 6: Offer Next Steps

> **Research artifact:** `.ai/research_{name}.md`
>
> Ready to `/spike-it` with this as input, or adjust anything?

## Guiding Principles

- **Stale research is worse than none** -- a research doc that drifts from reality actively
  misleads. Every time a research artifact is referenced, verify its claims still hold. If a
  decision was overturned, a library was swapped, or an approach failed in practice -- update
  or delete the artifact immediately. Never leave stale research lying around.
- **Decisions, not descriptions** -- the artifact captures what was decided and why, not a
  survey of everything that exists
- **Anti-approaches are first-class** -- rejected options with reasoning prevent wasted cycles
- **Steering notes are the payoff** -- concrete directives that make the spike session faster
- **Durable** -- no assumptions about who reads this next. An agent dropped into the repo
  cold should get full context from this document alone
- **Prune aggressively** -- once a research artifact has been fully consumed by a spike and
  the decisions are implemented, delete it. The spike and code are now the source of truth.
  Research docs are transient by nature -- they exist to inform decisions, not to document them
  permanently
