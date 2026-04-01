# Skills

Claude Code skills for idiomatic, framework-agnostic software engineering workflows.

## Skills

| Skill             | Description                                                                                                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/spike-it`       | Deep-dive investigation of a problem. Relentlessly clarifies scope, researches the codebase, and produces a terse spike document.                                                               |
| `/plan-it`        | Breaks a task into ordered, atomic implementation steps — or skips planning if the task is trivial.                                                                                             |
| `/do-it`          | Executes a plan step-by-step, delegating each to `/tdd` with checkpoints between steps.                                                                                                        |
| `/tdd`            | Red-green-refactor loop. Vertical slices, tracer bullets, behavior-driven tests through public interfaces. Loads [stack contexts](tdd/SKILL.md#stack-contexts) for framework-specific patterns. |
| `/task-it`        | Decomposes a spike into demo-able, tracker-ready tickets with dependency ordering.                                                                                                              |
| `/close-it`       | Wraps up work: commit strategy, PR description with QA test plan, ready to ship.                                                                                                                |
| `/hunt-it`        | Hunts down a bug from user feedback — critically assesses the report, traces to root cause, produces a TDD-anchored fix plan.                                                                   |
| `/resolve-it`     | Critically assesses code review feedback before applying fixes. Doesn't blindly trust reviewers.                                                                                                |
| `/design-it`      | Generates multiple radically different interface designs for a module using parallel sub-agents.                                                                                                 |
| `/grill-it`       | Interviews you relentlessly about a plan or design until reaching shared understanding.                                                                                                         |
| `/explain-it`     | Unpacks the agent's reasoning on demand — traces observations, inferences, and assumptions until shared understanding.                                                                          |
| `/improve-it`     | Explores a codebase for architectural friction and proposes module-deepening refactors as GitHub issue RFCs.                                                                                    |
| `/audit-workflow`  | Audits Claude Code configuration and suggests workflow optimizations.                                                                                                                           |
| `/document-it`    | Analyzes code changes and updates all documentation surfaces — reference docs, comments, naming, types — to match reality.                                                                      |
| `/learn-it`       | Analyzes the current conversation to extract repeatable patterns and codify them into a new skill.                                                                                              |
| `/teach-it`       | Corrects repeated undesired agent behaviour by writing feedback to memory, then updating skills and docs at global and project scope.                                                            |

## Typical Flow

```
spike-it → task-it → plan-it → do-it (uses tdd) → close-it
                                  ↑                    ↑
                              grill-it (stress-test)   resolve-it (PR feedback)
                              design-it (explore APIs)  hunt-it (track bugs)
                              improve-it (architecture)

Anytime:  explain-it (unpack reasoning)
          teach-it (correct agent behaviour)
          learn-it (extract new skills)
          document-it (sync docs)
          audit-workflow (optimise setup)
```

## Setup

### Install as a local marketplace

Add the following to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "xxkeefer-skills": {
      "source": {
        "source": "directory",
        "path": "/path/to/this/repo"
      }
    }
  },
  "enabledPlugins": {
    "xxkeefer-skills@xxkeefer-skills": true
  }
}
```

Replace `/path/to/this/repo` with the absolute path to your local clone of this repo.

### Publishing a new version

After editing skills or adding new ones, follow these steps so Claude Code picks up the changes:

1. **Bump the version** in the relevant `plugin.json` (e.g. `1.0.1` → `1.0.2`):
   - Root plugin: `.claude-plugin/plugin.json`
   - Sanctum plugin: `sanctum/.claude-plugin/plugin.json`
2. **Commit and push** the changes to `main`:
   ```sh
   git add -A && git commit -m "feat: bump to vX.Y.Z"
   git push origin main
   ```
3. **On each machine**, pull the latest and restart Claude Code:
   ```sh
   cd /path/to/this/repo && git pull origin main
   ```
   Then restart Claude Code (exit and relaunch, or start a new conversation). On startup it compares the source repo's HEAD SHA against its cached SHA — if they differ, it re-caches the plugin at the new version.

> **How it works:** Claude Code stores installed plugin state in `~/.claude/plugins/installed_plugins.json`, keyed by `gitCommitSha` and `version`. When the source directory's HEAD moves ahead of the cached SHA, a restart triggers a re-cache into `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`.

### Updating an installed plugin

If you're consuming this on another machine (not the source repo):

1. `cd` into your local clone and `git pull origin main`
2. Restart Claude Code — the new version is detected and cached automatically

No manual edits to `installed_plugins.json` or cache directories are needed.

## Attribution

Several skills were inspired by or adapted directly from
[Matt Pocock's skills repo](https://github.com/mattpocock/skills):

- **grill-it** — taken from Matt's repo
- **design-it** — taken from Matt's repo
- **improve-it** — taken from Matt's repo
- **spike-it** — inspired by Matt's approach to investigation workflows
- **tdd** — inspired by Matt's TDD skill, particularly the tracer bullet pattern and
  anti-horizontal-slice philosophy

Thanks Matt for sharing these publicly.
