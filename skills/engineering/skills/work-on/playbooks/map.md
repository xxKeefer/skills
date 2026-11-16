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
- **Spec.** `spec_<prefix>-<N>.md`, written with `/write-to-file`, doctype `spec`.
- **Plan.** `plan_<prefix>-<N>.md`, written by the map-unit route of `/plan`.

## Steps

Run the steps once for each batch. A batch is the output of step 1.

| # | Step | Stop after the step |
| --- | --- | --- |
| 1 | Run `python3 $SCRIPT next $MAP --batch 5`. Each line is `<N>\t<title>`, in map order. On exit 1, show the error line, which names the unit with no `Done:` line. | H3 on exit 1. With no lines, the map is done: go to step 7. |
| 2 | For each unit in the batch, in order, write its spec with `/write-to-file`, doctype `spec`. `goal` comes from the unit's `Done:` line. `status` is `confirmed`, because the user approved the map at H0. `## Intent` comes from the unit's bullets. `## Decisions` holds the map Decisions that the unit names. `## Acceptance criteria` has one lettered AC for each unit bullet, and the `Done:` line as the last AC. Then run `/plan @<spec path>` in the current worktree, with the map path, the plan name, and the branch name. Skip a unit that already has a plan. | H3 when the spec check fails. |
| 3 | When each plan in the batch has `status: approved`, go to step 4 with no stop. When the `## Progress` of a draft plan records this H2 stop, the continue command is the user's yes: set `status: approved` in that plan. Else stop once for the whole batch. Write the playbook, the stop, and the next step into the `## Progress` of each plan. | H2, only when a plan in the batch is not approved: the user approves the batch of plans. Continue: `/work-on @$MAP`. |
| 4 | For each unit, in order: run `gh stack add <branch>`, then run `/build @<plan path>` in a fresh subagent. Wait for the build before the next unit, because each layer builds on the one below. Skip `gh stack add` when the branch exists, and skip `/build` when each step of the plan is done. | H3, only when a build returns an open `D` entry. Stop the batch at that unit. |
| 5 | For each unit, from the bottom of the stack: check out its branch, then run `/ship @<plan path>`. `/create-pr` runs `gh stack submit --auto` itself, so it opens a draft PR for the layer with no stop. | H3 when `/ship` gives no-go. H4, only before an action on the pause list, such as mark a PR ready or merge. |
| 6 | When `/ship` opened the draft PR of a unit, run `python3 $SCRIPT tick $MAP <N>`. Tick each unit after its own PR, not after its build, so a batch that stops before its PRs gives the same units to the next run. | H3 on exit 1. |
| 7 | Offer `/retro` on the batch. The user runs it, or says no. Then start the next batch at step 1. | H5, when the user runs `/retro`: the user picks the skill edits. |

When `/plan` splits a unit, remove the unit from the batch. At the H2 stop, give the wave 1
commands that `/plan` returns. The split unit gets no tick until each of its sub-tasks has a PR.

**Done when:** each unit of the batch has a stack layer, a draft PR, and a tick on the map, and the
user has the `/retro` offer.
