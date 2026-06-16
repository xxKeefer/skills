# Experimental

Personal skills on probation. Promote once usage justifies it; demote to `deprecated` if it doesn't.

## Skills

| Skill | Purpose |
|---|---|
| `/define-concept` | Mine the codebase for one concept's terminology, verify term-by-term, add as a glossary section |
| `/define-term` | Add a single term to the glossary under a user-specified concept |
| `/update-language` | Compare a conversation against the glossary, propose restrained edits/additions |
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/patch-doctor` | Diagnose and fix drift between a skill's current output contract and the artifacts it already produced |

> Migrated in from the work marketplace (`xxkeefer-work` `maintain`) — fully generic glossary tooling,
> no Megaport content. On probation here pending promotion to a stable domain.

## Installation

```json
{
  "enabledPlugins": {
    "experimental@xxkeefer-skills": true
  }
}
```
