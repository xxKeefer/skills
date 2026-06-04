# Nix Manager

NixOS config management skills -- add, remove, rice, refine, debug, and explain. Designed for
incremental improvement of a flake-based NixOS config with home-manager.

## Dependencies

Requires `primitives` plugin (`/grill-it`, `/write-to-file`).

## Philosophy

Zen labour. Every interaction leaves the config more idiomatic. Skills restructure freely --
splitting modules, renaming files, reorganising imports are all welcome. The goal is convergence
toward a clean, maintainable, well-understood system.

## Conventions

- Config discovery: skills assume cwd is the config repo root (contains `flake.nix`)
- Apply: edit files, explain changes, offer `nixos-rebuild test` or `switch` -- never auto-rebuild
- Teaching: inline comments for non-obvious *why*; chat explanation after every change
- Boundary: `home/` (home-manager), `system/` (NixOS modules), `hosts/` (hardware, don't touch)
- Restructuring: always allowed. Split modules, rename files, reorganise imports as needed.

## Best practice guidelines

- Design for LLM collaboration -- config should be modifiable in userspace without root access
- Modular over monolithic -- single-responsibility files, clean imports, logical grouping
- Home-manager via nixos-rebuild integration, not standalone
- Prefer declarative `programs.*` / `services.*` modules over raw package lists
- No single dogma -- follow community consensus from popular, well-maintained public configs

## Skills

| Skill | Type | Purpose |
|---|---|---|
| `/add-it` | HITL | Find and add packages or capabilities |
| `/remove-it` | HITL | Cleanly remove packages or capabilities |
| `/rice-it` | HITL | Visual customization from screenshots, descriptions, or repos |
| `/refine-it` | HITL | Best-practice audit and improvement (targeted or full) |
| `/debug` | AFK | Diagnose and fix build errors |
| `/explain` | AFK | Plain-language explanation of nix config |
