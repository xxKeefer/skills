---
name: tabular-analysis
description: >
  Compare and contrast concepts in a markdown table whose columns are exactly the headers you
  supply (pipe-delimited), one row per concept. Usage is order-flexible: tabular-analysis <topic>
  <col|headers> OR tabular-analysis <col|headers> <topic>. The topic may be @file links or any
  resource /look-up can resolve. Use when the user says "tabular analysis", "compare X and Y in a
  table", "table this", or hands a topic plus pipe-split column names.
argument-hint: "<topic> <column|headers|split|by|pipes>"
---

# Tabular Analysis

Turn a topic into a side-by-side comparison: a markdown table with the user's exact columns and
one row per concept being compared. The user controls the lens (the columns); you supply the
evidence (the cells).

## Step 1: Parse the arguments

Two arguments in either order. **The pipe-delimited one is the column headers; the other is the
topic.** Split the headers on `|`, trim each, and preserve their order — these become the table
columns verbatim.

- Neither argument contains pipes → ask the user for the column headers (the comparison lens).
- Both contain pipes → ask which is the headers and which is the topic.

**Done when:** you have an ordered list of column headers and a topic string.

## Step 2: Resolve the topic

If the topic contains `@`-style file links or any resolvable reference (paths, URLs, tracker
tickets, doc pages), delegate to `/look-up` to fetch and ingest them. If it's a plain subject,
gather what you need to compare it accurately — `/look-up` for anything you can't speak to
reliably from the codebase or knowledge. Do not fabricate; an unknown is better surfaced than guessed.

**Done when:** you have the material needed to fill the table.

## Step 3: Determine the rows (the concepts)

Identify the set of concepts being compared — one per row:

- Two or more named/linked things (files, libraries, approaches) → one row each.
- A single topic that implies a set (e.g. "state libraries", "the auth strategies in this repo") →
  enumerate the members as rows.
- Ambiguous what's being compared → ask the user to name the concepts (one short question).

**Done when:** you have the row set, and it's clear what each row represents.

## Step 4: Build the table

- Always prepend a `#` column as the very first column: an auto-incrementing, 1-indexed row
  count (1, 2, 3, …). This is the one column you add yourself — it gives every row a stable id to
  reference in discussion ("row 3", "#3"). It sits before the user's headers and is never part of them.
- After the `#` column, columns are **exactly** the Step 1 headers — same wording, same order.
  Never add, rename, drop, or reorder the user's columns. If the user wants a first "concept"/name
  column, it's already in their headers; don't invent one.
- One row per concept from Step 3, numbered sequentially from 1 in the `#` column.
- Fill each cell from the resolved material. Keep cells terse — phrases, not paragraphs. For
  source-backed comparisons, ground cells in the evidence (`file:line` where it helps).
- Missing/inapplicable data → `—`, not a guess.

**Done when:** every row has a value (or `—`) for every column.

## Step 5: Present

Output the markdown table directly in the response. Below it, add at most a couple of lines only
if something needs flagging — gaps, caveats, or a one-line takeaway. Don't pad with prose; the
table is the deliverable. If the user wants it persisted, offer `/write-to-file`.

**Done when:** the table is shown with a leading `#` column, then the user's exact columns, and one row per concept.
