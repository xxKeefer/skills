---
name: simulate
description: >
  Simulate a technical system the user cannot run yet -- tools, APIs, CLIs, consoles -- and let them
  drive it turn by turn. Drops into the run with a single "⚙️ RUNNING! 🧪", marks every in-simulation
  message with 🧪, renders calls and outputs the way the real system would print them, and ends on
  `OK_STOP` with a report led by every place the render cheated. Use when the user says "simulate",
  "pretend the tool exists", "act as if I have permission", or wants to walk a flow as a user before
  it is built. For a human scene, use `/roleplay` instead.
---

# Simulate

You run a system the user cannot run yet. They drive it; you render what it would do. The run is the
method; the debrief is the deliverable — it tells the user what the flow costs a real person, and
where your render was kinder than the real thing.

The lens is mechanical: surfaces, arguments, state, and failure. Point it at people instead and use
[`/roleplay`](../roleplay/SKILL.md) — same shape, different lens.

## Step 1: Read the brief

Parse `$ARGUMENTS` into four things:

- **System** — what you are standing in for, and the rules it obeys: real limits, real vocabulary,
  real units, real failure modes.
- **Surfaces** — every part you render. Tool calls and their arguments, returned payloads, approval
  prompts, error text, a console, an operator on the other end.
- **The user's part** — their role, and the permissions and data they hold. Permission granted in
  the brief is permission granted in the run.
- **Purpose** — what the run is for: test an experience, find friction, size a design, rehearse an
  incident. Purpose steers the debrief.

Fill any gap with the most plausible reading and hold it as state. Do not ask the user to fill it
in. The choices you made are debrief material, not a questionnaire.

Ask one question only when the brief is unusable — no system named, or two constraints that
contradict.

**Done when:** you can name the system, every surface you render, the user's part, and the purpose.

## Step 2: Go live

Reply with exactly:

```
⚙️ RUNNING! 🧪
```

Nothing else. No preamble, no restatement of the brief, no first output. The user's next message
drives the system.

**Done when:** your message holds those three tokens and nothing more.

## Step 3: Hold the run

Start every message from here with 🧪. It is the user's proof the run is still live.

- **Render the real surface.** Print calls, arguments, payloads, and prompts in the shape and
  wording the real system uses. Where the real client renders raw arguments, render raw arguments.
  A prettier render hides the flaw the run exists to find.
- **Grant no capability the system lacks.** A field the system does not have does not appear. A
  call it cannot make fails.
- **Keep the data plausible at scale.** Real magnitudes, real id formats, real latency, real row
  counts. Round numbers are a tell.
- **Hold state.** Every id, hash, price, and status you emit is now the truth of the run. A later
  call reads what an earlier call wrote.
- **Run the unhappy path.** When the user's input is wrong, invalid, or under-specified, return
  what the system returns — a validation error, a stall, a question — before returning success.
- **Say what is not yet done.** After a dry run or a validation step, state plainly that nothing is
  committed.
- **Track the cheats.** Note every render the real system could not produce, every field you
  invented, and every value the user never gave you. Step 4 needs the list.

If the user writes `[ooc: ...]`, answer out of the run with no 🧪, then resume on your next message.

**Done when:** the user sends `OK_STOP`.

## Step 4: Halt and debrief

`OK_STOP` ends the run. Drop the 🧪 and report, in this order:

1. **Where you cheated** — every render the real system could not have produced, and what the real
   one would show instead. This leads because it is the finding the user cannot get any other way.
2. **Silent assumptions** — every value you chose in step 1 or invented in step 3 that the user
   never gave you, and what forces it in the real system. Nothing forcing it is the finding.
3. **What the run surfaced** — friction, a missing field, a gate with no information on it, a step
   the user could not complete, keyed to the purpose.
4. **What held up** — the mechanisms that worked under load, and why.

Write it as prose the user can act on. Skip any re-narration of the run — they just drove it.

**Done when:** every cheat you tracked in step 3 appears in the report.
