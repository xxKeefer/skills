# Gazette config

Copy this file to `~/.claude/gazette.md` and fill it in. An argument in the call overrides a line here.

- paper name: The Daily Commit
- accent: any CSS colour for the tags, the Breaking box, and a storm. Default: `#d0021b` (red)
- window: 24 hours
- repos:
  - ~/code/app-one
  - ~/code/app-two
- board: one or more board IDs from the tracker, such as `42` or `42, 57`
- workflows: optional. The CI workflow names for build time and test time:
  - app-one build: CI
  - app-one test: E2E Playwright
- metrics: optional. One line per metric that a repo records, with the command or the file that gives the number:
  - app-one bundle size: `cat dist/stats.json`
