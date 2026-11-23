#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_bulletin.py")


def entry(day, masthead=True, extra=""):
    head = '<header class="masthead"><h2>Day</h2></header>' if masthead else ""
    return f'<article class="entry" data-date="{day}">{head}<p>Goals moved.</p>{extra}</article>\n'


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


if __name__ == "__main__":
    unittest.main()
