#!/usr/bin/env python3
"""Tests for skill-tally.py. Run: python3 skill-tally.spec.py"""
import json
import os
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill-tally.py")


def run(event, tally_file, stdin=None):
    payload = stdin if stdin is not None else json.dumps(event)
    return subprocess.run(
        ["python3", SCRIPT],
        input=payload,
        capture_output=True,
        text=True,
        env={**os.environ, "SKILL_TALLY_FILE": tally_file},
    )


def event(skill):
    return {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": skill}}


class SkillTally(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.tally = os.path.join(self.dir, "skill-tally.json")

    def read(self):
        with open(self.tally) as f:
            return json.load(f)

    def test_first_seen_skill_starts_at_one(self):
        run(event("tools:spike-it"), self.tally)
        self.assertEqual(self.read(), {"tools:spike-it": 1})

    def test_repeated_invocations_compound(self):
        for _ in range(3):
            run(event("primitives:grill-it"), self.tally)
        self.assertEqual(self.read()["primitives:grill-it"], 3)

    def test_distinct_skills_tracked_separately(self):
        run(event("a:one"), self.tally)
        run(event("b:two"), self.tally)
        run(event("a:one"), self.tally)
        self.assertEqual(self.read(), {"a:one": 2, "b:two": 1})

    def test_missing_skill_name_is_silent_noop(self):
        r = run({"tool_name": "Skill", "tool_input": {}}, self.tally)
        self.assertEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(self.tally))

    def test_malformed_stdin_is_silent_noop(self):
        r = run(None, self.tally, stdin="not json{{{")
        self.assertEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(self.tally))

    def test_empty_stdin_is_silent_noop(self):
        r = run(None, self.tally, stdin="")
        self.assertEqual(r.returncode, 0)

    def test_corrupt_tally_file_is_reset(self):
        with open(self.tally, "w") as f:
            f.write("}}garbage")
        run(event("x:y"), self.tally)
        self.assertEqual(self.read(), {"x:y": 1})

    def test_non_skill_tool_with_skill_field_still_counts(self):
        # matcher is the harness's job; the script just reads tool_input.skill
        run(event("z:zed"), self.tally)
        self.assertEqual(self.read(), {"z:zed": 1})

    def test_concurrent_invocations_no_lost_update(self):
        procs = [
            subprocess.Popen(
                ["python3", SCRIPT],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
                env={**os.environ, "SKILL_TALLY_FILE": self.tally},
            )
            for _ in range(20)
        ]
        for p in procs:
            p.stdin.write(json.dumps(event("hot:skill")))
            p.stdin.close()
        for p in procs:
            p.wait()
        self.assertEqual(self.read(), {"hot:skill": 20})


if __name__ == "__main__":
    unittest.main(verbosity=2)
