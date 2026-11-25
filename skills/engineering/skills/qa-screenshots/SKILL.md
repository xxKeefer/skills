---
name: qa-screenshots
description: >
  Run a happy-path QA checklist in your own browser, save a screenshot for each item, show them in
  the QA report, and append a Manual QA section to the PR. Use when the user says "qa screenshots",
  or asks to run the QA checklist in the browser.
---

# QA Screenshots

Turn a `/engineering:happy-path` checklist into screenshot evidence on the PR. Every write to a
shared environment is one that the user approved.

> **Tools:** the browser is the tool that the user's `## Tools on this machine` block names. It
> must drive the user's own signed-in browser. Read its notes file, if the block names one, for how
> to reach the right tab, take a screenshot, and save it to disk. The code host is GitHub, through
> `gh`. If either tool is missing, stop and say which one.

`$SKILL_DIR` is this skill's base directory.

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

Work in the tab from Step 2. Run `python3 $SKILL_DIR/../verify/scripts/find_drivers.py --repo <repo root> --base <base>`. The base is the base branch of the PR or the plan, else the default branch of the repo. When it prints a
driver path, read the feature map of that driver for the user path to each screen, and drive the screens in this tab. Do not run `/verify` here: it drives its own
instance, not your tab. With no driver, use the browser flow below.

- **Sign-in or device check:** stop and tell the user. Use no other browser, and do not go around
  it.
- **Flag change:** use a local override that changes this browser only, if the project or the
  browser notes name one. Record the old value before you write, and put it back after the item.
  Change a real flag only when the user approved it.
- **Stale page:** after a new push, check one changed string first. If the page still shows the
  old text, hard-reload the tab.
- **Two kinds of capture.** A check is a small capture that shows you the state. A keeper is the
  evidence for the PR: full size, cropped to the content area, and saved to disk. Never use a check
  as a keeper. The browser notes say how to take each kind.
- **Keeper:** wait until the page shows the result of the last action, because an early capture
  shows the state before it. Move the mouse off the page, and close any panel that covers the
  subject. Save it as a PNG at `<report folder>/screenshots/<nn>-<slug>.png`. An item with two
  states gets `<nn>a` and `<nn>b`. Keep checks out of that folder.
- **Short-lived state** (a skeleton, a spinner): try once. If the capture misses it, capture the end
  state and record the miss.
- **Result differs from the checklist:** before you call it a fail, compare it with the default
  branch, and read the AC that the item proves. A result that matches the default branch and meets
  the AC is a pass, and the checklist text is out of date. Report each fail with four parts: the
  AC, the verdict on that AC, the cause, and the fix.
- **Cannot do** (such as blocking a request in developer tools): skip it and record why.

Record each write as you make it: what, which record, and which item.

Read the pixel width of each keeper. A keeper under 1200 px wide is too small to read on the PR,
so retake it.

**Done when:** each item has a keeper of 1200 px or more, or a recorded skip reason, and each flag
override has its old value again.

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
report. Under each heading, put one image reference for each keeper, with the heading as its alt
text. Put a line of evidence under a heading only where the screenshot alone does not prove the
item.

```markdown
<details>
<summary>Manual QA</summary>

#### 1. <heading>

![1. <heading>](./01-<slug>.png)

</details>
```

Write the new body, the old body and then this section, to `<report folder>/screenshots/body.md`,
so that each `./` path resolves to its keeper.

Show the draft, the skipped items with their reasons, the findings, and every write. **Wait for a
yes.**

## Step 6: Update the PR

1. Run `gh pr edit --help`. If it lists `--attach`, upload the keepers with the body in one call,
   from the screenshots folder. Give one `--attach` for each keeper:
   `gh pr edit <n> --body-file body.md --attach './01-<slug>.png#1. <heading>'`.
   gh rewrites each `./` reference to the uploaded image.
2. Read the body back. Count the `user-attachments` image URLs. Each keeper must appear once. A
   multi-file upload can skip a file, and gh exits non-zero when one upload fails. For each `./`
   reference that is left, save the read-back body to `body.md`, and run the command again with
   only that file.
3. If gh has no `--attach`, say that a newer gh uploads the images. Try to open the PR in the
   browser, and paste each image under its heading. If the page does not open, change each image
   reference to `_Screenshot: drag in <file>._`, and append the section with
   `gh pr edit <n> --body-file`.
4. Check that the old body is an unchanged prefix of the new one.

**Done when:** the prefix check passes, and each keeper is an uploaded image or a drag-in line.
Report the PR link, and any files to drag in, in heading order.
