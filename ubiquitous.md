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
| **HITL**                   | Human-in-the-loop. A skill or task that requires human judgment, design review, or architectural decision. Signalled by the `*-it` suffix. |
| **AFK**                    | Away-from-keyboard. A task fully specified for autonomous agent execution without human interaction.                                         |
| **Vertical slice**         | A unit of work that cuts through all layers end-to-end, is demo-able or verifiable on its own.                                              |
| **Durability**             | The principle that issue content must survive radical codebase changes -- no file paths, domain language, behavioural criteria.              |
| **Agent brief**            | A structured comment added to AFK issues describing current/desired behaviour, key interfaces, acceptance criteria, and scope boundaries.   |
| **Triage state**           | Label-based state for GitHub issues: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix.                                   |
| **Vault**                  | The user's Obsidian vault. Wiki domain skills run from the vault root.                                                                       |
| **Absorb-and-split**       | Wikipedia-model algorithm: insert content into an existing knowledge doc, then split oversized sections into new docs with cross-links.       |
| **Canonical frontmatter**  | The standard YAML frontmatter shape for knowledge notes: `up`, `related`, `also`, `aliases`, `tags`. Defined in the wiki domain spec.        |
| **INDEX.md**               | Agent-maintained directory index file with frontmatter (`description`, `conventions`) and body describing purpose and structure.              |
| **Classification routing** | The decision process mapping raw notes to destinations: `03-knowledge/`, `04-notes/`, `05-projects/`, or `00-raw/hitl/`.                     |
| **Kaizen**                 | Continuous tiny improvement. Journal-domain principle: 1% better every day, experiments graduate to standards, friction triggers 5 Whys.     |
| **Standard**               | A locked-in baseline in `kaizen.md` graduated from a kept experiment. Carried into every sprint by `/weekly` unless explicitly calibrated.   |
| **Improvement Log**        | Append-only dated section of `kaizen.md` capturing one tiny improvement per `/reflect`. Reviewed by `/ponder`, summarised by `/chronicle`.   |
| **Active Calibration**     | A recorded adjustment to a standard or habit (typically a kaizen-shrink) under trial for one sprint, logged in `kaizen.md`.                  |
| **One-Day PDCA**           | The daily Plan-Do-Check-Act micro-loop: `/daily` plans an intent, the day acts, `/reflect` checks outcome and adjusts.                       |
| **5 Whys**                 | Root-cause mini-dialogue triggered in `/reflect` when friction recurs. Result recorded in the `kaizen.md` 5 Whys Log with a counter-measure. |
| **Kaizen-shrink**          | Reducing a failing habit to a near-zero-friction floor instead of abandoning it. Logged to Active Calibrations and trialled for one sprint.  |
