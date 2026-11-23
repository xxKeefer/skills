---
name: write-report
description: >
  Write an HTML report: the answer first, then visuals, then rows whose ticks build a prompt. A
  re-run adds a run to the same file. Use when a skill or the user needs an HTML report.
---

# Write Report

A report is one HTML file: [`template.html`](template.html) plus one JSON block that holds every
run. The page builds itself from the JSON, so a re-run changes only the JSON.

Write every sentence in the report in Simplified Technical English. Read [`STE.md`](../../STE.md)
before you write, and follow every rule in it.

## Input

The caller gives these:

- `kind`: a short slug for the type of report, such as `review`, `split`, or `qa`.
- `key`: optional. Without it, Step 1 finds it.
- `title`: the report title.
- `skill`: the skill that the prompt runs, with its plugin prefix, such as
  `/engineering:post-review-comments`. Without it, the report has no ticks and no prompt.
- `track`: optional. The ticks that only mark a row, such as `["pass"]`.
- The run: its title, `head`, `meta`, `answer`, `visuals`, `columns`, and `rows`.

## Step 1: Find the path

1. Find `<KEY>`: the ticket key, else `pr-<n>`, else the current branch name with each `/`
   changed to `-`. Outside a git repo, use a kebab-case slug of the topic.
2. Name the file `<kind>_<KEY>.html`. This name replaces the `/write-to-file` naming pattern.
3. Find the folder by the `/write-to-file` folder rule for doctype `report`. When the user's
   instructions give one folder per ticket, use `<KEY>` for it.
4. If the file exists, read it. This run is a re-run.

**Done when:** you have the absolute path, and you know if the file exists.

## Step 2: Build the run JSON

Write the run JSON to a temp file. It holds the top fields and one `run` object, with no `run`
number. The script in Step 3 adds the run number, `path`, `date`, and row IDs. The JSON has this
shape:

```json
{
  "title": "Review of PR #456",
  "skill": "/engineering:post-review-comments",
  "run": {
    "title": "Panel run",
    "head": "4f2c9e1",
    "meta": { "PR": "#456", "Base": "main" },
    "answer": "Two issues block the merge. Tick the replies to post, then copy the prompt.",
    "visuals": [
      {
        "question": "How many findings does each tier hold?",
        "bars": [["Blocker", 2], ["Major", 3]]
      },
      {
        "question": "Which lanes ran?",
        "fold": true,
        "table": { "columns": ["Lane", "Findings"], "rows": [["correctness", "2"]] }
      },
      {
        "question": "Which modules call the cart?",
        "mermaid": "flowchart LR\n  A[checkout] --> B[cart]"
      }
    ],
    "columns": [
      { "key": "tier", "label": "Tier" },
      { "key": "where", "label": "Where", "mono": true },
      { "key": "issue", "label": "Issue" },
      { "key": "draft", "label": "Draft reply", "fold": true }
    ],
    "rows": [
      {
        "ticks": ["reply"],
        "cells": { "tier": "Blocker", "where": "src/cart.ts:42", "issue": "...", "draft": "..." }
      }
    ]
  }
}
```

Follow these rules:

- **Runs.** The script gives a new file one run, number 1. On a re-run, it gives the new run the
  highest earlier `run` plus 1, puts it first, and keeps each earlier run exactly as it is. It
  never drops a run.
- **Head.** `head` is the commit that the run looked at. The caller gives it, else use
  `git rev-parse --short HEAD`. Two runs can have the same head.
- **Top fields.** Set `title` and `skill` from this call. The script sets `path` to the absolute
  path from Step 1, and the prompt names it.
- **Date.** The script sets `date` to today when the run has none.
- **Answer.** One or two sentences: the verdict, and what the user does next.
- **Visuals.** The user decides from the picture, not from the text. A run with rows needs at
  least one visual with no `fold`, before the rows, and `check_report.py` fails a run without
  one. Each visual answers one question. Write that question in `question`. Leave out a visual
  that answers no question that the user has. Use one of these types:
  - `mermaid` for graphs and flows.
  - `bars` for counts, as `[label, count]` pairs.
  - `table` for a small table of plain text.
  - `html` for inline SVG or hand-made CSS, when no other type fits. Tailwind classes work. The
    page is dark: use `text-paper` for text, `bg-slab` for a panel, and `mag` for the accent.
- **Fold.** Set `fold` on a visual that the user checks only sometimes, such as a long table.
  The page then shows only its question, and a click opens it. Do not fold a `mermaid` visual,
  because Mermaid can draw a closed graph at the wrong size.
- **Rows.** Give one row to each item that the user can act on. The script gives each row with no
  `id` the ID `r<run>.<n>`, with `<n>` from 1 in row order, such as `r2.3`. `columns` gives each
  `key` and `label`. Set `mono` for code, such as `file:line`. Set `fold` for long text, such as
  a draft reply. `cells` maps each column key to plain text. Keep each cell that has no `fold`
  to about 25 words, and move the rest into a column with `fold`.
- **Ticks.** `ticks` lists the actions that the user can tick for the row, such as `["reply"]`
  or `["fix", "reply", "resolve"]`. A row with no ticks gets no checkbox and no note field.
- **Track.** The top-level `track` lists the ticks that only mark a row for the user, such as
  `["pass"]`. A tick in `track` shows a checkbox, but it adds nothing to the prompt.

**Done when:** the temp file holds the top fields and the new run.

## Step 3: Write the file

1. Run `python3 $SKILL_DIR/scripts/write_report.py <path> <json>`. `$SKILL_DIR` is this skill's
   base directory. `<path>` is the absolute path from Step 1. `<json>` is the temp file from
   Step 2. The script does these things:
   - It copies `template.html` with no change, except the `runs` block. On a re-run, it writes
     the whole file again from the current template.
   - It writes `</` as `<\/` in the JSON, so a `</script>` in the data does not close the block.
   - It writes `reports.js` in the same folder. The file lists each `.html` file there, this
     report included, newest first, in this form: `window.REPORTS = ["a.html", "b.html"];`. The
     page shows the other names as links in a fold at the top. A browser cannot list a local
     folder, so the page reads this file instead.
   - It prints the `file://` URL of the report.

   If the script exits 1, read its message, fix the temp file, and run it again. Put no HTML
   comment in a string.
2. Run `python3 $SKILL_DIR/scripts/check_report.py <path>`. It prints `ok` and exits 0, or prints
   one line for each error in the `runs` block, with a fix, and exits 1. On exit 1, fix the temp
   file, and run both scripts again.
3. Return the `file://` URL that the script printed, not a bare path. A caller shows this URL to
   the user, because an editor opens a bare path.

**Done when:** both scripts exit 0, and you return the `file://` URL.

## The prompt

The page shows the answer first, then the visuals, then the rows, for each run, newest run first.
A box at the bottom of the page holds the prompt that the ticks build, with a copy button. The
report saves no tick, because the prompt is the output. The prompt has this form:

```text
/engineering:post-review-comments @/abs/path/to/review_pr-456.html r2.1 r2.3:fix+reply
Notes:
- r2.3: Keep the old name.
```

- An ID stands alone when its row has one tick that is not in `track`. Else a colon follows the ID, then the ticked
  actions joined with `+`.
- The Notes list holds each ticked row that has a note.

The skill that the prompt runs reads each ticked row, and the run that holds it, from the JSON
block.
