#!/usr/bin/env python3
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edition


def run(folder, date):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = edition.main([folder, "--date", date])
    return code, json.loads(out.getvalue())


def write(folder, name, html):
    with open(os.path.join(folder, name), "w") as f:
        f.write(html)


class Edition(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_sunday_2026_11_22_is_week_47(self):
        self.assertEqual(run(self.dir, "2026-11-22")[1]["path"], os.path.join(self.dir, "2026-wk47-broadsheet.html"))

    def test_monday_2026_11_23_is_week_48(self):
        self.assertEqual(run(self.dir, "2026-11-23")[1]["path"], os.path.join(self.dir, "2026-wk48-broadsheet.html"))

    def test_2027_01_01_is_in_the_iso_year_2026_week_53(self):
        self.assertEqual(run(self.dir, "2027-01-01")[1]["path"], os.path.join(self.dir, "2026-wk53-broadsheet.html"))

    def test_a_single_digit_week_has_two_digits(self):
        self.assertEqual(run(self.dir, "2026-01-05")[1]["path"], os.path.join(self.dir, "2026-wk02-broadsheet.html"))

    def test_last_week_crosses_the_iso_year(self):
        write(self.dir, "2026-wk53-broadsheet.html", "<p></p>")
        self.assertEqual(run(self.dir, "2027-01-04")[1]["last_path"], os.path.join(self.dir, "2026-wk53-broadsheet.html"))

    def test_exists_is_false_when_this_weeks_page_is_not_there(self):
        self.assertEqual(run(self.dir, "2026-11-21"), (0, {
            "path": os.path.join(self.dir, "2026-wk47-broadsheet.html"),
            "exists": False,
            "last_path": None,
            "last_ids": [],
            "muted": [],
        }))

    def test_exists_is_true_when_this_weeks_page_is_there(self):
        write(self.dir, "2026-wk47-broadsheet.html", "<p></p>")
        self.assertTrue(run(self.dir, "2026-11-21")[1]["exists"])

    def test_lists_last_weeks_row_ids_in_page_order_without_repeats(self):
        write(self.dir, "2026-wk46-broadsheet.html", (
            '<ul><li data-id="stale:a">a</li><li data-id="ledger:b">b</li>'
            '<li class="x">c</li><li data-id="stale:a">a</li></ul>'
        ))
        _, out = run(self.dir, "2026-11-21")
        self.assertEqual(out["last_path"], os.path.join(self.dir, "2026-wk46-broadsheet.html"))
        self.assertEqual(out["last_ids"], ["stale:a", "ledger:b"])

    def test_a_page_with_no_ids_gives_an_empty_list(self):
        write(self.dir, "2026-wk46-broadsheet.html", "<ul><li>a</li></ul>")
        _, out = run(self.dir, "2026-11-21")
        self.assertEqual(out["last_path"], os.path.join(self.dir, "2026-wk46-broadsheet.html"))
        self.assertEqual(out["last_ids"], [])

    def test_lists_vetoed_ids_in_file_order_without_repeats(self):
        write(self.dir, "broadsheet-memory.md", "letters:a.md | veto\nthe-board:b | veto\nletters:a.md | veto\n")
        self.assertEqual(run(self.dir, "2026-11-21")[1]["muted"], ["letters:a.md", "the-board:b"])

    def test_a_snooze_mutes_its_id_up_to_and_on_its_end_date(self):
        write(self.dir, "broadsheet-memory.md", "stale-shelf:x.md | snooze until 2026-11-21\n")
        self.assertEqual(run(self.dir, "2026-11-20")[1]["muted"], ["stale-shelf:x.md"])
        self.assertEqual(run(self.dir, "2026-11-21")[1]["muted"], ["stale-shelf:x.md"])

    def test_a_snooze_ends_the_day_after_its_end_date(self):
        write(self.dir, "broadsheet-memory.md", "stale-shelf:x.md | snooze until 2026-11-21\n")
        self.assertEqual(run(self.dir, "2026-11-22")[1]["muted"], [])

    def test_a_later_snooze_of_the_same_id_still_mutes_it(self):
        write(self.dir, "broadsheet-memory.md", "editorial:x | snooze until 2026-10-01\neditorial:x | snooze until 2026-12-01\n")
        self.assertEqual(run(self.dir, "2026-11-21")[1]["muted"], ["editorial:x"])

    def test_no_memory_file_gives_no_muted_ids(self):
        self.assertEqual(run(self.dir, "2026-11-21"), (0, {
            "path": os.path.join(self.dir, "2026-wk47-broadsheet.html"),
            "exists": False,
            "last_path": None,
            "last_ids": [],
            "muted": [],
        }))

    def test_a_line_it_cannot_read_is_skipped_and_the_rest_still_mute(self):
        write(self.dir, "broadsheet-memory.md", (
            "# Broadsheet memory\n\nnot a row\nletters:a.md | maybe\n"
            "letters:b.md | snooze until soon\n | veto\nletters:c.md | veto\n"
        ))
        self.assertEqual(run(self.dir, "2026-11-21"), (0, {
            "path": os.path.join(self.dir, "2026-wk47-broadsheet.html"),
            "exists": False,
            "last_path": None,
            "last_ids": [],
            "muted": ["letters:c.md"],
        }))

    def test_no_date_uses_today(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            edition.main([self.dir])
        year, week, _ = edition.datetime.date.today().isocalendar()
        self.assertEqual(json.loads(out.getvalue())["path"], os.path.join(self.dir, f"{year}-wk{week:02d}-broadsheet.html"))


if __name__ == "__main__":
    unittest.main()
