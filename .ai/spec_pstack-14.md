---
doctype: spec
ticket: none
status: confirmed
goal: claim on a branch inside a stack returns the stack's worktree, synced.
---

# Spec: stacks in claim and stand-up

Unit 14 of `.ai/map_pstack-program.md`. The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: `claim` treats a gh-stack stack as one worktree. `stand-up` shows which worktree holds each PR, and flags a local branch that differs from its remote. `install-agents-md` offers the worktrunk template that names a worktree by its ticket key.
- User: the user, on a stack of PRs that crosses branches in one worktree.
- Why now: a stack once got a second worktree, built from a stale local branch (the worktree note, items 1 to 5).
- Success: `claim` on a branch inside a stack returns the stack's worktree, synced.
- Constraint: subtract before you add. Remove the dead and repeated text in each touched skill first. Add no script. Use the public `gh stack view --json` and the `remote` field of `wt list --format=json`, not gh-stack's private state file.
- Out of scope: `ship` and `gh stack sync` before a merge (unit 15). A change to the user's `~/.claude/AGENTS.md` or worktrunk config: the skill offers the edit, and the user runs it.

## Decisions

- Stack check: run `gh stack view --json` in each worktree. A worktree holds a stack when its `currentBranch` is one of the stack's `branches[].name`. The trunk worktree also returns the stack, so the trunk does not count.
- Stale check: the `remote.ahead` and `remote.behind` counts of `wt list --format=json`. Both `claim` and `stand-up` read them.
- Sync is a push: `gh stack sync` pushes, with `--force-with-lease` after a rebase. When another person wrote a PR in the stack, `claim` asks first (the pause list: force-push to a branch another person uses).
- Template step: the template moves from the note into `install-agents-md`, as a step that asks first, with `wt step relocate --dry-run` before the move. The system map edit `<repo>.<branch>/` → `<repo>.<KEY>/` is listed in that step, only after a yes to the template. The `lists: <repo>.<KEY>/` line in `sections/tools.md` goes: it searched for the new text, so it never matched the old line.
- Keep the old-layout path in `claim` Step 3 (`handoff_` names and the migration): the user's plan folder still holds plans with no YAML header.

## Acceptance criteria

- [ ] **A.** Read `claim`, `stand-up`, and `install-agents-md` → the repeated `plans or plans`, the `stand-up` Principles section that restates its steps, and the wrong `lists:` line are gone.
- [ ] **B.** Read `claim` → a branch inside a stack resolves to the worktree that holds the stack, with `gh stack checkout <branch>` there. A worktrunk refusal because another worktree sits at the expected path resolves the same way.
- [ ] **C.** Read `claim` → a stack branch whose local copy differs from the remote gets `gh stack sync` first, and the sync asks first when another person wrote a PR in the stack.
- [ ] **D.** Read `stand-up` → each PR row names the worktree that holds it, and a local branch that differs from its remote is flagged.
- [ ] **E.** Run the template in a scratch repo with `wt --config` → a ticket branch gets `<repo>.<KEY>`, a second branch with the same key is refused, and a branch with no key keeps its sanitized name. `install-agents-md` offers it, with relocate and the system map line.
- [ ] **F.** Run the `claim` stack check on a real stack whose worktree holds its top branch → the check returns that worktree for the bottom branch, and not the trunk worktree.
