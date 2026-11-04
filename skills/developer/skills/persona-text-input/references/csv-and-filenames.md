# CSV export and filenames (rules 11 and 12)

11. **CSV quoting and encoding (Change Requested).** An export that joins fields with `,` and doesn't quote commas, quotes, and newlines; an export with no UTF-8 BOM, so Excel shows `Zürich` as `ZÃ¼rich`; an upload read without an explicit encoding, so an em dash becomes `�`. Formula injection (`=`, `+`, `-`, `@`) → `persona-security`. (IN-H2, IN-H3)
12. **Filename built from user text (Nit).** A download named from a service or company name with `/`, `:`, `"`, or a 200-character name left in it. Strip reserved characters and cap the length. (IN-H4)
