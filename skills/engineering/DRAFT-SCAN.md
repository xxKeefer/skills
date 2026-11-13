# Draft scan

Scan text that a person outside this session reads, such as a PR, a ticket, or a review comment.
Fix each hit:

- An em dash or an en dash used as a connector.
- `e.g.`, `i.e.`, `etc.`, `vs.`, or `via`.
- A prose word spelled outside the locale that the user's instructions name. Identifiers, API
  fields, config keys, quoted UI strings, and names from the product keep their spelling.
- A list of three or more items with no Oxford comma.
- The name of a personal skill, an agent, or a review tool.

The calling skill names any exception.
