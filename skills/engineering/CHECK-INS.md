# Check-ins

A check-in stops the run for the user. The user gets one check-in, at the end of the loop. Stop
earlier only at a **gate**.

A change needs a gate when one of these is true:

- It is sensitive: a secret, a permission, billing, or stored data.
- It is a one-way door, as `/create-pr` Step 4 defines it.
- Another person can see it: a PR with a human reviewer other than the user, a ticket, or a shared
  channel. A repo has other people when it has a human author other than the user in the last 90
  days (`git shortlog -sne --since=90.days HEAD`, minus bots), or the user's instructions say so.

When you cannot tell, gate. At a gate, show the change and wait for the user before it goes out.

Every other change gets no check-in: a trivial change, the user's own solo work, and any result
that a command can verify. Do it, verify it, and report at the end of the loop:

- Push the work branch, open the PR, and run CI on it.
- Check each result that a command can show. Leave the user only the results that need eyes on a
  screen.
- Mark the PR ready and merge it after `/ship` gives go.

Never push the default branch.
