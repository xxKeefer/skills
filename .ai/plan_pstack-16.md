---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills
branch: pstack-16_babysit
status: approved
goal: "A CI change on a watched PR shows a notification and the right chip, and leading spaces survive in the real status line."
spec: .ai/spec_pstack-16.md
---

# Plan: pstack-16 `babysit` and the status line chips

## Goal

Make the status line cheaper first, then add `/babysit`, its watcher script, the notifier role, and the PR chips on line 1. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-16.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Run `/babysit` on a PR → the watcher polls `gh` in the background, writes `~/.cache/babysit/state.json`, and calls the notifier only when the state of a PR changes. Watch a stack → the watcher polls only the lowest PR that is not merged.
- [ ] **B.** Hydrate `install-agents-md` → the `tools` block has a Notifier row, and `HYDRATE.md` names the key and where to look for it on the machine.
- [ ] **C.** Render the status line with a state file → line 1 shows one chip for each watched PR on the right, in urgency order, with a done chip gone after 10 minutes. Render it twice with the same transcript size → the second render reads the token count from the cache.
- [ ] **D.** Change the CI state of a watched PR → the notifier fires once, the chip shows the new state, and the leading spaces of the chips survive in the real status line.

## Context

- Map: `.ai/map_pstack-program.md`, unit 16. Done line: a CI change on a watched PR shows a notification and the right chip, and leading spaces survive in the real status line.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Step 1 removes cost from `statusline.sh` before step 3 adds the chips. The watcher keeps one state file, and the ticker keeps no state.
- Model: each subagent runs at `sonnet`, by the user's request.
- Production gate: none. `/babysit` does nothing until the user runs it, and the chip segment draws nothing when `~/.cache/babysit/state.json` does not exist. The installed status line changes only when the user runs `/setup-statusline` again.
- Push-only map: this run uses no `gh` command on this repo. Tests put a fake `gh` script first on `PATH`. The push step runs `git push -u origin pstack-16_babysit`.
- Evidence rule: the repo is public. Proof runs use a temporary `HOME`, never the real `~/.cache` or `~/.claude`.
- Status line facts from the Claude Code docs: the script gets `COLUMNS`, and `refreshInterval` has a minimum of 1. The docs do not say if the leading spaces of a line are kept, so the user checks that by eye (step 5 QA).
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `python3 skills/utility/skills/setup-statusline/statusline.spec.py`, `python3 skills/engineering/skills/babysit/scripts/watch_prs.spec.py`, `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, `sh .githooks/pre-commit_test.sh`, and `sh .githooks/commit-msg_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the state of a PR from the `gh` fields | M | new code with many branches; a wrong state gives a wrong alert |
| A | an alert only on a change | M | an alert on each poll is noise, and no alert defeats the unit |
| A | the lowest PR of a stack | M | new code; a wrong pick polls a PR that waits on its base |
| A | one `run` loop at a time | L | a second loop sends each alert twice; a pid file guards it |
| B | the Notifier row and the HYDRATE key | L | text in a template |
| C | the chips: order, alignment, ticker, done expiry | M | new code in a script that runs each second on each session |
| C | the token cache and the one `jq` read | M | a refactor of a script with no tests; a wrong read blanks line 2 |
| D | the live alert and the leading spaces | M | the docs do not say if Claude Code keeps leading spaces |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | C | for the two sample payloads of `/setup-statusline` Step 5, the output after the refactor is byte-equal to the output before it | use case | Integration | `statusline.spec.py` |
| C2 | C | a second render with the same transcript size gives the same tokens and does not parse the transcript; a larger transcript parses again | state transition | Integration | `statusline.spec.py` |
| C3 | A | each row of the state table maps the `gh` fields to its state: done, failed, stale, threads, pending, ready, and review required gives pending | decision table | Unit | `watch_prs.spec.py` |
| C4 | A | the first poll of a PR sends no alert; a poll with the same state sends no alert; a poll with a new state sends one alert with the PR and the new state | state transition | Integration | `watch_prs.spec.py` |
| C5 | A | with PRs A (base `main`) and B (base A's head), the poll calls `gh` for A only; after A is done, the next poll calls `gh` for B | use case | Integration | `watch_prs.spec.py` |
| C6 | A | `run` exits when no watched PR is open; a second `run` while the pid in the pid file is alive exits at once | state transition | Integration | `watch_prs.spec.py` |
| C7 | A | `notifier_command` is `none` or absent → no call and no error | equivalence partition | Integration | `watch_prs.spec.py` |
| C8 | C | with a state file of six PRs, one in each state, the chips are in the order red, amber, blue, yellow, green, grey, and the line is `COLUMNS` columns wide | use case | Integration | `statusline.spec.py` |
| C9 | C | a done PR with `done_at` more than 600 seconds ago has no chip | boundary value | Integration | `statusline.spec.py` |
| C10 | C | when the chips do not fit, red and amber chips stay on the left, and the window of the other chips moves one column per epoch second | use case | Integration | `statusline.spec.py` |
| C11 | C | with no state file, line 1 is the same as before the change | equivalence partition | Integration | `statusline.spec.py` |

### Not testing

- A real `gh` call and a real desktop alert: the run uses no `gh` command on this repo. The QA checklist gives the user a live check.
- The leading spaces in the real Claude Code status line: only the user can see it. It is a `you` row in the QA checklist.

## Steps

- [x] **1. Subtract: one `jq` read and the token cache in `statusline.sh`.** Seam: `statusline.sh`, stdin JSON to stdout. Conditions: C1, C2.
  - Before you change the script, save its output for the two sample payloads of `/setup-statusline` Step 5, with a fixed `HOME`, as the C1 fixtures.
  - Replace the eight `jq` reads of `$input` with one `jq` call that prints each field on its own line.
  - Cache the token count in `${XDG_CACHE_HOME:-$HOME/.cache}/statusline/tokens`, keyed by the transcript path and its size. Parse the transcript only on a miss.
  - Add `statusline.spec.py` beside the script.
  - Done: `statusline.spec.py` passes C1 and C2.
- [x] **2. The watcher script.** Seam: `watch_prs.py` commands `add`, `poll`, and `run`. Conditions: C3, C4, C5, C6, C7.
  - Add `engineering/skills/babysit/scripts/watch_prs.py`. It keeps the watch list and the last state in `~/.cache/babysit/state.json`: one entry for each PR, with `repo`, `number`, `head`, `base`, `state`, `threads`, and `done_at`.
  - `add <owner/repo> <number>` adds a PR. `poll` runs one pass: for each open PR that is the lowest of its stack, it calls `gh pr view` for the fields of the state rule, and `gh api graphql` for the count of unresolved review threads. It writes the file atomically. It calls `notifier_command` from `~/.claude/agents-md.values.json` with a title and a body, only when a known state changes.
  - `run [--interval <seconds>]` polls in a loop and exits when no watched PR is open. It writes its pid to `~/.cache/babysit/run.pid`, and exits at once when that pid is alive.
  - Add `watch_prs.spec.py` with a fake `gh` first on `PATH` and a temporary `HOME`.
  - Done: `watch_prs.spec.py` passes C3 to C7.
- [x] **3. The chips on line 1.** Seam: `statusline.sh`, with a state file. Conditions: C8, C9, C10, C11.
  - Read `~/.cache/babysit/state.json` with one `jq` call that sorts by urgency and drops a done PR older than 600 seconds.
  - Draw each chip as ` <symbol> <number> ` on a background colour, from the chip table in the spec. Right-align the chips on line 1 with `COLUMNS`.
  - When the chips do not fit, pin the red and amber chips on the left, and show a window of the other chips that starts at `epoch second mod length`.
  - Set `refreshInterval: 1` in the `statusLine` setting that `/setup-statusline` writes.
  - Add the tests to `statusline.spec.py`.
  - Done: `statusline.spec.py` passes C8 to C11, and C1 still passes.
- [x] **4. The skill, the notifier role, and the docs.** Kind: docs.
  - Add `engineering/skills/babysit/SKILL.md`: take PR numbers, or a stack, and run `add` for each. Start `run` detached with `nohup`, once. Name the chip table and the state file. Tell the user how to stop it.
  - Add a Notifier row to `install-agents-md/sections/tools.md`, and a `notifier_command` row to `HYDRATE.md`, with an example for Linux and for macOS.
  - Update the `setup-statusline` SKILL and README for the chips and `refreshInterval`, and add `/babysit` to the `engineering` README table.
  - Done: the skill and the docs name the state file, the chip table, and the notifier key, and `install_agents_md.spec.py` passes.
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green: statusline.spec.py, watch_prs.spec.py, install_agents_md.spec.py, pre-commit_test.sh, commit-msg_test.sh all pass.
- [x] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-16.md`. This step changes no code.
  - Done: the report is `.ai/review_pstack-16_babysit.html`. Reviewed: base f33d9fd, head 9ffdc2a (panel read a6ac67b). The fix commit 9ffdc2a holds 3 fixes, and 3 nits stay open.
- [x] **7. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green on 9ffdc2a: statusline.spec.py, watch_prs.spec.py, install_agents_md.spec.py, pre-commit_test.sh, commit-msg_test.sh.
- [x] **8. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-16.md`. This step changes no code. The rows that stay open from `.ai/review_pstack-16_babysit.html` (the three code-quality nits) are not raised again.
  - Done: the report is `.ai/review_pstack-16_babysit.html` (run 2). Reviewed: base f33d9fd, head 9ffdc2a. Fix commit acf5b53 holds 3 fixes: a failed gh call no longer kills the loop, add keeps a poll result, and the token cache is capped. The 3 nits from run 1 stay open.
- [x] **9. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green on acf5b53: statusline.spec.py, watch_prs.spec.py, install_agents_md.spec.py, pre-commit_test.sh, commit-msg_test.sh.
- [x] **10. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-16.md`. This step changes no code. The rows that stay open from `.ai/review_pstack-16_babysit.html` (the three code-quality nits) are not raised again.
  - Done: the report is `.ai/review_pstack-16_babysit.html` (run 3). Reviewed: base f33d9fd, head acf5b53 (branch tip 0cf13f6 adds only plan docs). No finding, so no fix commit.
- [x] **11. Push.** Push the branch with `git push -u origin pstack-16_babysit`. The map is push-only, so open no PR.
  - Done: pushed `origin/pstack-16_babysit`.

## Suggested skills

- `/build @.ai/plan_pstack-16.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-16.md`: one step per session, from the worktree.
- `/tdd`: steps 1, 2, and 3.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-inspired`, for the branch `pstack-16_babysit`.
- Decision log: decisions_pstack-16.tsv
- 2026-11-17: five judgement calls written to `decisions_pstack-16.tsv`.
- 2026-11-17: step 1 done in commit 883c074. `statusline.sh` has one `jq` read and the token cache. `statusline.spec.py` passes C1 and C2. The C1 fixtures are in `skills/utility/skills/setup-statusline/fixtures/`.
- 2026-11-17: step 2 done in commit f11f7b7. `watch_prs.py` has `add`, `poll`, and `run`. The state file is a JSON list. `add` calls `gh pr view` once, to read the head and base of the PR. `watch_prs.spec.py` passes C3 to C7. Step 3 reads the same list: each entry has `repo`, `number`, `head`, `base`, `state`, `threads`, and `done_at`. The `state` values are done, failed, stale, threads, pending, and ready.
- 2026-11-17: step 3 done in commit 193baa2. `statusline.sh` draws the chips with one `jq` call, and `refreshInterval: 1` is in the `setup-statusline` SKILL and README. `statusline.spec.py` passes C1, C2, and C8 to C11. The leading spaces in the real status line need the user's eye (step 5 QA).
- 2026-11-17: step 4 done in commit b1becaf. `babysit/SKILL.md` runs `add` for each PR, then starts one `run` with `nohup`. The Notifier row is in `tools.md`, and `HYDRATE.md` has `notifier_command` and `notifier_notes`. The chips are in the `setup-statusline` SKILL and README. `/babysit` is in the `engineering` README table. All five gates pass.
- 2026-11-17: step 6 done. Light review in `.ai/review_pstack-16_babysit.html`: base f33d9fd, head 9ffdc2a. Fix commit 9ffdc2a: `poll` no longer loses a PR that `add` writes mid-poll, two classify rows for commit statuses, and the committed pyc is gone. Three code-quality nits stay open.
- 2026-11-17: step 8 done. Light review run 2 in `.ai/review_pstack-16_babysit.html`: base f33d9fd, head 9ffdc2a. Fix commit acf5b53 (3 fixes, test-first). One reviewer read the code, with no lane subagents.
- 2026-11-17: step 10 done. Light review run 3 in `.ai/review_pstack-16_babysit.html`: base f33d9fd, head acf5b53. No finding that a run proves. One reviewer read the code, with no lane subagents.
- 2026-11-17: blast-radius (base f33d9fd): verdict clear, rung 4. Safety fact: `statusline.sh` exits 0 and draws line 1 and line 2 for each of: no state file, a malformed or wrong-shape state file, `COLUMNS` unset, empty, or non-numeric, and empty or garbage stdin; and the C1 output is byte-equal. Command: run `HOME=<tmp> python3 -I skills/utility/skills/setup-statusline/statusline.spec.py` (8 tests OK), then `env -i PATH="$PATH" HOME=<tmp> COLUMNS=<v> bash statusline.sh < fixtures/payload_full.json` against `<tmp>/.cache/babysit/state.json` set to `''`, `{`, `null`, `{"a":1}`, `[null]`, `[1,"x"]`. No confirmed risk. Open notes: an old `agents-md.values.json` makes `install_agents_md.py` exit 1 with `missing value notifier_command` and write nothing, until the user adds the two keys (documented in SKILL Step 2). The chip line is exactly `COLUMNS` wide, so a UI that pads the status line may wrap it (user check, step 5 QA). Not run: bash 3.2 and jq 1.6 (read only).
- 2026-11-17: `/ship` checks go: the patch-id of the reviewed head acf5b53 matches HEAD. Pushed `origin/pstack-16_babysit`, and ticked unit 16 on the map. Map playbook: next is step 8, the `/retro` offer (H5).
- 2026-11-17: `/retro` (H5): the user approved all 9 rows. Rows 1 to 7 are applied in 7a7f981, 738d489, 0865096, and the calibration backlog. Rows 8 and 9 are report only. Next: the home machine opens the PR into `pstack-inspired`, reviews it, and merges it (H4). Then `/work-on @.ai/map_pstack-program.md` starts unit 17.

## Follow-ups

- The chip line is exactly `COLUMNS` wide. If Claude Code pads the status line, the chips can wrap. QA row Y1 checks it. A gap one or two columns narrower is the fix. From `/blast-radius`.
- Run the chip render once on macOS with bash 3.2 and jq 1.6. Only checked by reading. From `/blast-radius`.
