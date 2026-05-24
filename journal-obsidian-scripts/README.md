# journal-obsidian-scripts

Templater user scripts and templates for the journal domain. Manual redundancy for when agents
aren't available (mobile, offline, Obsidian-only sessions). Produces files that `/reflect` and
other journal skills can operate on without modification.

## Setup

### 1. Install scripts

Copy `scripts/*.js` into your vault's Templater scripts directory:

```
cp scripts/*.js <vault>/99-meta/scripts/
```

### 2. Install templates

Copy `templates/*.md` into your vault's templates directory:

```
cp templates/*.md <vault>/99-meta/templates/
```

### 3. Configure occasions

The repo ships `vault_occasions.js` with stubbed example data. Replace it with your real
occasion data by running `/update-occasions-config` in the journal domain, or edit
`<vault>/99-meta/scripts/vault_occasions.js` directly.

### 4. Configure Templater

In Obsidian Settings > Templater:

- **Script files folder**: `99-meta/scripts`
- **Template folder**: `99-meta/templates`

## Scripts

| Script | Purpose |
|---|---|
| `journal_config.js` | Singleton: paths, types, tags, week config |
| `journal_daily_name.js` | `date -> "YYYY-wkNN-day"` |
| `journal_weekly_name.js` | `date -> "YYYY-wkNN-week"` |
| `journal_monthly_name.js` | `date -> "YYYY-MM-mon"` |
| `journal_yearly_name.js` | `date -> "YYYY"` |
| `journal_prev_next.js` | `(date, level) -> { prev, next }` wikilink names |
| `journal_up_link.js` | `(date, level) -> parent` wikilink name |
| `journal_occasions.js` | `(date) -> { chores, events }` filtered from occasions |
| `vault_occasions.js` | Occasion data (stubbed example -- replace with your own) |
| `prompt_date.js` | Date prompt utility |
| `prompt_boolean.js` | Boolean prompt utility |

## Templates

| Template | Produces |
|---|---|
| `template-journal_daily.md` | Daily file with chores, events, tasks, reflect sections |
| `template-journal_weekly.md` | Weekly file with 7-day links table and goals |
| `template-journal_monthly.md` | Monthly file with weekly overview table |
| `template-journal_yearly.md` | Yearly file with 12-month table |

## Development

```
pnpm install
pnpm build      # compile src/*.ts -> scripts/*.js
pnpm test       # run tests
pnpm typecheck  # type-check without emitting
```

Built output is committed to `scripts/` so users can grab it without running a build.
