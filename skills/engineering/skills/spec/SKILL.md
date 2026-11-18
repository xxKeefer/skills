---
name: spec
description: >
  ★ Spec: define what to build. A ticket key goes to /refine-ticket. A raw idea gets an interview to
  an explicit yes, then a written spec that /plan reads. Use when the user says "spec", has a new
  idea to build, or gives a ticket key to define.
argument-hint: "<ticket key> | <idea in a sentence>"
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
4. Classify each gap by the `/grill` fork rule first, and ask only the decisions.
5. Stop when you can predict the user's reaction to your next three questions. If you still cannot
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

Write the spec with `/write-to-file`, doctype `spec`, in the layout of its template:

- Header: `doctype: spec`, `ticket` (the key, or `none`), `status: confirmed`, and `goal` (the
  Outcome line).
- `## Intent`: the six lines of the restatement from Step 4.
- `## Decisions`: the decisions from Step 3, each with its reason.
- `## Acceptance criteria`: one lettered AC for each requirement, in the form
  `- [ ] **A.** <action> → <expected>`. Letters start at A, with no gap.
- `## Out of scope`: optional. Remove it when the Intent line says all.
- `## Open questions`: optional. Remove it when no question is open. `/plan` stops while it holds
  an item.

`/write-to-file` runs `check_spec.py` on the spec. Fix each line that it names, and run it again
until it exits 0.

Then stop. Give the spec path. When the check prints `open questions: <n>` with `<n>` above 0,
list each item of `## Open questions`, and tell the user to answer or delete each one before
`/plan @<spec path>`. Else give the next command: `/plan @<spec path>`.

**Done when:** the spec is on disk, the check exits 0, and the user has its path and the next
command.
