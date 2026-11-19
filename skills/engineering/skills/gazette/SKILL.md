---
name: gazette
description: "Print a one-page HTML newspaper for a time window: your action items, repo news, the board, and CI."
disable-model-invocation: true
argument-hint: "[time-period] [repo paths...] [board=<query>]"
---

# Gazette

Join `/engineering:stand-up` and `/engineering:codebase-news` into one newspaper page. The front
page answers "what do I do today", and the inside pages answer "what happened around me".

`$SKILL_DIR` is this skill's base directory. The page is [`template.html`](template.html). The
check is `$SKILL_DIR/scripts/check_gazette.py`.

> **Tools:** use the tracker and the code host that the repo's `## Agent skills` block names, else
> the ones in the user's `## Tools on this machine` block, else ask. Read the tracker notes file
> that the block names for the query forms and the ticket URL form. When a role has no tool, skip
> its section, and say so in the classifieds.

## Step 1: Resolve the edition

1. Read `~/.claude/gazette.md` if it exists. Its layout is in
   [`config.example.md`](config.example.md).
2. Let each argument override its config line: a time period, repo paths, `board=<query>`.
3. Defaults: the window is the last 24 hours. The repos are the current repo. The paper name is
   "The Daily Commit". With no board, skip the board section.
4. Read the ticket URL form from the tracker notes. Each reporter brief gives it, so that each
   ticket link uses it.

**Done when:** you have the window, the list of repo folders, the paper name, the ticket URL form,
and a board query or a note that there is none.

## Step 2: Send the reporters

Start these subagents in parallel. Give each one the window, the ticket URL form, and the return
shape below. Each subagent brief names no model.

1. **Desk reporter:** run `/engineering:stand-up`. Return the tables, the notes, and the bulletin
   as markdown, with every link kept.
2. **Repo reporter**, one per repo folder: in that folder, run `/engineering:codebase-news` with
   the window. Then collect the inputs to Steps 3 and 4. Return:
   - the news paragraph and the table, with each ticket key and PR as a link;
   - each PR that merged in the window: number, URL, title, author, merge commit, lines added and
     removed. With GitHub:
     `gh pr list -R <owner/repo> --state merged --search "merged:>=<start date>" --json number,url,title,author,mergeCommit,additions,deletions`;
   - the CI runs on the default branch in the window, and in the window of the same length before
     it, one workflow at a time, so that a busy workflow cannot push the others past the limit.
     With GitHub, list the workflows with `gh workflow list -R <owner/repo> --json name`, then for
     each one:
     `gh run list -R <owner/repo> --workflow "<name>" --branch <default> --created "<start>..<end>" --limit 200 --json name,conclusion,createdAt,updatedAt,url`.
     When a call returns 200 runs, say that its count is a lower bound;
   - each metric line from the config for this repo, with the number that its command gives.
3. **Board reporter:** run the board query for the tickets whose status changed in the window.
   Return each ticket's key, URL, summary, assignee, old status, and new status.

**Done when:** each reporter returned, or you have a note for each one that failed.

## Step 3: Read the CI weather

For each repo, and for each window:

- Pass rate: successful runs divided by the runs that succeeded, failed, or timed out. Cancelled
  and skipped runs do not count.
- Median duration of each workflow: `updatedAt` minus `createdAt`. Build time and test time come
  from the workflows that the config's `workflows` line names. Without that line, use the
  workflows whose names hold `build` or `test`. With neither, write "not recorded", and show the
  median of each workflow that ran in the window.
- The forecast from the pass rate: ☀️ Sunny at 95% or more, ⛅ Cloudy from 80% to 94%, ⛈️ Storm
  below 80%. With fewer than five runs, the forecast is "No reading".
- The trend: an arrow from the earlier window to this one, for the pass rate and each duration.
- A metric from the config, such as bundle size, gets its number and its trend. A metric that the
  repo does not record is "not recorded", never a guess.

Give each number its run count, such as `92% of 38 runs`. Link the most recent failed run.

**Done when:** each repo has a forecast, or "No reading", and each number has its count.

## Step 4: Pick the honour roll

Name an engineer when a PR of theirs that merged in the window meets one of these:

- It fixed a check that failed or flaked on the default branch.
- It cut a CI duration or a config metric, which the Step 3 trend shows.
- It landed a breaking change together with its migration across the callers.
- It removed at least 300 more lines than it added.
- It closed the last open ticket of an epic.

Give each entry the name, one sentence on the change, and the PR link. The roll holds at most five
entries, the largest effect first. With no entry, write "No callouts this edition."

**Done when:** each entry has a rule from the list above and a link.

## Step 5: Lay out the page

Copy `template.html`, and replace each `{{placeholder}}` with HTML. Use only the template's
classes. The page holds no inline style.

| Placeholder | Content |
| --- | --- |
| `paper_name`, `date`, `window`, `edition`, `repos_covered` | From Step 1. The edition is the date in words, such as "Thursday edition" |
| `lead_*` | The biggest story of all sources: a breaking change, a storm, a release, or the first item of the bulletin's suggested order. A headline, a one-line standfirst, and two to four paragraphs |
| `breaking_box` | `<div class="box breaking"><h3>Breaking</h3>…</div>` for each breaking change, with its migration. Empty when there is none |
| `weather_body` | A table with one row per repo: the forecast, the pass rate, the build time, the test time, each metric, and the trends |
| `your_desk_body` | An `<ol>`, one `<li>` per stand-up row, in the bulletin's suggested order. Start each item with `<span class="tag">TYPE</span>`. Then the bulletin as prose. The stand-up refers to its rows as `#<n>`, which reads as a PR number. Name the PR or the ticket instead |
| `around_the_repos_body` | One `<article>` per codebase-news row: `<span class="repo">`, an `<h3>` headline, and the summary. Then each repo's news paragraph |
| `board_body` | The board tickets grouped as Done, Started, New, and Blocked, each with its assignee |
| `honour_roll_body` | The Step 4 roll |
| `classifieds_body` | The stand-up notes, such as worktrees to remove, and each skipped source |
| `colophon` | The sources, the window, and the time of print |

- Each PR, ticket, and commit that the page names is a link, with `target="_blank"` and
  `rel="noopener"`.
- Write in plain prose with newspaper headlines. Facts only. Each cell traces to a reporter's
  return.

**Done when:** each stand-up row, each codebase-news row, and each board ticket is on the page, and
no placeholder is left.

## Step 6: Print

1. Find the folder by the `/write-to-file` folder rule for doctype `report`, with `gazette` as the
   key.
2. Write the page to `gazette_<YYYY-MM-DD>.html` in that folder.
3. Run `python3 $SKILL_DIR/scripts/check_gazette.py <path>`. On exit 1, fix each line that it
   names, and run it again.
4. Open the page in the default browser.
5. Reply with the path and the lead headline.

**Done when:** the check prints `ok`, and the user has the path.
