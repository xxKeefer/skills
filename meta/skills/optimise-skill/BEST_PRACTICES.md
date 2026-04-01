# Skill Best Practices

Checklist for Phase 3 recommendation alignment.

## Structure

- [ ] SKILL.md under 100 lines (details in reference files)
- [ ] Frontmatter has `name`, `description` with trigger phrases
- [ ] Steps are numbered with clear entry/exit conditions
- [ ] User checkpoints before destructive or irreversible actions
- [ ] Supporting files use SCREAMING_SNAKE.md naming

## Agnosticism

- [ ] No tool names where a general term works
- [ ] No language assumptions where the workflow is universal
- [ ] No framework coupling where the concept is portable
- [ ] No platform assumptions (OS, shell, editor)
- [ ] Domain language used only when the skill IS domain-specific

## Composability

- [ ] Single responsibility -- the skill does one thing well
- [ ] Primitives referenced by name, not inlined
- [ ] Sub-workflows that appear in 2+ skills are candidates for extraction
- [ ] Inputs and outputs are documented (what goes in, what comes out)

## Durability

- [ ] No version numbers or temporal references that will rot
- [ ] No references to "current" state -- the skill IS current
- [ ] Principles stated as principles, not as snapshots
- [ ] Links to supporting files use relative paths

## Clarity

- [ ] Every line earns its place -- no filler
- [ ] Decision points are explicit with conditions and branches
- [ ] Terse over verbose -- the reader is an AI agent, not a tutorial student
- [ ] Examples used sparingly and only when the concept is genuinely ambiguous
