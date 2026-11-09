---
name: write-report
description: >
  Write an HTML report through /write-to-file: the answer first, then the visuals, then rows with
  ticks that build a prompt to copy. A re-run adds a run to the same file and keeps every earlier
  run. Model-invocable -- other skills call it for each report that the user reads and ticks. Use
  when a skill or the user needs an HTML report.
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
  `/code-review:post-review-comments`. Without it, the report has no ticks and no prompt.
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

## Step 2: Build the data

The data has this shape:

```json
{
  "title": "Review of PR #456",
  "path": "/abs/path/to/review_pr-456.html",
  "skill": "/code-review:post-review-comments",
  "runs": [
    {
      "run": 2,
      "title": "Panel run",
      "head": "4f2c9e1",
      "date": "2026-11-07",
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
          "id": "r2.1",
          "ticks": ["reply"],
          "cells": { "tier": "Blocker", "where": "src/cart.ts:42", "issue": "...", "draft": "..." }
        }
      ]
    }
  ]
}
```

Follow these rules:

- **Runs.** A new file has one run, number 1. On a re-run, parse the JSON in
  `<script type="application/json" id="runs">`. The new run number is the highest `run` plus 1.
  Put the new run first. Keep each earlier run exactly as it is. Never drop a run.
- **Head.** `head` is the commit that the run looked at. The caller gives it, else use
  `git rev-parse --short HEAD`. Two runs can have the same head.
- **Top fields.** Set `title`, `path`, and `skill` from this call. `path` is the absolute path
  from Step 1, and the prompt names it.
- **Answer.** One to three sentences: the verdict, and what the user does next.
- **Visuals.** Each visual answers one question. Write that question in `question`. Leave out a
  visual that answers no question that the user has. Use one of these types:
  - `mermaid` for graphs and flows.
  - `bars` for counts, as `[label, count]` pairs.
  - `table` for a small table of plain text.
  - `html` for inline SVG or hand-made CSS, when no other type fits. Tailwind classes work.
- **Fold.** Set `fold` on a visual that the user checks only sometimes, such as a long table.
  The page then shows only its question, and a click opens it. Do not fold a `mermaid` visual,
  because Mermaid can draw a closed graph at the wrong size.
- **Rows.** Give one row to each item that the user can act on. A row ID is `r<run>.<n>`, with
  `<n>` from 1 in row order, such as `r2.3`. `columns` gives each `key` and `label`. Set `mono`
  for code, such as `file:line`. Set `fold` for long text, such as a draft reply. `cells` maps
  each column key to plain text.
- **Ticks.** `ticks` lists the actions that the user can tick for the row, such as `["reply"]`
  or `["fix", "reply", "resolve"]`. A row with no ticks gets no checkbox and no note field.
- **Track.** The top-level `track` lists the ticks that only mark a row for the user, such as
  `["pass"]`. A tick in `track` shows a checkbox, but it adds nothing to the prompt.

**Done when:** the data holds the new run first and every earlier run unchanged.

## Step 3: Write the file

1. Copy `template.html` with no change. Replace the content of the `runs` block with the data.
2. In each JSON string, write `</` as `<\/`. This stops a `</script>` in the data from closing
   the block. Put no HTML comment in a string.
3. Write the file with `/write-to-file`, doctype `report`, at the path from Step 1. A re-run
   writes the whole file again from the current template.
4. Read the JSON block back and parse it. If the parse fails, fix the JSON and write the file
   again.
5. Write `reports.js` in the same folder. It lists the name of each `.html` file in the folder,
   this report included, newest first, in this form:

   ```js
   window.REPORTS = ["review_pr-456.html", "qa_pr-456.html"];
   ```

   Write it again each time, because other skills add files to the folder. The page shows the
   other names as links in a fold at the top. A browser cannot list a local folder, so the page
   reads this file instead. A file that you delete stays in the list until the next write.
6. Open the file in the default browser with the OS open command: `open` on macOS, `xdg-open`
   on Linux. If the command fails, go on.
7. Return a `file://` URL of the absolute path, not a bare path. A caller shows this URL to the
   user, because an editor opens a bare path.

**Done when:** the file holds every earlier run and the new run, its JSON block parses,
`reports.js` lists every `.html` file in the folder, and you return the `file://` URL.

## The prompt

The page shows the answer first, then the visuals, then the rows, for each run, newest run first.
A box at the bottom of the page holds the prompt that the ticks build, with a copy button. The
report saves no tick, because the prompt is the output. The prompt has this form:

```text
/code-review:post-review-comments @/abs/path/to/review_pr-456.html r2.1 r2.3:fix+reply
Notes:
- r2.3: Keep the old name.
```

- An ID stands alone when its row has one tick that is not in `track`. Else a colon follows the ID, then the ticked
  actions joined with `+`.
- The Notes list holds each ticked row that has a note.

The skill that the prompt runs reads each ticked row, and the run that holds it, from the JSON
block.
