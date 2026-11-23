#!/usr/bin/env python3
"""Tests for write_report.py. Run: python3 write_report.spec.py"""
import datetime
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "write_report.py")
TEMPLATE = os.path.join(HERE, "..", "template.html")
BLOCK = re.compile(r'(<script type="application/json" id="runs">)(.*?)(</script>)', re.S)


def run(report, payload, cwd=None):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
    try:
        return subprocess.run(
            ["python3", SCRIPT, report, f.name],
            capture_output=True,
            text=True,
            cwd=cwd,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    finally:
        os.remove(f.name)


def runs_of(path):
    with open(path, encoding="utf-8") as f:
        return json.loads(BLOCK.search(f.read()).group(2))


class WriteReport(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "review_x.html")
        self.payload = {
            "title": "Review of x",
            "skill": "/engineering:post-review-comments",
            "run": {
                "title": "Panel run",
                "head": "abc1234",
                "meta": {"PR": "#1"},
                "answer": "Tick the rows.",
                "visuals": [{"question": "How many rows are open?", "bars": [["open", 2]]}],
                "columns": [{"key": "issue", "label": "Issue"}],
                "rows": [
                    {"ticks": ["reply"], "cells": {"issue": "one"}},
                    {"ticks": ["reply"], "cells": {"issue": "two"}},
                ],
            },
        }

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_new_file_holds_one_run_numbered_1_with_absolute_path(self):
        result = run(self.path, self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = runs_of(self.path)
        self.assertEqual([r["run"] for r in data["runs"]], [1])
        self.assertEqual(data["path"], os.path.abspath(self.path))
        self.assertEqual(data["title"], "Review of x")
        self.assertEqual(data["skill"], "/engineering:post-review-comments")

    def test_relative_report_path_is_stored_as_absolute(self):
        result = run("review_x.html", self.payload, cwd=self.dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(runs_of(self.path)["path"], os.path.realpath(self.path))

    def test_new_file_keeps_the_template_outside_the_block(self):
        run(self.path, self.payload)
        with open(TEMPLATE, encoding="utf-8") as f:
            template = BLOCK.sub("", f.read())
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(BLOCK.sub("", f.read()), template)

    def test_track_is_copied_to_the_top_when_given(self):
        self.payload["track"] = ["pass"]
        run(self.path, self.payload)
        self.assertEqual(runs_of(self.path)["track"], ["pass"])

    def test_date_defaults_to_today(self):
        run(self.path, self.payload)
        self.assertEqual(runs_of(self.path)["runs"][0]["date"], datetime.date.today().isoformat())

    def test_date_is_kept_when_the_run_has_one(self):
        self.payload["run"]["date"] = "2026-01-02"
        run(self.path, self.payload)
        self.assertEqual(runs_of(self.path)["runs"][0]["date"], "2026-01-02")

    def test_rows_with_no_id_get_run_and_row_order(self):
        run(self.path, self.payload)
        ids = [r["id"] for r in runs_of(self.path)["runs"][0]["rows"]]
        self.assertEqual(ids, ["r1.1", "r1.2"])

    def test_row_with_an_id_keeps_it(self):
        self.payload["run"]["rows"][0]["id"] = "keep"
        run(self.path, self.payload)
        ids = [r["id"] for r in runs_of(self.path)["runs"][0]["rows"]]
        self.assertEqual(ids, ["keep", "r1.2"])

    def test_existing_file_gets_the_next_run_first_and_keeps_earlier_runs(self):
        run(self.path, self.payload)
        run(self.path, self.payload)
        before = runs_of(self.path)["runs"]
        self.payload["run"]["title"] = "Third"
        result = run(self.path, self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = runs_of(self.path)["runs"]
        self.assertEqual([r["run"] for r in after], [3, 2, 1])
        self.assertEqual(after[0]["title"], "Third")
        self.assertEqual(after[0]["rows"][0]["id"], "r3.1")
        self.assertEqual(after[1:], before)

    def test_existing_file_is_written_again_from_the_current_template(self):
        run(self.path, self.payload)
        with open(self.path, encoding="utf-8") as f:
            stale = f.read().replace("<title>Report</title>", "<title>Stale</title>")
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(stale)
        run(self.path, self.payload)
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("<title>Report</title>", text)
        self.assertNotIn("Stale", text)

    def test_script_close_tag_in_the_data_is_escaped(self):
        self.payload["run"]["answer"] = "Bad </script> text"
        run(self.path, self.payload)
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("<\\/script> text", text)
        self.assertEqual(runs_of(self.path)["runs"][0]["answer"], "Bad </script> text")

    def test_reports_js_lists_html_files_newest_first(self):
        for name, stamp in [("a.html", 1000), ("b.html", 3000), ("c.html", 2000)]:
            p = os.path.join(self.dir, name)
            open(p, "w").close()
            os.utime(p, (stamp, stamp))
        open(os.path.join(self.dir, "notes.txt"), "w").close()
        run(self.path, self.payload)
        with open(os.path.join(self.dir, "reports.js"), encoding="utf-8") as f:
            text = f.read().strip()
        self.assertEqual(
            text,
            'window.REPORTS = ["review_x.html", "b.html", "c.html", "a.html"];',
        )

    def test_prints_the_file_url(self):
        result = run(self.path, self.payload)
        self.assertEqual(result.stdout.strip(), "file://" + os.path.abspath(self.path))

    def test_input_with_no_run_exits_1(self):
        del self.payload["run"]
        result = run(self.path, self.payload)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no run object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(os.path.exists(self.path))

    def test_rerun_sorts_runs_newest_first(self):
        run(self.path, self.payload)
        run(self.path, self.payload)
        data = runs_of(self.path)
        data["runs"].reverse()
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        text = BLOCK.sub(lambda m: m.group(1) + json.dumps(data) + m.group(3), text, count=1)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)
        result = run(self.path, self.payload)
        self.assertEqual(result.returncode, 0)
        self.assertEqual([r["run"] for r in runs_of(self.path)["runs"]], [3, 2, 1])
        check = subprocess.run(
            ["python3", os.path.join(HERE, "check_report.py"), self.path],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(check.returncode, 0, check.stdout)

    def test_unparsable_runs_block_in_the_existing_file_exits_1_and_keeps_it(self):
        run(self.path, self.payload)
        with open(self.path, encoding="utf-8") as f:
            broken = BLOCK.sub(lambda m: m.group(1) + "{not json" + m.group(3), f.read())
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(broken)
        result = run(self.path, self.payload)
        self.assertEqual(result.returncode, 1)
        self.assertIn("runs", result.stderr)
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(f.read(), broken)


if __name__ == "__main__":
    unittest.main()
