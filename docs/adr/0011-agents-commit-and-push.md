# 0011 Agents commit and push

**Status:** Accepted, 2026-11-07.

## Context

Until now, a skill asked the user before it committed or pushed code. `/create-pr` asked once
before the push. `/migrate-a-skill` asked before it committed. `/sync-docs`, `/self-improve`, and
`/update-personas` left their changes uncommitted, and `/squash-bugs` pushed nothing. A run that
went through several skills stopped at each of these gates, and each gate came after a human
check-in that already covered the same work: the review report before the push step.

## Decision

Agents commit and push their own work. The one human check-in is at the end: the review report
that `mob-review` writes before the push step. The user ticks the fixes to make there, and the
push step runs after that without another yes.

- `/create-pr` pushes without asking. It stops only on drift since the review or on a
  `reason needed` gap.
- `/run-wave` makes a branch named from the handoff when it starts on the default branch.
- `/resolve-conflicts` runs `--continue` once each conflict is resolved and the tests pass.
- `/sync-docs`, `/self-improve`, `/update-personas`, and `/migrate-a-skill` commit.
- `/squash-bugs`, `/migrate-a-skill`, and `/retire-a-skill` push.

These gates stay, because they guard against lost work, not against a commit or a push:

- the yes before `/retire-a-skill` deletes a skill
- the stop on a dirty tree in `/run-wave`
- the question about local commits in `/pickup` and `/review-pr`
- the check in `/apply-review`, which runs only when the user asks for it

## Consequences

- A run goes from the plan to a draft PR with one stop, at the review report.
- A branch can reach the remote before the user reads the diff. A draft PR and the review report
  are where the user reads it.
- No skill force-pushes. Each push step still says "Never force".
- A new skill that commits or pushes follows this rule. A new gate before a commit or a push needs
  its own ADR.
- Vault skills keep their rule: they never commit in the vault.
