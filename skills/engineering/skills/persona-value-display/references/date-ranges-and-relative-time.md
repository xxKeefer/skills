# Date ranges and relative time (rules 5 and 6)

5. **Date range edges (Change Requested when it changes what's billed or filtered, else Nit).** An "until" date sent or compared as midnight at the start of the day, so the last day is excluded; seconds and milliseconds epochs mixed (a 1970 date, or year 50000). (DS-E10, DS-E5)
6. **Relative time oddities (Nit).** "in 0 seconds", "1 days ago", a negative "−3 minutes ago" from client clock skew, or a relative label that never updates while the page stays open. Use `Intl.RelativeTimeFormat` and clamp. (DS-E7, DS-E8)
