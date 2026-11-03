# persona-charts catalogue: charts and telemetry graphs

Scope: telemetry and usage charts (Chart.js and ECharts) in a Vue 3 and TypeScript single-page app (SPA) built on Reka UI, vue-router, TanStack Query, and vue-i18n.

Each item has a **Bug** (what the user sees), **Cause**, **Test** (data and steps), **Spot** (what to look for in a diff), **Fix**, and **Sources**. Test datasets live in `fixtures.md`.

`[uncertain]` marks a claim the cited source doesn't fully back. Check it before you rely on it.

---

## A. Empty, sparse and flat data

### CH-A1. Empty dataset gives a blank or broken chart
- **Bug:** A new service has no telemetry yet. The chart shows bare axes, a meaningless 0 to 1 axis, or an error-styled "Unable to display chart".
- **Cause:** The chart is rendered whatever the data, with no check for an empty series or a series of only `null` values. The empty case shares the error branch.
- **Test:** Feed `[]`, a series where every point is `null`, and a date range that ends before the service was provisioned.
- **Spot:** `<Chart :data="series" />` with no `v-if` on `series.length` or on "has any non-null value"; one `v-else` that covers both error and empty.
- **Fix:** A container-level empty state that says why (new service, range before provisioning) and what to do next. Style it as information, not as an error.
- **Sources:** [AEMO GEL Design System: Empty state](https://gel.aemo.com.au/docs/components/miscellaneous/empty-state)

### CH-A2. A single data point is invisible
- **Bug:** A line series with one point draws nothing, so the chart looks empty though there is data.
- **Cause:** A line needs two points to draw a segment, and "clean" line styles set `pointRadius: 0`, so the lone point isn't drawn either.
- **Test:** A series with one point; a series with two points; a range that contains one bucket.
- **Spot:** `pointRadius: 0` (Chart.js) or `showSymbol: false` (ECharts) set globally with no rule for short series.
- **Fix:** Show points when the series is short (for example, under three points), or show a value tile in place of the chart.
- **In Unovis:** `VisLine` and `VisArea` draw no point markers, so a lone point never shows. Add a `VisScatter` for short series, or show a value tile in place of the chart.
- **Sources:** [Chart.js: Line chart (pointRadius)](https://www.chartjs.org/docs/latest/charts/line.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-A3. All-zero or flat series draws a misleading axis
- **Bug:** A series of zeros sits in the middle of the chart and looks like traffic. A constant value auto-scales so tiny noise fills the whole height.
- **Cause:** The y axis auto-fits the data range. With every value equal, the library picks an arbitrary range around it. For hand-rolled scaling (sparklines, bars) where `max - min` is 0, see DS-L6 (persona-value-display).
- **Test:** All zeros, a constant non-zero value, and `[0, 1e-9]`.
- **Spot:** No `beginAtZero`, `min` or `suggestedMax` on non-negative metrics; custom `/ (max - min)` scaling.
- **Fix:** `beginAtZero` or `min: 0` for non-negative metrics, and `suggestedMax` so a flat line reads as flat.
- **In Unovis:** Set the y domain on the container with `yDomain`, `yDomainMinConstraint` or `yDomainMaxConstraint` (for example, a minimum of 0 for non-negative metrics). `preventEmptyDomain` only extends an empty domain by +1, so it doesn't make a flat line read as flat.
- **Sources:** [Chart.js: Linear axis](https://www.chartjs.org/docs/latest/axes/cartesian/linear.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-A4. Gaps drawn as zeros or bridged
- **Bug:** A telemetry outage looks like the service dropped to 0 Mbps, or a straight line spans the gap and looks like steady traffic.
- **Cause:** A mapper fills missing values with `value ?? 0`, or the chart is set to `spanGaps: true` (Chart.js) or `connectNulls: true` (ECharts). Missing timestamps (no row at all) are also bridged unless the series is filled with `null` for each expected bucket.
- **Test:** A run of `null` values in the middle of the range; missing timestamps with no row; a gap at the start and at the end.
- **Spot:** `?? 0` or `|| 0` in a telemetry mapper; `spanGaps: true`; `connectNulls: true`.
- **Fix:** Keep `null`, leave the gap visible, and say "No data" in the tooltip for that span.
- **In Unovis:** `VisLine` breaks the line at `undefined` by default; `fallbackValue` replaces missing values and `interpolateMissingData` draws a dashed bridge over gaps, so set either one only on purpose. `VisArea` always turns `null` into 0, so an area chart can't show a gap.
- **Sources:** [Chart.js: Line chart (spanGaps)](https://www.chartjs.org/docs/latest/charts/line.html), [ECharts: series-line options (connectNulls)](https://echarts.apache.org/en/llms-documents/option-parts/option.series-line.md), [Unovis docs](https://unovis.dev/docs/intro)

### CH-A5. One spike flattens everything else
- **Bug:** A single burst sets the axis maximum, so normal traffic becomes a line on the floor of the chart.
- **Cause:** A linear axis scaled to the maximum value, with no other view offered.
- **Test:** A series of values around 100 with one value of 100,000.
- **Spot:** A fixed linear scale on bursty metrics with no scale toggle or clipping.
- **Fix:** Offer a logarithmic scale, or clip the maximum and mark the clipped spike.
- **In Unovis:** There is no built-in log toggle. The container's `yScale` accepts `Scale.scaleLog` or `Scale.scaleSymlog`, but a log scale can't take 0, so prefer clipping with `yDomainMaxConstraint` and marking the clipped spike [verify through the Vue wrapper].
- **Sources:** [Chart.js: Logarithmic axis](https://www.chartjs.org/docs/latest/axes/cartesian/logarithmic.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-A6. Counter resets drawn as huge negative rates
- **Bug:** A device restart resets a byte counter, and the derived rate shows a massive negative dip.
- **Cause:** The rate is computed as a plain difference between samples, with no handling for a counter that goes back to zero.
- **Test:** A cumulative counter that climbs, drops to 0, and climbs again.
- **Spot:** `(curr - prev) / dt` on counter data in the client, with no reset check.
- **Fix:** Compensate for resets in the rate calculation, as Prometheus `rate()` does, before aggregating. Use `min: 0` only for metrics that can't be negative, so a real negative value isn't hidden.
- **Sources:** [Prometheus: Query functions (rate)](https://prometheus.io/docs/prometheus/latest/querying/functions/)

---

## B. Time zones and bucketing

### CH-B1. Chart time zone differs from the rest of the page
- **Bug:** Ticks are in local time while the range picker and table use UTC, or the reverse. Date labels elsewhere are covered by DS-E2 (persona-value-display); this item covers the chart configuration.
- **Cause:** ECharts `useUTC` defaults to `false` (local time). Chart.js relies on its date adapter for zones. Strings with no zone parse as local time.
- **Test:** Set the OS zone to UTC+5:45 and UTC-3:30, then compare the ticks, the tooltip, and the range picker for the same point.
- **Spot:** No `useUTC` or adapter zone setting; timestamps passed as zone-less strings.
- **Fix:** One display zone across chart, tooltip, and picker, and label it on the chart.
- **In Unovis:** The x scale is epoch milliseconds, so the time zone only appears in the axis `tickFormat` and the `VisCrosshair` `template`. Use the same zone-aware formatter in both.
- **Sources:** [ECharts: root options (useUTC)](https://echarts.apache.org/en/llms-documents/option.md), [Chart.js: Time axis](https://www.chartjs.org/docs/latest/axes/cartesian/time.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-B2. DST gives 23-hour or 25-hour buckets
- **Bug:** Daily buckets around a DST change differ in size, an hourly view shows a repeated or missing hour, and daily totals look wrong. DST in inputs is covered by FM-J7 (persona-form-behaviour).
- **Cause:** Buckets built as fixed 24-hour steps, or bucketed in UTC and labelled in local time.
- **Test:** Ranges across the first Sundays of April and October in Australia/Sydney.
- **Spot:** `start + i * 86400000` to build daily buckets; a server aggregation with no time zone parameter.
- **Fix:** Bucket with an explicit time zone and a calendar-aware interval, and label the changeover.
- **Sources:** [Elasticsearch: Date histogram aggregation (time zone)](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-datehistogram-aggregation)

### CH-B3. Range and resolution mismatched
- **Bug:** "Last 90 days" at 5-minute resolution sends about 26,000 points to a 600 px chart, and the page lags.
- **Cause:** The resolution is fixed, not derived from the selected range.
- **Test:** Pick the longest range on every chart and watch the point count in the response and the frame rate while hovering.
- **Spot:** A hard-coded `interval` or `step` in the telemetry request; no decimation.
- **Fix:** Derive the bucket size from the range, or use decimation, and say what the aggregation is (for example, "5-minute average").
- **In Unovis:** There is no decimation. Derive the bucket size from the selected span before the data reaches the chart.
- **Sources:** [Chart.js: Performance (decimation)](https://www.chartjs.org/docs/latest/general/performance.html), [Unovis docs](https://unovis.dev/docs/intro)

---

## C. Axes, tooltips and legends

### CH-C1. Axis labels overlap or are cut off
- **Bug:** Date labels collide on mobile, and long y labels ("10,000,000,000 bps") are clipped.
- **Cause:** Auto-skip turned off, no rotation limit, full-length number formats, and no room reserved for labels.
- **Test:** A 320 px wide viewport; values in the billions; a 90-day range.
- **Spot:** `autoSkip: false`; raw numbers as tick labels; ECharts grid with no label containment.
- **Fix:** Keep `autoSkip`, set `maxRotation`, and use compact formatters. In ECharts, use `grid.containLabel` (deprecated in v6 in favour of `outerBoundsMode`).
- **In Unovis:** Use `VisAxis` `tickTextHideOverlapping`, `tickTextAngle`, `numTicks`, and `tickTextWidth` with `tickTextFitMode`. `autoMargin` defaults to `true` on the container, so don't turn it off without reserving room.
- **Sources:** [Chart.js: Cartesian axes (ticks)](https://www.chartjs.org/docs/latest/axes/cartesian/), [ECharts: grid options](https://echarts.apache.org/en/llms-documents/option-parts/option.grid.md), [Unovis docs](https://unovis.dev/docs/intro)

### CH-C2. Tooltip clipped at the chart edge
- **Bug:** Tooltips on the last points are cut off by the card's `overflow:hidden`. The general case is DS-H3 (persona-value-display); this item covers the chart setting.
- **Cause:** The tooltip is drawn inside the chart container, which a parent clips.
- **Test:** Hover the first and last points in a card with `overflow-hidden`, at the right edge of the screen.
- **Spot:** A chart inside `overflow-hidden` with no tooltip containment option.
- **Fix:** ECharts `tooltip.confine: true` or `appendTo` (`appendToBody` is deprecated). In Chart.js, use an external tooltip with your own placement.
- **In Unovis:** Use the `VisTooltip` `container` option to insert the tooltip outside the clipping parent.
- **Sources:** [ECharts: tooltip options](https://echarts.apache.org/en/llms-documents/option-parts/option.tooltip.md), [Chart.js: Tooltip](https://www.chartjs.org/docs/latest/configuration/tooltip.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-C3. Tooltip value unformatted or in another unit
- **Bug:** The axis says "1.2 Mbps" but the tooltip shows `1234567.891` or a value in bps, or the tooltip title is a raw epoch.
- **Cause:** Axis ticks have a formatter and the tooltip uses the library default.
- **Test:** Hover points with large values, small values, and decimals; compare with the axis and any summary tiles.
- **Spot:** A `ticks.callback` with no matching tooltip `label` callback; two different unit helpers.
- **Fix:** One formatter shared by axis ticks, the tooltip `label` callback, and summary tiles.
- **In Unovis:** Share one formatter between the `VisAxis` `tickFormat` and the `VisCrosshair` `template`.
- **Sources:** [Chart.js: Tooltip (label callback)](https://www.chartjs.org/docs/latest/configuration/tooltip.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-C4. Legend overflow, or every series hidden
- **Bug:** Twelve connection series make the legend taller than the chart. Hiding every series leaves an empty plot with a stale axis.
- **Cause:** A plain legend with no scrolling, and no empty state for "all series hidden".
- **Test:** 12 or more series; very long series names; click every legend entry off.
- **Spot:** Default legend options on charts with a variable series count.
- **Fix:** ECharts `legend.type: 'scroll'`, truncated names (full name in a tooltip), and an empty state when everything is hidden.
- **In Unovis:** `VisBulletLegend` has only `labelMaxWidth` for long names and no scroll mode. A new legend needs its own overflow and all-hidden handling.
- **Sources:** [ECharts: legend options](https://echarts.apache.org/en/llms-documents/option-parts/option.legend.md), [Unovis docs](https://unovis.dev/docs/intro)

### CH-C5. Chart text ignores the user's font size
- **Bug:** Users with a larger default browser font get readable HTML but 12 px canvas labels.
- **Cause:** Chart.js font sizes are in pixels, so they don't follow the root font size.
- **Test:** Set the browser's default font size to "Very large" and reload a chart page.
- **Spot:** Hard-coded `font: { size: 12 }` in chart options.
- **Fix:** Compute chart font sizes from the root font size (`getComputedStyle(document.documentElement).fontSize`).
- **In Unovis:** Unovis draws SVG, not canvas. `VisAxis` `tickTextFontSize` takes a CSS string, so pass a `rem` value to follow the root font size.
- **Sources:** [Chart.js: Fonts](https://www.chartjs.org/docs/latest/general/fonts.html), [Unovis docs](https://unovis.dev/docs/intro)

---

## D. Sizing, lifecycle and accessibility

### CH-D1. Chart doesn't follow its container's size
- **Bug:** Collapsing the nav leaves the chart at its old width. A chart in a hidden tab starts at width 0. A Chart.js chart in an auto-height flex child keeps growing or won't shrink. Other layout measured once (textareas, popovers, virtual lists) is DS-M4 (persona-value-display).
- **Cause:** ECharts doesn't resize itself when its container changes. Chart.js needs a dedicated, relatively positioned container to measure.
- **Test:** Collapse and expand the sidebar, resize the window, change browser zoom, and open a tab that holds a chart.
- **Spot:** `echarts.init(el)` with no `ResizeObserver`; a chart initialised with an explicit width; Chart.js canvas inside a flex child with `maintainAspectRatio` left on.
- **Fix:** A `ResizeObserver` (or VueUse `useResizeObserver`) that calls ECharts `resize()`, including when a tab becomes visible. For Chart.js, give the canvas a relatively positioned container used only by the chart, and set `maintainAspectRatio: false` when the container is resized.
- **In Unovis:** The container has its own `ResizeObserver`. The known problem is the width locking too narrow, worked around with VueUse `useElementSize`.
- **Sources:** [ECharts: echartsInstance API (resize)](https://echarts.apache.org/en/llms-documents/api-parts/api.echartsInstance.md), [Chart.js: Responsive charts](https://www.chartjs.org/docs/latest/configuration/responsive.html), [Whittaker attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf), [Unovis docs](https://unovis.dev/docs/intro)

### CH-D2. Chart instance leaks, or is made deeply reactive
- **Bug:** Memory grows when moving between services, ghost tooltips appear, and the page is slow when the instance sits in a `ref`.
- **Cause:** The instance is never destroyed on unmount, and Vue wraps a large library object in a deep reactive proxy.
- **Test:** Move between 20 services and take heap snapshots; hover after navigating away and back.
- **Spot:** `ref(echarts.init(el))` or `ref(new Chart(...))`; no `dispose()` or `destroy()` in `onBeforeUnmount`.
- **Fix:** Hold the instance with `markRaw` or `shallowRef`, and call `destroy()` (Chart.js) or `dispose()` (ECharts) in `onBeforeUnmount`.
- **In Unovis:** This only applies to an imperative `new XYContainer(...)`, which needs `destroy()` on unmount. The `@unovis/vue` components call `destroy()` on unmount themselves.
- **Sources:** [Chart.js: API (destroy)](https://www.chartjs.org/docs/latest/developers/api.html), [Vue: markRaw and shallowRef](https://vuejs.org/api/reactivity-advanced.html), [Unovis docs](https://unovis.dev/docs/intro)

### CH-D3. Chart not accessible
- **Bug:** A screen reader finds an unnamed canvas, and series can be told apart only by colour.
- **Cause:** Canvas has no accessible content of its own, and the palette is the only series cue.
- **Test:** VoiceOver or NVDA on the chart; a greyscale or colour-blindness filter in DevTools.
- **Spot:** `<canvas>` with no `role`, `aria-label`, or fallback; no `aria` option in ECharts.
- **Fix:** `role="img"` with an `aria-label` summary, plus fallback content or a data table. In ECharts, `aria.enabled` with `decal` patterns (line series need `areaStyle` for decals to show).
- **In Unovis:** The output is SVG and containers take `ariaLabel`. There are no decals, so use `lineDashArray` to tell series apart without colour.
- **Sources:** [Chart.js: Accessibility](https://www.chartjs.org/docs/latest/general/accessibility.html), [ECharts: aria options](https://echarts.apache.org/en/llms-documents/option-parts/option.aria.md), [Unovis docs](https://unovis.dev/docs/intro)
