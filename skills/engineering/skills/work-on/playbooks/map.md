# Playbook: Map

Build the next batch of units of a map as layers of one gh stack. Each step calls one ★ command or
one script. The stops are the stops in [`SKILL.md`](../SKILL.md).

A map holds one unit per heading `### [ ] N. Title` under `## Units`, each with a `Done:` line. A
ticked heading `### [x] N. Title` is a unit with a PR. The user approved the map before the first
run (H0), so this playbook does not stop for it.

`$MAP` is the map path. `$SCRIPT` is `$SKILL_DIR/scripts/map_units.py`.

## Names

- **Prefix.** The map's `branch_prefix` frontmatter key. Else, the part of the file slug before its
  first `-`: `map_pstack-program.md` gives `pstack`.
- **Branch.** `<prefix>-<N>_<short-desc>`. The short description is two or three kebab-case words
  from the unit title, such as `pstack-7_agents-md`.
- **Plan.** `plan_<prefix>-<N>.md`, written with `/write-to-file`.

## Steps

Run the steps once for each batch. A batch is the output of step 1.

| # | Step | Stop after the step |
| --- | --- | --- |
| 1 | Run `python3 $SCRIPT next $MAP --batch 5`. Each line is `<N>\t<title>`, in map order. On exit 1, show the error line, which names the unit with no `Done:` line. | H3 on exit 1. With no lines, the map is done: go to step 7. |
| 2 | For each unit in the batch, in order, run `/plan` in the current worktree. Give it the unit section of the map as the spec, the map path, the unit's `Done:` line, the plan name, and the branch name. Skip a unit that already has a plan with `status: approved`. | none |
| 3 | When each plan in the batch has `status: approved`, go to step 4 with no stop. Else stop once for the whole batch. Write the playbook, the stop, and the next step into the `## Progress` of each plan. | H2, only when a plan in the batch is not approved: the user approves the batch of plans. Continue: `/work-on @$MAP`. |
| 4 | For each unit, in order: run `gh stack add <branch>`, then run `/build @<plan path>` in a fresh subagent. Wait for the build before the next unit, because each layer builds on the one below. | H3, only when a build returns an open `D` entry. Stop the batch at that unit. |
| 5 | When the build of a unit is done, run `python3 $SCRIPT tick $MAP <N>`. Tick each unit after its own build, not at the end of the batch. | H3 on exit 1. |
| 6 | Run `gh stack submit --auto`. It opens a draft PR for each layer, with no stop. | H4, only before an action on the pause list, such as mark a PR ready or merge. |
| 7 | Offer `/retro` on the batch. The user runs it, or says no. Then start the next batch at step 1. | H5, when the user runs `/retro`: the user picks the skill edits. |

When `/plan` splits a unit, remove the unit from the batch. At the H2 stop, give the wave 1
commands that `/plan` returns. The split unit gets no tick until each of its sub-tasks has a PR.

**Done when:** each unit of the batch has a stack layer, a draft PR, and a tick on the map, and the
user has the `/retro` offer.
