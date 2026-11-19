---
name: create-verification-skill
description: >
  Write a verification driver for an app: a skill that launches the app, drives it the way a user
  does, and keeps the evidence. Proves the driver by one run before it hands it over. The
  `maintain` mode keeps a driver and its feature map true as the app changes. Use when the user
  says "create verification skill" or "make a driver", or when /verify returns `no driver`; for
  the maintain mode, when the user says "maintain verification skill", "maintain the verify skill",
  or "audit the verify skill", or when a driver fails its run because the app moved.
argument-hint: "[maintain] [<app name> | <driver name>]"
---

# Create a verification skill

A driver is a skill that runs one app the way a user does. `/verify` finds a driver from a diff
and runs it. The next agent reads the driver cold, in the middle of a task, and has never seen the
app. Write the driver for that reader.

Principle: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)).

`$SKILL_DIR` is this skill's base directory.

**Maintain mode.** When the arguments start with `maintain`, or the user asks to maintain or audit
a driver, or a driver fails its run because the app moved, read [`MAINTAIN.md`](MAINTAIN.md) and
follow it in place of the steps below. Otherwise run the create steps.

```
interview the repo → pick the name and place → write the driver → seed the feature map → check → prove → hand over
```

## Step 1: Interview the repo

Answer each question from the code. Ask the user only what you cannot see.

- **Surface.** What does a user touch: a web UI, a CLI or TUI, a desktop app, an API, a mobile app,
  or a library? Pick the main surface and note the others.
- **Run.** How does the app start on a local machine? Use the repo's own command (package script,
  Makefile, README). Note ports, environment variables, seed data, and sign-in.
- **Drive.** How can an agent use the app? Use a harness that the repo has first: a browser test,
  an `expect` script, a PTY helper, a `curl` call, or a debug port. Else use a generic recipe:
  a browser driver for web and desktop, a tmux or PTY session for CLI and TUI, plain HTTP for a
  service.
- **Observe.** What evidence can you keep? Screenshots, a terminal transcript, response bodies,
  logs, exit codes, stored state.
- **Isolate.** Can two instances run side by side (ports, data folders, profiles)? If not, the
  driver says so, and it refuses to drive an instance that it did not start.

A library has no surface of its own. Drive it as its consumer does: through Storybook, a PTY, or a
scratch consumer script that imports the built package.

When the checkout does not build or start, fix that first, or report the fault exactly. A driver
written on a broken base teaches wrong steps.

**Done when:** you can name the surface, the start command, the harness, and the evidence.

## Step 2: Pick the name and the place

1. The name is `verify-<repo>-<app>`. `<repo>` is the last part of `git remote get-url origin`,
   with no `.git`. `<app>` is a short kebab-case name for the app.
2. The place follows the owner rule. The remote owner is the part before the repo name in the URL.
   - The owner is one that the user's global instructions (`~/.claude/AGENTS.md`) name as the
     user's own: write the driver to `<repo root>/.claude/skills/<name>/` and commit it.
   - Any other owner, or no match: write the driver to `~/.claude/skills/<name>/`. A wrong home
     folder costs a move. A wrong repo folder commits a driver into a team repo.
3. Tell the user the place, and the reason, in one line.

`/verify` finds the driver from the name, `repo`, and `app-paths`, so keep all three exact.

**Done when:** you have the name and the folder.

## Step 3: Write the driver

Write `<folder>/SKILL.md`. The frontmatter holds four keys:

- `name`: the name from step 2.
- `description`: names the app, the surface, and when to use the driver.
- `repo`: the `<repo>` from step 2. `/verify` matches a driver only when this value equals the repo
  name, so a repo with a longer name that starts the same way does not match.
- `app-paths`: a list of globs from the repo root that cover the app's source. `/verify` matches
  the diff against them. `*` matches inside one folder. `**` matches across folders.

```
---
name: verify-<repo>-<app>
repo: <repo>
description: <the app, the surface, when to use it>
app-paths:
  - src/**
  - package.json
---
```

The body holds these six sections, each as an H2, each from what the interview found. Leave no
placeholder.

| Section | Holds |
|---|---|
| Launch | The exact command that starts the app for verification, and how to tell that it is ready. Launch reaches a usable state from an empty data folder, with migrations and seed data. Ready means usable, not only that a process answers. A short-lived CLI has no server: build it once, then start each drive in its own PTY or tmux session. |
| Doctor | One read-only check: is this instance worth driving? Process up, right build, port owned by us, sign-in valid. An agent runs it first when anything looks wrong. |
| Drive | The harness recipe with the real selectors and commands of this repo. Use stable handles (ARIA names, data attributes, prompt text, routes), not coordinates. |
| Evidence | What to keep, and where it goes. Proof standards: use the real user path, not internal setters or test-only endpoints. Keep the action and the resulting state, not only the last screen. Check side effects (files, rows, messages) next to what is visible. Use a mock only where a production boundary already isolates the outside system. Check what a dry run really skips. |
| Cleanup | How to stop the instances that the run made. Never kill by process name. Kill what you started. Cleanup removes instances and scratch state. It never removes the evidence. Name a place where the evidence stays. |
| Helpers | Each script that the driver ships. Each is executable, and the section shows its call. Write `None.` when there is none. |

**Done when:** `SKILL.md` has the three keys and the six sections.

## Step 4: Seed the feature map

1. Write `<folder>/features/README.md`: baseline preconditions, driving conventions, the proof and
   skip rules, and an index with one link for each feature file.
2. Write one file for each user-facing feature. Take the top three to five from the routes,
   commands, menus, or docs.
3. Each feature file has an H1, one paragraph, and then these four H2 sections, in this order:
   `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.
   Name the real harness in the third title. The check accepts any name there.
4. Follow the shape in [`references/feature-map-example/`](references/feature-map-example/). It
   shows a README and two feature files.
5. When the seed data lacks a state that a journey needs, the journey reports a failure. Write the
   reason in `Gotchas`. Do not weaken the journey to make it pass.

**Done when:** the index links each feature file, and each file has the four H2 sections.

## Step 5: Check the layout

Run `python3 $SKILL_DIR/scripts/check_driver.py <folder>`. It exits 0 with `ok`, or it exits 1 and
names each missing key, section, or file with the fix. Fix each error and run it again.

**Done when:** the script prints `ok`.

## Step 6: Prove the driver

Follow the driver as written, from a cold start: Launch, Doctor, Drive one mapped feature, keep the
evidence, Cleanup. One feature is enough, because the map lets later runs cover the rest.

1. After Cleanup, check that the evidence still exists at the place that the driver names. A
   cleanup that removes the evidence fails this step.
2. Fix each failure. Run Cleanup after each failed attempt, so that no process or port stays.
3. A driver that no run has proved is a draft. Do not hand it over as done.
4. When you proved it in a stand-in for the real target, list each setup step that the stand-in
   did and the target will not. Those steps stay unproved.

Then run `python3 $SKILL_DIR/../verify/scripts/find_drivers.py --repo <repo root> --base <base>`
with the app changed. It must print the path of the driver. If it prints `no driver`, the `name`
or the `app-paths` is wrong.

**Done when:** the run passes, the evidence survives Cleanup, and `/verify` finds the driver.

## Step 7: Hand over

Tell the user the folder, whether the driver is committed, and the one feature that the proof run
drove. A repo driver is a change to the repo: leave the commit to the normal flow. Point the user
at `/create-verification-skill maintain` for keeping the map true as the app changes.

**Done when:** the reply names the folder, the proof result, and the next skill.
