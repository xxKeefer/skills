---
name: scope-ticket
description: >
  Scope a ticket before work starts: size the change with cheap probes, then give one verdict,
  SCOPED, SPLIT, or CLARIFY, with a points estimate. A direct run on the split path hands off to
  /split-ticket. Use when the user asks to scope a ticket or asks whether a ticket is too big to
  land in one PR, or when another skill needs a scope check before work starts.
argument-hint: "<ticket key>"
---

# Scope Ticket

Answer one question: does this ticket hold one goal that lands in one reviewable PR? Size the
change to answer it, then give one verdict. This is a surface check, not a plan. Size the work, and
leave the design to the plan.

## Budget

Speed is the point. A scope check that costs as much as a plan has no value.

- Search, count, and read signatures. Read no file end to end.
- Run one parallel batch of probes. Add at most one search subagent, and only when the ticket's
  target area is unknown.
- Write no code and no plan. If you start to decide how to build the change, stop.

## Step 1: Read the ticket

1. Read the key from `$ARGUMENTS`. If it is not there and not in context, ask for it.
2. If the caller already read the ticket and its linked tickets, use that. Else read them with
   `/look-up`.
3. Note the goal, the ACs, the areas and flags that the ticket names, and its linked tickets.

**Done when:** you have the goal and every AC.

## Step 2: Judge the ACs

Be antagonistic. Assume that the ticket is broader than it claims, and make it prove otherwise.

Write the goal as one sentence with no "and". If you cannot, the ticket holds two goals.

Split signals:

- More than six lettered ACs.
- Several deliverables: ACs that could each ship alone, or a list joined by "and also", "as well
  as", or "plus".
- Vague scope words: "improve", "clean up", "audit", "refactor as needed", "everywhere", "all X",
  "across the app". An AC with no bound gives a diff with no bound.
- Several projects: the ACs change more than one app or package.
- Build, rollout, and cleanup in one: add behind a flag, move the call sites, delete the old path,
  and remove the flag.
- Mixed kinds of change: a refactor and a feature, a dependency bump and app changes, or a
  production change and a large test rewrite.
- A migration that the ACs do not state: the end state needs many existing call sites to move.
- Hidden discovery: an AC cannot pass until someone investigates. The spike and its fix are two
  pieces of work.

Keep the ticket whole when one of these holds:

- No cut gives slices that each pass the vertical test (Step 4).
- The change is big but atomic: a mechanical codemod, one generated file, or a lockfile.
- The size is small: under about 400 changed lines and 10 files.
- The split costs more in overhead than it saves the reviewer.

"The scope is fine" is a common and valid verdict. Say it in one line.

**Done when:** you have the one-sentence goal or the reason that it fails, and each split signal
that fires.

## Step 3: Size the change

Run the probes from the root of the repo that the ticket changes, in one parallel batch. For
example:

```bash
git grep -l '<the thing that changes>'        # files in the blast radius
git grep -c '<call site pattern>' | wc -l     # files with call sites to move
git ls-files | grep -i '<module name>'        # where it lives
git log --oneline -8 -- <target folder>       # recent changes
```

Turn the counts into files touched, call sites to move, subsystems crossed, new files, and test
files. Leave out generated files, lockfiles, and snapshots. Say that the size is an estimate.

### The scale

One table sets the points and the split thresholds, so the points and the verdict agree.

| Points | Changed lines | Files | Subsystems | Meaning |
|---|---|---|---|---|
| 1 | under ~150 | up to ~5 | 1 | Local or mechanical. The approach is clear before you start. |
| 2 | ~150 to 400 | up to ~10 | 1 | A clear approach, and a few call sites to carry along. |
| 3 | ~400 to 600 | up to ~20 | up to 2 | A clear approach with real breadth. The most that one reviewable PR holds. |
| 5 | over 600, or over 20 files | | up to 2 | On the split line. It stays whole only with a one-line reason, such as an atomic codemod. |
| 8 | over two thresholds | | over 2 | It cannot start as one piece of work. Split it, or give CLARIFY. |

More than about 15 call sites to move, or more than one unrelated concern, also crosses a
threshold.

- Size the change, not the calendar. A one-line fix that took three days is a 1.
- A spike is 1, 2, or 3, set by its timebox. A spike gives a decision, not code. A spike over 3
  asks too broad a question, so narrow it.
- Between two values, take the larger. Name the probe that would settle it.
- Each number traces to a probe that you ran. When the probes are too thin to place the ticket in
  a row, the verdict is CLARIFY.
- A 5 with SCOPED needs its one-line reason. An 8 with SCOPED is a contradiction, so go back to
  Step 2.

**Done when:** each count traces to a probe, and the ticket sits in one row of the scale, or the
probes are too thin to place it.

## Step 4: Give the verdict

Give exactly one:

- **SCOPED:** one goal, and a reviewable size. Give the points.
- **SPLIT:** give the slices.
- **CLARIFY:** the ACs are too vague to size. Give each question that blocks the size, and your
  guess at its answer.

Each slice passes every check:

1. It has one goal in one sentence, with no "and".
2. It passes the vertical test: once it merges, a user can exercise it end to end. A pure refactor
   or rename of code that already ships also passes. New code that nothing calls yet, such as a
   type, a util, or a schema with no reader, is never a slice of its own. Put it in the first slice
   that uses it.
3. It names the real files or areas from the probes.
4. It has 1 to 3 ACs of its own, in the form `- [ ] **A.** <action> → <expected>`, lettered from A.
   It names the parent ACs that it delivers. Each parent AC lands in exactly one slice.
5. Its size is 1, 2, or 3 points. A slice at 5 is still too big.

Order the slices. Slice 1 is the narrowest path that a user can exercise end to end, and each later
slice widens it. Work outside the ticket's goal goes under Deferred, not into a slice.

```
Verdict: SPLIT. The ticket holds a create form, an edit form, and a bulk delete.

Goal (as written): "..."
Goal (one sentence): "..."
Size: ~1,100 lines, ~26 files, 2 subsystems. 8 points. The ticket has none.

| # | Slice (one goal) | Files or areas | Parent ACs | Size | Points | Builds on |
|---|---|---|---|---|---|---|
| 1 | Create a project | ... | A, C | ~350 lines | 2 | none |
| 2 | Edit a project | ... | B | ~300 lines | 2 | 1 |
| 3 | Delete many projects | ... | D, E | ~380 lines | 2 | 1 |

Slice 1 ACs:
- [ ] **A.** ... → ...

Deferred: ...
```

**Done when:** you gave one verdict. For SPLIT, each slice passes the five checks, and each parent
AC is in exactly one slice.

## Step 5: Pick the path (SPLIT only)

One ticket gets one branch and one PR. If the caller says that the user chose to split, take path
2 and ask no question. Else ask the user which path to take:

1. **Keep one ticket.** The slices become the phases of the plan, in order, on one branch and one
   PR. This is the path when the user does not own the ticket.
2. **Split into sub-tasks.** `/split-ticket` cuts the pieces and creates the sub-tasks after a yes.
   Each sub-task gets its own branch and PR. The parent ticket gets none.

**Done when:** the user picked a path, or the caller said that the user chose to split.

## Step 6: Offer the estimate

1. Find the points field by its name, such as "Story Points". Fetch all the fields of the ticket's
   type, not only the required ones. Hold no field ID. If the tracker has no points field, show the
   estimate and write nothing.
2. The estimate is the ticket's points.
3. Use the first row that fits:

   | Case | Do |
   |---|---|
   | CLARIFY | Write nothing. No size is the finding. |
   | SPLIT, path 2 | Write nothing. `/split-ticket` writes the points of each sub-task. |
   | The field has the same value | Write nothing. |
   | The field has another value | Show both, such as `ticket says 1, probes say 5`. Write nothing. |
   | The field is blank | Show the estimate and ask once. Write it after a yes. |

4. Say in one line what you wrote and what the field held before, or that you wrote nothing.

**Done when:** the field holds the estimate after a yes, or you said why you wrote nothing.

## Step 7: Return

For CLARIFY, refine the ticket before you return:

1. Run `/refine-ticket` with the key and the ticket text that you read.
2. Give it each Step 4 question as a caller question, with your guess as the proposed answer.
3. When it returns, go back to Step 2 with its summary and ACs. Use them even if it wrote nothing.
4. If that run gives CLARIFY again, return CLARIFY with the open questions. Do not run
   `/refine-ticket` again.

Return the verdict, the Step 6 estimate, and the one-sentence goal. For SPLIT, also return the
slices and the path. If `/refine-ticket` ran, also return its summary, its ACs, and whether it
wrote them. A calling skill continues from here. With a caller, this skill does not run
`/split-ticket`.

With no caller, SPLIT path 2 runs `/split-ticket`. Give it the key, the slices, and the ticket text
that you read, so it runs no second scope check. Then stop. On any other result, stop.

**Done when:** the caller or the user has the verdict. With no caller on SPLIT path 2,
`/split-ticket` returned.

## Rules

- Judge only the size and the split. Correctness, naming, style, and architecture belong to the
  review.
- Give one verdict. Do not hedge across two.
