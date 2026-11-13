---
name: spec
description: "★ Spec: define what to build. A ticket key goes to /refine-ticket. A raw idea gets an interview to an explicit yes, then a written spec that /plan reads."
argument-hint: "<ticket key> | <idea in a sentence>"
disable-model-invocation: true
---

# Spec

Define what to build before anyone plans it. This command ends at a confirmed spec. `/plan` comes
next.

```
ticket key → /refine-ticket
idea       → hypothesis → one question at a time → restate → explicit yes → write the spec
```

## Step 1: Route

- `$ARGUMENTS` is a ticket key: run `/refine-ticket` with the key. Then stop, and give the next
  command: `/plan <key>`.
- `$ARGUMENTS` is an idea, or is empty: go to Step 2. If it is empty, ask what to build.

**Done when:** a ticket went to `/refine-ticket`, or you have the idea.

## Step 2: Hypothesise

Read what the corpus can tell you first: `CONTEXT.md`, the ADRs, and the code near the idea. Then
write one line:

```
HYPOTHESIS: <what the user wants, in one sentence>
CONFIDENCE: <0–100%> — missing: <what is still open>
```

**Done when:** the user can see the hypothesis and the number.

## Step 3: Interview

Follow `/grill`, with these rules on top:

1. Each question carries your guess: `Q: …` then `GUESS: …`.
2. Ask about the gaps in this order: who gains, why now, what success looks like, the binding
   constraint.
3. When an answer sounds like what a good answer should be ("scalable", "the standard way"), ask:
   "If you did not have to justify this to anyone, what would you want?"
4. Stop when you can predict the user's reaction to your next three questions. If you still cannot
   after eight questions, say that something basic is missing, and ask to step back.

**Done when:** you can predict the next three answers, or the user stepped back.

## Step 4: Restate and confirm

Write back the intent, in the user's words where you can:

```
- Outcome:      <one line>
- User:         <who gains>
- Why now:      <what changed>
- Success:      <how we know it worked>
- Constraint:   <the binding limit>
- Out of scope: <what we will not build>
```

The gate is an explicit yes. "Sounds good" and "whatever you think" are not a yes. For "whatever
you think", offer two concrete options. For "sounds good", ask what you should change. Fold in each
correction and restate.

**Done when:** the user said yes to the restatement.

## Step 5: Write the spec

Write the restatement, the decisions from Step 3, and the open questions with `/write-to-file`,
doctype `spec`. Give each requirement a lettered AC in the form
`- [ ] **A.** <action> → <expected>`.

Then stop. Give the spec path and the next command: `/plan @<spec path>`.

**Done when:** the spec is on disk, and the user has its path and the next command.
