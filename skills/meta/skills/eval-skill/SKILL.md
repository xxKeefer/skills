---
name: eval-skill
description: >
  Run a blind A/B trial of two versions of one skill, and report a winner or "no difference". Use
  when the user says "eval skill" or asks if a skill change helps, or when /retro offers it.
---

# Eval Skill

Adapted from the eval playbook of pstack. `$SKILL_DIR` is the folder of this skill. The `$ARGUMENTS`
value is the skill to trial, and can name two versions.

## Rules for blinding

- A candidate sees no word from `$SKILL_DIR/scripts/leak_check.py`, in any folder, file, or prompt.
- The prompt reads like a request from a user. It states the goal, never the purpose of the run.
- The prompt never asks which skills, rules, or files the candidate used.
- No candidate learns that another candidate exists.
- The judge sees the outputs under neutral labels only, never the version that made them.

## Step 1: Frame

Name the skill and its two versions. Version A defaults to the last commit that changed the skill
before the edit. Version B defaults to the working tree. Write what success looks like, and a
rubric of 3 to 6 concrete criteria. Only the judge sees the rubric.

**Done when:** the versions, the success line, and the rubric are written.

## Step 2: Set up

Make four folders with project-shaped names under the temp folder: two for each version. In each,
copy the version's `SKILL.md` and its sibling files to `.claude/skills/<name>/`. Add any project
files that an organic task needs.

**Done when:** each folder holds its version of the skill.

## Step 3: Write the prompt

Write one organic prompt to a file. Run `python3 $SKILL_DIR/scripts/leak_check.py <folder>
<prompt file>` on each folder. Fix each word it lists, then run it again.

**Done when:** the check prints nothing for all four folders.

## Step 4: Run the candidates

Run four subagents in parallel, all on one model and with the same brief: the folder path, the
prompt, and "the skills of this project are in `.claude/skills/`". Use the subagent model that the
caller names, else the session model.

**Done when:** each subagent returned its output.

## Step 5: Run the judge

Run one fresh subagent on a different model. Give it the rubric and the four outputs under the
labels `P`, `Q`, `R`, and `S`, in a shuffled order. It scores each criterion for each output in
one pass, on one scale.

**Done when:** the judge returned a score for each criterion and output.

## Step 6: Read the outputs

Read every output yourself, end to end. Where you disagree with the judge, the cause is bias or an
unclear criterion. Say where.

**Done when:** each output has a note.

## Step 7: Report

Reply with the versions, the rubric, the total for each output by version, the verdict, and your
read. The verdict is a winner when both runs of one version beat both runs of the other on the
judge's total. Else it is "no difference". Delete the four folders.

**Done when:** the user has the report and the folders are gone.
