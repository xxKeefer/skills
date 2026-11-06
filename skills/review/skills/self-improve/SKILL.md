---
name: self-improve
description: Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put every proposal to you in one table, apply the approved persona edits through update-personas, and write a report and the repo's defect hotspots.
disable-model-invocation: true
argument-hint: "[--since <YYYY-MM-DD>] [--until <YYYY-MM-DD>]"
---

# self-improve: learn from history, then sharpen the reviewers

The review panel learns from four records: the defects that the repo's fixes and its tracker
bugs corrected, what its reviewers keep asking for, what its CI keeps catching, and the signals
that `mob-review` Step 7 wrote to the calibration backlog. This skill mines each record that the
repo has, puts each proposal to you in one table, and changes only what you approve. It never
commits. It also writes the repo's defect hotspots, which `start-ticket` and `persona-test-design`
read when they plan or review a test.

Run it from inside the repo to mine. `$SKILL_DIR/..` is this domain's `skills/` folder.

## State

Machine files live outside every repo:

```bash
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/self-improve"
BACKLOG="$STATE_ROOT/improve-personas.md"
REPO_DIR="$STATE_ROOT/<repo key>"
```

`$REPO_DIR/state.json` holds `lastRunAt` (ISO 8601, UTC), `window` (`<start>..<end>`), `sources`
(each source name, with `ran` or `skipped: <reason>`), and `tracker` (the tracker and its query, or
`"none"`). A missing or unparseable file means "never run". The backlog sits in the state root, because the personas serve every repo. Its entry
format is in `$SKILL_DIR/../mob-review/SKILL.md` Step 7.

`$CACHE` is `$REPO_DIR/cache/<window start>--<window end>`. It holds the defect, review, and CI
data of one window. `$REPO_DIR/themes.json` holds the review and CI themes of the last run, so the
next run can compare its rates with them. `$REPO_DIR/classified.jsonl` holds the class of each
defect of the last 12 months, so a run classifies only new ones. `$REPO_DIR/defect-hotspots.md` is
the hotspots file.

## Step 1: Resolve the repo and the window

1. Find the repo root with `git rev-parse --show-toplevel`. Outside a git repo, stop.
2. Get the repo key. Parse `<owner>/<repo>` from `git remote get-url origin`, and use
   `<owner>--<repo>`. With no `origin`, use `local--<folder name>`, where the folder is the parent
   of `git rev-parse --path-format=absolute --git-common-dir`. That folder is the main worktree,
   so each linked worktree gets the same key.
3. Decide whether the repo is yours. It is yours when it has no `origin`, or when `<owner>` matches
   `gh api user --jq .login`. Without `gh`, ask.
4. Set the window. The end is `--until` from `$ARGUMENTS`, else now. The start is `--since`, else
   `lastRunAt` from `state.json`, else 90 days before the end.
5. Print the repo key, whether the repo is yours, and the window.

**Done when:** you printed the repo key, the owner result, and the window.

## Step 2: Run each source

A source runs only when the repo has data for it. Record each source as run, or as skipped with
the reason. The report lists both.

| Source | Runs when | How |
|---|---|---|
| Fix commits | 5 or more fix commits in the window (`fixCommitsInWindow`) | [`references/defect-mining.md`](references/defect-mining.md) |
| Tracker bugs | A tracker is set, and 5 or more of its bugs in the window trace to a commit (`trackerInWindow`) | The same file |
| Defect hotspots | The bug list of the last 12 months has an item | The same file |
| Review threads | 20 or more review threads on the PRs merged in the window | [`references/review-mining.md`](references/review-mining.md): fetch, then mine the chunks |
| Failed CI runs | 5 or more failed runs in the window | The same file: fetch, then draft the CI themes |
| Calibration backlog | `$BACKLOG` has an entry with `Status: open` | Each `open` entry is a Step 4 row as it is |

The three defect rows share one trace and one classification. The two GitHub sources share one
fetch, and each ends with the rating command in `review-mining.md`.

**Done when:** each source has a result: themes, open entries, the hotspots file, or a skip reason.

## Step 3: Route each theme

A defect theme is two or more real fixes of one kind of defect (`defect-mining.md` section 6). A
review or CI theme is one that the rating marks `floor: true`. Give each theme one route. Find the
lane that owns a check in the panel table of `$SKILL_DIR/../mob-review/SKILL.md`.

| Theme | Route | On yes |
|---|---|---|
| General, and a reviewer can check it on a changed line | Persona rule, in the lane that owns it | The backlog entry goes to `approved`, and Step 5 applies it |
| General, and no changed line shows it | A rule in the `install-rules` sources | Report only: the rule text |
| Specific to this codebase or team | The repo's `CLAUDE.md`, `AGENTS.md`, or lint config | Your repo: Step 5 makes the edit. Another repo: report only |
| Checkable on a changed line, and no lane owns it | Candidate new lane | Report only |
| A bot theme that is mostly ignored | Narrow or remove the persona rule that checks the same thing. With no such rule, report only | The backlog entry goes to `approved`, and Step 5 applies it |
| A flaky CI theme | The job and the step that flake | Report only |

Before you route a theme to the lint config, read that config. If a rule there covers the theme,
propose only to turn that rule on.

Then write each persona-rule theme into the backlog:

- A `rejected` entry names the same target and problem: drop the theme.
- Another entry names the same target and problem: add this run's Evidence line to it.
- No entry names them: append an entry in the `mob-review` Step 7 format, with `Status: open`
  and the source as the Signal (`fix commits`, `tracker bugs`, `review threads`, or `CI runs`). The Evidence line
  names the repo key and the commits, threads, or runs.

Write the Edit line in general words, with no names, paths, keys, URLs, or counts, because it
becomes rule text in a shared repo. The specifics stay in the Evidence line and the report.

**Done when:** each theme has one route, and each persona-rule theme is a backlog entry.

## Step 4: Put every proposal to you

Print one table, with one row for each open backlog entry and each theme, numbered from 1:

| # | Source | Target | Route | Proposal | Evidence |
|---|---|---|---|---|---|

- Source: `backlog`, `fix commits`, `tracker bugs`, `review threads`, or `CI runs`.
- Target: a persona, `mob-review`, `install-rules`, a repo file, or `new lane`.
- Proposal: the Edit line, or the rule text.
- Evidence: the count of items and one short example. For a review theme, add how many threads
  changed. For a review or CI theme, add the trend.

Then ask once: "Name the rows to approve and the rows to reject. A row that you do not name stays
open." For a report-only row, the report records your answer and nothing else changes.

**Done when:** each row is approved, rejected, or left open by your answer.

## Step 5: Apply your answers

1. In `$BACKLOG`, set the Status of each named backlog row to `approved` or `rejected`.
2. If any entry is now `approved`, invoke `/review:update-personas backlog`. It applies each
   approved entry, lints each persona that it changed, and runs the scrub check.
3. For each approved row whose target is a file in your repo, make the edit, then show the diff.
4. Leave every change uncommitted.

**Done when:** each approved row is applied, or is report only, and `update-personas` printed its
table.

## Step 6: Write the report

Write one note through `/write-to-file`, with doctype `report` and the file name
`<repo>-<YYYY-MM-DD>.md`, where `<repo>` is the repo name. If that file exists, add `-2`, `-3`, and
so on. The folder, and any frontmatter fields for reports, come from the user's instructions.

Frontmatter: `repo` (the repo key), `window`, and `sources` (the Step 2 results), plus the fields
that the user's instructions name.

The body, in this order:

1. **Summary**, six lines or fewer: the top themes, the rising and declining themes, the rows
   still open, the skipped sources, and the hotspots coverage with any Skewed line.
2. **Proposals**: the Step 4 table with each answer, and what Step 5 changed.
3. **Themes**: each theme with its route, its trend, and its items: commits (short SHA and
   subject), thread links, or run links. Then the dropped themes.
4. **Hotspots**: the path of `defect-hotspots.md`, its Source and Coverage lines, its first five
   areas, and each area where fewer than half the fixes changed a test.
5. **Below the floor**: each real fix that is in no theme, and each review or CI theme under the
   floor, one line each.

The report can name the repo, its files, its commits, and its PRs, because it stays out of the
shared repo.

**Done when:** the note exists at the path that `/write-to-file` reported.

## Step 7: Save the state and return

If a GitHub source ran, copy `$CACHE/themes.json` to `$REPO_DIR/themes.json`. Then write
`$REPO_DIR/state.json` with `lastRunAt` set to the window end, the window, the sources, and the
tracker. Write
it last, so that a run that stops early mines the same window again.

Print the report path, the count of rows approved, rejected, and open, and the files that changed in
each checkout.

**Done when:** `state.json` holds this run's window end, and you printed the report path.
