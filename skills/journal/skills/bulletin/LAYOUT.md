# Layout

Step 6 of the bulletin skill writes one entry from this file. The entry is HTML for the
`<main id="entries">` section of `template.html`. The template has no placeholder for the entry
body.

An entry has this frame. The `data-date` is today, as `YYYY-MM-DD`:

```html
<article class="entry" data-date="2026-11-24">
  <header class="masthead">
    <div class="dateline">Tuesday 24 November 2026 · Entry 2 of week 48</div>
    <h2 id="head-2026-11-24">The Obsidian Oracle Bulletin</h2>
  </header>
  <p class="standfirst">One line: what moved since the entry below, or that this is the first entry of the week.</p>
  <div class="layout">
    <div class="main">
      <section>...</section>
      <section>...</section>
      <section>...</section>
      <section>...</section>
      <section>...</section>
      <section>...</section>
    </div>
    <aside class="side" aria-labelledby="head-2026-11-24">
      <section>...</section>
      <section>...</section>
      <section>...</section>
    </aside>
  </div>
</article>
```

The main column holds six plain `<section>` elements in this order: week, last, next, reflect, board, notes. The side column holds three: weather, events, chores. Each section opens with an `<h3>`. An empty section keeps its `<h3>` and one line that says it has
none. The `id` of the `<h2>` is `head-` and the `data-date`, and the `aside` names it with `aria-labelledby`. Each `<table>` opens with a `<thead>` row of `<th scope="col">` cells, one for each column that the section row names.

## Main column

| Section | Content |
| --- | --- |
| `week` | The lead. A `<table>` with a row for each goal of this week only: the goal, its status as served, not served, or carried, and what changed since the entry below. For the first entry of the week, the change column says "First entry of the week". Add a chart of goals by status. The entry holds no yearly or monthly goal table |
| `last` | How each goal of last week ended: served, not served, or carried. Then a chart of this week against last week, from the numbers that the chart rule names |
| `next` | Marked as a projection in the `<h3>` or the first line. A `<ul>`: the goals that carry over, the events of each day of next week from `occasions.py` in date order (a day with none says so), and the ideas for the week |
| `reflect` | A `<div class="masonry">` of four cards, below |
| `board` | One `<article>` for each project with a move: the project in `<strong>`, then the cards that moved |
| `notes` | A `<ul>` with one `<li>` for each note edited in the window, outside the journal |

### Reflect cards

Each card is `<article class="card" data-card="...">` with an `<h4>` and a `<ul>`. Each `<li>` names
the week of the item (`wk47` or `wk48`) and links its note. A card with no item holds one line that
says it has none. The four cards, in this order:

| `data-card` | Title | Source |
| --- | --- | --- |
| `learning` | Learning | The `What I learned` lines of the dailies |
| `ideas` | Ideas | The `Thoughts and Ideas` section of the dailies |
| `friction` | Friction | `What caused friction` |
| `next` | What's next | `What is next` |

Take the learning, friction, and next items from `reflections` in the scan. Take the ideas from the `Thoughts and Ideas` section of the dailies that Step 4 reads, because `reflections` holds only the `Reflect` sections. Use this week and last week only.

## Side column

| Section | Content |
| --- | --- |
| `weather` | One `<p class="forecast">` for each place: the label in `<strong>`, then the conditions, the high and low with the unit, and the chance of rain. With `available: false`, "The forecast is not available today." for that place. With no places, "Set a place in the config for a forecast." |
| `events` | Today's due items by section. Then one `<p>` for each later day of this week, in date order. A day with none says so. When `errors` is not empty in any run, add one line with the count of rows that cannot be read, and say that `/update-occasions-config` fixes them |
| `chores` | A `<table>`: chore, ticked of seen, since the Monday of last week. The scan counts the whole window. Add a chart of the ticks |

## Charts

Follow the rule of `/show-me`: the smallest visual that makes the point. `/show-me` has no SVG
form, and the page has no script, so write each chart by hand as an inline SVG bar chart in the
shape below.

- A chart appears only when the scan holds its numbers. Draw no chart from a guess.
- Suggested charts, each with its source:
  - goals by status: count the rows of the week table;
  - this week against last week: dailies for each week from `journal.dailies_in_window` by date, and
    notes edited for each week from `recent[].age_days`, where an age at or under the days since
    `week_start` is this week;
  - chore ticks: `journal.checklists`, which covers the whole window;
  - edits by weekday: `activity.weekdays`, which also covers the whole window.
- Each chart is `<figure>` with `<svg class="chart" viewBox="..." role="img" aria-label="...">` and
  a `<figcaption>` that gives the point in one line.
- The `aria-label` says what the chart shows, with its numbers.
- Use classes only, and no `style` attribute. Inside the `<svg>`: `line.axis` for the baseline,
  `text.label` for a category name, `rect.fill-accent` for the bar that makes the point, and
  `rect.fill-muted` for the other bars.
- The entry holds at least one chart.

## Stories

A story is one `<article>`, `<li>`, or `<tr>` that carries a `data-id`. Give each goal
row, each board article, and each note item a `data-id`.

- The form is `<section>:<short kebab-case name>`, where the section is a part of the entry. The sections are `week`, `last`, `next`,
  `reflect`, `weather`, `events`, `chores`, `board`, and `notes`.
- A goal takes the journal file name, then a short name of the goal, such as
  `week:2026-wk48-week:finish-the-quilt`.
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
