---
name: refine-ticket
description: >
  Refine a ticket before work starts: grill out each ambiguity, derive lettered ACs from the user
  story, and write a plain summary, then write both back to the ticket after one yes. Use when the
  user asks to refine a ticket, or when another skill finds a ticket with no user story, no ACs,
  or vague scope words.
argument-hint: "<ticket key>"
---

# Refine Ticket

A ticket is for every reader of the board, technical or not. Refine it until the next person can
scope it and build it with no question: each ambiguity resolved, ACs that a person can check, and a
summary that any reader understands.

```
read → check → grill → draft → gate → return
```

Change only the summary and the ACs. The size and the split belong to `/scope-ticket`.

## Step 1: Read the ticket

1. Read the key from `$ARGUMENTS`. If it is not there and not in context, ask for it.
2. If the caller already read the ticket and its linked tickets, use that. Else read them with
   `/look-up`, in parallel.
3. Note the title, the description, the user story, the ACs, the comments, and the linked tickets.
   Note each open question that the caller gives.

**Done when:** you have the ticket text and each caller question.

## Step 2: Check the ticket

| Check | Passes when |
|---|---|
| User story | The ticket names who gains, what changes, and why. |
| ACs | Each AC has the form `- [ ] **A.** <action> → <expected>`, and a person can check it. "Tests pass" is not an AC. |
| Summary | Two or three sentences at the top of the description tell any reader what changes. |
| Scope | No AC holds a vague scope word from [`../scope-ticket/SKILL.md`](../scope-ticket/SKILL.md) Step 2. |

List each gap: a check that fails, each vague word, each AC with no expected result, and each
statement that two readers can read in two ways. Close a gap from the linked tickets and the
comments before you list it.

If the list is empty and the caller gave no question, say so in one line, and go to Step 6. Write
nothing.

**Done when:** each check passes, or each gap is on the list.

## Step 3: Grill out each gap

Run `/grill` on the list. Put the caller's questions first, then the gaps in ticket order.

- A missing user story is one question: who gains, what changes, and why.
- A vague scope word becomes a bound: the list of screens, records, or cases that the AC covers.

**Done when:** each gap and each caller question has an answer from the user.

## Step 4: Draft the change

**ACs.** Derive them from the user story and the answers. Give each end state that a person can
check one AC.

- Keep each letter that the ticket has. A rewritten AC keeps its letter.
- If the ACs have no letters, letter them in ticket order from A.
- A new AC takes the next free letter.
- A dropped AC keeps its letter, struck through: `- ~~**C.** <action> → <expected>~~`. Never
  re-letter.
- A sub-check is `A.1`, nested under its AC.

**Summary.** Write two or three sentences that a reader with no code knowledge understands. They
carry the user story: who gains, what changes, and why. Keep a name only when the reader sees it in
the product, such as a label on a screen. Write each part as if it was always right, with no note
of what changed. Write in Simplified Technical English. Read [`STE.md`](../../STE.md) first, and
follow every rule in it.

**Scan.** Scan the summary and the ACs as [`DRAFT-SCAN.md`](../../DRAFT-SCAN.md) says.

**Done when:** each gap from Step 2 is closed in an AC or the summary, and the scan finds nothing.

## Step 5: Gate and write

1. Place the summary at the top of the description, under the ticket's own summary heading, else
   under `## Summary`. Put the ACs in place of the old AC list, else under
   `## Acceptance criteria` after the summary.
2. Show the exact change, before and after. Say that the title and the rest of the description stay
   as they are.
3. Ask once. On a no, write nothing, and go to Step 6.
4. After a yes, write the description through the tracker. Change no other field.
5. Read the ticket back. Check that only the summary and the ACs changed. Show any other difference.

**Done when:** the ticket holds the change after a yes, or the user said no.

## Step 6: Return

Return the summary, the lettered ACs, and whether you wrote them. If the answers show more than one
goal, say so. `/scope-ticket` decides the split. A calling skill continues from here. With no
caller, stop.

**Done when:** the caller or the user has the summary, the ACs, and the write result.
