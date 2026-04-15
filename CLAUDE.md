@ubiquitous.md

# xxkeefer-skills

A marketplace of personal skills for working with AI agents. Every skill is framework-agnostic,
language-agnostic, and tool-agnostic -- pure best-practice principles expressed as markdown
workflows.

## Domains

| Domain | Purpose | Always required? |
|---|---|---|
| `primitives` | Foundational skills other domains compose | Yes |
| `developer` | Engineering workflows -- investigation to closure | No |
| `journal` | Life admin -- agile-inspired personal growth | No |
| `meta` | Skills about skills -- writing, auditing, teaching | No |
| `omen` | Creative -- TTRPG, worldbuilding, narrative | No |
| `wiki` | Raw note intake, knowledge management, vault indexing | No |

## Architecture

Each domain is an independent plugin in the `xxkeefer-skills` marketplace. Domains are versioned
separately and can be enabled/disabled independently. The `primitives` domain is a prerequisite
for all others -- it provides foundational skills (like `/grill-it`) that other domains compose.

The root directory owns only the marketplace registry (`.claude-plugin/marketplace.json`) and
shared documentation. No skills live at root.

## North Star

Everything-agnostic. Skills encode *how to think about problems*, not how to use specific tools.
A skill should work equally well whether you're writing Rust, TypeScript, Python, or anything
else. No framework lock-in, no language assumptions, no tool dependencies beyond the agent itself.
