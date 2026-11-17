---
name: sitrep
description: >
  Show what a plan leaves open: the pending decisions, the choices that the agent made alone,
  the skipped steps, and the follow-ups. Use when the user says "sitrep" or "what did the agent
  decide", or after a /build.
argument-hint: "@path/to/plan.md"
---

Show the state of the @-tagged plan. Write no file.

## Step 1: Collect

Run `python3 $SKILL_DIR/scripts/sitrep.py <absolute plan path>`. `$SKILL_DIR` is this skill's base
directory. The script prints one section for each of these, and leaves out an empty section:

- The open `D`, `B`, and `N` entries of `Pending Decisions`.
- The rows of the decision log, `decisions_<KEY>.tsv` beside the plan. A row whose result starts with `open` shows `Still open` and its row number. To close it, run the `result` form of `/update-plan`'s `log_decision.py` with that number.
- The skipped steps, with their reasons.
- The `Follow-ups`.

If the script prints `Nothing is pending.`, say that and stop.

## Step 2: Judge

Give each item three lines:

- **Evidence:** the file, the command, or the step that shows the item. Read it. Do not guess.
- **Risk:** H, M, or L, with the reason.
- **Pick:** your choice, and the reason. For an open entry, name an option. For a choice made alone,
  say keep or reverse.

Order the items by risk, highest first.

Write every line you add in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before
you write, and follow every rule in it.
