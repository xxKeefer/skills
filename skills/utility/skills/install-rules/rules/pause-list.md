## Pause Rule

An action stops for the user when another person reads its output. An action whose output only
the user or the agent reads runs with no stop.

A skill can call a workflow skill with no stop. The stop is on the action, not on the skill.

### Pause List

Stop and get a yes from the user before each of these actions:

- Mark a PR ready for review.
- Merge.
- Force-push to a branch that another person uses.
- Deploy.
- Delete data, or delete a branch that is not merged.
- Post a comment, a review, or a ticket update as the user.
- Write a ticket.
- Send a message to a person.

### No Stop

These actions run with no stop:

- The end of a ★ skill.
- A test round or a review round.
- A push to the agent's own branch.
- A draft PR.

When you cannot tell if another person reads the output, stop.
