---
id: fuh-023zn1
title: reflect skill
type: feat
status: done
created: '2026-03-25'
flag: completed
parent: fuh-022xhx
priority: 4
blocks:
  - fuh-0245tl
---

## Description

Evening reflection. Appends to the same daily file produced by /daily. Sections: what learned, what went well, what is next, friction. Coach flags recurring friction patterns from recent reflects. Accepts date or file path as input.

## Acceptance Criteria

- [x] Running /reflect appends reflection section to existing daily file
- [x] Does not overwrite morning standup content
- [x] Coach flags friction patterns recurring across recent days
- [x] Friction entries are later aggregated by /ponder
