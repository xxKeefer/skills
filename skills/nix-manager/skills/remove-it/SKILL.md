---
name: remove-it
description: >
  Cleanly remove a package, module, or capability from the NixOS config. Traces all references
  and cleans up. Use when user says "remove X", "uninstall X", "drop X", "I don't use X anymore".
---

# Remove It

Cleanly remove a package or capability. Traces all references, proposes a removal plan, cleans up.

## Step 1: Parse the Request

`$ARGUMENTS` is what to remove.

Examples: "steam", "bluetooth", "the gaming module", "firefox"

## Step 2: Trace References

Search the entire config for all references to the target:
- Package declarations (`home.packages`, `environment.systemPackages`)
- Service/program modules (`programs.*`, `services.*`)
- Module imports
- Related config blocks (e.g. removing bluetooth might touch waybar, desktop env)
- Comments referencing the target

Present findings:

> Found 3 references to bluetooth:
> - `system/desktop.nix:18` -- `hardware.bluetooth.enable`
> - `system/desktop.nix:19` -- `hardware.bluetooth.powerOnBoot`
> - `system/desktop.nix:20` -- `services.blueman.enable`

**Done when:** all references are mapped.

## Step 3: Propose Removal Plan

For each reference, state what will happen:
- **Delete** -- the line/block is removed
- **Modify** -- the surrounding code is adjusted
- **Flag** -- related config that *might* want removing but isn't certain

If a module file would become empty after removal, propose deleting the file and its import.

Ask user to confirm scope -- they might want to keep some parts.

**Done when:** user approves the plan.

## Step 4: Execute Removal

Remove approved items. Also clean up:
- Dangling imports (importing a file that no longer exists)
- Empty module files
- Orphaned comments
- Empty lists (`imports = [];`, `packages = [];`)

**Done when:** all removals applied, no orphans left.

## Step 5: Explain

Post-edit, explain:
- What was removed
- Any side effects or related config that was left in place and why
- Anything the user should know ("bluetooth was also referenced in your waybar config for
  the battery widget -- I left that alone, flag if you want it removed too")

**Done when:** user acknowledges.

## Step 6: Offer Rebuild

Ask: "Want me to run `nixos-rebuild test` to try it, or `nixos-rebuild switch` to apply?"

If the rebuild fails, invoke `/debug` to diagnose.

**Done when:** rebuild succeeds or user declines.

## Principles

- Conservative by default -- flag related config rather than silently removing it.
- Clean up after yourself -- no empty imports, orphaned modules, or dead comments.
- Explain side effects the user might not anticipate.
