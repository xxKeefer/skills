# Layout

Step 6 of the bulletin skill writes one entry from this file. The entry is HTML for the
`<main id="entries">` section of `template.html`. The template has no placeholder for the entry
body.

An entry has this frame. The `data-date` is today, as `YYYY-MM-DD`:

```html
<article class="entry" data-date="2026-11-24">
  <header class="masthead">
    <div class="dateline">Tuesday 24 November 2026 · Entry 2 of week 48</div>
    <h2>The Obsidian Oracle Bulletin</h2>
  </header>
  <p class="standfirst">One line: what moved since the entry below, or that this is the first entry of the week.</p>
  ...parts...
</article>
```

Each part opens with an `<h3>`. Use these parts in this order.

| Part | Content |
| --- | --- |
| Goals | The lead. A `<table>` for each level with a row for each goal of the year, the month, and the week: the goal, its status as served, not served, or carried, and what changed since the entry below. For the first entry of the week, the change column says "First entry of the week". Then the filled reflections of the window as `<blockquote>` with a `<cite>` that links the note |
| Weather | One `<p class="forecast">` for each place: the label in `<strong>`, then the conditions, the high and low with the unit, and the chance of rain. With `available: false`, "The forecast is not available today." for that place. With no places, "Set a place in the config for a forecast." |
| Events | Today's due items by section, then one `<p>` for each later day of the week with its due items, in date order. A day with none says so. When `errors` is not empty in any run, add one line with the count of rows that cannot be read, and say that `/update-occasions-config` fixes them |
| Chores | A `<table>`: chore, ticked of seen, to date |
| Board | One `<article>` for each project with a move: the project in `<strong>`, then the cards that moved |
| Notes | A `<ul>` with one `<li>` for each note edited in the window, outside the journal |

An empty part keeps its `<h3>` and one line that says it has none.

## Stories

A story is one `<article>` or `<li>` or `<tr>` that carries a `data-id`. Give each goal row, each
board article, and each note item a `data-id`.

- The form is `<section>:<short kebab-case name>`. The sections are `goals`, `weather`, `events`,
  `chores`, `board`, and `notes`.
- A goal takes the journal file name, then a short name of the goal, such as
  `goals:2026-wk48-week:finish-the-quilt`.
- A board story takes the project folder name, such as `board:garden`.
- A note takes its vault path, with `.md`, such as `notes:02-knowledge/soup.md`.
- When a story is the same item as an id in `last_ids`, use that id.
- Each id is unique in the entry. An id holds no space and no `|`: write a space as `%20`.

Mark each story against the latest earlier entry:

- New: `<span class="tag">new</span>`.
- Changed: `<span class="tag">changed</span>`, and say what changed.
- Unchanged: `<span class="tag unchanged">unchanged</span>` and one line. Give no more.

With no earlier entry, mark nothing.

## Rules

- Each note that the entry names is a link: `obsidian://open?vault=<vault folder name>&file=<path
  without .md, URL-encoded>`, with `target="_blank"` and `rel="noopener"`.
- The entry has no class `action`, `choice`, or `comment`. It has no `<select>`, `<textarea>`,
  `<input>`, `<button>`, or `<script>`.
- The entry has no `{{placeholder}}`.
- The page holds no inline style. Use only the classes of the template.
- Write in plain prose. Each fact traces to the scan, a note, or a script.
