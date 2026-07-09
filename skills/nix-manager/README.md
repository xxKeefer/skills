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
| `/add` | Find and add packages or capabilities to your config |
| `/remove` | Cleanly remove packages or capabilities |
| `/rice` | Visual customization from screenshots, descriptions, or repo links |
| `/refine` | Best-practice audit and improvement |
| `/debug` | Diagnose and fix build errors |
| `/explain` | Plain-language explanation of nix config blocks |
