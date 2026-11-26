---
name: gazette
description: >
  Print a one-page HTML newspaper for a time window: your action items, the news of each repo and
  each part of it, each board with its sprint progress, a person filter, the CI weather, and an
  honour roll. Use when the user says "gazette" or "newspaper", or
  wants their day and the repos' news on one page.
argument-hint: "[time-period] [repo paths...] [board <id>...] [accent=<colour>]"
---

# Gazette

Join `/engineering:stand-up` and `/engineering:codebase-news` into one newspaper page. The front
page answers "what do I do today", and the inside pages answer "what happened around me".

`$SKILL_DIR` is this skill's base directory. The page is [`template.html`](template.html). The
check is `$SKILL_DIR/scripts/check_gazette.py`. The sprint progress bar comes from
`$SKILL_DIR/scripts/sprint_progress.py`.

> **Tools:** use the tracker and the code host that the repo's `## Agent skills` block names, else
> the ones in the user's `## Tools on this machine` block, else ask. Read the tracker notes file
> that the block names for the query forms and the ticket URL form. When a role has no tool, skip
> its section, and say so in the classifieds.

## Step 1: Resolve the edition

1. Read `~/.claude/gazette.md` if it exists. Its layout is in
   [`config.example.md`](config.example.md).
2. Let each argument override its config line: a time period, repo paths, `board <id>`, and
   `accent=<colour>`, such as `36hrs board 42`. `board <id>` can come more than once, such as
   `board 42 board 57`.
3. Defaults: the window is the last 24 hours. The repos are the current repo. The paper name is
   "The Daily Commit". The accent is red, `#d0021b`. With no board, skip the board reporters and
   the sprints. The check needs the board section, so it holds one line.
4. Read the ticket URL form from the tracker notes. Each reporter brief gives it, so that each
   ticket link uses it.
5. Split each repo folder into news units. A news unit is a part of the repo that a reader
   follows on its own. Pick the split that fits the shape of the repo:
   - A workspace config, such as `pnpm-workspace.yaml`, the `workspaces` key of `package.json`,
     `nx.json`, a `Cargo.toml` workspace, or `go.work`, lists the apps and libs. Each one can be a
     unit.
   - With no workspace, read the folders and the recent commits. Group by top-level folder, by
     service, or by theme, such as `services/billing`, the docs, or the CI and infra files.
   - A unit can hold several folders. Join small parts that change together into one themed unit.

   Give each unit a short name and its paths as git pathspecs. When the units leave part of the
   repo out, add one unit for the rest: its paths are `.` and `:(exclude)<path>` for each path of
   the other units. A small repo, or a repo with no clear parts, is one unit.
6. In each repo folder, find `<default>`: run `git symbolic-ref --short refs/remotes/origin/HEAD`,
   and remove the `origin/` prefix. Fetch it with `git fetch origin <default>`.
7. Drop each unit with no commit in the window on the default branch:
   `git log -1 --since=<start> --until=<end> origin/<default> -- <paths>` prints nothing.

**Done when:** you have the window, the list of repo folders, the news units with a commit in the
window, the paper name, the accent, the ticket URL form, and the board IDs or a note that there is
none.

## Step 2: Send the reporters

Start these subagents in parallel. Give each one the window, the ticket URL form, and the return
shape below. Each subagent brief names no model.

1. **Desk reporter:** run `/engineering:stand-up`. Return the tables, the notes, and the bulletin
   as markdown, with every link kept.
2. **News reporter**, one per news unit: in its repo folder, run
   `/engineering:codebase-news` with the window and the unit's paths. Return the unit name, the
   news paragraph, and the table, with each ticket key and PR as a link.
3. **Repo reporter**, one per repo folder: collect the inputs to Steps 3 and 5. Return:
   - each PR that merged in the window: number, URL, title, author, merge commit, lines added and
     removed. With GitHub:
     `gh pr list -R <owner/repo> --state merged --search "merged:<start>..<end>" --limit 200 --json number,url,title,author,mergeCommit,additions,deletions`.
     Give `<start>` and `<end>` as UTC timestamps, such as `2026-11-19T09:00:00Z`. When the call
     returns 200 PRs, say that the list is a lower bound;
   - the CI runs on the default branch in the window, and in the window of the same length before
     it, one workflow at a time, so that a busy workflow cannot push the others past the limit.
     With GitHub, list the workflows with `gh workflow list -R <owner/repo> --json name`, then for
     each one:
     `gh run list -R <owner/repo> --workflow "<name>" --branch <default> --created "<start>..<end>" --status completed --limit 200 --json name,conclusion,createdAt,updatedAt,url`.
     When a call returns 200 runs, say that its count is a lower bound;
   - each metric line from the config for this repo, with the number that its command gives.
4. **Board reporter**, one per board ID: through the tracker, find two sets of tickets on that
   board: each ticket whose status changed in the window, and each ticket in the current iteration
   that is in progress or in review. Return each ticket's key, URL, summary, assignee, old status, and new status. For a
   ticket in a review status, also find its open PR on the code host, such as with
   `gh pr list -R <owner/repo> --search "<KEY>" --json number,url`, and return the PR URL.
   Then read the board's current iteration and the board's columns. The tracker notes name the
   iteration field, the estimate field, and the board tools. Return the board name, and the
   iteration's name, goal, start date, and end date. For each ticket in the iteration, return the
   key, URL, summary, assignee, epic, estimate, whether it is a sub-task, and its bucket from its
   board column: `todo` for the first column, `done` for the last column, and `progress` for each
   other column. With no current iteration, say so.

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

## Step 4: Read each sprint

Do this step for each board whose reporter found a current iteration.

1. Split the goal into its items, one per line or sentence. For each item, find its tickets: the
   tickets that it names, the tickets of the epic that it names, and the tickets whose summary is
   on its subject. Give the item its done estimate out of its total, such as `8 of 13 points`. An
   item with no ticket gets "No tickets match this goal".
2. Draw the progress bar. Pipe this JSON to `python3 $SKILL_DIR/scripts/sprint_progress.py`, with
   one entry for each ticket of the iteration, and keep the HTML that it prints:

   ```json
   {"tickets": [{"points": <n or null>, "bucket": "done | progress | todo", "subtask": <true or false>}]}
   ```

   The script counts estimates by board column, as a tracker's sprint progress does: it leaves out
   sub-tasks, and counts tickets when no ticket has an estimate.
3. Compare the done share with the elapsed share of the iteration: on track when the done share is
   the same or more, else behind by the difference, such as "18% behind".

**Done when:** each goal item has a count or "No tickets match this goal", and the progress bar
and the on-track line come from the reporter's return.

## Step 5: Pick the honour roll

Name an engineer when a PR of theirs that merged in the window meets one of these:

- It fixed a check that failed or flaked on the default branch.
- It cut a CI duration or a config metric, which the Step 3 trend shows.
- It landed a breaking change together with its migration across the callers.
- It removed at least 300 more lines than it added.
- It closed the last open ticket of an epic.

Give each entry the name, one sentence on the change, and the PR link. The roll holds at most five
entries, the largest effect first. With no entry, write "No callouts this edition."

**Done when:** each entry has a rule from the list above and a link.

## Step 6: Lay out the page

Copy `template.html`, and replace each `{{placeholder}}` with HTML. Use only the template's
classes. The page holds no inline style.

| Placeholder | Content |
| --- | --- |
| `paper_name`, `date`, `window`, `edition`, `repos_covered` | From Step 1. The edition is the date in words, such as "Thursday edition" |
| `accent` | The accent from Step 1, as a CSS colour. It colours the tags, the Breaking box, and a storm |
| `lead_*` | The biggest story of all sources: a breaking change, a storm, a release, or the first item of the bulletin's suggested order. A headline, a one-line standfirst, and two to four paragraphs |
| `breaking_box` | `<div class="box breaking"><h3>Breaking</h3>…</div>` for each breaking change, with its migration. Empty when there is none |
| `weather_body` | A table with one row per repo: the forecast, the pass rate, the build time, the test time, each metric, and the trends |
| `your_desk_lede` | The bulletin in one or two sentences: what to do first, and why. Plain text |
| `your_desk_body` | Groups of cards, one card per stand-up row, in the bulletin's suggested order. The stand-up refers to its rows as `#<n>`, which reads as a PR number. Name the PR or the ticket instead |
| `around_the_repos_body` | Groups of cards, one card per codebase-news row, with the news unit as the label. Then each unit's news paragraph, after an `<h4>` with the unit name |
| `sprint_body` | One `<div class="sprint"><div class="box"><h3>Sprint goal</h3>…</div><div class="box"><h3>Sprint progress</h3>…</div></div>` for each board, in argument order. The goal box names the board, the iteration, and its end date, gives the on-track line, and lists each goal item with its count. The progress box holds the HTML from Step 4. A board with no current iteration gets `<p>No current sprint on <board name>.</p>` |
| `board_people_options` | One `<option>` for each person on a card of any board, in name order, then `<option>Unassigned</option>` when a card has no assignee |
| `board_body` | Groups of cards, one card per board ticket, in the order Done, Started, In progress, New, then Blocked. A ticket on two boards gets one card. The label is the status and the assignee, then the board name when the page has more than one board. Each card is `<article data-person="<assignee>">`, with the same name as its `<option>`, or `Unassigned` |
| `honour_roll_body` | The Step 5 roll |
| `classifieds_body` | The stand-up notes, such as worktrees to remove, and each skipped source |
| `colophon` | The sources, the window, and the time of print |

- A card is `<article><span class="label">LABEL</span><h4>headline</h4><p>description</p></article>`.
  A Your desk card is an action item: write it as `<article class="action">`, and start it with
  `<input type="checkbox" class="done" aria-label="Done: <headline>">`. The box is only a visual
  cue. A tick dims the card, and nothing saves it.
  The label is a few words, such as the row type and the repo. The headline names the PR or the
  ticket. The description says in one or two sentences what changed or what to do.
- Group the cards in Your desk, Around the repos, and the board by theme: what they share, such as
  an epic, a goal, a kind of work, or a part of the code. Each group is
  `<div class="group"><h3 class="tagline">tagline</h3>cards</div>`, and the headline of each card
  in it is an `<h4>`.

  - The tagline is one descriptive line that says what the cards add up to, such as "Three reviews
    wait on you" or "The forms library grows up". A bare category, such as "Reviews", is not a
    tagline.
  - A group holds two or more cards. A card that fits no group goes in one last group, such as
    "Also on the desk".
  - Keep the order of the cards inside a group. Order the groups by their first card.
- Each PR, ticket, and commit that the page names is a link, with `target="_blank"` and
  `rel="noopener"`.
- A card about a review, such as a review request, a review to address, or a ticket in a review
  status, links its headline to the PR on the code host, and puts "review" in its label. The
  reviewer acts on the PR, not the ticket. Link the ticket in the description. When no PR exists,
  link the headline to the ticket.
- Write in plain prose with newspaper headlines. Facts only. Each cell traces to a reporter's
  return.

- The person filter hides each board card of another person. A group with no card left shows
  "<person> is not working on this." The template's script does both, so write no empty state.

**Done when:** each stand-up row, each codebase-news row, and each board ticket is on the page, and
no placeholder is left.

## Step 7: Print

1. Find the folder by the `/write-to-file` folder rule for doctype `report`, with `gazette` as the
   key.
2. Write the page to `gazette_<YYYY-MM-DD>.html` in that folder.
3. Run `python3 $SKILL_DIR/scripts/check_gazette.py <path>`. On exit 1, fix each line that it
   names, and run it again.
4. Open the page in the default browser.
5. Reply with the path and the lead headline.

**Done when:** the check prints `ok`, and the user has the path.
