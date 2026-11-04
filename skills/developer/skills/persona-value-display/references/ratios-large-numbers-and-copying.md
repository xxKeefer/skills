# Ratios, large numbers, and copying (rules 9 to 11)

9. **A ratio of zero (Change Requested).** A utilisation or percentage computed as `used / total` with no zero check, so a new service shows "NaN%" or "Infinity%"; a value already in percent multiplied by 100 again by `Intl.NumberFormat` `style: 'percent'`. (DS-D12, DS-D13)
10. **Large numbers unreadable or unsafe (Nit).** Counts and prices in tables with no thousands separator; numbers not right-aligned or tabular (`tw:tabular-nums`) in a column; an id above `Number.MAX_SAFE_INTEGER` parsed as a number; compact notation ("1.2K") hiding a difference that matters. (DS-D1, DS-D8, DS-D14, DS-D16)

**Copying**

11. **Copy button copies the wrong thing (Nit).** A copy button on a formatted value that copies "$1,234.00" or "10 Gbps" where the user needs the raw value, or an id with surrounding whitespace or a hidden zero-width character; a copy with no feedback, or feedback that never resets. (DS-F1, DS-F2, DS-F3, DS-F5)
