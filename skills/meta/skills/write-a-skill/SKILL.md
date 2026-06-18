---
name: write-a-skill
description: >
  Create a new skill from scratch. Gathers requirements, drafts the skill, reviews with the user.
  Use when the user says "write a skill", "create a skill", "new skill", or wants to author a
  skill from a description rather than extracting from a conversation (use /learn-it for that).
---

# Write a Skill

Author a new skill from scratch. Gather requirements, draft it, review with the user.

## Step 1: Gather Requirements

`$ARGUMENTS` may contain:

- **Skill name** -- what to call it
- **Description** -- what it should do
- **Domain** -- which domain it belongs to (developer, meta, journal, etc.)

If anything is missing, use **AskUserQuestion** to fill gaps. Then invoke `/grill-it` to flesh
out the skill design:

- **Purpose** -- what problem does this skill solve?
- **Trigger phrases** -- when would someone invoke it?
- **Inputs** -- what does it accept? (`$ARGUMENTS`, conversation context, files)
- **Steps** -- what's the workflow? What order? What decision points?
- **Outputs** -- what does it produce? (files, issues, commits, conversation output)
- **Principles** -- any guiding rules or constraints?
- **Composition** -- does it delegate to other skills? (`/grill-it`, `/write-to-file`, etc.)
- **Supporting files** -- does it need templates, references, or scripts?

## Step 2: Check for Conflicts

Before writing:

1. **Check existing skills** in the target domain -- does this duplicate anything?
2. **Check primitives** -- should any part of this be a primitive instead?
3. **Naming** -- follow conventions:
   - `*-it` suffix for HITL skills (user drives the session)
   - Terse kebab-case for agent-only, setup, or non-HITL skills

Present findings. If there's overlap with an existing skill, discuss whether to extend the
existing skill or create a new one.

## Step 3: Draft the Skill

Write `SKILL.md` following this structure:

```yaml
---
name: {skill-name}
description: >
  {What the skill does. When to use it. Trigger phrases. 2-3 lines max.}
---
```

### Skill body rules

- **Step-based** -- numbered steps with clear entry/exit criteria
- **Everything-agnostic** -- no hardcoded tools, libraries, or languages unless inherently
  stack-specific
- **Decision points explicit** -- state the condition and each path
- **User checkpoints** -- mark where the skill pauses for confirmation
- **Terse** -- every line earns its place
- **Link, don't inline** -- reference supporting files rather than embedding large blocks
- **Under 500 lines** -- move detailed references to separate files

### Quality checklist

Before presenting:

- [ ] Each step has a clear "done when" signal
- [ ] Inputs are documented (what `$ARGUMENTS` accepts)
- [ ] Doesn't duplicate an existing skill's responsibility
- [ ] No unnecessary framework or tool coupling
- [ ] Supporting files only created when they add value
- [ ] Follows naming convention (`*-it` for HITL, plain for non-HITL)

## Step 4: Write Supporting Files (if needed)

Only create supporting files when they serve a clear purpose:

- **Templates** -- if the skill produces structured output with a consistent format
- **References** -- if the skill applies detailed principles that would bloat SKILL.md
- **Scripts** -- if the skill runs external tooling

## Step 5: Review

Present the complete skill to the user:

> **Skill: `{name}`**
> **Domain:** {domain}
> **Files:** {list of files created}
>
> {brief summary of what it does}

Ask:

1. **Test it** -- invoke the skill to verify
2. **Adjust** -- revise
3. **Done** -- accept

### Split criteria

If during review the skill feels too large, consider splitting when:

- Two distinct user intents are served (should be two skills)
- A reusable step appears that other skills would benefit from (extract to primitive)
- The SKILL.md exceeds 500 lines despite linking references
