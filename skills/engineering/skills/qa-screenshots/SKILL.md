---
name: qa-screenshots
description: Run a happy-path QA checklist in your own browser, save a screenshot for each item, show them in the QA report, and append a Manual QA section to the PR.
disable-model-invocation: true
---

# QA Screenshots

Turn a `/engineering:happy-path` checklist into screenshot evidence on the PR. Every write to a
shared environment is one that the user approved.

> **Tools:** the browser is the tool that the user's `## Tools on this machine` block names. It
> must drive the user's own signed-in browser. Read its notes file, if the block names one, for how
> to reach the right tab, take a screenshot, and save it to disk. The code host is GitHub, through
> `gh`. If either tool is missing, stop and say which one.

**Inputs:** a PR number, or the PR of the current branch. The QA report is the `qa` report that
`/engineering:happy-path` wrote for the branch, in the folder that `/write-to-file` uses for
reports.

## Step 1: Read the checklist

1. Read the JSON block in the QA report. Take the rows of the latest run (`r<run>.<n>`): area, step,
   and expected result.
2. Read the PR body with `gh pr view <n> --json body`.
3. Mark each item that writes data (save, create, link, delete), needs a feature flag change, needs
   data that the test account may lack, or needs the browser's developer tools.

**Done when:** every row is listed with its marks.

## Step 2: Ask before you touch anything

Ask in one `AskUserQuestion`. Each question names its items.

1. Which tab holds the app, and which account it uses.
2. Which marked writes and flag changes are approved. Skip each item that is not approved.
3. For each item that needs missing data: skip it, or use another account.

**Done when:** every marked item has an answer.

## Step 3: Capture

Work in the tab from Step 2.

- **Sign-in or device check:** stop and tell the user. Use no other browser, and do not go around
  it.
- **Flag change:** use a local override that changes this browser only, if the project or the
  browser notes name one. Record the old value before you write, and put it back after the item.
  Change a real flag only when the user approved it.
- **Screenshot:** save it as a PNG at `<report folder>/screenshots/<nn>-<slug>.png`. An item with
  two states gets `<nn>a` and `<nn>b`. Move the mouse off the page first, and close any panel that
  covers the subject.
- **Short-lived state** (a skeleton, a spinner): try once. If the capture misses it, capture the end
  state and record the miss.
- **Text differs from the checklist:** compare the label on the default branch before you call it a
  fail. A label that matches the default branch means that the checklist text is out of date.
- **Cannot do** (such as blocking a request in developer tools): skip it and record why.

Record each write as you make it: what, which record, and which item.

**Done when:** each item has a PNG or a recorded skip reason, and each flag override has its old
value again.

## Step 4: Show the screenshots in the QA report

Write an items file, then run [`add-report-screenshots.py`](add-report-screenshots.py):

```sh
python3 -I add-report-screenshots.py <report.html> <items.json>
```

Each item gets one `<details>` with the item heading as its summary. A skipped item is one plain
line with its reason. The script adds a visual to the latest run. It adds no run and ticks no box.

**Done when:** the script prints the run count and the details count, and the user has the report
path.

## Step 5: Draft the PR section

Use one `####` heading per item, numbered as in the checklist, with the same headings as the
report. Put a line of evidence under a heading only where the screenshot alone does not prove the
item.

```markdown
<details>
<summary>Manual QA</summary>

#### 1. <heading>

_Screenshot: drag in `01-<slug>.png`._

</details>
```

Show the draft, the skipped items with their reasons, the findings, and every write. **Wait for a
yes.**

## Step 6: Update the PR

1. Try to open the PR in the browser. If the page opens, paste each image under its heading in the
   web editor.
2. If the page does not open, keep the placeholder lines. Append the section with
   `gh pr edit <n> --body-file`, and leave every other section as it is.
3. Read the body back. Check that the old body is an unchanged prefix of the new one.

**Done when:** the prefix check passes. Report the PR link and the files to drag in, in heading
order.
