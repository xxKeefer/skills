# Contract edge cases

These cases extend rules 1 and 3 of the persona. They keep the severity of their rule, unless the case says otherwise.

## Rule 1: option list built by exclusion

An option list built as "every client enum value minus a hidden list", for a value another service validates, is a rule 1 finding: the next value the client adds reaches the select, and the server, before that service accepts it. Ask for an allow list of the values the service accepts, with a link to its enum.

## Rule 3: legacy API client that only validates

Some legacy API clients run their schemas as validators only. They `safeParse`, report a mismatch through a callback, and return the raw data. There the impact is an error-tracker parse report, not a broken query. Say that in `detail`, and lower the finding to Nit when the gap is already on `main`.
