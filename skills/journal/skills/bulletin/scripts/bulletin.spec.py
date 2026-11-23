#!/usr/bin/env python3
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bulletin


def entry(day, ids=()):
    rows = "".join(f'<li data-id="{i}">x</li>' for i in ids)
    return f'<article class="entry" data-date="{day}"><header class="masthead">{day}</header><ul>{rows}</ul></article>\n'


def state(folder, date):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = bulletin.main(["state", folder, "--date", date])
    return code, json.loads(out.getvalue())


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, name, text):
        with open(os.path.join(self.dir, name), "w") as f:
            f.write(text)

    def add(self, path, text, date):
        entry_file = os.path.join(self.dir, "entry.html")
        with open(entry_file, "w") as f:
            f.write(text)
        with contextlib.redirect_stderr(io.StringIO()):
            return bulletin.main(["add", path, entry_file, "--date", date])


class Name(Case):
    def test_sunday_2026_11_22_is_week_47(self):
        self.assertEqual(state(self.dir, "2026-11-22")[1]["path"], os.path.join(self.dir, "2026-wk47-bulletin.html"))

    def test_monday_2026_11_23_is_week_48(self):
        self.assertEqual(state(self.dir, "2026-11-23")[1]["path"], os.path.join(self.dir, "2026-wk48-bulletin.html"))

    def test_2027_01_01_is_in_iso_year_2026_week_53(self):
        self.assertEqual(state(self.dir, "2027-01-01")[1]["path"], os.path.join(self.dir, "2026-wk53-bulletin.html"))

    def test_a_single_digit_week_has_two_digits(self):
        self.assertEqual(state(self.dir, "2026-01-05")[1]["path"], os.path.join(self.dir, "2026-wk02-bulletin.html"))

    def test_the_week_matches_the_broadsheet_for_every_day_of_two_years(self):
        import datetime
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "broadsheet", "scripts"))
        import edition
        day = datetime.date(2025, 1, 1)
        while day < datetime.date(2027, 1, 10):
            self.assertEqual(bulletin.name_for(day), edition.name_for(day).replace("broadsheet", "bulletin"))
            day += datetime.timedelta(days=1)


class State(Case):
    def test_no_file_gives_exists_false_and_no_days(self):
        _, out = state(self.dir, "2026-11-24")
        self.assertFalse(out["exists"])
        self.assertFalse(out["today_present"])
        self.assertEqual(out["days"], [])
        self.assertIsNone(out["days_since_last"])
        self.assertEqual(out["last_ids"], [])

    def test_week_start_is_the_monday(self):
        self.assertEqual(state(self.dir, "2026-11-26")[1]["week_start"], "2026-11-23")
        self.assertEqual(state(self.dir, "2026-11-22")[1]["week_start"], "2026-11-16")
        self.assertEqual(state(self.dir, "2026-11-23")[1]["week_start"], "2026-11-23")

    def test_the_window_runs_from_monday_of_last_week_to_today(self):
        cases = [
            ("2026-11-23", "2026-11-16", 7),
            ("2026-11-24", "2026-11-16", 8),
            ("2026-11-25", "2026-11-16", 9),
            ("2026-11-26", "2026-11-16", 10),
            ("2026-11-27", "2026-11-16", 11),
            ("2026-11-28", "2026-11-16", 12),
            ("2026-11-29", "2026-11-16", 13),
            ("2027-01-01", "2026-12-21", 11),
        ]
        for day, start, days in cases:
            _, out = state(self.dir, day)
            self.assertEqual((out["last_week_start"], out["window_days"]), (start, days), day)

    def test_today_present_when_an_entry_has_the_date(self):
        self.put("2026-wk48-bulletin.html", entry("2026-11-24") + entry("2026-11-23"))
        _, out = state(self.dir, "2026-11-24")
        self.assertTrue(out["exists"])
        self.assertTrue(out["today_present"])
        self.assertEqual(out["days"], ["2026-11-24", "2026-11-23"])

    def test_days_since_last_for_gaps_of_1_2_and_4_days(self):
        self.put("2026-wk48-bulletin.html", entry("2026-11-23"))
        self.assertEqual(state(self.dir, "2026-11-24")[1]["days_since_last"], 1)
        self.assertEqual(state(self.dir, "2026-11-25")[1]["days_since_last"], 2)
        self.assertEqual(state(self.dir, "2026-11-27")[1]["days_since_last"], 4)

    def test_days_since_last_is_none_for_the_first_entry(self):
        self.put("2026-wk48-bulletin.html", "<main id=\"entries\">\n</main>")
        self.assertIsNone(state(self.dir, "2026-11-24")[1]["days_since_last"])

    def test_last_ids_come_from_the_latest_entry_only(self):
        self.put("2026-wk48-bulletin.html", entry("2026-11-25", ["goals:a", "goals:b", "goals:a"]) + entry("2026-11-24", ["goals:old"]))
        self.assertEqual(state(self.dir, "2026-11-26")[1]["last_ids"], ["goals:a", "goals:b"])


class Add(Case):
    def test_creates_the_file_with_one_entry(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        self.assertEqual(self.add(path, entry("2026-11-24"), "2026-11-24"), 0)
        text = open(path, encoding="utf-8").read()
        self.assertEqual(text.count('<article class="entry"'), 1)
        self.assertNotIn("{{", text)
        self.assertIn("Bulletin · 2026 week 48", text)

    def test_a_page_with_no_entries_marker_is_left_unchanged(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        body = "<html><body></body></html>"
        self.put("2026-wk48-bulletin.html", body)
        self.assertEqual(self.add(path, entry("2026-11-24"), "2026-11-24"), 1)
        self.assertEqual(open(path, encoding="utf-8").read(), body)

    def test_inserts_above_older_entries_and_keeps_their_bytes(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        self.add(path, entry("2026-11-23", ["a"]), "2026-11-23")
        before = open(path).read()
        old = entry("2026-11-23", ["a"])
        self.assertIn(old, before)
        self.add(path, entry("2026-11-24", ["b"]), "2026-11-24")
        after = open(path).read()
        self.assertLess(after.index('data-date="2026-11-24"'), after.index('data-date="2026-11-23"'))
        self.assertIn(old, after)
        self.assertEqual(after.replace(entry("2026-11-24", ["b"]), "", 1), before)

    def test_a_day_with_an_entry_exits_1_and_writes_nothing(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        self.add(path, entry("2026-11-24"), "2026-11-24")
        before = open(path).read()
        self.assertEqual(self.add(path, entry("2026-11-24", ["z"]), "2026-11-24"), 1)
        self.assertEqual(open(path).read(), before)

    def test_a_backfilled_day_goes_below_newer_entries(self):
        path = os.path.join(self.dir, "2026-wk47-bulletin.html")
        self.add(path, entry("2026-11-20"), "2026-11-20")
        before = open(path, encoding="utf-8").read()
        self.assertEqual(self.add(path, entry("2026-11-18"), "2026-11-18"), 0)
        after = open(path, encoding="utf-8").read()
        self.assertLess(after.index('data-date="2026-11-20"'), after.index('data-date="2026-11-18"'))
        self.assertEqual(after.replace(entry("2026-11-18"), "", 1), before)

    def test_a_backfilled_day_goes_between_two_entries(self):
        path = os.path.join(self.dir, "2026-wk47-bulletin.html")
        self.add(path, entry("2026-11-17"), "2026-11-17")
        self.add(path, entry("2026-11-20"), "2026-11-20")
        self.assertEqual(self.add(path, entry("2026-11-18"), "2026-11-18"), 0)
        text = open(path, encoding="utf-8").read()
        order = [text.index(f'data-date="2026-11-{d}"') for d in (20, 18, 17)]
        self.assertEqual(order, sorted(order))

    def test_an_entry_file_with_no_final_newline_keeps_the_layout(self):
        path = os.path.join(self.dir, "2026-wk47-bulletin.html")
        self.add(path, entry("2026-11-18"), "2026-11-18")
        self.assertEqual(self.add(path, entry("2026-11-20").rstrip("\n"), "2026-11-20"), 0)
        self.assertEqual(self.add(path, entry("2026-11-16").rstrip("\n"), "2026-11-16"), 0)
        text = open(path, encoding="utf-8").read()
        self.assertEqual(text.count("</article><article"), 0)
        self.assertEqual(text.count("</article>\n"), 3)

    def test_a_crlf_page_keeps_every_older_byte(self):
        path = os.path.join(self.dir, "2026-wk47-bulletin.html")
        self.add(path, entry("2026-11-18"), "2026-11-18")
        crlf = open(path, encoding="utf-8").read().replace("\n", "\r\n")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(crlf)
        self.assertEqual(self.add(path, entry("2026-11-20"), "2026-11-20"), 0)
        with open(path, encoding="utf-8", newline="") as f:
            after = f.read()
        self.assertEqual(after.replace(entry("2026-11-20"), "", 1), crlf)

    def test_an_entry_dated_for_another_day_exits_1_and_writes_nothing(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        self.assertEqual(self.add(path, entry("2026-11-23"), "2026-11-24"), 1)
        self.assertFalse(os.path.exists(path))

    def test_a_missing_folder_exits_1(self):
        path = os.path.join(self.dir, "gone", "2026-wk48-bulletin.html")
        self.assertEqual(self.add(path, entry("2026-11-24"), "2026-11-24"), 1)

    def test_a_date_outside_the_file_week_exits_1_and_writes_nothing(self):
        path = os.path.join(self.dir, "2026-wk48-bulletin.html")
        self.assertEqual(self.add(path, entry("2026-12-01"), "2026-12-01"), 1)
        self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
