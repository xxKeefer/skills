# Defect hotspots

`/self-improve` writes a defect hotspots file for each repo that it mines. Read the file of this
repo, if it exists:

`${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/<repo key>/defect-hotspots.md`

The repo key is `<owner>--<repo>` from the `origin` URL. With no `origin`, it is
`local--<main worktree folder name>`.

- A changed file in or under one of its Hotspots areas is a hotspot. It raises the behaviour's
  likelihood one step, the same as a file with a history of fixes. Raise it only once.
- The area's Usually missed column names the escape types that got past the tests before. Derive
  the conditions for those types first.
- A Skewed line means that the table misses the areas whose commits do not name their bug. An area
  that is not in the table can still be a hotspot.
