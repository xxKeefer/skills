#!/usr/bin/env python3
"""Tests for map_units.py. Run: python3 map_units.spec.py"""
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "map_units.py")
FIXTURE = os.path.join(HERE, "fixtures", "map_program.md")

MAP = """---
doctype: map
---

# Map: test

## Decisions

### [ ] 99. Not a unit, outside Units

## Units

### [x] 1. First

- Done: one.

### [ ] 2. Second

- A note.
- Done: two.

### [ ] 3. Third

- Done: three.

### [x] 4. Fourth

- Done: four.

### [ ] 5. Fifth

- Done: five.
"""


def run(*args):
    return subprocess.run(
        ["python3", SCRIPT, *args],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class MapUnits(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        self.map = os.path.join(self.dir, "map_test.md")

    def write(self, text):
        with open(self.map, "w") as f:
            f.write(text)

    def read(self):
        with open(self.map) as f:
            return f.read()

    # C1
    def test_next_lists_units_with_no_tick_in_order(self):
        self.write(MAP)
        r = run("next", self.map)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "2\tSecond\n3\tThird\n5\tFifth\n")

    def test_next_stops_at_batch(self):
        self.write(MAP)
        r = run("next", self.map, "--batch", "2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "2\tSecond\n3\tThird\n")

    def test_next_with_every_unit_ticked_prints_nothing(self):
        self.write(MAP.replace("### [ ]", "### [x]"))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "")

    # C2
    def test_unit_with_no_done_line_fails_with_its_line(self):
        self.write(MAP.replace("- Done: three.\n", ""))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        self.assertEqual(
            r.stderr,
            f"error: {self.map}:22: unit 3 has no Done: line. "
            "Fix: add a '- Done: <claim>' line under the heading.\n",
        )

    def test_malformed_unit_heading_fails_with_its_line(self):
        self.write(MAP.replace("### [ ] 2. Second", "### [ ] 2 Second"))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        self.assertIn(f"{self.map}:17: malformed unit heading", r.stderr)

    def test_next_rejects_a_batch_below_1(self):
        self.write(MAP)
        r = run("next", self.map, "--batch", "0")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, "")

    # C3
    def test_tick_ticks_one_unit_and_changes_no_other_line(self):
        self.write(MAP)
        r = run("tick", self.map, "3")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.read(), MAP.replace("### [ ] 3.", "### [x] 3."))

    def test_tick_on_a_missing_unit_exits_1(self):
        self.write(MAP)
        r = run("tick", self.map, "7")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unit 7 does not exist", r.stderr)
        self.assertEqual(self.read(), MAP)

    def test_tick_on_a_ticked_unit_exits_1(self):
        self.write(MAP)
        r = run("tick", self.map, "1")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unit 1 is already ticked", r.stderr)
        self.assertEqual(self.read(), MAP)

    def test_tick_ignores_a_heading_outside_units(self):
        self.write(MAP)
        r = run("tick", self.map, "99")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.read(), MAP)

    # C4
    def test_program_map_with_units_1_to_6_ticked_lists_7_to_11(self):
        r = run("next", FIXTURE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            [line.split("\t")[0] for line in r.stdout.splitlines()],
            ["7", "8", "9", "10", "11"],
        )


if __name__ == "__main__":
    unittest.main()
