#!/usr/bin/env python3
"""Run: python3 install_agents_md.spec.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_agents_md.py")
REAL_SECTIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sections")

ALPHA = "Alpha rule.\n"
BETA = "## Beta heading\n\nTool is {{beta_tool}}.\n"
SECTIONS = {
    "alpha.md": "lists: Alpha old\n\n" + ALPHA,
    "beta.md": "replaces: ## Beta heading\n\n" + BETA,
}
VALUES = {"beta_tool": "hammer"}

ALPHA_BLOCK = "<!-- managed: alpha -->\nAlpha rule.\n<!-- end managed -->\n"
BETA_BLOCK = "<!-- managed: beta -->\n## Beta heading\n\nTool is hammer.\n<!-- end managed -->\n"
BLOCKS = ALPHA_BLOCK + "\n" + BETA_BLOCK


class Env:
    def __init__(self, tc, sections=None, values=VALUES):
        self.dir = tempfile.mkdtemp()
        tc.addCleanup(lambda: __import__("shutil").rmtree(self.dir, ignore_errors=True))
        self.sections = os.path.join(self.dir, "sections")
        os.makedirs(self.sections)
        for name, text in (sections or SECTIONS).items():
            with open(os.path.join(self.sections, name), "w") as f:
                f.write(text)
        self.target = os.path.join(self.dir, "AGENTS.md")
        self.bak = self.target + ".bak"
        self.values = os.path.join(self.dir, "values.json")
        if values is not None:
            with open(self.values, "w") as f:
                json.dump(values, f)

    def write(self, text):
        with open(self.target, "wb") as f:
            f.write(text.encode())

    def read(self):
        with open(self.target, "rb") as f:
            return f.read().decode()

    def run(self, *extra):
        p = subprocess.run(
            [sys.executable, SCRIPT, "--target", self.target, "--values", self.values,
             "--sections", self.sections, *extra],
            capture_output=True, text=True,
        )
        return p.returncode, p.stdout, p.stderr


class FirstRun(unittest.TestCase):
    def test_blocks_go_at_the_top_and_user_text_stays_byte_for_byte(self):
        e = Env(self)
        old = "# Mine\r\n\nline  with trailing space \n\n\nend"
        e.write(old)
        code, _, err = e.run()
        self.assertEqual(code, 0, err)
        self.assertEqual(e.read(), BLOCKS + "\n" + old)

    def test_backup_holds_the_old_bytes(self):
        e = Env(self)
        e.write("old text\n")
        e.run()
        with open(e.bak) as f:
            self.assertEqual(f.read(), "old text\n")

    def test_missing_target_is_created_with_the_blocks_and_no_backup(self):
        e = Env(self)
        code, _, err = e.run()
        self.assertEqual(code, 0, err)
        self.assertEqual(e.read(), BLOCKS)
        self.assertFalse(os.path.exists(e.bak))


class SecondRun(unittest.TestCase):
    def test_second_run_gives_the_same_bytes_and_keeps_the_first_backup(self):
        e = Env(self)
        e.write("# Mine\n\ntext\n")
        e.run()
        first = e.read()
        code, out, err = e.run()
        self.assertEqual(code, 0, err)
        self.assertEqual(e.read(), first)
        with open(e.bak) as f:
            self.assertEqual(f.read(), "# Mine\n\ntext\n")

    def test_old_markers_replace_only_the_inside_and_text_around_stays(self):
        e = Env(self)
        stale = (
            "before\n\n<!-- managed: alpha -->\nstale alpha\n<!-- end managed -->\n"
            "\nbetween\n\n<!-- managed: beta -->\nstale beta\n<!-- end managed -->\n\nafter\n"
        )
        e.write(stale)
        code, _, err = e.run()
        self.assertEqual(code, 0, err)
        self.assertEqual(
            e.read(),
            "before\n\n" + ALPHA_BLOCK + "\nbetween\n\n" + BETA_BLOCK + "\nafter\n",
        )
        with open(e.bak) as f:
            self.assertEqual(f.read(), stale)

    def test_a_block_missing_from_the_file_goes_to_the_top(self):
        e = Env(self)
        e.write("<!-- managed: beta -->\nstale\n<!-- end managed -->\nmine\n")
        e.run()
        self.assertEqual(e.read(), ALPHA_BLOCK + "\n" + BETA_BLOCK + "mine\n")


class Hydration(unittest.TestCase):
    def test_missing_value_exits_1_names_the_key_and_writes_nothing(self):
        e = Env(self, values={})
        e.write("mine\n")
        code, _, err = e.run()
        self.assertEqual(code, 1)
        self.assertIn("beta_tool", err)
        self.assertIn("HYDRATE.md", err)
        self.assertEqual(e.read(), "mine\n")
        self.assertFalse(os.path.exists(e.bak))

    def test_missing_values_file_counts_as_no_values(self):
        e = Env(self, values=None)
        e.write("mine\n")
        code, _, err = e.run()
        self.assertEqual(code, 1)
        self.assertIn("beta_tool", err)


class BadMarkers(unittest.TestCase):
    def check(self, text):
        e = Env(self)
        e.write(text)
        code, _, err = e.run()
        self.assertEqual(code, 1)
        self.assertTrue(err)
        self.assertEqual(e.read(), text)
        self.assertFalse(os.path.exists(e.bak))

    def test_unmatched_start_marker(self):
        self.check("<!-- managed: alpha -->\nno end\n")

    def test_unknown_block_name(self):
        self.check("<!-- managed: gamma -->\nx\n<!-- end managed -->\n")

    def test_end_marker_with_no_start(self):
        self.check("x\n<!-- end managed -->\n")


class OldSections(unittest.TestCase):
    OLD = "# Top\n\n## Beta heading\n\nold beta text\n\n### Sub\n\nsub text\n\n## Next\n\nnext text\n"

    def test_old_heading_is_listed_and_kept_without_the_flag(self):
        e = Env(self)
        e.write(self.OLD)
        code, out, err = e.run()
        self.assertEqual(code, 0, err)
        self.assertIn("OLD beta", out)
        self.assertIn("## Beta heading", out)
        self.assertTrue(e.read().endswith("\n" + self.OLD))

    def test_block_heading_inside_markers_is_not_listed(self):
        e = Env(self)
        e.write("mine\n")
        e.run()
        _, out, _ = e.run()
        self.assertNotIn("OLD", out)

    def test_drop_deletes_the_section_up_to_the_next_heading_of_the_same_level(self):
        e = Env(self)
        e.write(self.OLD)
        code, _, err = e.run("--drop", "beta")
        self.assertEqual(code, 0, err)
        self.assertEqual(e.read(), BLOCKS + "\n# Top\n\n## Next\n\nnext text\n")

    def test_drop_at_end_of_file_deletes_to_the_end(self):
        e = Env(self)
        e.write("# Top\n\n## Beta heading\n\ntail\n")
        e.run("--drop", "beta")
        self.assertEqual(e.read(), BLOCKS + "\n# Top\n\n")

    def test_drop_stops_at_a_higher_level_heading(self):
        e = Env(self)
        e.write("## Beta heading\n\nx\n\n# Higher\n\ny\n")
        e.run("--drop", "beta")
        self.assertEqual(e.read(), BLOCKS + "\n# Higher\n\ny\n")

    def test_drop_works_on_a_file_that_already_has_the_blocks(self):
        e = Env(self)
        e.write(self.OLD)
        e.run()
        code, _, err = e.run("--drop", "beta")
        self.assertEqual(code, 0, err)
        self.assertEqual(e.read(), BLOCKS + "\n# Top\n\n## Next\n\nnext text\n")

    def test_drop_of_an_unknown_name_exits_1_and_writes_nothing(self):
        e = Env(self)
        e.write(self.OLD)
        code, _, err = e.run("--drop", "nope")
        self.assertEqual(code, 1)
        self.assertIn("nope", err)
        self.assertEqual(e.read(), self.OLD)

    def test_listed_lines_are_shown_and_never_changed(self):
        e = Env(self)
        e.write("Alpha old rule\nkeep\n")
        code, out, _ = e.run()
        self.assertEqual(code, 0)
        self.assertIn("EDIT alpha", out)
        self.assertIn("Alpha old rule", out)
        self.assertTrue(e.read().endswith("\nAlpha old rule\nkeep\n"))


class ShippedSections(unittest.TestCase):
    def test_shipped_sections_install_twice_with_the_keys_they_name(self):
        import re
        keys = set()
        names = []
        for name in sorted(os.listdir(REAL_SECTIONS)):
            names.append(name[:-3])
            with open(os.path.join(REAL_SECTIONS, name)) as f:
                keys |= set(re.findall(r"\{\{(\w+)\}\}", f.read()))
        self.assertEqual(names, ["coding", "models", "tools"])
        e = Env(self, sections={}, values={k: "v" for k in keys})
        e.sections = REAL_SECTIONS
        e.write("mine\n")
        self.assertEqual(e.run()[0], 0)
        first = e.read()
        self.assertNotIn("{{", first)
        self.assertTrue(first.endswith("\nmine\n"))
        e.run()
        self.assertEqual(e.read(), first)


if __name__ == "__main__":
    unittest.main()
