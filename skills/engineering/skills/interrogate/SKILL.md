---
name: interrogate
description: >
  Send adversaries to break a change, re-run each finding's command, and report only the
  reproduced findings. Applies no fix. Use when the user says "interrogate", "adversarial review", or
  "try to break this", or when /work-on runs it after the build loop.
argument-hint: "[@<plan path> | <scope>]"
---

# Interrogate

Adversaries try to break a change. A finding stays in the report only when a re-run of its command
reproduces it. Each unreproduced finding goes to the Dropped list with its reason. Report the findings. Apply
no fix: the report's ticks build a `/engineering:fix` prompt.

Principles: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)) and **principle-separate-before-serializing-shared-state** ([`../principle-separate-before-serializing-shared-state/SKILL.md`](../principle-separate-before-serializing-shared-state/SKILL.md)).

`$SKILL_DIR` is this skill's base directory.

```
frame → fan out adversaries → collect findings → rerun_findings.py → intent check → report → remove worktrees
```

## Step 1: Frame

1. Find the scope. It is what the user names. Else it is the diff of the current branch from its
   merge base with the base branch, plus the working tree. With a plan path, the base is the plan's
   base branch when it names one.
2. Write the intent in your own words, in one to three sentences. Take it from the user's message,
   the plan's goal and ACs, the commits, and the PR description. When the intent is not clear, ask
   the user.
3. Record the head SHA and the list of changed files.

**Done when:** you have the scope, the intent, the head SHA, and the changed files.

## Step 2: Fan out the adversaries

1. Pick the adversaries: one for each model of the `panel` role of the `models` block in
   `~/.claude/AGENTS.md`. With no `models` block or no `panel` role, use `opus` at high effort,
   `sonnet` at high effort, and the session model (leave `model` unset). When the Agent tool
   refuses a model, drop that adversary and say so. Keep at least two: add one on the session model
   when fewer remain.
2. Give each adversary its own git worktree, so that no two adversaries write the same files:
   `git worktree add --detach /tmp/interrogate-<branch>-<n> <head SHA>`. Copy the scope's
   uncommitted changes into it: `git diff HEAD --binary | git -C <worktree> apply --allow-empty`, then copy each
   untracked file of the scope.
3. Spawn every adversary in one message, each as a `general-purpose` subagent with
   `run_in_background: true`. Give each one the scope, the intent, its worktree path, and this
   brief, word for word:

   > Break this change. Work only in your worktree: `<worktree path>`. Prove each finding with a
   > run against the real code, such as a failing test, a repro script, or command output that
   > shows the wrong behaviour. For a design or a plan, run a prototype or probe the current tree.
   > Keep each repro file in your worktree. Each command must exit non-zero when the bug is
   > present, so add an assert or an `exit 1` to a repro script. Report only what you ran. Style,
   > naming, structure, and risks that need a future change are not findings. No findings is a
   > valid result.
   >
   > Return a JSON list, and nothing after it. Each item is
   > `{"title": "<one line>", "command": "<the exact shell command>", "evidence": "<one line from its output that shows the failure>", "intent": "<how the failure breaks the intent>"}`.
   > Run each command from the root of your worktree.
   >
   > When the repo has a driver, you may prove a finding through `/verify`, one run at a time. The
   > finding still needs a `command` that exits non-zero: write a script that replays the driver's
   > steps and exits 1 on the failure.

4. Wait for every adversary. When an adversary returns no JSON, record it as a dropout and go on.

**Done when:** each adversary returned a list or is a dropout.

## Step 3: Re-run each finding

1. Write every finding into one JSON file in a temp folder. Add `adversary` (its model) and `cwd`
   (its worktree path) to each item. Keep a finding with no command: the script drops it.
2. Run `python3 $SKILL_DIR/scripts/rerun_findings.py <findings file>`. Add `--timeout <seconds>`
   when a command needs more than 120 seconds, such as a full test suite.
3. The script keeps a finding when its command exits non-zero and its output holds the evidence
   line. It drops each other finding with one reason: `no command`, `no evidence`, `cwd not found`,
   `cannot run`, `timed out`, `passed on re-run`, or `evidence not in output`. A kept finding gets its `output`
   and `exit`.

Only the script decides if a finding is reproduced. Keep no finding that it drops.

**Done when:** you have the script's `kept` and `dropped` lists.

## Step 4: Check each kept finding against the intent

1. Read the output of each kept finding. Drop it with the reason `does not break the intent` when
   the failure is in a repro that tests behaviour outside the scope, or when the intent allows the
   behaviour.
2. Merge kept findings that have one root cause into one finding. List each adversary that found
   it.

Different adversaries find different failures, so keep every reproduced finding. Do not pick one
adversary's list.

**Done when:** each kept finding breaks the intent, and no two kept findings share a root cause.

## Step 5: Write the report

Write one report with `/write-report`:

- `kind`: `interrogate`.
- `skill`: `/engineering:fix`.
- `title`: `Interrogate <branch>`.
- `head`: the head SHA from Step 1. `meta`: `Base`, `Scope`, `Intent`, and `Adversaries`. Add
  `Plan` when the run has a plan.
- `answer`: the count of reproduced findings, and the next action. With none, say "No reproduced
  findings."
- `columns`: `title`, `command` (mono), `output` (mono, fold), `intent`, and `adversaries`.
- `rows`: one row for each kept finding, with `ticks: ["fix"]`. In `output`, keep the lines around
  the evidence line, at most 40 lines.
- `visuals`: a table that answers "What did each adversary drop, and why?". It has one row for
  each adversary: the adversary, the count of dropped findings, and each reason with its count.
  Add each dropout as a row with the reason `no findings JSON`.

**Done when:** the report exists, each kept finding is a row, and the Dropped table has a row for
each adversary.

## Step 6: Clean up

Remove each adversary worktree with `git worktree remove --force <path>`, and delete the findings
file. Then give the report path, the count of kept and dropped findings, and each principle that
shaped a choice.

**Done when:** `git worktree list` shows no adversary worktree, and the user has the report path.
