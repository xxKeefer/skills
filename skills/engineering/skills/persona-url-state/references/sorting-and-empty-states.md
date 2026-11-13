# Sorting and empty states (rules 11 and 12)

11. **Sorting by the string, not the value (Change Requested).** `.sort()` with no comparator on numbers; a comparator on formatted strings ("10 Gbps" before "2 Gbps", "01/02" dates); `a > b` returning a boolean; `.sort()` mutating query data in place; a client sort on one page of server-paginated data. Sort on the raw value; use `localeCompare` with `numeric: true` for names. (NV-M1, NV-M4, NV-M5, NV-M6, NV-M7)
12. **"No data" and "no matches" share one empty state (Nit).** A filtered list saying "You have no services" when the filter matched nothing; no way to clear the filter from the empty state; a "Clear filters" button that resets the controls but not the URL. (NV-K1, NV-K2, NV-K3)
