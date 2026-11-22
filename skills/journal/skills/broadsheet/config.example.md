# Broadsheet config

Copy this file to `~/.claude/broadsheet.md` and fill it in. An `accent=<colour>` argument in the call overrides its line here.

- paper name: The Obsidian Oracle
- accent: any CSS colour for the headings, tags, and chosen rows. Default: `#8b1e3f` (oxblood)
- places: the weather box shows a forecast for each place. Give each place as a sub-bullet, `<label>: <place name>`, such as `home: Brisbane`. A place name is looked up when the page is printed, so no coordinates are needed. A pair of coordinates, `<label>: <lat> <lon>` in decimal degrees, such as `office: 51.5072 -0.1276`, skips the lookup and is exact for a suburb. With no places, the box says to set one. A `place=<label or name>` argument shows only that place: a label picks a place from this list, and any other name is looked up
- stale: 90 days. A note outside the journal, inbox, archive, meta, and knowledge folders with no edit for this long goes on the stale shelf
- archive: 180 days. An archived note this old, with no link from outside the archive, is a delete candidate
