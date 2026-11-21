#!/usr/bin/env python3
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import occasions

HEAD = "---\ntype: occasions\n---\n\n"
TABLE = "| Item | When | Section |\n| --- | --- | --- |\n"


class Occasions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "occasions.md")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def run_on(self, date):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = occasions.main([self.path, "--date", date])
        return code, json.loads(out.getvalue())

    def rows(self, *rows, heading="Weekly"):
        self.write(HEAD + f"## {heading}\n\n" + TABLE + "".join(f"| {r} |\n" for r in rows))

    def due(self, date):
        return self.run_on(date)[1]["due"]["chores"]

    def assert_due_on(self, when, yes, no):
        self.rows(f"Thing | {when} | chores")
        for date in yes:
            self.assertEqual(self.due(date), ["Thing"], f"{when} on {date}")
        for date in no:
            self.assertEqual(self.due(date), [], f"{when} on {date}")

    def test_a_weekday_is_due_on_that_day_only(self):
        self.assert_due_on("Sun", ["2026-11-22", "2026-11-29"], ["2026-11-23", "2026-11-21"])

    def test_several_weekdays_are_due_on_each(self):
        self.assert_due_on("Mon Wed", ["2026-11-23", "2026-11-25"], ["2026-11-24", "2026-11-22"])

    def test_names_ignore_case(self):
        self.assert_due_on("wED", ["2026-11-25"], ["2026-11-24"])

    def test_even_parity_is_by_iso_week(self):
        self.assert_due_on("Wed even", ["2026-11-25"], ["2026-11-18", "2026-11-24"])

    def test_odd_parity_is_by_iso_week(self):
        self.assert_due_on("Wed odd", ["2026-11-18"], ["2026-11-25"])

    def test_odd_weeks_53_and_1_are_both_odd(self):
        self.assert_due_on("Wed odd", ["2026-12-30", "2027-01-06"], ["2027-01-13"])

    def test_a_yearly_date_is_due_each_year(self):
        self.assert_due_on("Jan 5", ["2026-01-05", "2027-01-05"], ["2026-01-06", "2026-02-05"])

    def test_sept_is_an_alias_for_sep(self):
        self.assert_due_on("Sept 4", ["2026-09-04"], ["2026-09-05"])

    def test_feb_29_is_due_on_feb_29_in_a_leap_year(self):
        self.assert_due_on("Feb 29", ["2028-02-29"], ["2028-02-28", "2028-03-01"])

    def test_feb_29_is_due_on_feb_28_in_other_years(self):
        self.assert_due_on("Feb 29", ["2027-02-28"], ["2027-03-01"])

    def test_nth_weekday_of_a_month(self):
        self.assert_due_on("2nd Sun May", ["2026-05-10", "2027-05-09"], ["2026-05-03", "2026-05-17", "2026-06-14"])

    def test_nth_weekday_with_no_month_is_due_each_month(self):
        self.assert_due_on("1st Sun", ["2026-11-01", "2026-12-06"], ["2026-11-08", "2026-12-01"])

    def test_a_fifth_weekday_is_not_due_in_a_month_without_one(self):
        self.assert_due_on("5th Sun", ["2026-11-29"], ["2026-12-27"])

    def test_easter(self):
        self.assert_due_on("easter", ["2026-04-05", "2027-03-28"], ["2026-04-06", "2027-04-04"])

    def test_easter_plus_a_day(self):
        self.assert_due_on("easter+1", ["2026-04-06", "2027-03-29"], ["2026-04-05"])

    def test_easter_minus_two_days(self):
        self.assert_due_on("Easter-2", ["2026-04-03", "2027-03-26"], ["2026-04-05"])

    def test_every_3_months_repeats_from_the_anchor(self):
        self.assert_due_on("every 3 months from Feb 15", ["2026-02-15", "2026-05-15", "2026-11-15", "2027-02-15"], ["2026-03-15", "2026-05-16"])

    def test_every_3_months_is_due_in_months_before_the_anchor_month(self):
        self.assert_due_on("every 3 months from Nov 15", ["2026-02-15", "2026-08-15"], ["2026-01-15"])

    def test_a_repeat_day_past_the_month_end_falls_on_the_last_day(self):
        self.assert_due_on("every 1 months from Jan 31", ["2027-02-28", "2026-04-30", "2026-03-31"], ["2026-03-30", "2026-04-29"])

    def test_a_one_off_is_due_on_its_date(self):
        self.rows("Party | 2026-11-03 | tasks", heading="One-off")
        _, out = self.run_on("2026-11-03")
        self.assertEqual(out["due"]["tasks"], ["Party"])
        self.assertEqual(out["past"], [])

    def test_a_one_off_is_past_the_day_after(self):
        self.rows("Party | 2026-11-03 | tasks", heading="One-off")
        _, out = self.run_on("2026-11-04")
        self.assertEqual(out["due"], {"chores": [], "work": [], "tasks": []})
        self.assertEqual(out["past"], [{"line": 9, "item": "Party", "when": "2026-11-03", "section": "tasks"}])

    def test_a_future_one_off_is_neither_due_nor_past(self):
        self.rows("Party | 2026-11-03 | tasks", heading="One-off")
        _, out = self.run_on("2026-11-02")
        self.assertEqual(out["due"]["tasks"], [])
        self.assertEqual(out["past"], [])

    def test_an_empty_section_is_chores(self):
        self.rows("Thing | Sun | ")
        self.assertEqual(self.due("2026-11-22"), ["Thing"])

    def test_items_go_to_their_section(self):
        self.rows("A | Sun | work", "B | Sun | tasks", "C | Sun | chores")
        self.assertEqual(self.run_on("2026-11-22")[1]["due"], {"chores": ["C"], "work": ["A"], "tasks": ["B"]})

    def test_the_heading_does_not_decide(self):
        self.rows("Thing | Jan 5 | ", heading="Weekly")
        self.assertEqual(self.due("2026-01-05"), ["Thing"])

    def test_items_keep_links_emoji_and_escaped_pipes(self):
        self.rows("🎂 [[Some Person\\|Them]] | Jan 5 | ")
        self.assertEqual(self.due("2026-01-05"), ["🎂 [[Some Person\\|Them]]"])

    def test_an_unknown_when_goes_to_errors_and_other_rows_still_print(self):
        self.rows("Fair | Aug (varies) | ", "Thing | Sun | ")
        code, out = self.run_on("2026-11-22")
        self.assertEqual(code, 0)
        self.assertEqual(out["due"]["chores"], ["Thing"])
        self.assertEqual(len(out["errors"]), 1)
        self.assertEqual(out["errors"][0]["line"], 9)
        self.assertEqual(out["errors"][0]["row"], "| Fair | Aug (varies) |  |")
        self.assertTrue(out["errors"][0]["why"])

    def test_bad_rows_go_to_errors(self):
        self.rows(
            "Empty |  | ",
            "Bad section | Sun | garden",
            "Old | Jan 5 | event | chores",
            "Bad day | Feb 30 | ",
            "Bad date | 2026-02-30 | ",
            "Zero | every 0 months from Jan 1 | ",
            "Sixth | 6th Sun | ",
            "Thing | Sun | ",
        )
        _, out = self.run_on("2026-11-22")
        self.assertEqual([e["line"] for e in out["errors"]], [9, 10, 11, 12, 13, 14, 15])
        self.assertEqual(out["due"]["chores"], ["Thing"])

    def test_daily_lines_are_kept_as_written(self):
        self.write(HEAD + "## Daily\n- [ ] **Kitchen**\n\t- [ ] 🧼 Dishes\n  - [ ] Bins\n\n- [ ] **Pets**\n\n## Weekly\n\n" + TABLE + "| Thing | Sun | |\n")
        _, out = self.run_on("2026-11-22")
        self.assertEqual(out["daily"], ["- [ ] **Kitchen**", "\t- [ ] 🧼 Dishes", "  - [ ] Bins", "- [ ] **Pets**"])
        self.assertEqual(out["due"]["chores"], ["Thing"])

    def test_the_output_has_the_date_and_every_key(self):
        self.write(HEAD + "## Daily\n- [ ] A\n")
        self.assertEqual(self.run_on("2026-11-22"), (0, {
            "date": "2026-11-22",
            "daily": ["- [ ] A"],
            "due": {"chores": [], "work": [], "tasks": []},
            "errors": [],
            "past": [],
        }))

    def test_a_missing_file_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(occasions.main([self.path, "--date", "2026-11-22"]), 2)
        self.assertTrue(err.getvalue())

    def test_no_date_uses_today(self):
        self.write(HEAD)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            occasions.main([self.path])
        self.assertEqual(json.loads(out.getvalue())["date"], occasions.datetime.date.today().isoformat())


if __name__ == "__main__":
    unittest.main()
