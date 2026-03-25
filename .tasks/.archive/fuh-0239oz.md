---
id: fuh-0239oz
title: smart-goal skill
type: feat
status: done
created: '2026-03-25'
flag: completed
parent: fuh-022xhx
priority: 4
blocks:
  - fuh-023dz7
---

## Description

Conversational SMART goal grilling for any user-defined domain. Coach walks through Specific, Measurable, Achievable, Relevant, Time-bound using /grill-it mechanics until landing on a concrete goal. Writes to north-stars.md. Accepts domain as input.

## Acceptance Criteria

- [x] Running /smart-goal <domain> produces a conversational grilling session
- [x] Session ends with a concrete SMART goal written to north-stars.md
- [x] Works for any user-defined domain tag (#domain/<area>)
- [x] Manual template exists as fallback
