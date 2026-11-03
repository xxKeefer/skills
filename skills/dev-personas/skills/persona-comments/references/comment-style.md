# persona-comments: made-up reasons and prose style

17. **A made-up reason for an existing pattern (Change Requested).** A *why* comment the diff adds to code it didn't write, giving a rationale nothing in the diff, the ticket, or the history supports. A wrong reason is worse than none: the next reader trusts it. Remove it unless the PR description or a linked source shows the reason.
18. **Comment prose style (Nit).** In added comments: Latin abbreviations (`e.g.`, `i.e.`, `etc.`; write "such as", "in other words"), "execute" where "run" works, should/must hedging where the comment can state what happens, exclamation marks, rhetorical questions, metaphors, or a missing subject ("Called on logout" → "The store calls this on logout"). Don't flag the codebase's own acronyms or contractions.
19. **`NOTE:`/`TODO:`/`FIXME:` on something unremarkable (Nit).** A marker on an ordinary comment dilutes the ones that flag something real. Drop the marker.
