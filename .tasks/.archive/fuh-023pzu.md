---
id: fuh-023pzu
title: weekly skill
type: feat
status: done
created: '2026-03-25'
flag: completed
parent: fuh-022xhx
priority: 4
blocks:
  - fuh-023v96
---

## Description

Monday sprint planning. Coach reviews last ponder, surfaces dormant domains (pushes back hard after 3+ sprints), challenges overcommitment via /grill-it mechanics. Enforces 3-domain WIP limit with stretch-goal override. Reads backlog + north stars + previous ponder. Produces sprint plan file. Accepts week number or file path.

## Acceptance Criteria

- [x] Running /weekly produces a sprint plan file (2026-wkNN-sprint.md)
- [x] WIP limit of 3 active domains enforced — 4th blocked by default, stretch override available
- [x] Coach challenges vague or overloaded plans conversationally
- [x] Dormant domains (3+ sprints) flagged with hard pushback
- [x] Sprint file has valid Obsidian frontmatter with prev/next/up wikilinks
