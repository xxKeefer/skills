---
name: optimise-skill
description: >
  Analyse and optimise a skill for durability, agnosticism, and size. Takes a skill name as
  argument. Hardens fragile language, extracts specifics into reference files, and recommends
  primitive extractions. Use when user says "optimise skill", "optimise-skill", "harden skill",
  "slim down skill", or wants to improve an existing skill's quality.
---

# Optimise Skill

Take a skill and make it more durable, more agnostic, and smaller. Three phases, applied in order.

## Step 0: Locate the Skill

`$ARGUMENTS` must contain a skill name (e.g. `close-it`, `hunt-it`).

1. Search all domain `skills/` directories for a matching directory name
2. Read the `SKILL.md` and all supporting files in that directory
3. If not found, **AskUserQuestion**: "Which skill? Give me the name or path."

Present a brief summary of the skill before proceeding:

> **Skill:** `{name}` ({line count} lines, {N} supporting files)
> **Purpose:** {one-sentence summary from frontmatter}
>
> Starting optimisation. Phase 1: Harden.

## Phase 1: Harden

Goal: replace fragile, specific, non-durable, or non-agnostic language with fundamental
alternatives.

Scan every line of SKILL.md and supporting files. Flag anything that is:

- **Tool-specific** -- names a specific tool when the principle is tool-agnostic
  (e.g. "run Jest" when "run the test suite" works)
- **Language-specific** -- assumes a language when the workflow applies broadly
  (e.g. "TypeScript interface" when "type contract" works)
- **Framework-coupled** -- depends on a framework when the idea is universal
  (e.g. "React component" when "UI unit" works)
- **Temporally fragile** -- references versions, dates, or current state that will rot
- **Platform-specific** -- assumes OS, shell, or environment when not necessary
- **Over-prescribed** -- dictates implementation details when intent would suffice

For each issue found, apply the criteria in [HARDEN_CRITERIA.md](HARDEN_CRITERIA.md).

Present findings as a table:

| Line | Current | Proposed | Reason |
|------|---------|----------|--------|
| ... | ... | ... | ... |

Ask: "Apply these hardening changes? (yes / adjust / skip)"

Apply approved changes. Move to Phase 2.

## Phase 2: Disclose

Goal: reduce the size and complexity of SKILL.md by extracting specifics into reference files.
The root SKILL.md should contain only the core problem-solving workflow.

### Pass 1: SKILL.md

Scan for content that is:

- **Detailed criteria or checklists** -- belongs in a reference file
- **Templates or formats** -- belongs in a template file
- **Examples or samples** -- belongs in a reference file
- **Domain-specific knowledge** -- belongs in a reference file
- **Long inline lists** (5+ items of specifics) -- condense or extract

For each extraction:

1. Identify the content block
2. Name the target file (SCREAMING_SNAKE.md convention)
3. Replace inline content with a link: `See [FILE.md](FILE.md).`

Present the extraction plan:

> **Extractions from SKILL.md:**
>
> 1. Lines {N-M} -> `{FILENAME}.md` ({reason})
> 2. ...
>
> Estimated SKILL.md reduction: {X} lines -> {Y} lines

Ask: "Apply these extractions? (yes / adjust / skip)"

### Pass 2: Reference Files

Apply the same scan to each newly created or existing reference file. If a reference file itself
has extractable specifics, split further. Stop when each file has a single clear responsibility.

## Phase 3: Recommend

Goal: identify opportunities beyond the current skill.

Assess and present recommendations in three categories:

### Primitive Extraction

Could any part of this skill be a standalone primitive in `primitives/`?

Criteria:
- Used (or usable) by 2+ skills across different domains
- Encodes a single, complete sub-workflow
- Has no domain-specific assumptions

### Cross-Domain Applicability

Could this skill (or a generalised version) serve other domains?

Look for:
- Workflows that are domain-specific only by naming, not by logic
- Patterns that map to other contexts (e.g. code review -> document review)

### Best Practice Alignment

Compare the skill against the principles in [BEST_PRACTICES.md](BEST_PRACTICES.md).
Flag any gaps.

Present all recommendations:

> **Recommendations for `{skill-name}`:**
>
> **Primitives:** {list or "none identified"}
> **Cross-domain:** {list or "already maximally general"}
> **Best practices:** {list or "fully aligned"}

Ask: "Want me to action any of these?"
