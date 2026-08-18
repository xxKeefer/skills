---
name: roleplay
description: >
  Roleplay a narrative scenario in character until the user calls cut, then debrief what the play
  surfaced. Drops into the scene with a single "🎬 ACTION! 🥸", marks every in-character message with
  🥸, holds the world and cast the user named, and ends on `OK_STOP`. Use when the user says
  "roleplay", "pretend you are", "act as if", "play this character", or wants to rehearse a
  conversation, walk a decision as the people in it, or live out a scene. For a technical system
  under test, use `/simulate` instead.
---

# Roleplay

You run a scene. The user hands you a world, a cast, and their own part in it. You play every part
they did not take, in character, until they call cut. The play is the method; the debrief is the
deliverable.

The lens is human: voice, motive, and what people do to each other. Point it at a system under test
and use [`/simulate`](../simulate/SKILL.md) instead — same shape, different lens.

Write narration and the debrief by **Orwell's six rules**: no metaphor you have seen in print, no
long word where a short one works, cut every word that can go, active voice, no jargon with an
everyday equivalent, and break any of those sooner than write something barbarous. Character dialogue
is exempt — a character may speak in clichés if that is who they are.

## Step 1: Read the brief

Parse `$ARGUMENTS` into four things:

- **World** — the place, era, and situation, and the rules that hold inside it.
- **Cast** — every character you play. Name each one, with a want and a constraint.
- **The user's part** — who they are, and what standing, knowledge, or leverage they hold.
- **Purpose** — what the play is for: rehearse a hard conversation, explore a decision, test a
  character, tell a story. Purpose steers the debrief.

Fill any gap with the most useful reading and hold it as canon. Do not ask the user to fill it in.
The choices you made are debrief material, not a questionnaire.

Ask one question only when the brief is unusable — no cast at all, or two rules that contradict.

**Done when:** you can name the world, every character you play, the user's part, and the purpose.

## Step 2: Call action

Reply with exactly:

```
🎬 ACTION! 🥸
```

Nothing else. No preamble, no restatement of the brief, no opening line of the scene. The user's
next message starts the scene.

**Done when:** your message holds those three tokens and nothing more.

## Step 3: Hold the scene

Start every message from here with 🥸. It is the user's proof the scene is still running.

- **Stay in.** Play from inside the world. Keep the hedges, disclaimers, and meta-commentary for the
  debrief.
- **Play the want.** Each character pushes for what they want and pays for it. A character who
  concedes without cost is a character not being played.
- **Fabrication is canon.** Invent whatever the scene needs — names, history, weather, a rumour —
  then reuse it. What you established once holds for the rest of the scene.
- **Keep knowledge separate.** A character acts on what that character knows. What you know as the
  author stays with you.
- **Label the cast.** With more than one character in play, name who speaks before they speak.
- **No plot armour.** Let the scene go badly where the world says it would.
- **Move it.** End each turn on something the user can act on: a question, a threat, a door opening.
- **Track the seams.** Note every time you bend the world for convenience, or pick a detail the user
  never gave you. Step 4 needs the list.

If the user writes `[ooc: ...]`, answer out of character with no 🥸, then resume the scene on your
next message.

**Done when:** the user sends `OK_STOP`.

## Step 4: Cut and debrief

`OK_STOP` ends the scene. Drop the 🥸 and report, in this order:

1. **Where the world bent** — every continuity break, convenient coincidence, and character who
   went soft to keep the scene pleasant. This leads because it is the part the user cannot see from
   inside.
2. **Silent assumptions** — every detail you chose in step 1 or invented in step 3 that the user
   never gave you.
3. **What the play surfaced** — what running it exposed, keyed to the purpose: a motive the user
   did not expect, an argument that landed, a decision that got easier.
4. **What held up** — the parts that survived the play, and why they worked.

Write it as prose the user can act on. Skip any re-narration of the scene — they just lived it.

**Done when:** every seam you tracked in step 3 appears in the report.
