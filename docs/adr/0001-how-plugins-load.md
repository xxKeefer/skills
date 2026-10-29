# 0001 How the marketplace plugins load

**Status:** Accepted, 2026-10-28

## Context

The marketplace is a `directory` source, and every plugin entry in `.claude-plugin/marketplace.json`
is a relative path (`./skills/<domain>`). The Claude Code docs say that such a plugin loads in place
from the repo. But `~/.claude/plugins/installed_plugins.json` gives each domain an `installPath`
under `~/.claude/plugins/cache/xxkeefer-skills/<domain>/<version>/`, and those folders hold copies
that differ from the repo. If sessions loaded the copies, an edit would reach this machine only
after a version bump and an update.

## Observation

One session on 2026-10-28 showed three facts that only an in-place load explains:

- `/do-next` loaded from `<repo>/skills/primitives/skills/do-next`, not from a cache folder.
- The loaded `/do-next` text has the "Done when" lines that `primitives` 2.10.0 added. The newest
  cache copy is 2.9.0, which lacks them. No 2.10.0 cache folder exists.
- The skill list held `developer:codebase-news` and `experimental:append-to-note`. Neither skill
  exists in any cache folder.

This matches the plugin loading reference
(https://code.claude.com/docs/en/plugins/loading.md, "In-place and copied plugins"): a
relative-path plugin in a marketplace added from a local path "loads in place from its path inside
the marketplace folder", and edits "take effect at the next session start or `/reload-plugins`, and
you don't need to increase the version."

## Decision

The repo is the live copy on this machine. The cache folders are install records. They do not
decide what a session loads.

## Consequences

- An edit applies at the next session start, or after `/reload-plugins` in a running session.
- A version bump is release hygiene. It marks the change in the git log, and it releases the
  change to any install that copies the plugin, such as one from GitHub.
- A path above a plugin root resolves here, but not in a copied install. Skills must not depend
  on one.
- Claude Code deletes a cache folder 14 days after it writes an `.orphaned_at` marker in it.
