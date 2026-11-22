---
name: update-occasions-config
description: Migrate the vault's occasions.md to the one fixed layout when it is in the old layout, after one yes, then sync it into vault_occasions.js for Templater. Run after you edit occasions.md.
disable-model-invocation: true
---

# Update Occasions Config

Keeps `occasions.md` in the journal directory in the one fixed layout, and generates
`vault_occasions.js` in the vault's Templater scripts directory from it.

`$SKILL_DIR` is this skill's base directory. The occasions script is
`$SKILL_DIR/../../scripts/occasions.py`. The layout is
[templates/occasions.md](../../templates/occasions.md): a `## Daily` list, then one table,
`| Item | When | Section |`, under each of `## Weekly`, `## Yearly`, `## Maintenance`, and
`## One-off`. This skill writes only that layout.

## Step 1: Discover Paths

Find the journal directory with `/discover-vault-directory * holding occasions.md`.
Find the Templater scripts directory with `/discover-vault-directory *meta/scripts`.

## Step 2: Check the Layout

Run the script for today:

```sh
python3 $SKILL_DIR/../../scripts/occasions.py <journal directory>/occasions.md --date <YYYY-MM-DD>
```

The file is in the old layout when the JSON has `old_layout` true: the file has no `## Daily`
heading, or a table has a `Type` or `Date/Rule` column. The old layout has headings such as `## Chores (Daily Default)`,
`## Chores (Day-Specific)`, `## Recurring Events`, `## Home Maintenance`, and
`## One Off Events - YYYY`. When the file is in the old layout, do Step 3. Else go to Step 4.

## Step 3: Migrate

Build the whole file in the new layout. Keep the frontmatter. Put the `%%` comment block of
[templates/occasions.md](../../templates/occasions.md) under the frontmatter, above the first
heading, so the file names the `When` forms. Convert each row:

| Old row | New row |
|---|---|
| A line under `## Chores (Daily Default)` | The same line under `## Daily` |
| `\| Monday \| 🧹 Vacuum \|` under `## Chores (Day-Specific)` | `\| 🧹 Vacuum \| Mon \| chores \|` under `## Weekly` |
| Day `Wednesday (even weeks)`, `Wednesday (odd weeks)` | When `Wed even`, `Wed odd` |
| `Mon DD` or `Nth Day Mon` under `## Recurring Events` | The same When under `## Yearly` |
| `Easter calc`, with Good Friday, Easter Saturday, Easter Sunday, or Easter Monday in the name | When `easter-2`, `easter-1`, `easter`, or `easter+1` |
| `Quarterly`, `Biannual`, or `Annual` with the anchor `Feb 15` under `## Home Maintenance` | When `every 3 months from Feb 15`, `every 6 months from Feb 15`, or `every 12 months from Feb 15`, under `## Maintenance` |
| `Monthly (1st Sun)` | When `1st Sun` |
| `Weekly (Sun)` | When `Sun` |
| `Oct 12` under `## One Off Events - 2026` | When `2026-10-12` under `## One-off` |
| A cell that holds two items split by `<br>` | One row for each item, with the same When and Section |
| A rule with an `am` or `pm` suffix, such as `Jun 19 pm` | The rule without the suffix as When, and the suffix in the item text, such as `🍽 Dinner (pm)` |
| A month written `Sept`, such as `Sept 3` | `Sep 3` |
| A `Type` value other than `event` or `reminder`, such as `PM` | The value in the item text, such as `Board game night (PM)` |

Also:

- Drop the `Type` column and the `Anchor Date` column. Keep `Section`. An empty `Section` stays
  empty, which means `chores`, except under the old one-offs: their old default was `tasks`, so
  write `tasks`.
- A one-off heading with no year: use the current year, and name each of its rows in the report.
- A row that no line of the table converts, such as `Aug (varies)`: keep the row in its new table,
  with its When as written. `occasions.py` then lists it in `errors`, and no row is lost.
- Drop the prose lines that explain the old layout. Keep any other heading and its lines as
  written, and name the heading in the report.

Show the whole migrated file, then the rows that it could not convert, one line each:
`{item}: {old rule}`. Ask one question:

> Write this to `occasions.md`? A copy of the old file goes to `occasions.md.bak`. (`yes` or `no`)

- `yes`: copy the old file to `occasions.md.bak` beside it, then write the migrated file. When
  `occasions.md.bak` exists, use `occasions.md.bak.<YYYY-MM-DD>`, so no backup is lost.
- Any other answer: write nothing, and stop the skill.

Run the script from Step 2 on the new file, and show each row in `errors`:
`line {line}: {row} -- {why}`. When `errors` is empty, say so.

## Step 4: Read the Rows

Run the script from Step 2. Take each line of `daily`, and each table row of the file that is not
in `errors`. List each row in `errors` as skipped in the Step 6 report.

Split each item into `sym` (its first emoji, or empty) and `name` (the rest). For a line of
`daily`, drop the indent and the `- [ ] ` first. A line of `daily` whose text is all bold, such as
`- **Kitchen**`, is a group line: it is not a reminder, so write no entry for it.

## Step 5: Generate vault_occasions.js

Write `<scripts-dir>/vault_occasions.js`. Each `daily` line is
`{ sym, name, type: 'reminder', section: 'chores', test: () => true }`. Each table row is
`{ sym, name, type: 'event', section, test }`, with `section` from the row (`chores` when empty).
Build `test` from the When, so that it gives the same days as `occasions.py`:

| When | `test: (m) =>` |
|---|---|
| `Sun`, `Mon Wed` | `[1, 3].includes(m.day())`, with Sun=0 to Sat=6 |
| `Wed even`, `Wed odd` | `m.day() === 3 && m.isoWeek() % 2 === 0` (odd: `!== 0`) |
| `Jan 5` | `m.month() === 0 && m.date() === Math.min(5, m.daysInMonth())` |
| `2nd Sun May`, `1st Sun` | `m.day() === 0 && Math.ceil(m.date() / 7) === 2 && m.month() === 4` (no month check when the When has no month) |
| `every 3 months from Feb 15` | `(m.month() - 1 + 12) % 3 === 0 && m.date() === Math.min(15, m.daysInMonth())`: the step, then the start month |
| `easter`, `easter+1`, `easter-2` | `easter(m.clone().subtract(N, 'days'))`, with N the offset (`+1` is 1, `-2` is -2) |
| `2027-10-12` | `m.format('YYYY-MM-DD') === '2027-10-12'` |

Months are zero-indexed: Jan=0 to Dec=11. When a row uses Easter, add this helper above the list.
It is the Anonymous Gregorian algorithm:

```js
function easter(m) {
  const y = m.year(), f = Math.floor,
    g = y % 19, c = f(y / 100),
    h = (c - f(c / 4) - f((8 * c + 13) / 25) + 19 * g + 15) % 30,
    i = h - f(h / 28) * (1 - f(29 / (h + 1)) * f((21 - g) / 11)),
    j = (y + f(y / 4) + i + 2 - c + f(c / 4)) % 7,
    month = 3 + f((i - j + 40) / 44),
    day = i - j + 28 - 31 * f(month / 4);
  return m.month() === month - 1 && m.date() === day;
}
```

The file has this structure, with one comment block for each heading of `occasions.md` that has
rows:

```js
const OCCASIONS = [
  // --- DAILY ---
  { sym: '...', name: '...', type: 'reminder', section: 'chores', test: () => true },

  // --- WEEKLY ---
  { sym: '...', name: '...', type: 'event', section: 'chores', test: (m) => ... },
];

function vault_occasions() {
  return OCCASIONS;
}

module.exports = vault_occasions;
```

Write no empty comment block.

## Step 6: Report

> Updated `vault_occasions.js` with **N** occasions:
> - **D** daily
> - **W** weekly
> - **Y** yearly
> - **M** maintenance
> - **O** one-off
>
> Skipped: (each row in `errors`, with its line and why)
> Past one-offs to prune: (each row in `past`)

When Step 3 ran, give its report lines first: the rows that it could not convert, the one-offs with
no year, and the headings that it kept as written.
