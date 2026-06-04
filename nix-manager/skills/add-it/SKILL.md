---
name: add-it
description: >
  Find and add a package or capability to the NixOS config, even when the user doesn't know the
  exact package name. Use when user says "add X", "I need X", "install X", or describes a
  capability they want.
---

# Add It

Find and add a package or capability to the config. Fuzzy -- the user describes what they want,
the skill finds the right package and wires it up idiomatically.

## Step 1: Parse the Request

`$ARGUMENTS` is a free-text description of desired functionality.

Examples: "image editing", "a terminal file manager", "docker support", "bluetooth"

Identify: what capability does the user want? Is it a user app, a system service, or both?

## Step 2: Find Candidates

Search for candidate packages. Use `nix search nixpkgs`, web search, or training knowledge.

Present a short comparison table:

| Package | Description | Notes |
|---|---|---|
| `gimp` | Full-featured image editor | GTK, large |
| `krita` | Digital painting | KDE, tablet support |
| `inkscape` | Vector graphics | SVG-focused |

Recommend one with rationale. Ask user to pick.

**Done when:** user has chosen a package (or accepted the recommendation).

## Step 3: Determine Placement

Read the current config structure to understand existing module organisation.

Decide:
- **home/** -- user-level app, dotfile, or home-manager program module
- **system/** -- system service, driver, hardware, or daemon
- **Both** -- things like Docker (system service + user group) or apps needing system deps

If both, explain the split to the user.

**Done when:** placement is decided.

## Step 4: Check Existing Modules

Does a relevant module already exist? (e.g. adding a second terminal emulator to an existing
`home/terminal/` module)

- If yes: add to the existing module
- If no: decide whether to create a new module file or add to an existing catch-all
- If restructuring improves the result (e.g. splitting a bloated file): do it

**Done when:** target file(s) identified or created.

## Step 5: Write the Config

Prefer `programs.*` or `services.*` home-manager/NixOS modules over raw package lists when
available -- they're more idiomatic and configurable.

Add inline comments only for non-obvious *why* choices.

**Done when:** config is written.

## Step 6: Explain

Post-edit, explain in chat:
- What was added and where
- Why this pattern was chosen (e.g. "added via `programs.git` instead of `home.packages`
  because the programs module lets you configure git declaratively")
- Any nix concepts worth understanding

**Done when:** user acknowledges.

## Step 7: Offer Rebuild

Ask: "Want me to run `nixos-rebuild test` to try it, or `nixos-rebuild switch` to apply?"

If the rebuild fails, invoke `/debug` to diagnose.

**Done when:** rebuild succeeds or user declines.

## Principles

- Prefer home-manager `programs.*` modules over raw packages when available.
- If adding something that spans system and home config, handle both and explain the split.
- Restructuring is welcome if it improves organisation.
- Always explain why this pattern, not just what was added.
