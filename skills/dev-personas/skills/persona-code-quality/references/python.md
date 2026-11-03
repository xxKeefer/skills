# persona-code-quality: Python rules

### Python (scripts and tooling)

1. **Stdlib reuse (Change Requested / Nit).** Hand-rolled logic the stdlib already has: `pathlib` over `os.path` string joins, `collections.Counter`/`defaultdict` over manual count dicts, `itertools` (`groupby`, `chain`, `pairwise`, `batched`) over index loops, `json`/`csv` over string splitting, `subprocess.run(..., check=True)` over hand-checked return codes, `datetime`/`timedelta` over string date arithmetic, `argparse` over manual `sys.argv` parsing.
2. **Oversized / multi-responsibility functions (Change Requested / Nit).** One function = one thing. A `main()` that fetches, transforms, plots and prints is several functions. Split fetch / transform / render so each can be read (and cached or tested) alone.
3. **Duplication (Nit).** The same query, request loop, or parsing block pasted with small changes (e.g. three near-identical GraphQL pagination loops) → one parameterised helper.
4. **Mutation and shared state (Nit).** Module-level mutable globals written from functions; mutable default arguments (`def f(x=[])` is Change Requested. It is shared across calls); in-place mutation of a caller's list/dict where returning a new value works.
5. **Imperative accumulation (Nit).** `for` loops that only build a list/dict/set → comprehensions; `any()`/`all()`/`sum()`/`max(key=…)` over flag-and-break loops.
6. **Resource cleanup (Change Requested).** Files, sockets, or temp dirs opened without `with` (or `tempfile.TemporaryDirectory()`), so an exception leaks the handle or leaves junk on disk.
7. **Boolean flag parameters (Nit).** Split into separate functions or use an `Enum`/`Literal[...]`.

Python correctness defects (a wrong date boundary, an unchecked subprocess failure silently caching an empty result) belong to a general code review unless they are a direct consequence of one of the structure rules above.
