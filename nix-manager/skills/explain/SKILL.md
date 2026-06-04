---
name: explain
description: >
  Explain what a block of nix config does in plain language. Layered explanation: what, how, why.
  Agent-invocable. Other skills call this to teach, or the user asks directly.
---

# Explain

Plain-language explanation of nix config. Layered: what it does, how it works, why it's written
that way.

## Step 1: Identify the Target

`$ARGUMENTS` may contain:
- A file path -- explain the whole file/module
- A module name -- find and explain it
- A code snippet in conversation -- explain that block
- A nix concept -- explain the concept with examples from the user's config

If unclear, ask what the user wants explained.

**Done when:** target code is identified and read.

## Step 2: Explain in Layers

**What** -- one sentence on what this code does.

**How** -- walk through the nix constructs used:
- Function arguments (`{ pkgs, lib, ... }:`)
- Attribute sets and nesting
- `let...in` bindings
- `mkIf`, `mkMerge`, `mkOption` and other `lib` functions
- `imports` and module composition
- `with`, `inherit`, `rec`
- Overlays, `specialArgs`, `extraSpecialArgs`

**Why** -- the pattern or idiom behind this structure:
- Why is it a separate module?
- Why this approach over alternatives?
- What's the design principle?

**Done when:** all three layers covered.

## Step 3: Flag Issues (if any)

If the code is non-idiomatic, mention what the idiomatic version would look like -- but don't
change it. That's `/refine-it`'s job.

If the code is genuinely wrong or confusing, say so directly.

**Done when:** issues flagged (or confirmed clean).

## Step 4: Connect to Context

Show how this piece fits the bigger picture:
- "This module is imported by your `flake.nix` here, which means..."
- "This `specialArgs` value flows from your flake through to every module via..."
- "The `follows` declaration means this input shares the same nixpkgs as..."

If the user asked about a nix concept, show where it appears in their own config.

**Done when:** context is connected.

## Principles

- Assume novice level but don't be condescending -- explain concepts, don't dumb them down.
- Connect to the bigger picture. Isolated explanations are less useful than connected ones.
- Use the user's own config for examples, not abstract ones.
- If something is weird or wrong, say so. Don't pretend bad code is fine.
