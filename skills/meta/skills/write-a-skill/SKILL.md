---
name: write-a-skill
description: >
  Create a new skill from scratch. Gathers requirements, drafts the skill, reviews with the user.
  Use when the user says "write a skill", "create a skill", "new skill", or wants to author a
  skill from a description.
---

# Write a Skill

Author a new skill from scratch. Gather requirements, draft it, review with the user.

## Step 1: Gather Requirements

`$ARGUMENTS` may contain:

- **Skill name** -- what to call it
- **Description** -- what it should do
- **Domain** -- default to `experimental`. New skills land there and earn promotion to a stable
  domain.

If anything is missing, use **AskUserQuestion** to fill gaps. Then invoke `/grill` to flesh
out the skill design:

- **Purpose** -- what problem does this skill solve?
- **Invocation** -- must the agent or another skill invoke it?
- **Trigger phrases** -- ask only when the answer to Invocation is yes. One phrase per distinct
  situation that should fire it.
- **Inputs** -- what does it accept? (`$ARGUMENTS`, conversation context, files)
- **Steps** -- what's the workflow? What order? What decision points?
- **Outputs** -- what does it produce? (files, issues, commits, conversation output)
- **Principles** -- any guiding rules or constraints?
- **Composition** -- does it delegate to other skills? (`/grill`, `/write-to-file`, etc.)
- **Supporting files** -- does it need templates, references, or scripts?

## Step 2: Check for Conflicts

Before writing:

1. **Check the name** -- search the skill folders of every domain in this repo, and the skills
   this session lists, for the new name. The name must be unique. In a domain bound to one tool,
   prefix the name with the tool name, such as `nix-add`.
2. **Check existing skills** in the target domain -- does this duplicate anything?
3. **Check primitives** -- should any part of this be a primitive instead?
4. **Invocation** -- make it model-invoked only when the agent must reach it on its own, or
   another skill must. Otherwise make it user-invoked. State the choice and why.

Present findings. If there's overlap with an existing skill, discuss whether to extend the
existing skill or create a new one.

## Step 3: Draft the Skill

Write `SKILL.md` with the frontmatter that matches the Step 2 invocation choice.

Model-invoked:

```yaml
---
name: {skill-name}
description: >
  {What the skill does, in one line.} Use when {one trigger per branch}.
---
```

User-invoked:

```yaml
---
name: {skill-name}
description: {One line for the human: what the skill does.}
disable-model-invocation: true
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

Before presenting, read `../writing-great-skills/SKILL.md` and its `GLOSSARY.md` as files. That
rubric is user-invoked, so no skill can invoke it. Check the draft against the rubric, then
against this list:

- [ ] Each step has a clear "done when" signal
- [ ] Inputs are documented (what `$ARGUMENTS` accepts)
- [ ] Doesn't duplicate an existing skill's responsibility
- [ ] No unnecessary framework or tool coupling
- [ ] Supporting files only created when they add value
- [ ] Invocation matches the rubric

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
