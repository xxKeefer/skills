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

    def test_fails_a_review_card_whose_headline_links_the_ticket(self):
        card = ('<article><span class="label">Review requested</span>'
                '<h3><a href="https://x/browse/ABC-12" target="_blank" rel="noopener">ABC-12</a> needs a review</h3>'
                '<p>Read it.</p></article>')
        result = check(page(card))
        self.assertEqual(result.returncode, 1)
        self.assertIn("review card", result.stdout)

    def test_passes_a_review_card_whose_headline_links_the_pr(self):
        card = ('<article><span class="label">Review requested</span>'
                '<h3><a href="https://x/pull/4" target="_blank" rel="noopener">#4</a> needs a review</h3>'
                '<p>For <a href="https://x/browse/ABC-12" target="_blank" rel="noopener">ABC-12</a>.</p></article>')
        result = check(page(card))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fails_a_your_desk_card_with_no_done_checkbox(self):
        html = page().replace('<section id="your-desk"><p>News.</p></section>',
                              '<section id="your-desk"><div class="group"><h3 class="tagline">Plans</h3>'
                              '<article><span class="label">Ticket</span><h4>Plan it</h4><p>Do it.</p></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Plan it", result.stdout)
        self.assertIn("done checkbox", result.stdout)

    def test_passes_a_your_desk_card_with_a_done_checkbox(self):
        html = page().replace('<section id="your-desk"><p>News.</p></section>',
                              '<section id="your-desk"><div class="group"><h3 class="tagline">Plans</h3>'
                              '<article class="action"><input type="checkbox" class="done" aria-label="Done: Plan it">'
                              '<span class="label">Ticket</span><h4>Plan it</h4><p>Do it.</p></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fails_a_card_that_is_not_in_a_group(self):
        for section in ("your-desk", "around-the-repos", "the-board"):
            html = page().replace(f'<section id="{section}"><p>News.</p></section>',
                                  f'<section id="{section}"><article><span class="label">News</span><h4>Loose card</h4></article></section>')
            result = check(html)
            self.assertEqual(result.returncode, 1, section)
            self.assertIn('"Loose card" is not in a group', result.stdout)

    def test_fails_a_group_with_no_tagline(self):
        html = page().replace('<section id="the-board"><p>News.</p></section>',
                              '<section id="the-board"><div class="group"><article><span class="label">Done</span><h4>A ticket</h4></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("group with no tagline", result.stdout)

    def test_passes_cards_grouped_under_taglines(self):
        html = page().replace('<section id="around-the-repos"><p>News.</p></section>',
                              '<section id="around-the-repos"><div class="group"><h3 class="tagline">The forms library grows up</h3>'
                              '<article><span class="label">web</span><h4>Delete a set</h4><p>Done.</p></article>'
                              '<article><span class="label">web</span><h4>Link a set</h4><p>Done.</p></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fails_a_board_card_with_no_person(self):
        html = page().replace('<section id="the-board"><p>News.</p></section>',
                              '<section id="the-board"><select id="board-person"><option value="">All</option></select>'
                              '<div class="group"><h3 class="tagline">Forms ship</h3>'
                              '<article><span class="label">Done</span><h4>A ticket</h4></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn('board card "A ticket" has no data-person', result.stdout)

    def test_fails_a_board_with_no_person_filter(self):
        html = page().replace('<section id="the-board"><p>News.</p></section>',
                              '<section id="the-board"><div class="group"><h3 class="tagline">Forms ship</h3>'
                              '<article data-person="Ann"><span class="label">Done</span><h4>A ticket</h4></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("#board-person", result.stdout)

    def test_passes_a_board_with_a_person_filter_and_people_on_cards(self):
        html = page().replace('<section id="the-board"><p>News.</p></section>',
                              '<section id="the-board"><select id="board-person"><option value="">All</option>'
                              '<option>Ann</option></select><div class="group"><h3 class="tagline">Forms ship</h3>'
                              '<article data-person="Ann"><span class="label">Done</span><h4>A ticket</h4></article></div></section>')
        result = check(html)
        self.assertEqual(result.returncode, 0, result.stdout)

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


    def test_fails_a_placeholder_left_in_an_attribute(self):
        link = '<a href="{{ticket_url}}" target="_blank" rel="noopener">ABC-12</a>'
        result = check(page(f"<p>{link}</p>"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("{{ticket_url}}", result.stdout)

    def test_fails_a_placeholder_left_in_the_stylesheet(self):
        html = page().replace("p {}", "p { color: {{accent}}; }")
        result = check(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("{{accent}}", result.stdout)

if __name__ == "__main__":
    unittest.main()
