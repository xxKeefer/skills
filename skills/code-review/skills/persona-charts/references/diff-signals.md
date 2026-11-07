# persona-charts diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-charts catalogue](catalogue.md)

- CH-A1: `<VisXYContainer>` or `<VisLine>` rendered with no `v-if` on `data.length` or "any non-null value"; one `v-else` shared by error and empty → A container-level empty state, styled as information [default: nit] (rule 1)
- CH-A2: `VisLine` or `VisArea` only (no point markers) for a series that can hold one point, with no `VisScatter` or value tile fallback → Add `VisScatter` for short series, or a value tile [default: nit] (rule 2)
- CH-A3: Non-negative metric on `VisXYContainer` with no `yDomain` or `yDomainMinConstraint`, relying on `preventEmptyDomain` for a flat series → Set `yDomainMinConstraint` 0 so a flat line reads flat [default: nit] (rule 4)
- CH-A4: `?? 0` or `|| 0` in a telemetry mapper, `VisLine` `fallbackValue` or `interpolateMissingData` set, or `VisArea` used for data with gaps → Keep gaps as `undefined` on `VisLine`; avoid `VisArea` for gappy data [default: nit] (rule 3)
- CH-A5: Fixed linear `yScale` on a bursty metric with no `yDomainMaxConstraint` clipping; `Scale.scaleLog` on data that can hold 0 → Clip with `yDomainMaxConstraint` and mark the clipped spike [default: nit] (rule 4)
- CH-A6: `(curr - prev) / dt` on cumulative counter data in the client, with no check for a counter reset → Compensate for counter resets before aggregating [default: nit] (rule 6)
- CH-B1: `VisAxis` `tickFormat` or `VisCrosshair` `template` formatting epoch ms without the page's display zone, or zone-less timestamp strings parsed → One zone-aware formatter for axis, crosshair and picker [default: nit] (rule 5)
- CH-B2: Daily buckets built as `start + i * 86400000`, or a server aggregation request with no time zone parameter → Bucket with an explicit zone and calendar-aware interval [default: nit] (rule 6)
- CH-B3: Hard-coded `interval` or `step` in a telemetry request, not derived from the selected span (Unovis has no decimation) → Derive bucket size from the span; label the aggregation [default: nit] (rule 6)
- CH-C1: `VisAxis` with raw numbers in `tickFormat`, `autoMargin: false`, or no `tickTextHideOverlapping`/`numTicks` on a date axis → Compact `tickFormat`, `tickTextHideOverlapping`, keep `autoMargin` [default: nit] (rule 7)
- CH-C2: `VisTooltip` or `VisCrosshair` inside an `overflow-hidden` card with no `container` option set → Set `VisTooltip` `container` outside the clipping parent [default: nit] (rule 8)
- CH-C3: `VisAxis` `tickFormat` and `VisCrosshair` `template` using different formatters or unit helpers, or the template printing raw values → Share one formatter between `tickFormat` and the crosshair `template` [default: nit] (rule 8)
- CH-C4: New `VisBulletLegend` on a variable series count with no `labelMaxWidth`, no overflow handling, or no empty state when all series are hidden → Truncate labels, handle overflow, empty state when all hidden [default: nit] (rule 10)
- CH-C5: `VisAxis` `tickTextFontSize` set in `px`, or a hard-coded pixel font size in chart options → Pass a `rem` CSS string to `tickTextFontSize` [default: nit] (rule 7)
- CH-D1: Chart given a fixed `width`, or container width read once, instead of following VueUse `useElementSize` → Drive width from `useElementSize` on the wrapper [default: nit] (rule 9)
- CH-D2: Imperative `new XYContainer(...)` held in `ref()` (not `shallowRef`/`markRaw`) or with no `destroy()` in `onBeforeUnmount` → Hold in `shallowRef`; call `destroy()` in `onBeforeUnmount` [default: nit] (rule 9)
- CH-D3: Several `VisLine` series told apart only by colour, with no `lineDashArray`, or a Unovis container with no `ariaLabel` → Add `lineDashArray` per series and an `ariaLabel` summary [default: nit] (rule 10)
