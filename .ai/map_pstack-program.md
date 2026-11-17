---
doctype: map
source: conversation
created: 2026-11-16
status: approved
repo: xxKeefer/skills
batch: 1
push_only: true
goal: Adopt the pstack philosophy as one program. One router runs the skills, claims are proven by a run, and a feedback loop raises quality.
---

#raw #skills #pstack

# Map: the pstack program

This map holds one program of 33 units for the `xxkeefer-skills` repo. Each unit is one PR into the feature branch, built one at a time. A grill on 2026-11-16 approved every decision below. An agent on any machine can run the program from this file alone.

Sources:

- The research report: `~/studio/notes/05-projects/agentic-skills/reports/research_pstack.html` (run 1, rows r1.1 to r1.26).
- pstack: https://github.com/cursor/plugins/tree/main/pstack
- The worktree note: `~/studio/notes/00-notes/worktree-names-for-stacked-prs-20261116.md`

## How to run this map

All program work happens in one worktree folder, `pstack-inspiration`, beside the main checkout: `~/studio/code/pstack-inspiration` beside `~/studio/code/xxkeefer-skills`. The main checkout stays on `main` as the fallback. This map lives in the worktree at `.ai/map_pstack-program.md`. Git tracks `.ai/`, and the repo is public.

### The branches

`main` stays pure until the whole overhaul is done. The long-lived feature branch `pstack-inspired` is the trunk. Each unit is one branch and one PR into the trunk, one unit at a time.

```
main                              untouched until the end
 └── pstack-inspired              the trunk: each merged unit lands here
      └── pstack-7_<short-desc>   one PR, merged into the trunk after review
```

Units 1 to 6 were built as six stack layers, then merged into `pstack-inspired` (PRs #45 to #51). From unit 7 on, each unit is one PR into the trunk. The machine already loads the skills from `pstack-inspiration`, and `enabledPlugins` has no `"experimental@xxkeefer-skills"`.

### Two machines

- **The build machine** (work) builds each unit and pushes its branch. Its `gh` account is a work account, so it runs no `gh` command on this repo. Git pushes use the `github-personal` SSH host, which signs in as the repo owner.
- **The home machine** opens each PR, reviews it, and merges it into `pstack-inspired`. It also runs any `gh stack` command, if the units ever need a stack.

### Before you start (build machine)

1. Check that the `xxkeefer-skills` marketplace `path` in `~/.claude/settings.json` names `~/studio/code/pstack-inspiration`.
2. In `pstack-inspiration`, check out `pstack-inspired`, then run `git pull`.
3. Start a new session in `pstack-inspiration`, and check that `/work-on` is in the `/` menu. If it is not, run `/plugin marketplace update xxkeefer-skills`, then reinstall `engineering@xxkeefer-skills` with `/plugin`.

### One unit (build machine)

1. Run `/work-on @.ai/map_pstack-program.md`. The map's `batch: 1` and `push_only: true` keys set a batch of one unit, no `gh` command, and a `git push` in place of a PR.
2. `/work-on` plans the unit, builds it on its branch, `pstack-<N>_<short-desc>`, pushes it, and ticks the unit. It does not stop for the plan, because this map's approval (H0) covers it.
3. Run `/retro` when `/work-on` offers it, or say no.

### One unit (home machine)

1. Open a draft PR from the unit branch into `pstack-inspired`.
2. Review the PR. Commit a review fix on the unit branch, then push it.
3. Mark the PR ready, then merge it into `pstack-inspired`.

Start the next unit on the build machine only after this merge. Then run `git pull` on `pstack-inspired` first, so that the new branch has the unit below it. If a unit must start before the merge, branch it from the last unit's branch. Then the home machine turns the two PRs into a stack.

### Rules

- No program commit goes to `main`.
- A fix to unit N goes on its own branch, if its PR is still open. After the merge, the fix goes into the next unit, or into its own PR into `pstack-inspired`.
- If the user commits to `main` for another reason, merge `main` into `pstack-inspired` on the home machine. Then run `git pull` on `pstack-inspired` on the build machine.
- To go back, change the marketplace `path` to the main checkout (see Trial).
- Tick a unit on this map when its branch is pushed.
- Only the top unit (33) changes a `plugin.json` version.
- Git tracks this map, and the repo is public. Keep work facts out of the map and out of every unit. The scrub hook checks both.
- Follow the repo's `CLAUDE.md`, `CONTEXT.md`, and `meta/writing-great-skills`.

## Trial

The user uses the trunk only after the last unit:

1. In `pstack-inspiration`, check out `pstack-inspired`, then run `git pull`.
2. Check that the marketplace `path` names `pstack-inspiration`, and that `enabledPlugins` has no `"experimental@xxkeefer-skills"`.
3. Run `/plugin marketplace update xxkeefer-skills`, then start a new session.
4. Run `/install-rules`, `/setup-statusline`, and `/install-agents-md` from the branch.
5. Use it for a few days. Then, on the home machine, merge `pstack-inspired` into `main` with one PR. This is the first program commit on `main`.

To go back:

1. In `~/.claude/settings.json`, change the marketplace `path` back to the main checkout, which is still on `main`.
2. Add `"experimental@xxkeefer-skills": true` to `enabledPlugins` again.
3. Run `/plugin marketplace update xxkeefer-skills`, then start a new session.
4. Run the same three installers from `main`.

After the merge, change the marketplace `path` back to the main checkout, and pull `main` there. Then remove the worktree: `git -C ~/studio/code/skills worktree remove ../skills.pstack-6_work-on`.

## Decisions

### Autonomy and the HITL line

- The HITL line moves from skills to actions. The workflow skills lose `disable-model-invocation`, so the router and other skills can call them. You can still type each one.
- Skills whose job needs the user's judgement keep the flag: `grill`, `retro`, `roleplay`, the journal skills, and the `meta` skills that change the marketplace. The 24 principle skills also keep it (see Principles).
- **The pause rule:** an action stops for the user when another person reads its output. Output only for the user or the agent runs with no stop.
- **The pause list:** mark a PR ready for review, merge, force-push to a branch another person uses, deploy, delete data or a branch that is not merged, post a comment, a review, or a ticket update as the user, write a ticket, and send a message to a person.
- These run with no stop: the end of a ★ skill, a test or review round, a push to the agent's own branch, and a draft PR. The draft PR's Why section comes from the approved spec, so it carries the user's intent.

### The stops

| Stop | What | When |
| --- | --- | --- |
| H0 | The user approves the map. | Once per program. |
| H1 | The user says yes to the spec. | Once per change, when a spec exists. |
| H2 | The user approves the plan. | Once per change. A map run has no H2 stop, because H0 covers each unit plan. |
| H3 | An open `Pending Decision` (a `D` entry) exists. | Only when the agent cannot decide. |
| H4 | An action is on the pause list. | Each time another person reads the output. |
| H5 | The user picks the skill edits from `/retro`. | After a unit. |

Ticking a report's rows is a stop only for a report the user reads, such as a review of another person's PR. In the user's own build loop, the review fixes each row with no stop.

### The flow for one unit of work

```
 you + /grill
      │
      ▼
 ┌─────────┐
 │   map   │  [H0] you approve the map
 └────┬────┘
      │  the router picks the next unit with no tick
      ▼
 needs its own design? ──yes──► /spec ──► ┌──────┐
      │                                   │ spec │  [H1] you say yes
      │ no                                └──┬───┘
      │◄─────────────────────────────────────┘
      ▼
 /plan reads the unit, plus the spec and any findings
      │
      ▼
 ┌─────────┐
 │  plan   │  [H2] you approve the plan
 └────┬────┘
      │  /build runs each step
      ▼
 ┌──────────────── build loop ─────────────────┐
 │ a step runs, then it:                       │
 │   - writes its Progress entry in the plan   │
 │   - appends a row to decisions.tsv          │
 │   - meets an unknown: /diagnose -> findings │
 │ test + review write a report, then:         │
 │   - a row with a fix: a new fix step        │
 │   - a row with no fix: a D entry   [H3]     │
 └──────────────────────┬──────────────────────┘
                        │
                        ▼
               /ship opens a draft PR
                        │
                        ▼  [H4] you mark it ready and merge
          the unit gets its tick on the map
                        │
                        ▼
      /retro reads decisions.tsv and the reports
                        │
                        ▼  [H5] you pick the skill edits
          back to the map for the next unit
```

`decisions.tsv` closes the loop. During a build, each choice the agent makes without the user adds a row. `/sitrep` reads it during a run. `/retro` reads it after the PR, compares each decision with its result, and proposes skill edits.

### File types

Five parsed layouts, plus `scratch`. `write-to-file` owns the templates and refuses any other doctype. Each markdown layout keeps its header in YAML frontmatter (`doctype`, `ticket`, `worktree`, `branch`, `status`, `goal`).

| Type | Holds | Writer | Reader |
| --- | --- | --- | --- |
| `map` | the order of many units, shared decisions, a tick per unit | a grill | `/plan`, one unit at a time, and the user |
| `spec` | what to build for one change, and why | `/spec` | `/plan` |
| `plan` | `Goal`, optional `Spec`, `Steps`, `Progress`, `Pending Decisions`, `Follow-ups` | `/plan`, `/update-plan` | `/do-next`, `/build`, `/work-on` |
| `findings` | a question, its answer, the evidence, open points | `/diagnose`, spike work | the user, `/spec`, `/plan` |
| `report` | HTML with a JSON `runs` block and rows to tick | `/write-report` | the user, then `/build` |
| `scratch` | anything | anyone | nobody |

- `plan` absorbs the old handoff and the vault Ticket. "Handoff" now means only the act of writing `Progress`.
- After approval, only `Progress`, `Pending Decisions`, and `Follow-ups` change in a plan.
- `findings` replaces `spike`, `hunt`, `risks`, and `research` markdown files.
- In-flight files are migrated once by a script. No parser accepts the old header.
- One pstack PR section maps to one plan file. A stack is a map that points at one plan per PR.

```
                     ┌──────────┐
                     │ findings │
                     └──┬────┬──┘
               evidence │    │ evidence
                        ▼    │
                     ┌──────┐│
                     │ spec ││
                     └──┬───┘│
             /plan reads│    │
                        ▼    ▼
┌─────┐  unit section  ┌──────────┐  /build writes   ┌────────┐
│     ├───────────────►│          ├─────────────────►│        │
│ map │                │   plan   │                  │ report │
│     │◄───────────────┤          │◄─────────────────┤        │
└─────┘ PR exists:tick └────┬─────┘   ticked rows    └────────┘
                            │
                            │ Progress links
                            ▼
                     ┌───────────────┐
                     │ decisions.tsv │
                     └───────────────┘
```

### The router: `/work-on`

- Lives in `engineering/work-on/`, user-only. It maps to pstack's `poteto-mode`.
- It picks a playbook from `playbooks/`. A playbook is an ordered list of skill calls, the stop between them, and a done line. The first playbook is "new ticket": spec, plan, build, ship, then an offer to run `/retro`.
- It calls the ★ skills. It does not replace them, and it does not copy their own routing.
- It copies the playbook steps into the todo list. A skipped step stays, with a reason (r1.17).
- It writes the plan at each stop, then ends with one line that names the stop and the command to continue.
- It holds the principles index (see Principles).

### Principles

- Take all 24 pstack `principle-*` skills, with pstack's names, into `engineering`. Each keeps `disable-model-invocation: true`, so it costs no context, and the user can type it on a smell.
- `/work-on` holds an inline index in pstack's five groups (Core, Architecture, Verification, Delegation, Meta), with one "when it applies" line each.
- The agent reads a principle's `SKILL.md` by path when it applies it. A skill that runs without the router names its principles in bold, with a sibling path such as `../principle-fix-root-causes/SKILL.md`.
- The reply names each principle that shaped a decision. The agent cites only a principle it read in this session.
- Adapt two: `principle-never-block-on-the-human` points at the pause list, and `principle-guard-the-context-window` points at subagents and `/checkpoint`.

### TDD

TDD by default. Skip a test only when it would be expensive, integration-heavy, or unclear, and use the closest real check instead (`/verify` when the repo has a driver). A skip is never silent: the plan step stays, marked skipped with its reason, and `/sitrep` shows it.

### Comments

- No comments in any code that the user or the agent writes, in every repo. This includes docblocks.
- Two exceptions: a tool directive (`eslint-disable-next-line`, `@ts-expect-error`) whose reason a check enforces, and a comment that the repo's lint requires.
- `persona-comments` has two lenses. On the user's branch, each added comment is a finding. On another person's PR, the current rules stay.

```
 an added comment
        │
        ▼
 the ladder, applied now (no stop)
   1. a better name
   2. a type
   3. a test whose title states the fact
   4. a check that fails with the fix in its error
   5. delete it
        │
        ▼
 did the comment mark a hack? ──no──► done
        │ yes
        ▼
 /blast-radius on the architectural fix
        │
        ├── small, inside the change's scope ──► a new step in the plan
        │
        └── too big, or outside the scope ────► a Follow-up entry in the plan
                                                  │
                                                  ▼
                                    /sitrep and the PR's notes show it,
                                    you decide whether a ticket is written
```

### Verification drivers

- A driver is a plain skill named `verify-<repo>-<app>`. An app or a library each get one. A library is driven as its consumer uses it: Storybook, a PTY, or a scratch consumer script.
- Work repos: the driver lives in `~/.claude/skills/`. The user's own repos (owner `xxKeefer` or `daniel-keefer`): it lives in the repo's `.claude/skills/`, committed.
- `/verify` is a thin router. It reads the repo from `git remote`, finds the apps from the diff paths, and calls each `verify-<repo>-<app>`. With no match, it returns "no driver", and the test step writes that in `Progress`. `/retro` then proposes `/create-verification-skill`.
- A driver's `SKILL.md` has Launch, Doctor, Drive, Evidence, Cleanup, and Helpers. `features/README.md` indexes one file per feature. Each feature file has `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.
- pstack sources: `create-verification-skill`, `maintain-verification-skill`, and `references/feature-map-example`.

```
 /create-verification-skill   (once per repo app)
        │ explores the app, writes
        ▼
 ┌──────────────────────┐   fixes stale steps   /maintain-verification-skill
 │  verify-<repo>-<app> │◄──────────────────────  after a failed run, or when
 │ Launch  Doctor       │                         the feature map is out of date
 │ Drive   Evidence     │
 │ Cleanup Feature map  │
 └──────────┬───────────┘
            │ called through /verify by
            ├──► /test            build loop: the agent runs the happy path itself
            ├──► /interrogate     a finding stays only if a run proves it
            ├──► /blast-radius    the "ran it" and "saw it live" rungs
            ├──► /qa-screenshots  drives to each screen to capture it
            └──► /benchmark       drives the flow that it times
```

### Models

A `models` managed block in `~/.claude/AGENTS.md`. A skill names a role, not a model.

| Role | Who | Model | Effort |
| --- | --- | --- | --- |
| judgement | `/work-on`, `spec`, `plan`, `grill`, `retro`, review triage | `opus` | medium |
| worker | each `build` step, `implement`, `fix` | `opus` | medium |
| mechanical worker | a step `/plan` marks mechanical: rename, codemod, move | `sonnet` | medium |
| reviewer | each persona lane | `opus` | medium |
| mechanical reviewer | a lane whose `PANEL.md` line says `sonnet` | `sonnet` | medium |
| verifier | `/verify` drives | `sonnet` | medium |
| prover | `interrogate`, `blast-radius` | `opus` | high |
| panel | `interrogate`, design-it-twice | `opus` high, `sonnet` high, the session model | as listed |
| explorer | read-only search, source checks | `haiku` | low |

1. After two failed fixes on one premise, the next attempt moves one effort step up, to a ceiling of Opus max. The decision log records each step.
2. Fable runs only when the user asks, in the prompt or in a plan step.
3. The user can override a mechanical mark at H2. `PANEL.md` stays as an override for one lane.

### Status line chips

- Line 1 keeps the branch and the cwd on the left. The chips sit on the right of line 1, aligned with `COLUMNS`. One chip per watched PR: a background colour, a symbol, and the PR number.
- Only uniform-width characters, in the family of `◀ ▶ ●`. No emoji.
- Order by urgency: red, amber, blue, yellow, green, grey.

| State | Chip | Colour | Meaning |
| --- | --- | --- | --- |
| Failed | ` × 101 ` | red | CI failed. |
| Stale | ` ! 105 ` | amber | The base moved, so the PR needs `gh stack sync`. |
| Threads | ` ◆2 102 ` | blue | Two review threads wait for an answer. |
| Pending | ` ○ 103 ` | yellow | CI is queued or running. |
| Ready | ` ● 104 ` | green | CI green, and approved or no review needed. |
| Done | ` ◌ 100 ` | grey | Merged or closed. The chip goes after 10 minutes. |

```
pstack-16_babysit · ~/s/c/pstack-inspiration            [× 101] [◆2 102] [○ 103] [● 104] [◌ 100]
```

When the chips do not fit, a ticker moves one column for each redraw (`refreshInterval: 1`). Red and amber chips are pinned on the left of the ticker. The `|` marks show the ticker window and are not drawn.

```
t=0   ...xxkeefer-skills   [× 101] |[◆2 102] [○ 103] [● 1|
t=1   ...xxkeefer-skills   [× 101] |◆2 102] [○ 103] [● 10|
t=2   ...xxkeefer-skills   [× 101] |2 102] [○ 103] [● 104|
```

- The chip segment reads only `~/.cache/babysit/state.json`, with no network call.
- The token count is cached by the transcript's file size, so the 1-second refresh stays cheap.
- Claude Code docs: `COLUMNS` is set for the script, `refreshInterval` has a minimum of 1. The docs do not say whether leading spaces are kept, so unit 16 must prove that by a run.
- A TUI is deferred. It can read the same JSON file.

### Files outside the repo

`utility/install-agents-md` writes managed blocks into `~/.claude/AGENTS.md`. The repo holds only generic text, and the machine facts are hydrated on the machine.

- Each block sits between `<!-- managed: <name> -->` and `<!-- end managed -->`. The first run puts the blocks at the top. A later run replaces only the text inside the markers.
- `HYDRATE.md` tells the agent how to fill each machine fact (for example, the notifier product), and asks the user to confirm.
- Text outside the markers is the user's own. The installer can list edits for it, such as the system map line `<repo>.<KEY>/`, but does not apply them.
- Each run first copies the file to `AGENTS.md.bak`.
- The first run shows the old plain-text sections beside the new blocks, and the user confirms the deletion of the old text.
- The worktrunk template is a separate step that asks first, because `wt step relocate` moves folders and the plans' `Worktree:` lines need an update.

### Domains and lifecycle

- `experimental` goes away. A new skill lands in its domain.
- A skill that falls out of favour moves to `deprecated` with `deprecated: <date>` in its frontmatter. After about a month, it is deleted.
- Moves: `retro`, `stand-up`, and `tidy-up` to `engineering`. `simulate` and `roleplay` to `primitives`. `lobotomize` to `deprecated`.
- Names: `/work-on`, `/checkpoint`, `/sitrep`, `/why`, `/verify`, `update-plan`. ADR 0005 requires unique names. The user's planned general self-improve skill for `meta` needs a name other than `self-improve`, which `engineering` already uses.
- Candidate to retire after the trial: `/do-next`. Do not move it during the program.

## Units

### [x] 1. ADR 0016, the pause list, callable workflow skills

- Write ADR 0016: the HITL line moves from skills to actions. Update the HITL row in `CONTEXT.md`.
- Add the pause rule and the pause list as a rule file in `install-rules/rules/`.
- Remove `disable-model-invocation` from the workflow skills. Keep it on the skills named in Decisions.
- Remove the line in `build/SKILL.md` that says the agent cannot run `/ship`.
- Done: the agent runs `/plan` after `/spec` when asked, and stops at an action on the pause list.

### [x] 2. Remove `experimental`

- Move `retro`, `stand-up`, `tidy-up` to `engineering`. Move `simulate`, `roleplay` to `primitives`. Move `lobotomize` to `deprecated` with today's date.
- Delete the `experimental` domain and its registry entry.
- A machine with `"experimental@xxkeefer-skills"` in `enabledPlugins` must delete that line. The bootstrap steps and the trial steps say so.
- Replace the Skill Maturity section in `CLAUDE.md` with the dated lifecycle. Write an ADR.
- Add `retire-a-skill/scripts/due.py`: list each deprecated skill over 30 days old, with its count from the skill tally.
- Done: no skill lives in `experimental`, and `due.py` lists `lobotomize` after 30 days.

### [x] 3. Rename "handoff" to "plan"

- Rename `update-handoff` to `update-plan`. Update about 41 files that say "handoff" (234 uses). Check each use for its meaning.
- Change the vault Ticket term in `CONTEXT.md` to the plan.
- No change in behaviour.
- Done: `grep -ri handoff skills docs CONTEXT.md` finds only the act of handing off.

### [x] 4. The plan layout (r1.4, r1.17)

- Template with frontmatter and the sections from Decisions, including `Follow-ups`. Most sections are optional.
- `write-to-file/scripts/check_plan.py` and `check_plan.spec.py`. Checks: header keys exist, the worktree exists, each step has a done line, each behaviour step names its seam and tests, each step is done, open, or skipped with a reason, count the open `Pending Decisions`. Exit 0 or 1. Each error names the line and the fix.
- A migration script for in-flight plans. No dual parser.
- `write-to-file` refuses a doctype outside the set.
- `plan`, `start-ticket`, `split-ticket`, and `promote-card` write the layout. `do-next`, `update-plan`, and `build` run the check. `primitives/handoff` writes a short plan.
- User note (r1.4): offload as much deterministic work to scripts as possible.
- Done: `/plan` on a ticket writes a plan that passes the check, and a broken plan fails with the line to fix.

### [x] 5. The spec layout

- Template and a check for `spec`. `spec` writes it, and `plan` reads it.
- Done: `/spec` then `/plan` with no hand edits between them.

### [x] 6. `/work-on`, the "new ticket" playbook, and the map playbook (r1.16)

- `engineering/work-on/SKILL.md`, user-only, `playbooks/new-ticket.md`, and `playbooks/map.md`.
- The stops from Decisions. The todo rule. The one-line end at a stop.
- The goal restated in each `build` subagent brief and in the `create-pr` Why section.
- The map playbook reads a map in this file's shape: each unit is a heading `### [ ] N. Title`, with a `Done:` line. For each batch of about 5 units with no tick, in order:
  1. Run `/plan` on each unit section, in the current worktree.
  2. Stop once, so the user approves the batch of plans (H2).
  3. For each unit: `gh stack add pstack-<N>_<short-desc>`, then `/build` on its plan in a fresh subagent.
  4. Tick each unit on the map when its build is done.
  5. Run `gh stack submit --auto` at the end of the batch. Draft PRs need no stop.
  6. Offer `/retro` on the batch, then start the next batch.
- Done: `/work-on <ticket>` takes a ticket to a draft PR and stops only at H1, H2, H3, and H4. `/work-on @<map>` builds the next batch of units as stack layers, with one stop for the plans.

### [x] 7. `install-agents-md` and the models block (r1.10)

- `utility/install-agents-md` as in Decisions, with `sections/`, `HYDRATE.md`, and the backup.
- Blocks: `coding` (the TDD rule), `tools` (the role table), `models` (the model table).
- `build`, `implement`, `mob-review`, and `/work-on` name roles and read the block.
- Done: a run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a second run changes nothing.

### [x] 8. Principles and the TDD skip rule (r1.2)

- 24 `principle-*` skills from pstack, user-only, in `engineering`. Adapt the two named in Decisions.
- The index in `/work-on`. The reply rule and the "read it first" rule.
- The skip rule in `engineering/tdd`.
- User note (r1.2): keep them skills, so the user can call one on a smell. A rule file gets lost in context drift.
- Done: `/work-on` on a task names the principle that shaped a choice, and the principle's file was read in that session.

### [x] 9. `interrogate` (r1.1)

- `engineering/interrogate` (new). Adversaries try to break a change. A finding stays only if a re-run command proves it. Others go to a Dropped list.
- `/work-on` runs it after the build loop when `blast-radius` finds risk. Uses the panel models.
- Done: on a branch with a planted bug, the report keeps the proven finding and drops an unproven one.

### [x] 10. `blast-radius` (r1.3)

- `engineering/blast-radius` (new). The ladder: said it, pointed at the line, walked it, ran it, saw it live. Prove by a run the one fact that makes the change safe. List what was cleared.
- Done: on a change, the output names the rung reached and the command that proved it.

### [x] 11. `/verify` and the drivers (r1.5)

- `engineering/verify` (the thin router), `create-verification-skill`, and `maintain-verification-skill`, as in Decisions.
- `/test`, `interrogate`, `blast-radius`, `qa-screenshots`, and the benchmark skill call `/verify`.
- User note (r1.5): personal at work, committed in hobby repos.
- Done: `/create-verification-skill` on a small app writes a driver that passes its own proof run, and `/verify` finds it from a diff.

### [x] 12. The decision log and `/sitrep` (r1.8, r1.26)

- `decisions_<KEY>.tsv` beside the plan. Columns: decision, reason, evidence pointer, result. `scripts/log_decision.py` appends each row.
- `build` writes it. The plan's `Progress` links it.
- `primitives/sitrep` (new): every pending decision, with the evidence, the risk, and the agent's pick. It reads the log and `Follow-ups`.
- User note (r1.26): call it sitrep.
- Done: after a `/build`, `/sitrep` lists the choices the agent made alone.

### [x] 13. `/checkpoint` (r1.24)

- `primitives/checkpoint` (new): finish or back out the step, make a `wip:` commit, write the resume note as a `Progress` entry.
- Done: `/checkpoint` mid-step leaves a clean tree, and `/do-next` or `/work-on` resumes from the plan.

### [x] 14. Stacks in `claim` and `stand-up`

- From the worktree note, items 2 to 5:
  - `claim`: if the branch is in a gh-stack stack, use the stack's worktree and `gh stack checkout <branch>`. Treat worktrunk's "worktree at the expected path" refusal the same way.
  - `claim`: if the local branch differs from the remote and is in a stack, run `gh stack sync` first.
  - `stand-up`: show the worktree that holds each PR row. Flag local branches that differ from the remote.
- The worktrunk template step in `install-agents-md` (note item 1), with `wt step relocate`. The system map edit (note item 5) is listed for the user.
- Reason: a stack once got a second worktree, built from a stale branch.
- Done: `claim` on a branch inside a stack returns the stack's worktree, synced.

### [x] 15. `ship` with gh-stack, and the map layout (r1.11)

- `engineering/ship`: `gh stack sync` and rebase with the tool, compare `git patch-id` so a review verdict still describes the head after a rebase, read the PR back after the merge.
- The `map` layout and its check. Use this file as the test fixture. The map playbook from unit 6 already reads this shape, so the layout must keep it. The playbook then runs the check before each batch.
- User note (r1.11): the workflow uses gh-stack and must cover its sync and rebase.
- Done: `/ship` on a rebased stack layer accepts the old review when the patch-id matches.

### [x] 16. `babysit` and the status line chips (r1.12)

- `engineering/babysit` (new). `scripts/watch_prs.py` polls `gh`, writes `~/.cache/babysit/state.json`, and calls the notifier on a change only. For a stack, it watches only the lowest PR not merged.
- The notifier tool role in the `tools` block, hydrated on the machine.
- The chip segment and the transcript cache in `statusline.sh`, as in Decisions.
- User note (r1.12): it must alert the user, beyond a skill call.
- Done: a CI change on a watched PR shows a notification and the right chip, and leading spaces survive in the real status line.

### [ ] 17. The `tidy-up` audit table (r1.25)

- A read-only table first: size, merged, dirty, PR state, last used. Delete only after the user picks.
- Done: `/tidy-up` shows the table and deletes nothing until a pick.

### [ ] 18. The correct ladder (r1.6)

- `engineering/constraints` and `engineering/self-improve`: architecture, then types, then a lint whose error names the fix, then a test, docs last. A mistake class counts after two times.
- Done: a repeated mistake gets a fix at the highest rung that works.

### [ ] 19. No comments (r1.21)

- `persona-comments`: the two lenses. `scripts/added_comments.py` lists each added comment line.
- The ladder and the follow-up flow from Decisions. The `Follow-ups` section from unit 4.
- The `coding` block in `install-agents-md`: "No comments. Two exceptions: tool directives and comments that lint requires."
- User note (r1.21): no comment has added value that the user could not get by asking a model.
- Done: a branch with an added comment gets a finding with the replacement, and a hack gets a step or a follow-up.

### [ ] 20. Two failures and model escalation (r1.13)

- `diagnose` and `fix` cite `principle-attack-the-premise` and `principle-fix-root-causes`.
- After two failed fixes on one premise, write the premise down, test it, and move one effort step up to Opus max. The log records it.
- Done: a third fix attempt starts with a written premise and a higher effort.

### [ ] 21. `eval-skill` (r1.23)

- `meta/eval-skill` (new): a blind A/B test of a skill change, with neutral prompts and no eval words the candidate can see.
- `/retro` offers it when it proposes an edit to a skill that `/work-on` calls. Never a required step.
- Done: one run compares two versions of a skill and reports a winner or "no difference".

### [ ] 22. `loop-until` (r1.9)

- `engineering/loop-until` (new): one change, one measure, keep or revert. Prove the harness can fail, then freeze it. A plateau means a new approach. Writes the decision log.
- Done: a loop on a small metric stops at the predicate, with one log row per try.

### [ ] 23. TypeScript rules (r1.14)

- `install-rules/rules/typescript-conventions.md`: branded primitives, discriminated unions, exhaustive checks with `never`, `satisfies` before `as`, parse at the boundary, the simplest total type. Cite the principles.
- Done: `/install-rules` installs the rule.

### [ ] 24. `benchmark` (r1.7)

- `engineering/benchmark` (new), called by `webperf`. Seven checks on a perf number: name the limiter, alternate A/B runs, count errors, confirm the work ran inside the timed region. Inconclusive is a valid verdict. Cites `principle-explain-the-number`.
- Done: `webperf` reports a verdict with its limiter, or "inconclusive".

### [ ] 25. `sharpen` (r1.15)

- `primitives/sharpen` (new, user-only): rewrite a prompt to go deeper, not wider.
- Done: `/sharpen` on a prompt returns a deeper version.

### [ ] 26. The fork rule (r1.18)

- `grill`, `spec`, and `plan` classify a question first. An observable fact goes to a prototype or a lookup, not the user. The pause list is already in unit 1.
- Done: a grill looks up a fact instead of asking it.

### [ ] 27. Design-it-twice rubric (r1.19)

- `codebase-design/DESIGN-IT-TWICE.md`: a rubric before the fan-out, pick a base, graft the strong parts of the losers, sketch the caller's usage first, scrap on known tells.
- Done: a design-it-twice run shows the rubric and the grafts.

### [ ] 28. `UNSLOP.md` (r1.20)

- `scribe/UNSLOP.md`: a numbered catalogue of AI tells with stable IDs. `proof-read` cites it.
- Done: `proof-read` flags a tell by its ID.

### [ ] 29. `/why` (r1.22)

- `engineering/why` (new): answer why from commits and PR threads, cite the authors, say what the record does not answer.
- User note (r1.22): name the skill `why`.
- Done: `/why` on a line returns its history with citations.

### [ ] 30. Text diagrams in `show-me`

- A new view: hand-drawn box diagrams for a flow or a dependency graph. Box-drawing characters and ASCII only, no emoji, one route per line, a label on each line. Mermaid stays for the HTML view.
- `show-me/scripts/check_diagram.py`: each character is one column wide, and box corners line up.
- Done: `/show-me` draws a flow that the check passes. The diagrams in this map are the examples.

### [ ] 31. `findings` and `report` layouts

- Template and check for `findings`. A check for the JSON `runs` block of `report`.
- `diagnose` writes `findings`.
- Done: `/diagnose` writes a findings file that passes the check.

### [ ] 32. Script audit

- A report that lists each skill step that a script can do (for example, report schema checks, the version bump, the skill table sync). The user ticks the rows to build later.
- Done: the report exists, with rows to tick.

### [ ] 33. Retire list and version bumps

- List the skills to retire after the trial: `/do-next`. Do not move them.
- Bump the version of each domain that changed. `engineering` goes to 3.0.0, because callable skills and the rename break existing prompts.
- Done: each changed domain has one new version, and only this unit changed a `plugin.json`.
