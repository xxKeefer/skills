# Suggested tests: library edge cases, spies and cached requests

- **Exception: an edge case that a shared library function owns.** Do not ask for an app-level test of an edge case that a shared library function handles and already tests. Name the library test instead. When the library has no such test, propose the test in the library.
- **Assert an observable result.** A suggested test asserts a request sent or a rendered row, not a spy on a library call such as a cache method. `persona-test-quality` rule 1 calls that spy coupling.
- **Check the cache before you mock a request.** Before a suggested test mocks or counts a request, read the cache freshness of the query that sends it (`staleTime`, a cache entry set earlier in the test). When the cache would answer, the test removes or expires the cache entry first. Otherwise the mock is never hit, and a "not requested" check passes either way.
