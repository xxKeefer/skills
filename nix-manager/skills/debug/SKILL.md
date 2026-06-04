---
name: debug
description: >
  Diagnose and fix nixos-rebuild failures or nix evaluation errors. Agent-invocable -- other
  skills call this when a rebuild fails. Also usable directly when the user pastes an error.
---

# Debug

Diagnose and fix nix build errors. Called by other nix-manager skills when rebuilds fail, or
directly when the user pastes an error.

## Step 1: Parse the Error

`$ARGUMENTS` contains error output or context from a failed rebuild.

Identify:
- The failing module or attribute path
- The error type (evaluation error, type mismatch, missing attribute, build failure, etc.)
- The relevant file(s) and line(s)

**Done when:** the error location and type are identified.

## Step 2: Read the Code

Read the relevant config files around the error location. Understand the context -- what was
the code trying to do?

**Done when:** the relevant code is understood.

## Step 3: Diagnose

Common causes:
- Typos in attribute names
- Missing flake inputs or `specialArgs`
- Type mismatches (string where list expected, etc.)
- Deprecated options (NixOS options change between releases)
- Version incompatibilities between inputs
- Incorrect `imports` paths
- `with pkgs;` scope issues hiding the real dependency
- Missing `lib` in function arguments

**Done when:** root cause is identified.

## Step 4: Explain

Explain the error in plain language:
- "This failed because X."
- "In nix, Y works like Z." (teach the concept if relevant)
- If the error stems from a pattern that `/refine-it` would flag, mention that.

**Done when:** explanation delivered.

## Step 5: Fix

Apply the fix. If the fix requires understanding a nix concept (option types, lazy evaluation,
the module system), give a brief explanation.

**Done when:** fix is applied.

## Step 6: Verify

Offer to rebuild to verify the fix.

If it fails again, loop back to Step 1.

**Done when:** rebuild succeeds or user takes over.

## Principles

- Always explain the error -- every failure is a teaching moment.
- Connect to broader patterns: "this is why `/refine-it` recommends avoiding `with pkgs;`".
- If the fix is a workaround rather than a proper solution, say so and suggest the proper fix.
