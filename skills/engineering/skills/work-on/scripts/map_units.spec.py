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
TEMPLATE = os.path.join(
    HERE, "..", "..", "..", "..", "primitives", "skills", "write-to-file", "templates", "map.md"
)

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

    def test_next_uses_the_batch_key_of_the_map(self):
        self.write(MAP.replace("doctype: map\n", "doctype: map\nbatch: 1\n"))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "2\tSecond\n")

    def test_batch_flag_overrides_the_batch_key(self):
        self.write(MAP.replace("doctype: map\n", "doctype: map\nbatch: 1\n"))
        r = run("next", self.map, "--batch", "2")
        self.assertEqual(r.stdout, "2\tSecond\n3\tThird\n")

    def test_next_with_no_batch_key_lists_five(self):
        extra = "".join(f"\n### [ ] {n}. Unit {n}\n\n- Done: x.\n" for n in range(6, 10))
        self.write(MAP + extra)
        r = run("next", self.map)
        self.assertEqual(len(r.stdout.splitlines()), 5)

    def test_next_rejects_a_batch_key_below_1(self):
        self.write(MAP.replace("doctype: map\n", "doctype: map\nbatch: 0\n"))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 1)
        self.assertIn("batch", r.stderr)

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

    def test_next_on_a_map_with_no_units_section_fails(self):
        self.write("---\ndoctype: map\n---\n\n# Map: K-1\n\n### [ ] 1. K-2 Sub\n\n- Done: two.\n")
        r = run("next", self.map)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        self.assertIn(f"error: {self.map}: no ## Units section.", r.stderr)

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

    # r2.1: a split unit becomes sub-units N.1, N.2 in the map
    def test_next_and_tick_read_sub_units_of_a_split_unit(self):
        split = MAP.replace(
            "### [ ] 3. Third\n\n- Done: three.\n",
            "### [ ] 3.1. Third, part one\n\n- Done: three a.\n\n"
            "### [ ] 3.2. Third, part two\n\n- Done: three b.\n",
        )
        self.write(split)
        r = run("next", self.map)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            r.stdout, "2\tSecond\n3.1\tThird, part one\n3.2\tThird, part two\n5\tFifth\n"
        )
        r = run("tick", self.map, "3.2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.read(), split.replace("### [ ] 3.2.", "### [x] 3.2."))
        r = run("tick", self.map, "3")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unit 3 does not exist", r.stderr)

    def test_sub_unit_with_no_done_line_fails_with_its_line(self):
        self.write(MAP.replace("### [ ] 3. Third\n\n- Done: three.\n", "### [ ] 3.1. Third\n\n- A note.\n"))
        r = run("next", self.map)
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.map}:22: unit 3.1 has no Done: line", r.stderr)

    # C3: the template layout, with the unit fields of /split-ticket
    def test_map_from_the_template_with_split_ticket_fields_passes_next(self):
        with open(TEMPLATE) as f:
            text = f.read()
        text += (
            "\n### [ ] 2. K-2 Sub\n\n- Wave 1. Estimate: 2. Parent ACs: A.\n"
            "- builds_on: none\n- merge: alone\n- Files or areas: x.\n"
            "- Done: the ACs of K-2 hold, and its PR is merged.\n"
        )
        self.write(text)
        r = run("next", self.map)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([l.split("\t")[0] for l in r.stdout.splitlines()], ["1", "2"])

    # C4
    def test_program_map_fixture_lists_unit_15_first(self):
        r = run("next", FIXTURE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.splitlines()[0].split("\t")[0], "15")


if __name__ == "__main__":
    unittest.main()
