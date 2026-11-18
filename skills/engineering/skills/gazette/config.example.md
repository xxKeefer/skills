# Gazette config

Copy this file to `~/.claude/gazette.md` and fill it in. An argument in the call overrides a line here.

- paper name: The Daily Commit
- window: 24 hours
- repos:
  - ~/code/app-one
  - ~/code/app-two
- board: the tracker query for the board's tickets, such as `project = ABC AND sprint in openSprints()`
- workflows: optional. The CI workflow names for build time and test time:
  - app-one build: CI
  - app-one test: E2E Playwright
- metrics: optional. One line per metric that a repo records, with the command or the file that gives the number:
  - app-one bundle size: `cat dist/stats.json`
