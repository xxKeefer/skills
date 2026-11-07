# Extra context: ticket intent and flag liveness

Cheap extra context (both optional, don't block on either):

- **Ticket / PR intent**: `gh pr view --json title,body 2>/dev/null`, and the ticket ID from the branch name. You need to know *which* behaviour change was asked for, because everything beyond that is unrequested production delta. If the ticket or PR names a flag, verify the code uses **that exact flag string**.
- **Flag liveness**: find the project's flag service (named in `CLAUDE.md`, `AGENTS.md` or the flag client code). It tells you whether a flag exists and its per-environment state. Use it when a diff references a flag you don't recognise and it is reachable; a flag that's already on for everyone in production is not a gate.
