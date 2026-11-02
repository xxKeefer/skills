# NixOS: wire the loader in home-manager

Home-manager owns `.zshrc` as a read-only link into the nix store. The user adds the loader to the
nix config once. After that rebuild, new modules need only `exec zsh`, and no rebuild.

Give the user this snippet. Put the loader from [SKILL.md](SKILL.md) in place of `<loader>`.

```nix
{ config, ... }:
{
  # Link ~/.config/zsh to the dotfiles checkout. Nix keeps the link, not the files.
  xdg.configFile."zsh".source =
    config.lib.file.mkOutOfStoreSymlink "${config.home.homeDirectory}/<dotfiles checkout>/zsh";

  # Load the modules each time a shell starts.
  programs.zsh.initContent = ''
    <loader>
  '';
}
```

Tell the user:

- Leave out the `xdg.configFile` line until the dotfiles checkout exists. The loader alone works on
  a plain folder.
- `initContent` is the option name from home-manager 25.05. Older versions use `initExtra`.
- If the config sets `programs.zsh.dotDir = ".config/zsh"`, home-manager writes `.zshrc` into that
  folder, and the link conflicts with it. Use a different `dotDir`.
