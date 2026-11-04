# Fixtures: chart datasets

Test data for this lane's catalogue. Feed each dataset to the chart a change touches (mock the telemetry response, or use a Storybook story), and cite the dataset as the failing input in a finding. Points are `[timestamp, value]` with ISO timestamps in UTC unless stated.

## Datasets

| # | Dataset | Expect | Catches |
| --- | --- | --- | --- |
| C1 | `[]` | an empty state that says why, not bare axes or an error | CH-A1 |
| C2 | `[["2026-10-01T00:00Z", null], ["2026-10-01T00:05Z", null], ["2026-10-01T00:10Z", null]]` | the same empty state as C1 | CH-A1 |
| C3 | `[["2026-10-01T00:00Z", 420]]` (one point) | a visible point or a value tile | CH-A2 |
| C4 | `[["2026-10-01T00:00Z", 420], ["2026-10-01T00:05Z", 430]]` | a visible line and both points on hover | CH-A2 |
| C5 | 288 points, every value `0` | a flat line at the bottom of a 0-based axis | CH-A3 |
| C6 | 288 points, every value `750` | a flat line that reads as flat, not noise | CH-A3, DS-L6 (persona-value-display) |
| C7 | `[0, 1e-9]` as two values | no NaN, no full-height jump | CH-A3, DS-L6 (persona-value-display) |
| C8 | 288 points with values 80 to 120, then 36 `null` values in the middle | a visible gap, "No data" in the tooltip, no drop to 0 | CH-A4 |
| C9 | the same as C8, but the 36 rows are missing (no timestamps at all) | a gap, not a straight bridge | CH-A4 |
| C10 | 288 points around 100, one point at `100000` | normal traffic still readable (log scale or clipped spike) | CH-A5 |
| C11 | values `[-50, -10, 0, 10, 50]` on a metric that can be negative | negatives drawn below 0, not hidden by `min: 0` | CH-A6 |
| C12 | cumulative counter `[1000, 2000, 3000, 0, 1000, 2000]` | a rate with no huge negative dip | CH-A6 |
| C13 | 90 days at 5-minute resolution: 90 × 288 = 25,920 points | decimation or a coarser bucket; no lag on hover | CH-B3 |
| C14 | 12 or more series | the legend scrolls and never covers the plot | CH-C4 |
| C15 | series names of 80 characters, for example `Data centre A to data centre B production link primary path 10 Gbps` | names truncated in the legend, full name on hover | CH-C4 |
| C16 | values up to `10000000000` (10 billion bps) | compact tick labels, nothing clipped | CH-C1, CH-C3 |
| C17 | values with long decimals, for example `1234567.891` | the tooltip uses the same unit and format as the axis | CH-C3 |

## Time zones and DST

Run every time-based chart with the OS (or browser) time zone set to each of these, then compare the chart ticks, the tooltip, the range picker, and any table on the page.

| Zone | Why | Catches |
| --- | --- | --- |
| `UTC` | baseline | CH-B1 |
| `Australia/Sydney` | DST ends on Sunday 5 April 2026 (that day has 25 hours) and starts on Sunday 4 October 2026 (that day has 23 hours) | CH-B1, CH-B2 |
| `Asia/Kathmandu` (UTC+5:45) | a 45-minute offset breaks hour-aligned buckets | CH-B1 |
| `America/St_Johns` (UTC-3:30) | a half-hour negative offset | CH-B1 |
| `Australia/Lord_Howe` | DST moves the clock by 30 minutes, not an hour (same Sundays as Sydney) | CH-B2 |

DST datasets:

- Hourly points from `2026-04-04T13:00Z` to `2026-04-05T14:00Z` (Sydney local 4 April 00:00 to 5 April 00:00, a 25-hour day): expect 25 hourly buckets for that local day and a repeated 02:00 hour, labelled.
- Hourly points from `2026-10-03T14:00Z` to `2026-10-04T13:00Z` (Sydney local 4 October 00:00 to 5 October 00:00, a 23-hour day): expect 23 buckets and no 02:00 hour.
- A daily chart from 1 March to 30 April 2026 and from 1 September to 31 October 2026: daily totals around the changeover must not jump by 1/24.

## Per-chart smoke script (about five minutes)

1. Load the chart with C1, C3, C5, and C8. Each reads correctly (CH-A1 to CH-A4).
2. Resize the window from wide to 320 px, then collapse and expand the side nav. The chart follows its container (CH-D1), and labels don't overlap (CH-C1).
3. Put the chart in a tab that starts hidden, then open the tab. It isn't 0 px wide (CH-D1).
4. Hover the first and last points in a card with `overflow-hidden`. Tooltips aren't clipped and match the axis format (CH-C2, CH-C3).
5. Click every legend entry off. The plot shows an empty state, not a stale axis (CH-C4).
6. Navigate between 10 services and back, then take a heap snapshot. There is one chart instance (CH-D2).
7. Switch to dark mode, then turn on forced colours (Windows High Contrast, or DevTools > Rendering > Emulate forced-colors). Lines, gridlines, and labels stay visible, and series are told apart by more than colour (CH-D3).
8. Set the browser's default font size to "Very large". Chart labels grow with the page text (CH-C5).
9. Tab to the chart and use VoiceOver or NVDA. It has a name and a summary, or a data table alternative (CH-D3).
10. Repeat steps 1 and 4 in `Australia/Sydney` and `Asia/Kathmandu` across the DST datasets (CH-B1, CH-B2).
