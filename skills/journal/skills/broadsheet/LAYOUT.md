# Layout

Step 7 of the broadsheet skill fills `template.html` from this file.

| Placeholder | Content |
| --- | --- |
| `paper_name`, `date`, `window`, `edition` | From Step 1. The window is "The last 7 days". The edition is the ISO week, such as "Week 47 edition" |
| `vault_counts` | Notes in the vault, notes edited in the last 7 days, and dailies written |
| `accent` | The accent from Step 1, as a CSS colour |
| `lead_*` | The week's story from Step 4: a headline, a one-line standfirst, and two to four paragraphs. Name the two-week trends from Step 3 |
| `compass_body` | First, each filled reflection, as a `<blockquote>` with its text and a `<cite>` that links the note and gives its level and date, newest first, grouped by window. Then a `<table>` of the four `compass` rows: window, dailies, edits, chore rate, and busiest folders, with each change since last week's page. The reflections get more space than the table. A window with no filled reflection names none |
| `weather_body` | From `weather.py`, one `<p class="forecast">` for each place: the label of the place in `<strong>`, then the conditions, the high and low with the unit, and the chance of rain. With `available: false`, "The forecast is not available today." for that place. With no places, "Set a place in the config for a forecast." |
| `chores_body` | A table of `journal.checklists`: chore, ticked of seen, and the rate in `<span class="rate">` as a percent. No weather icons. Give a chore seen fewer than three times "Too few days to rate". When `journal.occasions_errors` is not empty, add one line under the table with the count of rows that cannot be read, and say that `/update-occasions-config` fixes them |
| `gaps_body` | The missing days and the broken nav links. A `next` that names a file not yet due is expected, so leave it out |
| `ledger_body` | A table per cascade level, one `<tr class="action">` per goal: goal, served, not served, or carried, and the action |
| `letters_body` | One `<li class="action">` per inbox note, from Step 5 |
| `stale_body` | One `<li class="action">` per Step 5 pick, then the total |
| `morgue_body` | One `<li class="action">` per delete candidate, or the oldest archived notes as plain `<li>`, then the total |
| `editorial_body` | The Step 6 prose, then an `<ol>` with one `<li class="action">` per change |
| `floor_plan_body` | One `<article class="action">` per finding: `<span class="kicker">` with the folder, an `<h4>`, the reason, and the action |
| `honour_roll_body` | Up to three: the longest chore streak, the most-linked new note, and the biggest win of the week |
| `board_body` | One `<article>` per shown project from Step 5: `<span class="kicker">` with the project status, an `<h4>` with the project, and its next card. A status suggestion is an `<article class="action">` |
| `back_pages_body` | One `<article>` per story from Step 5, with `<span class="kicker">` for the folder. Each want list suggestion is an `<li class="action">` in that article |
| `colophon` | `dates_from`, the limits, last week's page or none, and the time of print |

Floor plan, the board, and the back pages print their articles as masonry cards, three columns on
a wide screen. Each card reads as a label, a headline, and one or two sentences.

Group the cards by theme: what they share, such as an epic, a goal, a kind of work, or a part of
the code. Each group is `<div class="group"><h3 class="tagline">tagline</h3>cards</div>`, and the
headline of each card in it is an `<h4>`.

- The tagline is one descriptive line that says what the cards add up to, such as "Three reviews
  wait on you" or "The forms library grows up". A bare category, such as "Reviews", is not a
  tagline.
- A group holds two or more cards. A card that fits no group goes in one last group, such as
  "Also on the desk".
- Keep the order of the cards inside a group. Order the groups by their first card.

Each suggestion row has this shape:

```html
<li class="action" data-id="letters:<inbox folder>/<note>.md">
  <input type="checkbox" class="done" aria-label="Done: Note title">
  <a href="obsidian://open?vault=..." target="_blank" rel="noopener">Note title</a>
  <span class="age">12 days</span> <span class="tag">new</span>
  <strong>Why:</strong> the reason. <strong>Do:</strong> what the action does.
  <select class="choice" aria-label="Choice for Note title"></select>
  <details><summary>Comment</summary><textarea class="comment" aria-label="Comment on Note title"></textarea></details>
</li>
```

- Start each row with the `done` checkbox, in its first cell for a table row. The box is only a
  visual cue. A tick dims the row, and nothing saves it or adds it to a prompt.
- Leave the `<select>` empty. The page script fills it from `data-choices` of the section. Each
  section of the template names its choices and has a `<dl class="legend">` that says what each
  one does there. Keep both as the template has them: a choice with no meaning for a section is
  not in `data-choices`, and the check fails a legend that does not match.
- Mark a new row with `<span class="tag">new</span>`, and a repeat with
  `<span class="age">repeat</span>`. With no page last week, mark nothing.
- The `data-id` is `<section id>:<target>`, so the same suggestion has the same id next week. The
  target is:
  - the vault path of the note, with `.md`, in the letters, stale shelf, and morgue;
  - the vault path of the folder in the floor plan;
  - the project folder name on the board;
  - the want list's vault path, then a short kebab-case name of the item, in the back pages, such
    as `back-pages:<path>.md:the-hobbit`;
  - the journal file name, then a short kebab-case name of the goal, in the ledger, such as
    `the-ledger:2026-wk47-week:finish-the-quilt`;
  - a short kebab-case name of the change in the editorial, such as
    `editorial:shopping-list-above-reflect`.

  When a row is the same suggestion as an id in `last_ids`, use that id. Each id is unique on the
  page: when two rows in one section share a target, add `:<action verb>`. An id holds no space and
  no `|`: write a space in the target as `%20` and a `|` as `%7C`, such as
  `stale-shelf:03-work/old%20plan.md`. Write no other code.
- The kind of a row is `data-prompt` on its section: `vault` or `suite`. A row can override it
  with its own `data-prompt`. Vault rows go in the vault prompt, and suite rows in the suite
  prompt. A suite row can carry `data-relates="<data-id of a vault row>"`, and the prompt then
  names that row. The check fails a relation to a row that is not a vault row on the page.
- Leave out each row whose `data-id` is in `muted` from Step 1. Do not name it on the page.
- The row text never holds ` | comment: `, because `/journal:act-on-broadsheet` splits there.
- Each note that the page names is a link: `obsidian://open?vault=<vault folder name>&file=<path
  without .md, URL-encoded>`, with `target="_blank"` and `rel="noopener"`. The `data-id` holds the
  path, so the row text names the note only by its link.
- Write in plain prose with newspaper headlines. Each fact traces to the scan or to a note.
