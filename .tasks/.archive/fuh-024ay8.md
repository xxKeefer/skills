---
id: fuh-024ay8
title: chronicle skill
type: feat
status: done
created: '2026-03-25'
flag: completed
parent: fuh-022xhx
priority: 3
---

## Description

Monthly or yearly progress arc. Coach generates narrative draft from sprint ponders, velocity trends, accomplishment log, friction themes, and north star progress. User reviews and adjusts. Produces chronicle file. Accepts month or year as input.

## Acceptance Criteria

- [x] Running /chronicle <month> produces monthly chronicle (2026-MM-chronicle.md)
- [x] Running /chronicle <year> produces yearly chronicle (YYYY-chronicle.md)
- [x] Narrative draft generated from sprint ponder data
- [x] North star progress table with trends
- [x] Velocity trend table across sprints
- [x] Friction themes identified across the period
- [x] File has valid Obsidian frontmatter with prev/next/up wikilinks
