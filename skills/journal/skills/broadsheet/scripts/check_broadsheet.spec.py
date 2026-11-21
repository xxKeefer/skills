#!/usr/bin/env python3
"""Run: python3 check_broadsheet.spec.py"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_broadsheet.py")
TEMPLATE = os.path.join(HERE, "..", "template.html")


def filled():
    with open(TEMPLATE) as f:
        return re.sub(r"\{\{[^}]*\}\}", "x", f.read())


def check(html):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    try:
        p = subprocess.run([sys.executable, SCRIPT, f.name], capture_output=True, text=True)
        return p.returncode, p.stdout
    finally:
        os.unlink(f.name)


class Check(unittest.TestCase):
    def test_a_filled_template_is_ok(self):
        self.assertEqual(check(filled()), (0, "ok\n"))

    def test_names_a_placeholder_left_on_the_page(self):
        code, out = check(filled().replace("<h2>The ledger</h2>", "<h2>{{ledger}}</h2>"))
        self.assertEqual(code, 1)
        self.assertIn("placeholder {{ledger}} is still on the page", out)

    def test_names_a_missing_section(self):
        code, out = check(filled().replace('id="the-morgue"', 'id="gone"'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-morgue is missing", out)

    def test_names_an_inline_style(self):
        code, out = check(filled().replace('<section id="gaps"', '<section style="color: red" id="gaps"'))
        self.assertEqual(code, 1)
        self.assertIn("has an inline style", out)

    def test_names_a_note_path_that_is_not_a_link(self):
        code, out = check(filled().replace("<h2>Editorial</h2>", "<h2>Editorial</h2><p>See 02-research/old note.md now.</p>"))
        self.assertEqual(code, 1)
        self.assertIn("note 02-research/old note.md is not a link", out)

    def test_a_linked_note_path_is_fine(self):
        link = '<a href="obsidian://open?vault=notes&amp;file=02-research%2Fa" target="_blank" rel="noopener">02-research/a.md</a>'
        self.assertEqual(check(filled().replace("<h2>Editorial</h2>", "<h2>Editorial</h2>" + link))[0], 0)

    def test_names_a_link_without_target_and_rel(self):
        code, out = check(filled().replace("<h2>Editorial</h2>", '<h2>Editorial</h2><a href="obsidian://x">x</a>'))
        self.assertEqual(code, 1)
        self.assertIn('link obsidian://x has no target="_blank"', out)
        self.assertIn('link obsidian://x has no rel="noopener"', out)


if __name__ == "__main__":
    unittest.main()
