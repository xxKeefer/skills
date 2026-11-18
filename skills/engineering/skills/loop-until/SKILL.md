---
name: loop-until
description: >
  Improve one measured number to a stated predicate, one change and one measure per try, keeping or
  reverting each. Use when the user says "loop until" or wants a metric moved to a target, or when a
  playbook needs a metric loop.
argument-hint: "<metric and target> [@plan]"
---

# Loop Until

Adapted from the hillclimb and autonomous-run playbooks of pstack. Move one number to a target.
Each try is one change, one measure, then keep or revert. The loop runs with no stop between
tries.

`/webperf` fixes one page bottleneck, and the user says yes to each fix. `/loop-until` runs many
tries to a predicate with no stop between tries.

Principles: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)), **principle-build-the-lever** ([`../principle-build-the-lever/SKILL.md`](../principle-build-the-lever/SKILL.md)), **principle-sequence-verifiable-units** ([`../principle-sequence-verifiable-units/SKILL.md`](../principle-sequence-verifiable-units/SKILL.md)), and **principle-explain-the-number** ([`../principle-explain-the-number/SKILL.md`](../principle-explain-the-number/SKILL.md)). Read a principle file before you apply it, and name it in the reply when it shaped a choice.

## Step 1: Frame

Write these down before any change:

1. The repro case: one input that shows the problem. With no repro, make the repro first.
2. One metric, and the direction that is better.
3. The predicate: a target, and a floor on tries. A lucky early win cannot end the run before the
   floor.
4. The regression gate: the command that must stay green.

With no plan, write one with `/write-to-file`, doctype `plan`, and put the frame in its Context. Its
loop step names `Seam:` (the code under the metric) and `Conditions:` (an ID for the gate).

**Done when:** the plan holds the repro case, the metric, the direction, the predicate, and the
gate command, and its loop step names `Seam:` and `Conditions:`.

## Step 2: Prove and freeze the harness

1. Write one command that prints the metric. It runs the case N times and prints the median. Pick N
   so that the noise is small against the target.
2. Run it on the repro case and on a contrast case that must give a different number. If the two
   numbers do not separate, change the case or the metric, and run it again.
3. Record the baseline, the noise, and one green run of the gate.
4. Freeze the harness. Change it no more.

**Done when:** the plan holds the baseline, the noise, the harness command, a green gate, and the
two numbers that show the harness separates the cases.

## Step 3: Loop

Before each try, read the decision log. Then:

1. Name one hypothesis and its mechanism, in the code, with the file. "Try some caching" is not a
   mechanism.
2. Give the change to one fresh subagent at the `worker` role of the `models` block in
   `~/.claude/AGENTS.md`, or at the session model when there is no `models` block, with a tight
   scope. It makes one change.
3. Measure with the frozen harness, and run the gate.
4. Keep the change only when the metric moves in the better direction by more than the noise and the
   gate is green. Commit it as one commit that stages only the changed files. Else revert in full.
   After a kept try, measure the noise again at the new level. Judge the next try against it.
5. Give the try to `/update-plan` as a choice, whether kept or reverted: `decision` is the try
   number and the change, `reason` is the mechanism, `evidence` is the metric before and after and
   the gate result, and `result` is `kept <sha>` or `reverted`.

A change that breaks behaviour is reverted, even when the number improves. A simplification that
holds the number is kept.

**Done when:** each try has one log row, the tree holds only kept commits, and the noise is
measured again after each kept try.

## Step 4: Plateau

After three rejected tries in a row, change the kind of change. Combine near-misses, or read the
code path again from the start. A plateau is not a stop.

**Done when:** the next try differs in kind from the three rejected tries.

## Step 5: Stop

Stop when the predicate holds: the target is met and the floor on tries is passed. Never relax the
predicate.

If no cheap untried hypothesis remains, or the loop is stuck, write a `D` entry in the format of
[`../build/STEP.md`](../build/STEP.md) that names the dead end and the evidence, and stop.

**Done when:** the predicate holds, or a `D` entry names the dead end.

## Step 6: Report

Reply with:

- The metric and the predicate.
- The baseline and the final value, with the percent change.
- The count of tries kept and reverted.
- Each kept commit, on one line.
- The path of the decision log.
- The best next idea.

**Done when:** the reply holds each item above.
