---
name: compress-a-skill
description: Shrink a skill that is over its size limit by rewriting it in terms of art, then prove with a blind trial that it still does the same work.
disable-model-invocation: true
---

# Compress a Skill

A skill over its size limit has two cures. **Disclosure** moves text that only some branches need into
a linked file. **Compression** rewrites the text that every branch needs in fewer words, with terms of
art and **leading words** that the reader already knows (see `../writing-great-skills/SKILL.md`). This
skill does compression, and it proves the result. Every cut word is a check that the agent can stop
making, and no lint shows it. Only a trial does.

The input is the path of a skill folder, and an optional byte limit. The default limit is 10,000 bytes,
from the Sprawl entry of `writing-great-skills`.

## Step 1: Measure and choose the cure

1. Measure `SKILL.md` in bytes, and print the gap to the limit.
2. Read the file by section. For each section, ask: does every branch of the skill need it?
3. If a section serves only some branches, stop and disclose it instead. Disclosure needs no trial.
4. If every section serves every branch, compress.

**Done when:** each section is marked as every-branch or some-branch, and the cure is chosen.

## Step 2: Freeze version A

Commit every pending change to the skill that is not compression, such as an approved rule edit. Then
`HEAD` is version A, and compression is the only difference that the trial measures.

**Done when:** the skill has no uncommitted change.

## Step 3: Write version B

Rewrite `SKILL.md` in the working tree until it is under the limit. Keep these exactly:

- the frontmatter, the section order, and every rule number
- each condition, severity, threshold, and command
- each example that anchors a check
- each lane boundary at full strength: its bold words, and words such as "never" and "at all"

Cut these: explanations that a term of art replaces, restated reasons, hedges, and joining words. A rule
can become a list of short phrases.

**Done when:** `SKILL.md` is under the limit, and each item in the keep list is present.

## Step 4: List the losses

Give a fresh subagent version A (`git show HEAD:<path>`) and version B, and ask it for every check,
condition, example, reason, or emphasis that B drops or weakens. Do not tell it what you cut.

Restore each loss in B, unless the user agrees to drop it. Measure again.

**Done when:** each listed loss is restored or dropped by the user, and B is still under the limit.

## Step 5: Build the fixture

Write a fixture that the skill can act on, with a ground-truth list that only the judge sees:

- planted defects for the rules that B rewrote most
- decoys at each lane boundary: an item for another lane, and an item to leave unreported
- more defects than any cap in the skill, so that ranking and overflow are tested

A decoy finds a loss that a planted defect does not. A weakened boundary still finds every defect, but
it also reports what belongs to another lane.

**Done when:** the fixture runs, and the ground-truth list names each defect and decoy with its
expected result.

## Step 6: Run the trial

Run `/meta:eval-skill` on the skill. A is `HEAD` and B is the working tree. Give it the fixture, and
build its rubric from the ground-truth list. Give the judge the words of each output only, with no
note from you.

**Done when:** `/eval-skill` reported a verdict and a score for each criterion.

## Step 7: Read each criterion

The verdict compares totals, and a total can hide a loss. For each criterion, compare the two B runs
with the two A runs.

- **Both B runs score below both A runs on one criterion:** find the B line behind it. Restore A's
  text for that line, word for word. A restore to A's text needs no new trial.
- **Any other edit to fix a loss:** run Step 6 again.
- **No criterion shows a loss:** keep B.

**Done when:** each criterion is clear, or its line holds A's text.

## Step 8: Apply

1. Measure `SKILL.md`. If the restores took it over the limit, return to Step 3.
2. Run the repo's checks for a skill edit, such as its lint and its scrub hook.
3. Commit, and say in the message what the trial showed and what each restore fixed.

**Done when:** the commit exists, and you printed the old size, the new size, the verdict, and each
restored line.
