# Stack facts for chart fixes

Stack facts to use in fixes. Check each against the project before you rely on it:
- Find the app's main XY chart wrapper (`VisXYContainer`, `VisLine`, `VisArea`, `VisAxis`, `VisCrosshair`, `VisTooltip`) and the charts that use it. Sparklines and `VisSankey` charts are usually separate.
- Check where the empty state lives. It often sits in the parent that gates the chart, not in the chart wrapper. A Sankey chart may have its own no-data message.
- Nulls: `VisArea` turns `null` into `0` (its stacking does `getNumber(...) || 0`), and `VisLine` breaks on `null` only while `fallbackValue` is left `undefined`. A wrapper should therefore feed each series its own samples with null edges trimmed. Interior nulls still dip an area to 0. The tooltip should show `—` for null.
- Time zone: the x scale is plain epoch milliseconds, so the zone exists only in the tick and tooltip formatters. Check which zone the page uses (local or UTC) and whether the wrapper passes it as a prop. Billing charts may use a fixed billing zone and build days with Luxon in that zone.
- Units: check whether a formatter scales values to Tbps, Gbps, Mbps, or kbps. The y axis should use one unit taken from the dataset peak; tooltips may scale each value separately.
- Width: a wrapper may drive `:width` from VueUse `useElementSize`, because the container's own measuring can lock too narrow when it mounts before layout settles. The `@unovis/vue` containers call `destroy()` when they unmount.
- Dark mode: Unovis reads its dark CSS variables from a theme class on `body`. Check that the app keeps that class in step with its own dark-mode class.
- Check Unovis option names against the installed version's type definitions (`node_modules/@unovis/ts/**/config.d.ts`) and [unovis.dev](https://unovis.dev) before you name any option.
