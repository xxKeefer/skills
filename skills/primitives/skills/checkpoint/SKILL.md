---
name: checkpoint
description: >
  Stop work at a safe point: finish or back out the current step, make one `wip:` commit, and
  write the resume note into the plan. Use when the user says "checkpoint" or "pause", or when
  the context window is about to fill.
argument-hint: "@path/to/plan.md"
---

Stop the work so that a fresh session can continue from the plan. Push nothing, and open no PR.

1. Find the plan. Use the @-tagged file, else the plan in `.ai/` for the current branch. If no plan
   exists, write one with `/write-to-file`, doctype `plan`, from this conversation: the goal, each
   step that is done or left with its done line, and `Progress`. Reference other files by path.
2. Reach a safe point. Finish the part that you are in, or back it out. Do not leave a half-made
   edit. Leave each file in a state that you can describe in one line.
3. Run `/update-plan` on the plan. In `Progress`, write what is done, the part that is open, and
   the next action. Name each file that the open part touches.
4. Stage every change, including the plan. Make one commit, with the message
   `wip: <step id> <one-line state>`. Follow the commit rules of the repo. Keep the hook on.
5. Run `git status --porcelain`. If it prints a line, fix the cause and commit again.

Reply with the commit SHA, the words "tree clean", and the command to continue: `/do-next @<plan
path>`, or `/work-on` with the plan.

Write every line you add in **Simplified Technical English**. Read
[`STE.md`](../../STE.md) before you write, and follow every rule in it.
