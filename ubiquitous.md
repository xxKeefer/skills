# Ubiquitous Language

Shared terminology for the xxkeefer-skills repository.

| Term                       | Definition                                                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Marketplace**            | The top-level registry (`xxkeefer-skills`) that groups all domains. Configured as a local directory source in Claude Code settings.         |
| **Domain**                 | A self-contained plugin within the marketplace. Each domain has its own version, skills, and documentation. Maps 1:1 to a plugin directory. |
| **Plugin**                 | The Claude Code concept that a domain maps to. Each domain directory contains `.claude-plugin/plugin.json`.                                 |
| **Skill**                  | A markdown-defined workflow in a domain's `skills/` directory. Invoked via `/skill-name`.                                                   |
| **Primitive**              | A foundational skill in the `primitives` domain that other domains compose.                                                                 |
| **Progressive disclosure** | The principle of decomposing complex skills into composable primitives, so users can engage at the level of abstraction they need.          |
| **Everything-agnostic**    | The north star: skills encode how to think about problems, not how to use specific frameworks, languages, or tools.                         |
