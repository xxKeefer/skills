#!/usr/bin/env python3
"""Tests for check_gazette.py. Run: python3 check_gazette.spec.py"""
import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check_gazette.py")
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

SECTIONS = ["masthead", "lead", "weather", "your-desk", "around-the-repos", "the-board", "honour-roll"]


def page(body_extra="", sections=SECTIONS):
    parts = "".join(f'<section id="{s}"><p>News.</p></section>' for s in sections)
    return f"<!doctype html><html><head><style>p {{}}</style></head><body>{parts}{body_extra}</body></html>"


def check(html):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        path = f.name
    try:
        return subprocess.run(["python3", CHECK, path], capture_output=True, text=True, env=ENV)
    finally:
        os.unlink(path)


class CheckGazette(unittest.TestCase):
    def test_passes_a_page_with_every_section_and_good_links(self):
        link = '<a href="https://x/browse/ABC-12" target="_blank" rel="noopener">ABC-12</a>'
        result = check(page(f"<p>{link} and <code>UTF-8</code></p>"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ok", result.stdout)

    def test_fails_a_link_that_opens_in_the_same_tab(self):
        result = check(page('<p><a href="https://x/pull/4">#4</a></p>'))
        self.assertEqual(result.returncode, 1)
        self.assertIn('target="_blank"', result.stdout)

    def test_fails_a_link_with_no_rel_noopener(self):
        result = check(page('<p><a href="https://x/pull/4" target="_blank">#4</a></p>'))
        self.assertEqual(result.returncode, 1)
        self.assertIn("noopener", result.stdout)

    def test_fails_a_ticket_key_that_is_not_a_link(self):
        result = check(page("<p>Fixed in ABC-12 today.</p>"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("ABC-12", result.stdout)

    def test_fails_a_pr_number_that_is_not_a_link(self):
        result = check(page("<p>Merged #481 today.</p>"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("#481", result.stdout)

    def test_fails_a_missing_section(self):
        result = check(page(sections=[s for s in SECTIONS if s != "weather"]))
        self.assertEqual(result.returncode, 1)
        self.assertIn("weather", result.stdout)

    def test_fails_an_inline_style(self):
        result = check(page('<p style="color: #222">Dark.</p>'))
        self.assertEqual(result.returncode, 1)
        self.assertIn("style", result.stdout)

    def test_fails_a_placeholder_left_from_the_template(self):
        result = check(page("<p>{{lead_headline}}</p>"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("{{lead_headline}}", result.stdout)


if __name__ == "__main__":
    unittest.main()
