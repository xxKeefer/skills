---
name: update-occasions-config
description: >
  Sync occasions.md from the vault into vault_occasions.js for Templater. Reads all sections
  (daily chores, day-specific chores, recurring events, one-off events, project milestones) and
  generates JS with the { sym, name, type, section, test } shape. Run when occasion data changes.
---

# Update Occasions Config

Reads `occasions.md` from the journal directory and generates `vault_occasions.js` in the
vault's Templater scripts directory.

## Step 1: Discover Paths

Find the journal directory by scanning the vault for a directory containing `occasions.md`.
Find the Templater scripts directory (typically `99-meta/scripts/` or `99 - Meta/scripts/`
relative to the vault root).

If either path cannot be found, ask:
> Where is your vault's Templater scripts directory?

## Step 2: Read occasions.md

Parse every section. Each occasion carries a **`section`** field that routes it into the matching
checklist group in the daily/weekly file: `chores`, `work`, or `tasks` (defaults to `chores` if a
section has no Section column). Always emit `section` on every object.

### Chores (Daily Default)

Lines matching `- [ ] <emoji> <name>`. These become reminders that fire every day. Section: `chores`.

```
- [ ] 🧼 Dishes On
```

Produces:
```js
{ sym: '🧼', name: 'Dishes On', type: 'reminder', section: 'chores', test: () => true },
```

### Chores (Day-Specific)

Table rows with `| <day-rule> | <emoji> <name> |`. Section: `chores`. Day rules:

| Rule pattern | JS test |
|---|---|
| `Monday` | `m.day() === 1` |
| `Tuesday` | `m.day() === 2` |
| `Wednesday` | `m.day() === 3` |
| `Thursday` | `m.day() === 4` |
| `Friday` | `m.day() === 5` |
| `Saturday` | `m.day() === 6` |
| `Sunday` | `m.day() === 0` |
| `<Day> (even weeks)` | `m.day() === N && m.isoWeek() % 2 === 0` |
| `<Day> (odd weeks)` | `m.day() === N && m.isoWeek() % 2 !== 0` |

These become reminders.

### Recurring Events

Table rows with `| <emoji> <name> | <date-rule> | <type> | <section> |`. The Section column routes
the occasion (defaults to `chores`). Date rules:

| Rule pattern | Example | JS test |
|---|---|---|
| `Mon DD` | `Jan 5` | `m.format('DDMM') === 'DDMM'` |
| `Nth Day Mon` | `2nd Sun May` | Floating holiday: `m.month() === M && m.day() === D && m.date() >= low && m.date() <= high` |
| `Easter calc` | | Computus algorithm for Good Friday (Easter - 2) and Easter Monday (Easter + 1) |
| `Mon (varies)` | `Aug (varies)` | Skip with a `// TODO: manually verify` comment |

For fixed-date holidays (`Jan 1`, `Jan 26`, `Apr 25`, `Dec 24`, `Dec 25`, `Dec 26`), add
weekend carry-over logic: if the date falls on Saturday, observe on Friday; if Sunday, observe
on Monday. Use compound test:

```js
(m.month() === M && m.date() === D) ||
(m.month() === M && m.date() === D + 1 && m.day() === 1) ||
(m.month() === M && m.date() === D - 1 && m.day() === 5)
```

Only apply carry-over to public holidays (New Year's, Australia Day, Anzac Day, Christmas,
Boxing Day). Birthdays and non-public-holiday events use exact date matching only.

### Easter Calculation

Use the Anonymous Gregorian algorithm (Computus):

```js
const y = m.year(), f = Math.floor,
  g = y % 19, c = f(y / 100),
  h = (c - f(c / 4) - f((8 * c + 13) / 25) + 19 * g + 15) % 30,
  i = h - f(h / 28) * (1 - f(29 / (h + 1)) * f((21 - g) / 11)),
  j = (y + f(y / 4) + i + 2 - c + f(c / 4)) % 7,
  month = 3 + f((i - j + 40) / 44),
  day = i - j + 28 - 31 * f(month / 4);
```

- Good Friday: `m.month() === month - 1 && m.date() === day - 2`
- Easter Monday: `m.month() === month - 1 && m.date() === day + 1`

### Month Parsing

Map month names to zero-indexed values:

```
Jan=0, Feb=1, Mar=2, Apr=3, May=4, Jun=5,
Jul=6, Aug=7, Sep=8, Oct=9, Nov=10, Dec=11
```

### Day Parsing

Map day names to moment `.day()` values:

```
Sun=0, Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6
```

### Floating Holiday Ranges

For `Nth DayName Month` rules, compute the date range:

| Nth | Date range |
|---|---|
| 1st | 1--7 |
| 2nd | 8--14 |
| 3rd | 15--21 |
| 4th | 22--28 |

### One Off Events

Section heading matches `## One Off Events` (optionally suffixed with a year, e.g.
`## One Off Events - 2026`). Table rows with `| <emoji> <name> | <date-rule> | <type> | <section> |`.

These fire **once on their date** and the user prunes them manually afterwards. Default Section is
`tasks`. Parse the date with the same `Mon DD` / `Nth Day Mon` rules as recurring events, but
**year-guard** them so a one-off doesn't recur every year:

- If the heading carries a year `YYYY`, add `m.year() === YYYY &&` to the test.
- If no year is given, fall back to the current year.

```
## One Off Events - 2026
| 💒 A Wedding | Oct 12 | event | tasks |
```

Produces:
```js
{ sym: '💒', name: 'A Wedding', type: 'event', section: 'tasks', test: (m) => m.year() === 2026 && m.month() === 9 && m.date() === 12 },
```

No weekend carry-over for one-offs -- exact date only.

### Projects

Section heading matches `## Projects`. This section is written by the `projects` domain's
`/schedule-goals` skill; the user does not normally hand-edit it. Same table shape as One Off Events:
`| <emoji> <project>: <milestone> | <date-rule> | <type> | <section> |`.

Project milestones are **dated, year-guarded, single-fire** like one-offs. Default Section is `tasks`
so they render in the daily/weekly Tasks group with no template change.

```
## Projects
| 🏗 New House: finance approved | Jul 3 | event | tasks |
```

Produces:
```js
{ sym: '🏗', name: 'New House: finance approved', type: 'event', section: 'tasks', test: (m) => m.year() === 2026 && m.month() === 6 && m.date() === 3 },
```

## Step 3: Generate vault_occasions.js

Write the output file to `<scripts-dir>/vault_occasions.js` with this structure:

```js
const OCCASIONS = [
  // --- DAILY DEFAULT CHORES ---
  { sym: '...', name: '...', type: 'reminder', section: 'chores', test: () => true },

  // --- DAY-SPECIFIC CHORES ---
  { sym: '...', name: '...', type: 'reminder', section: 'chores', test: (m) => ... },

  // --- RECURRING EVENTS ---
  { sym: '...', name: '...', type: 'event', section: 'chores', test: (m) => ... },

  // --- ONE OFF EVENTS ---
  { sym: '...', name: '...', type: 'event', section: 'tasks', test: (m) => ... },

  // --- PROJECTS ---
  { sym: '...', name: '...', type: 'event', section: 'tasks', test: (m) => ... },
];

function vault_occasions() {
  return OCCASIONS;
}

module.exports = vault_occasions;
```

Every object emits `section`. Omit a section block entirely if `occasions.md` has no such section --
do not write empty comment headers.

## Step 4: Confirm

Report what was generated:

> Updated `vault_occasions.js` with **N** occasions:
> - **X** daily chores
> - **Y** day-specific chores
> - **Z** recurring events
> - **A** one-off events
> - **B** project milestones
>
> Skipped: (list any rules that couldn't be parsed, if any)
