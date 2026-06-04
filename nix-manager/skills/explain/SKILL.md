---
name: explain
description: >
  Explain what a block of nix config does in plain language. Layered explanation: what, how, why.
  Agent-invocable. Other nix-manager skills call this to teach, or the user asks directly.
---

# Explain

Plain-language explanation of nix config. Composes on the `/explain` primitive with nix-specific
context.

## Step 1: Identify the Target

`$ARGUMENTS` may contain:
- A file path -- explain the whole file/module
- A module name -- find and explain it
- A code snippet in conversation -- explain that block
- A nix concept -- explain the concept with examples from the user's config

If unclear, ask what the user wants explained.

## Step 2: Explain via /explain

Invoke `/explain` with the identified target. When constructing the explanation layers, use
nix-specific framing:

- **What:** one sentence on what this code does
- **How:** walk through the nix constructs used -- function arguments (`{ pkgs, lib, ... }:`),
  attribute sets, `let...in`, `mkIf`/`mkMerge`, `imports`, `with`/`inherit`, overlays,
  `specialArgs`
- **Why:** the nix pattern or idiom behind the structure -- why a separate module, why this
  approach over alternatives

## Step 3: Flag Non-idiomatic Code

If the code is non-idiomatic, mention what the idiomatic version would look like -- but don't
change it. That's `/refine-it`'s job.

If the code is genuinely wrong or confusing, say so directly.

## Step 4: Connect to Context

Show how this piece fits the bigger picture:
- "This module is imported by your `flake.nix` here, which means..."
- "This `specialArgs` value flows from your flake through to every module via..."
- "The `follows` declaration means this input shares the same nixpkgs as..."

If the user asked about a nix concept, show where it appears in their own config.

## Principles

- Assume novice level but don't be condescending -- explain concepts, don't dumb them down.
- Use the user's own config for examples, not abstract ones.
- If something is weird or wrong, say so.
