---
name: refine-it
description: >
  Improve the NixOS config toward idiomatic best practices. Full audit or targeted at a specific
  file or module. Use when user says "refine my config", "improve my flake", "make this more
  idiomatic", or wants a best-practice review.
---

# Refine It

The zen polishing skill. Audit the config and improve it toward idiomatic nix. Every invocation
should leave the config measurably better.

## Step 1: Determine Scope

`$ARGUMENTS` is an optional target:
- A file path or module name -> targeted refinement
- Empty -> full config audit

If targeted: read the specified file/module.
If full audit: scan the entire config structure.

**Done when:** scope is set and code is read.

## Step 2: Evaluate

Assess against best practices, prioritised by impact:

**Module structure**
- Single-responsibility modules
- Clean imports (no circular, no dead)
- Logical file organisation

**Flake hygiene**
- Minimal inputs (only what's used)
- Proper `follows` declarations
- Clean outputs structure

**Home-manager patterns**
- `programs.*` / `services.*` over raw package lists
- Proper option types
- Declarative config over imperative scripts

**Nix idioms**
- Avoid `with pkgs;` at top level (pollutes scope, hides dependencies)
- Use `lib` functions properly (`mkIf`, `mkMerge`, `mkOption`)
- Proper `let...in` scoping
- `inherit` where it reduces noise

**Organisation**
- No catch-all files
- Related config grouped logically
- DRY without over-abstraction (three lines > premature module)

**Done when:** evaluation is complete.

## Step 3: Present Findings

Prioritised list -- highest impact first. Each item:

1. **What** -- the issue in one line
2. **Why** -- why it matters (reference community patterns, NixOS wiki, popular repos)
3. **Fix** -- what the fix looks like (brief)

Ask user which items to tackle, or "all".

**Done when:** user has chosen items.

## Step 4: Apply Fixes

Restructure freely -- rename files, split modules, reorganise imports, extract patterns.

For each change:
- Make the edit
- Add inline comments only for non-obvious *why*

**Done when:** all chosen fixes applied.

## Step 5: Explain

Walk through each change:
- What was done
- Why it's more idiomatic
- The nix concept behind it (if the user might not know it)

**Done when:** user acknowledges.

## Step 6: Offer Rebuild

Ask: "Want me to run `nixos-rebuild test` to try it, or `nixos-rebuild switch` to apply?"

If the rebuild fails, invoke `/debug` to diagnose.

**Done when:** rebuild succeeds or user declines.

## Principles

- Prioritise by impact. One structural improvement > ten cosmetic tweaks.
- Every invocation should leave the config measurably better.
- Reference community patterns when explaining *why* -- not just "this is better" but "this is
  what the NixOS module system is designed for".
- Restructuring is the point. Don't be shy about splitting, renaming, or reorganising.
