---
name: verify
description: >
  Find the verification drivers for a diff and run each one against the live app, then return the
  evidence paths, or `no driver`. Use when the user says "verify", or when a skill must see a
  change live, such as /test, /interrogate, /blast-radius, or /qa-screenshots.
argument-hint: "[<base ref>]"
---

# Verify

A driver is a skill that runs one app the way a user does. This skill finds the drivers for a diff,
runs them, and returns what they saw. It holds no drive steps. Each driver holds its own.

Principle: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)). Read it before you apply it, and name it in the reply when it shaped a choice.

`$SKILL_DIR` is this skill's base directory.

Run each driver at the `verifier` role of the `models` block in `~/.claude/AGENTS.md`. With no
`models` block, use the session model.

```
find the drivers → run each driver → return the evidence
```

## Step 1: Find the drivers

1. Find the base. It is the argument. Else it is the base branch of the plan, or the default branch
   of the repo.
2. Run `python3 $SKILL_DIR/scripts/find_drivers.py --repo <repo root> --base <base>`.
   The script reads the repo name from `git remote get-url origin`. It lists the diff paths from
   the merge base with the base, plus the working tree. It prints one driver path per line.
3. A line `no app-paths: <path>` on stderr names a driver that has no `app-paths` key. A line
   `no repo: <path>` names a driver whose `repo` key is missing or names another repo. Tell the
   user that the driver cannot match, and keep going.
4. When the output is `no driver`, return `no driver` and stop. Do not write a driver here. When a
   plan exists, write `no driver` in its `Progress`, and `/retro` proposes
   `/create-verification-skill`.

**Done when:** you have a list of driver paths, or you have returned `no driver`.

## Step 2: Run each driver

1. For each driver, read its `SKILL.md` and follow it: Launch, Doctor, Drive, Evidence, Cleanup.
2. Give the driver the change to look at: the diff paths, and what the caller wants to see.
3. Run independent drivers in parallel, each in a subagent at the `verifier` role.
4. When a driver fails at Doctor or Launch, record that as a result. Do not skip the driver.

**Done when:** each driver has a result of `pass`, `fail`, or `blocked`, with its evidence.

## Step 3: Return

Return one line for each driver: the driver path, the result, and the path of its evidence. Add one
sentence on what the evidence shows about the change. When a driver fails because the app moved
and its map did not, name `/create-verification-skill maintain` as the next step. Write no other
file.

**Done when:** the return names each driver, its result, and its evidence path.
