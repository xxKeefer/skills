# 0003 One home for shared text

**Status:** Accepted, 2026-10-29

## Context

Two blocks of rule text were copied across skills, so a change to a rule needed an edit in every
copy:

- **The STE rule.** Six skills told the agent to write in Simplified Technical English, and each
  copy listed up to six rules: `primitives:explain`, `primitives:handoff`,
  `primitives:update-handoff`, `experimental:repro`, `experimental:simulate`, and
  `deprecated:explain-reasoning`. The `repro` copy listed four of the six.
- **The proof-read hard rules.** `scribe:proof-read`, `scribe:grices-maxims`, `scribe:asd-ste100`,
  and `scribe:orwells-six` shared four identical rules. The `Editing` section of the scribe
  `CLAUDE.md` restated the first one.

A skill can reach a file inside its own plugin from any install, but not a file above its plugin
root (ADR 0001). So one repo-level file cannot serve skills in three plugins.

## Decision

**STE.** Each plugin that has an STE skill holds one `STE.md` at its plugin root:
`skills/primitives/STE.md`, `skills/experimental/STE.md`, and `skills/deprecated/STE.md`. The
three files are identical. Each skill keeps the leading word, links its plugin's file, and keeps
its own local clause.

The rule list changed in one place: an em dash is now allowed when used sparingly. The old copies
banned it. The other five rules are unchanged.

Options not chosen:

- The leading word alone, or with one clause, in each skill. This leaves the rule list to the
  model's idea of STE.
- No paragraph, with the `proof-read` output style as the source. Only machines that selected that
  style would get the rule.
- A model-invoked primitive that holds the rule. Its description costs context load every turn.
- One repo-level file. It breaks in a copied install.

**Hard rules.** `skills/scribe/HARD-RULES.md` holds the four shared rules. Each proof-read skill
links it and keeps its own fifth rule: the term-of-art exemption, or the ban on invented facts in
`grices-maxims`. The scribe `CLAUDE.md` links the file.

## Consequences

- To change the STE rule, edit all three `STE.md` files. To change a shared hard rule, edit
  `HARD-RULES.md` only.
- A new skill in another plugin that needs the STE rule adds an `STE.md` to that plugin.
- The skills link both files by a relative path (`../../STE.md`, `../../HARD-RULES.md`). The path
  stays inside the plugin, so it works from a copied install.
- The rule text now sits behind a link. Each pointer tells the agent to read the file before it
  writes or audits.
- The output styles and the `asd-ste100` lens still ban the em dash as a prose connector. They
  govern different text, and this decision does not change them.
