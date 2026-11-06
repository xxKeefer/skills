---
name: split-ticket
description: >
  Split a ticket that is too big for one PR into sub-tasks: cut the pieces, group them into waves
  with a merge order, write the split report, then create the sub-tasks and a stub handoff for each
  after one yes. Use when the user asks to split a ticket, or when /scope-ticket or the
  /start-ticket plan gate gives SPLIT and the user picks the split path.
argument-hint: "<ticket key>"
---

# Split Ticket

Turn one ticket that is too big into sub-tasks under it. Each sub-task gets one branch and one PR.
The parent ticket gets no PR of its own. Separate agents can build the pieces of one wave at the
same time.

```
read → cut the pieces → order the waves → write the report → gate → create → write the stubs
     → return
```

## Step 1: Read the input

1. Read the key from `$ARGUMENTS`. If it is not there and not in context, ask for it.
2. If the caller gave a SPLIT result, use its slices and the ticket text that it read. A SPLIT
   result has the slice format of [`../scope-ticket/SKILL.md`](../scope-ticket/SKILL.md) Step 4.
   It comes from `/scope-ticket`, or from the plan gate of `/start-ticket`. Else run
   `/scope-ticket` with the key. Tell it that the user chose to split, so it asks
   no path question and returns the slices here.
3. Use the verdict:
   - SCOPED: stop. Say that the ticket fits one PR, and give its points.
   - CLARIFY: stop, and return the open questions.
   - SPLIT: continue.
4. Check the tracker. Stop and say why when one of these holds:
   - The ticket already has sub-tasks. List them. A second split makes duplicate pieces.
   - The ticket is itself a sub-task, or its project has no sub-task type.
5. Fetch all the fields of the sub-task type. Find the points field by its name, such as "Story
   Points". Note each required field, and its value on the parent ticket. Hold no type ID or
   field ID.

**Done when:** you have the slices and the sub-task fields, or you stopped and said why.

## Step 2: Cut the pieces

A piece is one slice that becomes one sub-task.

1. Check each piece against the five slice checks in
   [`../scope-ticket/SKILL.md`](../scope-ticket/SKILL.md) Step 4. Its size is 3 points or less.
   Cut a piece that fails again, until it passes.
2. Draft the sub-task text of each piece by
   [`../refine-ticket/SKILL.md`](../refine-ticket/SKILL.md) Step 4. The title is the slice goal.
   The summary is plain, and the ACs are lettered from A. Add one line that names the parent ACs
   that the piece delivers. Run the scan from that step.
3. Note the files or areas of each piece from the probes. They go in the stub handoff, not in the
   sub-task.

**Done when:** each piece passes the five checks, each parent AC is in exactly one piece, and each
piece has a title, a summary, and ACs.

## Step 3: Order the waves

1. For each piece, name the pieces that it builds on. A piece builds on another piece only when it
   cannot build or pass its ACs without that piece's code. Prefer wide waves to long chains.
2. Group the pieces into waves. Wave 1 holds each piece that builds on nothing. Each later wave
   holds each piece whose pieces are all in earlier waves. No piece builds on a piece in its own
   wave.
3. List the pieces in merge order: by wave, then by piece number. Give each piece its merge line:
   `stacks on <piece>` when it builds on a piece, else `merges alone`.

**Done when:** each piece has a wave and a merge line, and the merge order puts each piece after
each piece that it builds on.

## Step 4: Write the report

Write the report with `/write-report`:

- `kind` `split`, `key` the parent key, and `title` `Split of <KEY>`. Give no `skill`, so the
  report has no ticks. The yes in Step 5 is the approval.
- Run title `Split proposal`. `meta` holds `Ticket` and `Points`, the sum of the pieces.
- `answer`: the number of pieces and waves, and what a yes in chat does.
- Visuals:
  - `mermaid`, "Which pieces can run at the same time?": one node per piece, an arrow from each
    piece to each piece that builds on it, and one `classDef` colour per wave.
  - `table`, "In which order do the PRs merge?": the columns Order, Piece, and Merge.
- Columns: `piece` (the title, a blank line, then the summary), `acs` (the ACs, then the parent
  AC line), `files` (mono), `points`, `wave`, `builds` (Builds on), and `merge`. One row per piece,
  in piece order.

**Done when:** `/write-report` returned the report path.

## Step 5: Gate

1. Give the report path, the number of pieces, and the waves.
2. Say what a yes does: it creates one sub-task per piece under `<KEY>`, writes the points of each,
   and writes one stub handoff per piece.
3. Name each required field that the parent cannot fill, and ask for its value in the same
   question.
4. Ask once. On a no, create nothing, and go to Step 8 with the report path.
5. If the user asks for a change, make it, write the report again, and ask again.

**Done when:** the user said yes or no.

## Step 6: Create the sub-tasks

Create the sub-tasks in merge order, one at a time.

1. Set the parent to `<KEY>`, and the title from Step 2.
2. Write the description in the layout of
   [`../refine-ticket/SKILL.md`](../refine-ticket/SKILL.md) Step 5: the summary, then the ACs, then
   the parent AC line.
3. Write the points in the points field. A new sub-task has a blank field, so the Step 5 yes covers
   the write. If the type has no points field, write none, and say so.
4. Fill each required field from the parent, else with the value from Step 5.
5. Read the sub-task back. Show any difference from the text that you sent.

If a create fails, stop. List the sub-tasks that exist and the pieces that have none.

**Done when:** each piece has a sub-task key, and each sub-task reads back as sent.

## Step 7: Write the stubs

1. For each piece, write `plan_<SUBKEY>.md` with `/write-to-file`, doctype `plan`, into the folder
   of the parent ticket `<KEY>`. `/claim <SUBKEY>` finds the stub by its name. Write in Simplified
   Technical English. Read [`STE.md`](../../STE.md) first, and follow every rule in it.

   ```markdown
   # Plan: <SUBKEY> <title>

   Ticket: <SUBKEY>, a sub-task of <KEY>. Goal: <title>. Scope: piece <n> of <m>, wave <w>. Estimate: <points>.
   Builds on: <SUBKEY list, or none>.
   Merge: after <SUBKEY list> | Merge: alone

   ## Acceptance criteria

   - [ ] **A.** <action> → <expected>

   ## Context

   Files or areas: <from Step 2>. Split report: <path>.
   ```

   The stub has no Steps section. `/start-ticket <SUBKEY>` drafts the plan into it.
2. If the parent ticket has a handoff, add a `## Split into` section to it. Give one line per
   sub-task: its key, its title, its wave, and its stub path.

**Done when:** each piece has a stub, and the parent handoff, if any, lists each stub.

## Step 8: Return

Return the report path, and each sub-task key with its wave and stub path. For each piece in wave
1, give the command `/start-ticket <SUBKEY>`. Each one runs in its own session, at the same time
as the others. A calling skill continues from here. With no caller, stop.

**Done when:** the caller or the user has the report path and the wave 1 commands.

## Rules

- Change nothing on the parent ticket. The sub-tasks under it record the split.
- Write no code and no plan steps. The plan of each piece belongs to `/start-ticket`.
