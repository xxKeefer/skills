# Playbook: Map

Build the next batch of units of a map as layers of one gh stack. Each step calls one ★ command or
one script. The stops are the stops in [`SKILL.md`](../SKILL.md).

A map holds one unit per heading `### [ ] N. Title` under `## Units`, each with a `Done:` line. A
ticked heading `### [x] N. Title` is a unit with a PR. A split unit is a set of sub-units
`### [ ] N.1. Title`, `### [ ] N.2. Title`, and so on. `N` in this playbook is a unit number or a
sub-unit number, such as `7.1`. The user approved the map before the first run (H0). That
approval covers the map and each unit plan, so this playbook stops for neither.

`$MAP` is the map path. `$SCRIPT` is `$SKILL_DIR/scripts/map_units.py`.

## Names

- **Prefix.** The map's `branch_prefix` frontmatter key. Else, the part of the file slug before its
  first `-`: `map_pstack-program.md` gives `pstack`.
- **Branch.** `<prefix>-<N>_<short-desc>`. The short description is two or three kebab-case words
  from the unit title, such as `pstack-7_agents-md`.
- **Spec.** `spec_<prefix>-<N>.md`, written with `/write-to-file`, doctype `spec`.
- **Plan.** `plan_<prefix>-<N>.md`, written by the map-unit route of `/plan`.
- **Batch size.** The map's `batch` frontmatter key. Else 5.

## Push only

A map with `push_only: true` in its frontmatter runs on a machine that runs no `gh` command.
Another machine opens, reviews, and merges each PR. In this mode, three steps change:

- **Step 4.** Make the branch with `git switch -c <branch> <base>`. `<base>` is the branch that
  was checked out at step 1. Run no `gh stack` command.
- **Step 6.** Run steps 1 to 3 of `/ship`, and skip its Stack check. On go, run
  `git push -u origin <branch>` in place of `/create-pr`.
- **Step 7.** Tick the unit after its push.

## Steps

Run the steps once for each batch. A batch is the output of step 1.

| # | Step | Stop after the step |
| --- | --- | --- |
| 1 | Run `python3 $SCRIPT next $MAP --batch <batch size>`. Each line is `<N>\t<title>`, in map order. On exit 1, show the error line. It names a unit with no `Done:` line, a malformed heading, or a map with no `## Units` section. | H3 on exit 1. With no lines, the map is done: go to step 8. |
| 2 | For each unit in the batch, in order, write its spec with `/write-to-file`, doctype `spec`. `goal` comes from the unit's `Done:` line. `status` is `confirmed`, because the user approved the map at H0. `## Intent` comes from the unit's bullets. `## Decisions` holds the map Decisions that the unit names. `## Acceptance criteria` has one lettered AC for each unit bullet, and the `Done:` line as the last AC. Then run `/plan @<spec path>` in the current worktree, with the map path, the plan name, and the branch name. Skip a unit that already has a plan. When `/plan` splits a unit, see [Split a unit](#split-a-unit). | H3 when the spec check fails, or when `/plan` returns a `D` entry. No stop on a split. |
| 3 | Check that each plan in the batch has `status: approved`. Set it on a plan that has `status: draft`. Write each judgement call that a plan makes, and that its unit does not decide, into the plan's `## Progress`. | No stop. |
| 4 | For each unit, in order: run `gh stack add <branch>`, then run `/build @<plan path>` in a fresh subagent. Wait for the build before the next unit, because each layer builds on the one below. Skip `gh stack add` when the branch exists, and skip `/build` when each step of the plan is done. When the current branch is not in a gh stack (`gh stack view` fails), run `gh stack init <branch>` in place of `gh stack add`. Add `--base <current branch>` when the current branch is not the default branch. | H3, only when a build returns an open `D` entry. Stop the batch at that unit. |
| 5 | For each unit, in order, on its branch: run `/blast-radius @<plan path>`. When it reports risk, run `/interrogate @<plan path>`, which runs its adversaries at the `panel` models. Until the `blast-radius` skill exists, skip the step with the reason `skipped: no /blast-radius skill`. | H3, only when the report keeps a finding and the plan has no fix step for it. |
| 6 | For each unit, from the bottom of the stack: check out its branch, then run `/ship @<plan path>`. `/create-pr` runs `gh stack submit --auto` itself, so it opens a draft PR for the layer with no stop. | H3 when `/ship` gives no-go. H4, only before an action on the pause list, such as mark a PR ready or merge. |
| 7 | When `/ship` opened the draft PR of a unit, or pushed its branch in push-only mode, run `python3 $SCRIPT tick $MAP <N>`. Tick each unit after its own PR, not after its build, so a batch that stops before its PRs gives the same units to the next run. | H3 on exit 1. |
| 8 | Offer `/retro` on the batch. The user runs it, or says no. Then start the next batch at step 1. | H5, when the user runs `/retro`: the user picks the skill edits. |

**Done when:** each unit of the batch has a stack layer, a draft PR, and a tick on the map, and the
user has the `/retro` offer.

## Split a unit

The map is the tracker, so a split goes into the map. The agent does the split with no stop:

1. In the map, replace the heading and the section of unit N with one sub-unit for each slice that
   `/plan` returned, in slice order: `### [ ] N.1. <slice goal>`, `### [ ] N.2. <slice goal>`, and
   so on. Give each sub-unit its slice ACs as bullets, and a `- Done: <claim>` line from its ACs.
2. Delete the spec of unit N.
3. In step 2, write the spec and run `/plan` for each sub-unit, in order, in place of unit N. The
   sub-units are in the same batch.

A sub-unit is a unit for each later step: it gets its own branch, plan, stack layer, PR, and tick.
`map_units.py` lists and ticks sub-unit numbers in map order.
