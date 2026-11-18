# Design It Twice

When the user wants to explore alternative interfaces for a chosen deepening candidate, use this parallel sub-agent pattern. Based on "Design It Twice" (Ousterhout) — your first idea is unlikely to be the best.

The rubric, the scrap check, and the base with grafts are adapted from pstack `arena` and `architect`.

Uses the vocabulary in [SKILL.md](SKILL.md) — **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

### 1. Frame the problem space

Before spawning sub-agents, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough illustrative code sketch to ground the constraints — not a proposal, just a way to make the constraints concrete

Then sketch the caller. Write the caller's code as it would read with an ideal interface, before any design. This is the **caller sketch**. A design must serve it.

Then write the **rubric**: three to five criteria, each with a weight. Take the criteria from the vocabulary in [SKILL.md](SKILL.md) (depth, locality, seam placement, testability through the interface) and from the constraints of this problem. Write the rubric now, so that no returned design can shape it.

Show the problem space, the caller sketch, and the rubric to the user, then immediately proceed to Step 2. The user reads and thinks while the sub-agents work in parallel.

### 2. Spawn sub-agents

Spawn 3+ sub-agents in parallel using the Agent tool. Each must produce a **radically different** interface for the deepened module.

Prompt each sub-agent with a separate technical brief (file paths, coupling details, dependency category from [DEEPENING.md](DEEPENING.md), what sits behind the seam). The brief is independent of the user-facing problem-space explanation in Step 1. Give each agent a different design constraint:

- Agent 1: "Minimize the interface — aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility — support many use cases and extension."
- Agent 3: "Optimise for the most common caller — make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Add the caller sketch and the rubric to each brief.

Include both [SKILL.md](SKILL.md) vocabulary and CONTEXT.md vocabulary in the brief so each sub-agent names things consistently with the architecture language and the project's domain language.

Each sub-agent outputs:

1. Interface (types, methods, params — plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [DEEPENING.md](DEEPENING.md))
5. Trade-offs — where leverage is high, where it's thin

### 3. Scrap, score, and graft

Scrap each design that shows a known tell. Name the tell for each scrapped design. Known tells:

- It needs a cast to compile.
- The caller must know the order of calls.
- The interface is as wide as its implementation.
- It does not serve the caller sketch.

Score each design that survives against the rubric. Show a table with one row per design, one column per criterion, and the weighted total.

Pick the design with the top score as the **base**. Do not pick by taste.

Then graft. Name each strong part of another design that the base lacks. Give the reason for each graft, and say what the graft changes in the base interface. If no part is worth a graft, say so.

Present the rubric, the scores, the scrapped designs with their tells, the base, and each graft, so the user can absorb each one. Be opinionated — the user wants a strong read, not a menu.
