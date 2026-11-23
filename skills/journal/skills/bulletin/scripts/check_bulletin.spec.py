#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_bulletin.py")


CARDS = ("learning", "ideas", "friction", "next")


def entry(day, masthead=True, extra="", drop=()):
    head = '<header class="masthead"><h2>Day</h2></header>' if masthead else ""
    cards = "".join(f'<article class="card" data-card="{c}"><p>x</p></article>' for c in CARDS if c not in drop)
    return f'<article class="entry" data-date="{day}">{head}<p>Goals moved.</p>{cards}{extra}</article>\n'


def page(*entries):
    return '<html><head><style>p{}</style></head><body><main id="entries">\n' + "".join(entries) + "</main></body></html>"


def check(html, name="2026-wk48-bulletin.html"):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, name)
        with open(path, "w") as f:
            f.write(html)
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
    return r.returncode, r.stdout


class Check(unittest.TestCase):
    def test_a_good_page_passes(self):
        code, out = check(page(entry("2026-11-25"), entry("2026-11-24"), entry("2026-11-23")))
        self.assertEqual((code, out.strip()), (0, "ok"))

    def test_a_suggestion_row_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra='<li class="action">x</li>')))[0], 1)

    def test_a_select_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra="<select></select>")))[0], 1)

    def test_a_textarea_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra="<textarea></textarea>")))[0], 1)

    def test_each_banned_control_and_class_fails(self):
        for extra in ("<input>", "<button>x</button>", '<li class="choice">x</li>', '<li class="comment">x</li>'):
            with self.subTest(extra=extra):
                self.assertEqual(check(page(entry("2026-11-24", extra=extra)))[0], 1)

    def test_a_script_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra="<script>1</script>")))[0], 1)

    def test_an_entry_with_no_masthead_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", masthead=False)))[0], 1)

    def test_two_entries_for_one_day_fail(self):
        self.assertEqual(check(page(entry("2026-11-24"), entry("2026-11-24")))[0], 1)

    def test_oldest_first_fails(self):
        self.assertEqual(check(page(entry("2026-11-23"), entry("2026-11-24")))[0], 1)

    def test_an_entry_outside_the_file_week_fails(self):
        self.assertEqual(check(page(entry("2026-12-01")))[0], 1)

    def test_a_placeholder_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra="<p>{{weather}}</p>")))[0], 1)

    def test_a_placeholder_in_an_attribute_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra='<li data-id="{{id}}">x</li>')))[0], 1)

    def test_a_page_with_no_entry_fails(self):
        self.assertEqual(check(page())[0], 1)

    def test_each_fault_prints_one_line(self):
        code, out = check(page(entry("2026-11-23"), entry("2026-11-24", masthead=False)))
        self.assertEqual(code, 1)
        self.assertEqual(len(out.strip().splitlines()), 2)

    def test_an_svg_with_role_and_label_passes(self):
        svg = '<svg role="img" aria-label="Goals by day"></svg>'
        code, out = check(page(entry("2026-11-24", extra=svg)))
        self.assertEqual((code, out.strip()), (0, "ok"))

    def test_an_svg_with_no_role_fails(self):
        code, out = check(page(entry("2026-11-24", extra='<svg aria-label="x"></svg>')))
        self.assertEqual((code, len(out.strip().splitlines())), (1, 1))

    def test_an_svg_with_no_label_fails(self):
        code, out = check(page(entry("2026-11-24", extra='<svg role="img"></svg>')))
        self.assertEqual((code, len(out.strip().splitlines())), (1, 1))

    def test_an_svg_with_an_empty_label_fails(self):
        code, out = check(page(entry("2026-11-24", extra='<svg role="img" aria-label="  "></svg>')))
        self.assertEqual((code, len(out.strip().splitlines())), (1, 1))

    def test_an_svg_with_the_wrong_role_fails(self):
        self.assertEqual(check(page(entry("2026-11-24", extra='<svg role="presentation" aria-label="x"></svg>')))[0], 1)

    def test_two_bad_svgs_print_two_lines(self):
        code, out = check(page(entry("2026-11-24", extra="<svg></svg><svg></svg>")))
        self.assertEqual((code, len(out.strip().splitlines())), (1, 2))

    def test_a_missing_card_fails_and_names_it(self):
        for name in CARDS:
            with self.subTest(card=name):
                code, out = check(page(entry("2026-11-24", drop=(name,))))
                self.assertEqual((code, len(out.strip().splitlines())), (1, 1))
                self.assertIn(name, out)

    def test_a_card_outside_the_entry_does_not_count(self):
        card = '<article class="card" data-card="learning"><p>x</p></article>'
        code, out = check(page(entry("2026-11-24", drop=("learning",)), card))
        self.assertEqual((code, len(out.strip().splitlines())), (1, 1))
        self.assertIn("learning", out)

    def test_each_entry_needs_its_own_cards(self):
        code, out = check(page(entry("2026-11-25"), entry("2026-11-24", drop=("ideas",))))
        self.assertEqual(code, 1)
        self.assertIn("2026-11-24", out)


if __name__ == "__main__":
    unittest.main()
