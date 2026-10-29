# Nix Manager

NixOS config management -- add, remove, rice, refine, debug, and explain.

Designed for incremental improvement of a flake-based NixOS config with home-manager. Teaches
idiomatic nix as it goes.

## Installation

```json
{
  "enabledPlugins": {
    "nix-manager@xxkeefer-skills": true
  }
}
```

## Usage

Run skills from your nixos-config directory (the one containing `flake.nix`).

## Skills

| Skill | Purpose |
|---|---|
| `/nix-add` | Find and add packages or capabilities to your config |
| `/nix-remove` | Cleanly remove packages or capabilities |
| `/nix-rice` | Visual customization from screenshots, descriptions, or repo links |
| `/nix-refine` | Best-practice audit and improvement |
| `/nix-debug` | Diagnose and fix build errors |
| `/nix-explain` | Plain-language explanation of nix config blocks |
