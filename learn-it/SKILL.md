---
name: learn-it
description: >
  Analyze the current conversation to extract repeatable patterns and codify them into a new skill.
  Use when the user says "learn this", "make a skill from this", "extract a skill", "turn this into
  a skill", or wants to capture a workflow they just performed so it can be reused.
---

# Learn It

Analyze the current conversation, identify repeatable patterns, and produce a new skill.

## Step 1: Scan the Conversation

Review the full conversation history. Look for:

- **Repeated sequences** — steps the user or agent performed in a consistent order
- **Decision points** — where the user was asked to choose and their choice shaped the workflow
- **Inputs and outputs** — what went in (ticket, file path, description) and what came out (document, code, commits)
- **Tool patterns** — which tools were used, in what order, with what kind of arguments
- **Clarification loops** — where ambiguity was resolved through questions
- **Checkpoints** — where the user reviewed and approved before continuing

## Step 2: Identify the Core Pattern

Distill what you found into:

- **One-sentence purpose** — what does this workflow accomplish?
- **Trigger phrases** — when would a user invoke this? (e.g. "do X", "run Y", "create Z")
- **Inputs** — what does the skill need to start? (arguments, context, files)
- **Steps** — the ordered sequence of actions, including decision branches
- **Outputs** — what does the skill produce? (files, commits, issues, documents)
- **Principles** — any recurring rules or constraints observed (e.g. "always ask before committing", "mock at boundaries only")

Present this summary to the user:

> **Pattern detected: `{name}`**
>
> **Purpose:** {one sentence}
> **Triggers:** {trigger phrases}
> **Inputs:** {what it needs}
> **Steps:** {N} steps
> **Outputs:** {what it produces}
>
> Does this capture it? Adjust anything before I write the skill.

Wait for confirmation. Iterate if needed.

## Step 3: Assess Skill Structure

Determine what files the skill needs:

- **SKILL.md** — always required. The main workflow instructions.
- **Supporting files** — only if needed:
  - Output templates (if the skill produces a structured document)
  - Reference material (if the skill applies specific principles repeatedly)
  - Scripts (if the skill runs external tools)

Keep SKILL.md under 500 lines. Move detailed reference material to separate files and link them.

## Step 4: Write the Skill

Write the skill files into the target directory. Resolve the target path:

1. If `$ARGUMENTS` contains a skill name, use it as the directory name
2. Otherwise, derive a name from the pattern (lowercase, hyphenated)
3. Use **AskUserQuestion** to confirm: "Write skill to `{path}`?"

### SKILL.md structure

```yaml
---
name: {skill-name}
description: >
  {What the skill does. When to use it. Trigger phrases.}
---
```

Follow these rules when writing the skill body:

- **Framework-agnostic** — no hardcoded tools, libraries, or languages unless the skill is inherently stack-specific
- **Step-based** — numbered steps with clear entry/exit criteria
- **Decision points explicit** — where the workflow branches, state the condition and each path
- **User checkpoints** — mark where the skill should pause for user confirmation
- **Terse** — every line earns its place. No filler.
- **Link, don't inline** — reference supporting files rather than embedding large blocks

### Quality checks

Before presenting the skill:

- [ ] Each step has a clear "done" signal
- [ ] Inputs are documented (what `$ARGUMENTS` accepts)
- [ ] The skill doesn't duplicate an existing skill's responsibility
- [ ] No framework or tool coupling unless inherently required
- [ ] Supporting files are only created when they add value

## Step 5: Present and Offer Next Steps

Show the file path(s) and a brief summary.

Ask:

1. **Test it** — try invoking the skill now to verify it works
2. **Adjust** — revise the skill
3. **Done** — leave as-is
