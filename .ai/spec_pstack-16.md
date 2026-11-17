---
doctype: spec
ticket: none
status: confirmed
goal: "A CI change on a watched PR shows a notification and the right chip, and leading spaces survive in the real status line."
---

# Spec: `babysit` and the status line chips

## Intent

- Outcome: `/babysit` watches the user's PRs in the background, alerts the user on each change, and the status line shows one chip for each watched PR.
- User: the user who has PRs in CI or in review while the agent works on something else.
- Why now: map unit 16 (r1.12). The alert must reach the user beyond a skill call.
- Success: a CI change on a watched PR fires the notifier once, and the chip shows the new state at the next redraw.
- Constraint: subtract before you add. The status line redraws each second, so its cost must go down before the chips add to it. One script and one state file. No second store.
- Out of scope: a TUI, and a `gh stack` command in the watcher.

## Decisions

- Status line chips, from the map Decisions: chips on the right of line 1, aligned with `COLUMNS`. One chip for each watched PR: a background colour, a symbol, and the PR number. Only uniform-width characters. Order by urgency: red, amber, blue, yellow, green, grey. A done chip goes after 10 minutes. When the chips do not fit, a ticker moves one column for each redraw, and red and amber chips stay pinned on the left. The chip segment reads only `~/.cache/babysit/state.json`, with no network call. The token count is cached by the transcript's file size.
- Subtract first in `statusline.sh`: one `jq` call reads stdin, in place of eight. The token count comes from a cache keyed by the transcript's size, so a redraw with no new message parses nothing.
- The ticker offset is the epoch second, so the ticker needs no stored state.
- One state file holds the watch list and the last state of each PR. No separate watch list.
- `watch_prs.py` has three commands: `add` (watch a PR), `poll` (one pass, safe to run again), and `run` (poll in a loop until no PR is open, then exit). `/babysit` starts `run` detached, once: a pid file stops a second loop.
- A stack needs no `gh stack` call. Among the open watched PRs, the watcher polls only a PR whose base branch is not the head branch of another open watched PR. That is the lowest PR of each stack not merged.
- The state of a PR, first match wins: merged or closed is done; a failed check is failed; a base that moved (`mergeStateStatus` `BEHIND` or `DIRTY`) is stale; an unresolved review thread is threads; a check that is not complete is pending; CI green with `reviewDecision` approved or empty is ready; else pending.
- The notifier is a tool role in the `tools` block of `install-agents-md`. `HYDRATE.md` fills `notifier_command`, a shell command that takes a title and a body as its two arguments, or `none`. The watcher reads it from `~/.claude/agents-md.values.json`. With `none`, the chip is the only alert.
- The watcher calls the notifier only when the state of a PR changes. The first poll of a PR records its state and sends no alert.

## Acceptance criteria

- [ ] **A.** Run `/babysit` on a PR → the watcher polls `gh` in the background, writes `~/.cache/babysit/state.json`, and calls the notifier only when the state of a PR changes. Watch a stack → the watcher polls only the lowest PR that is not merged.
- [ ] **B.** Hydrate `install-agents-md` → the `tools` block has a Notifier row, and `HYDRATE.md` names the key and where to look for it on the machine.
- [ ] **C.** Render the status line with a state file → line 1 shows one chip for each watched PR on the right, in urgency order, with a done chip gone after 10 minutes. Render it twice with the same transcript size → the second render reads the token count from the cache.
- [ ] **D.** Change the CI state of a watched PR → the notifier fires once, the chip shows the new state, and the leading spaces of the chips survive in the real status line.
