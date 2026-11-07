#!/usr/bin/env python3
"""Run: python3 triage_dir.spec.py"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

os.environ["TZ"] = "UTC"
time.tzset()

import triage_dir as td  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "triage_dir.py")
JAN_15 = 1_800_000_000  # 2027-01-15 08:00 UTC
JAN_20 = JAN_15 + 5 * 86400


def touch(root, rel, data=b"", mtime=JAN_15):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    os.utime(path, (mtime, mtime))
    return path


def item(name, size=1, kind="file", type_="text/plain", modified="2027-01-15"):
    return {"name": name, "kind": kind, "type": type_, "size": size, "modified": modified}


def category(name, items, action="keep", reason="why"):
    return {"name": name, "action": action, "reason": reason, "items": items}


class TempDir(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._cache = tempfile.TemporaryDirectory()
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()
        self._cache.cleanup()

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)

    def write_json(self, name, data):
        path = os.path.join(self._cache.name, f"{name}.json")
        with open(path, "w") as f:
            json.dump(data, f)
        return path


class Human(unittest.TestCase):
    def test_formats_sizes_in_decimal_units(self):
        self.assertEqual(td.human(999), "999 B")
        self.assertEqual(td.human(1500), "1.5 KB")
        self.assertEqual(td.human(2_000_000), "2.0 MB")
        self.assertEqual(td.human(3_400_000_000), "3.4 GB")


class Scan(TempDir):
    def test_lists_files_and_folders_with_kind_size_type_and_date(self):
        touch(self.root, "notes", b"hello\n")
        touch(self.root, "app/bin", b"x")
        os.utime(os.path.join(self.root, "app"), (JAN_20, JAN_20))
        found = {i["name"]: i for i in td.scan(self.root)["items"]}
        self.assertEqual(found["notes"], item("notes", size=6))
        self.assertEqual(found["app"], item("app", size=1, kind="folder", type_="folder", modified="2027-01-20"))

    def test_counts_a_folder_size_as_the_sum_of_its_files(self):
        touch(self.root, "pack/a", b"12345")
        touch(self.root, "pack/deep/b", b"123")
        self.assertEqual(td.scan(self.root)["items"][0]["size"], 8)

    def test_skips_dotfiles_partial_downloads_and_the_old_report(self):
        for name in [".DS_Store", "big.iso.crdownload", "song.mp3.part", "film.mkv.download",
                     "triage.html", "keep.txt"]:
            touch(self.root, name, b"x")
        self.assertEqual([i["name"] for i in td.scan(self.root)["items"]], ["keep.txt"])

    def test_records_the_absolute_dir(self):
        self.assertEqual(td.scan(self.root)["dir"], os.path.realpath(self.root))


class PlanProblems(unittest.TestCase):
    SCAN = {"dir": "/d", "items": [item("a"), item("b")]}

    def problems(self, *categories):
        return td.plan_problems(self.SCAN, {"categories": list(categories)})

    def test_accepts_a_plan_that_places_every_item_once(self):
        self.assertEqual(self.problems(category("Docs", ["a"]), category("Junk", ["b"], "delete")), [])

    def test_flags_an_item_left_out_of_the_plan(self):
        self.assertEqual(self.problems(category("Docs", ["a"])), ["b: not in any category"])

    def test_flags_an_item_placed_twice(self):
        self.assertEqual(self.problems(category("Docs", ["a", "b"]), category("Junk", ["b"])),
                         ["b: in more than one category"])

    def test_flags_an_item_the_scan_did_not_find(self):
        self.assertEqual(self.problems(category("Docs", ["a", "b", "c"])), ["c: not in the scan"])

    def test_flags_an_action_other_than_keep_archive_or_delete(self):
        self.assertEqual(self.problems(category("Docs", ["a", "b"], "maybe")),
                         ["Docs: action must be keep, archive, or delete"])

    def test_flags_a_category_name_that_is_not_a_plain_folder_name(self):
        for name in ["a/b", "", ".hidden", ".."]:
            self.assertEqual(self.problems(category(name, ["a", "b"])),
                             [f"{name}: not a plain folder name"])

    def test_flags_a_category_with_no_items(self):
        self.assertEqual(self.problems(category("Docs", ["a", "b"]), category("Empty", [])),
                         ["Empty: has no items"])

    def test_flags_two_categories_with_the_same_name_in_any_case(self):
        self.assertEqual(self.problems(category("Docs", ["a"]), category("docs", ["b"])),
                         ["docs: same name as another category"])


class Apply(TempDir):
    def setUp(self):
        super().setUp()
        touch(self.root, "a.txt", b"a")
        touch(self.root, "pack/b", b"b")
        self.scanned = td.scan(self.root)
        self.plan = {"categories": [category("Docs", ["a.txt"]), category("Folders", ["pack"])]}

    def test_moves_each_item_into_its_category_folder(self):
        self.assertEqual(td.apply(self.scanned, self.plan), [])
        self.assertTrue(os.path.isfile(os.path.join(self.root, "Docs", "a.txt")))
        self.assertTrue(os.path.isfile(os.path.join(self.root, "Folders", "pack", "b")))
        self.assertEqual(sorted(os.listdir(self.root)), ["Docs", "Folders"])

    def test_moves_nothing_when_a_category_name_already_exists_in_the_dir(self):
        touch(self.root, "Docs", b"")
        self.assertEqual(td.apply(self.scanned, self.plan), ["Docs: already exists in the directory"])
        self.assertTrue(os.path.isfile(os.path.join(self.root, "a.txt")))

    def test_moves_nothing_when_an_item_is_missing(self):
        os.remove(os.path.join(self.root, "a.txt"))
        self.assertEqual(td.apply(self.scanned, self.plan), ["a.txt: no longer in the directory"])
        self.assertTrue(os.path.isdir(os.path.join(self.root, "pack")))

    def test_moves_nothing_when_the_plan_has_problems(self):
        self.plan["categories"].pop()
        self.assertEqual(td.apply(self.scanned, self.plan), ["pack: not in any category"])
        self.assertTrue(os.path.isfile(os.path.join(self.root, "a.txt")))

    def test_cli_exits_non_zero_and_names_each_problem(self):
        self.plan["categories"].pop()
        result = self.run_cli("apply", "--scan", self.write_json("scan", self.scanned),
                              "--plan", self.write_json("plan", self.plan))
        self.assertEqual(result.returncode, 1)
        self.assertIn("pack: not in any category", result.stderr)


SCAN = {"dir": "/d", "scanned": "2027-02-01", "items": [
    item("small.pdf", size=10, modified="2027-01-03"),
    item("big.pdf", size=5000, modified="2027-01-09"),
    item("mid.pdf", size=300, modified="2027-01-01"),
    item("last.pdf", size=1, modified="2027-01-05"),
    item("setup.dmg", size=90, type_="application/x-apple-diskimage"),
    item("<b>x</b>.zip", size=2),
]}
PLAN = {"categories": [
    category("Keep Small", ["setup.dmg"], "keep"),
    category("Papers", ["small.pdf", "big.pdf", "mid.pdf", "last.pdf"], "archive", "Old <papers>"),
    category("Junk", ["<b>x</b>.zip"], "delete"),
]}


class Summary(unittest.TestCase):
    def test_orders_categories_by_action_then_by_size(self):
        plan = {"categories": PLAN["categories"] + [category("Keep Big", ["x"], "keep")]}
        scan = {**SCAN, "items": SCAN["items"] + [item("x", size=999)]}
        names = [line.split("|")[1].strip() for line in td.summary(scan, plan).splitlines()[2:]]
        self.assertEqual(names, ["Junk", "Papers", "Keep Big", "Keep Small"])

    def test_shows_action_count_size_and_three_largest_examples(self):
        row = td.summary(SCAN, PLAN).splitlines()[3]
        self.assertEqual(row, "| Papers | archive | 4 | 5.3 KB | big.pdf, mid.pdf, small.pdf |")


class Render(TempDir):
    def test_lists_each_category_with_action_reason_and_items_largest_first(self):
        html = td.render(SCAN, PLAN)
        papers = html[html.index("<h2>Papers"):html.index("<h2>Keep Small")]
        self.assertIn("archive", papers)
        self.assertIn("Old &lt;papers&gt;", papers)
        self.assertLess(papers.index("big.pdf"), papers.index("mid.pdf"))
        self.assertLess(papers.index("mid.pdf"), papers.index("small.pdf"))

    def test_shows_the_date_range_of_each_category(self):
        html = td.render(SCAN, PLAN)
        papers = html[html.index("<h2>Papers"):html.index("<h2>Keep Small")]
        self.assertIn("2027-01-01 to 2027-01-09", papers)

    def test_escapes_item_names(self):
        html = td.render(SCAN, PLAN)
        self.assertNotIn("<b>x</b>", html)
        self.assertIn("&lt;b&gt;x&lt;/b&gt;.zip", html)

    def test_cli_writes_the_report_into_the_dir(self):
        touch(self.root, "a.txt", b"a")
        scanned = td.scan(self.root)
        result = self.run_cli("render", "--scan", self.write_json("scan", scanned),
                              "--plan", self.write_json("plan", {"categories": [category("Docs", ["a.txt"])]}))
        report = os.path.join(scanned["dir"], "triage.html")
        self.assertEqual(result.stdout.strip(), report)
        with open(report) as f:
            self.assertIn("<h2>Docs", f.read())


if __name__ == "__main__":
    unittest.main()
