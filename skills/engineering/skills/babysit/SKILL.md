---
name: babysit
description: Watch PRs in the background and alert on each change of CI or review state, with one chip for each PR on the status line. Use when the user says "babysit" or "watch my PRs", or gives PR numbers or a stack to watch.
argument-hint: "<PR numbers, or a stack> [owner/repo]"
---

Watch the PRs that the user names. Edit no PR and post nothing.

## Step 1: Add

Find the code host repo as `owner/repo` from the argument or the current repo. For a stack, take the number of each PR in the stack. For each number, run:

`python3 $SKILL_DIR/scripts/watch_prs.py add <owner/repo> <number>`

`$SKILL_DIR` is this skill's base directory. The watcher keeps the watch list and the last state of each PR in `~/.cache/babysit/state.json`. For a stack, it polls only the lowest PR that is not merged.

**Done when:** each PR is in the state file.

## Step 2: Start

Start one loop, detached:

`nohup python3 $SKILL_DIR/scripts/watch_prs.py run --interval 60 >/dev/null 2>&1 &`

A second `run` exits at once, because `~/.cache/babysit/run.pid` holds the pid of the first. The loop exits when no watched PR is open.

**Done when:** `~/.cache/babysit/run.pid` exists.

## Step 3: Tell the user

- The loop calls `notifier_command` from `~/.claude/agents-md.values.json` once for each change of state. The first poll of a PR sends no alert. With no `notifier_command`, or `none`, the chip is the only alert. `/install-agents-md` fills the key.
- Each PR is a chip on the right of line 1 of the status line. `/setup-statusline` describes the chips.
- To stop: `kill $(cat ~/.cache/babysit/run.pid)`. To forget the PRs: delete `~/.cache/babysit/state.json`.

Write every line you add in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and follow every rule in it.
