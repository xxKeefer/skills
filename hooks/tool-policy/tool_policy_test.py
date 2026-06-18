#!/usr/bin/env python3
"""Run: python3 tool_policy_test.py  (exits non-zero on failure)."""
import json
import pathlib
import sys

import tool_policy

# Tests run against the worked example (it carries real rules); the shipped
# tool-policy.config.json is intentionally empty. Self-protection cases below
# still assert against the runtime config name, which is hardcoded in the hook.
CONFIG = json.loads((pathlib.Path(__file__).parent / "tool-policy.example.json").read_text())


def blocked(cmd):
    return tool_policy.evaluate(cmd, CONFIG)


CASES = [
    # (command, should_block, substring expected in reason or None)
    # --- runner redirection (redirects map) ---
    ("npx vitest run foo.spec.ts", True, "test:unit"),
    ("pnpm exec tsc --noEmit", True, "typecheck"),
    ("npx eslint .", True, "lint"),
    ("npx vue-tsc --noEmit", True, "typecheck"),
    ("npx playwright test", True, "test:integration"),
    ("pnpm dlx vite build", True, "build"),
    # block-all: unknown tool with no canonical equivalent -> generic + allowlist hint
    ("npx some-random-cli --flag", True, "allowlist"),
    ("pnpm exec made-up-tool", True, "allowlist"),
    # allowlist passes through
    ("pnpm exec syncpack list-mismatches", False, None),
    ("npx nx test:unit portal", False, None),
    ("npx playwright install", False, None),
    ("npx playwright install chromium", False, None),
    # second segment of a compound command is still inspected
    ("echo hi && npx eslint .", True, "lint"),
    ("npx vitest foo || true", True, "test:unit"),
    # runner appears only inside a quoted string -> NOT a real invocation
    ('git commit -m "switch to pnpm exec for syncpack"', False, None),
    ("grep -q 'npx vitest' file.txt", False, None),
    ('echo "run npx eslint manually"', False, None),
    # --- blockedCommands (folds in the old inline git-stash grep, but quote-aware) ---
    ("git stash", True, "clean state"),
    ("git stash push -m wip", True, "clean state"),
    ("git stash list", True, "clean state"),
    ("echo done && git stash", True, "clean state"),
    # blocked command named inside a string -> NOT blocked (the grep's old false-positive)
    ('git commit -m "remember to git stash first"', False, None),
    ("grep -q 'git stash' notes.txt", False, None),
    # near-miss prefix does not trip
    ("git status", False, None),
    # --- plain commands untouched ---
    ("nx test:unit portal", False, None),
    ("ls -la", False, None),
    # unparseable (stray quote) -> fail open, never false-block
    ('echo "unterminated', False, None),
    # --- self-protection: any command naming the config file is rejected ---
    ("echo x >> tool-policy.config.json", True, "human-managed"),
    ("sed -i '' s/x/y/ tool-policy.config.json", True, "human-managed"),
    ("cat tool-policy.config.json", True, "human-managed"),
]


def main():
    failures = []
    for cmd, should_block, needle in CASES:
        reason = blocked(cmd)
        is_blocked = reason is not None
        if is_blocked != should_block:
            failures.append(f"  {cmd!r}: expected block={should_block}, got block={is_blocked} ({reason!r})")
        elif should_block and needle and needle not in reason:
            failures.append(f"  {cmd!r}: reason missing {needle!r}: {reason!r}")

    if failures:
        print(f"FAIL ({len(failures)}/{len(CASES)}):")
        print("\n".join(failures))
        sys.exit(1)
    print(f"OK ({len(CASES)} cases)")


if __name__ == "__main__":
    main()
