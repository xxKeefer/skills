#!/usr/bin/env python3
"""Run: python3 defect_mining.spec.py"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import defect_mining as dm

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "defect_mining.py")
SINCE = "2025-11-04"
WINDOW = "2026-10-01"
UNTIL = "2026-11-04T00:00:00Z"
ISOLATED = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}


def git(root, *args, day="2026-01-01"):
    moment = f"{day}T12:00:00+00:00"
    env = dict(os.environ, GIT_AUTHOR_DATE=moment, GIT_COMMITTER_DATE=moment, **ISOLATED)
    command = ["git", "-C", root, "-c", "user.name=Test", "-c", "user.email=test@example.test", *args]
    return subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True, env=env).stdout.strip()


def commit(root, day, message, *files):
    for name in files:
        path = os.path.join(root, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.write(f"{message}\n")
    git(root, "add", "-A", day=day)
    git(root, "commit", "-q", "-m", message, day=day)
    return git(root, "rev-parse", "HEAD")


TRACKER = [
    {"id": "PROJ-1", "date": "2026-03-02", "title": "Total is wrong"},
    {"id": "PROJ-12", "date": "2026-10-21", "title": "Date format"},
    {"id": "PROJ-3", "date": "2026-10-23T09:30:00.000+1000", "title": "Session lost"},
    {"id": "PROJ-5", "date": "2026-05-01", "title": "Never traced"},
]


class Trace(unittest.TestCase):
    """A repo with one commit before the window, fixes in and out of the run window, and a merge."""

    @classmethod
    def setUpClass(cls):
        cls.root = root = tempfile.mkdtemp()
        cls.addClassCleanup(shutil.rmtree, root)
        git(root, "init", "-q", "-b", "main")
        commit(root, "2024-06-01", "fix: PROJ-9 before the 12 months", "src/old.ts")
        cls.c1 = commit(root, "2026-03-01", "fix(cart): PROJ-1 wrong total", "src/cart/total.ts",
                        "src/cart/total.test.ts")
        cls.c2 = commit(root, "2026-10-10", "feat(cart): PROJ-1 follow-up", "src/cart/sum.ts")
        cls.c3 = commit(root, "2026-10-12", "fix off by one in pager", "lib/pager.py")
        commit(root, "2026-10-15", "chore: bump deps", "package-lock.json")
        cls.c6 = commit(root, "2026-10-20", "fix(i18n): PROJ-12 date format", "src/i18n/date.ts")
        git(root, "switch", "-q", "-c", "topic", day="2026-10-22")
        commit(root, "2026-10-22", "wip", "src/auth/login.ts")
        git(root, "switch", "-q", "main", day="2026-10-23")
        git(root, "merge", "-q", "--no-ff", "-m", "Merge branch 'fix/proj-3-session'", "topic", day="2026-10-23")
        cls.merge = git(root, "rev-parse", "HEAD")
        commit(root, "2026-11-10", "fix: after the window", "src/late.ts")

    def setUp(self):
        self.cache, self.state = tempfile.mkdtemp(), tempfile.mkdtemp()
        for folder in (self.cache, self.state):
            self.addCleanup(shutil.rmtree, folder)

    def tracker(self, bugs=TRACKER):
        path = os.path.join(self.cache, "tracker.jsonl")
        with open(path, "w") as f:
            f.writelines(json.dumps(b) + "\n" for b in bugs)
        return path

    def trace(self, tracker=None, chunk=25):
        return dm.trace(self.root, "main", SINCE, WINDOW, UNTIL, self.cache, self.state, tracker, chunk)

    def items(self):
        with open(os.path.join(self.cache, "defects.jsonl")) as f:
            return {i["id"]: i for i in map(json.loads, f)}

    def chunk_ids(self, meta):
        ids = []
        for name in meta["chunks"]:
            with open(os.path.join(self.cache, name)) as f:
                ids.append([json.loads(line)["id"] for line in f])
        return ids


class TraceTrackerBugs(Trace):
    def test_joins_each_tracker_bug_to_every_commit_that_names_its_key(self):
        self.trace(self.tracker())
        bug = self.items()["PROJ-1"]
        self.assertEqual(bug["commits"], [self.c2, self.c1])
        self.assertEqual(bug["files"], ["src/cart/sum.ts", "src/cart/total.test.ts", "src/cart/total.ts"])

    def test_does_not_join_a_key_to_a_longer_key(self):
        self.trace(self.tracker())
        items = self.items()
        self.assertNotIn(self.c6, items["PROJ-1"]["commits"])
        self.assertEqual(items["PROJ-12"]["commits"], [self.c6])

    def test_reads_a_merge_as_one_item_and_matches_its_key_in_any_case(self):
        self.trace(self.tracker())
        bug = self.items()["PROJ-3"]
        self.assertEqual(bug["commits"], [self.merge])
        self.assertEqual(bug["files"], ["src/auth/login.ts"])

    def test_joins_a_bug_to_the_commits_that_its_tracker_gives(self):
        self.trace(self.tracker([{"id": "#7", "date": "2026-10-13", "title": "Pager", "commits": [self.c3[:10]]}]))
        self.assertEqual(self.items()["#7"]["commits"], [self.c3])

    def test_counts_a_bug_with_no_commit_as_untraced_and_writes_no_item_for_it(self):
        meta = self.trace(self.tracker())
        self.assertEqual((meta["bugs"], meta["traced"]), (4, 3))
        self.assertNotIn("PROJ-5", self.items())

    def test_marks_the_run_window_by_the_date_that_the_tracker_gives(self):
        meta = self.trace(self.tracker())
        items = self.items()
        self.assertEqual([items[k]["inWindow"] for k in ("PROJ-1", "PROJ-12", "PROJ-3")], [False, True, True])
        self.assertEqual(items["PROJ-3"]["date"], "2026-10-23")
        self.assertEqual(meta["trackerInWindow"], 2)


class TraceFixCommits(Trace):
    def test_lists_each_fix_commit_in_the_window_that_names_no_traced_bug(self):
        meta = self.trace(self.tracker())
        commits = [i["id"] for i in self.items().values() if i["source"] == "commit"]
        self.assertEqual(commits, [self.c3])
        self.assertEqual((meta["fixCommits"], meta["fixCommitsInWindow"]), (1, 1))

    def test_lists_every_fix_commit_on_the_first_parent_line_with_no_tracker(self):
        meta = self.trace()
        items = self.items()
        self.assertEqual(set(items), {self.c1, self.c3, self.c6, self.merge})
        self.assertEqual(items[self.c3]["title"], "fix off by one in pager")
        self.assertEqual(items[self.c1]["date"], "2026-03-01")
        self.assertFalse(items[self.c1]["inWindow"])
        self.assertEqual((meta["fixCommits"], meta["fixCommitsInWindow"]), (4, 3))

    def test_marks_each_fix_that_changed_a_test_file(self):
        self.trace()
        items = self.items()
        self.assertTrue(items[self.c1]["tested"])
        self.assertFalse(items[self.c3]["tested"])


class TraceChunks(Trace):
    def test_chunks_every_item_when_the_fix_commits_are_the_bug_list(self):
        meta = self.trace()
        self.assertEqual(meta["toClassify"], 4)
        self.assertEqual(sorted(sum(self.chunk_ids(meta), [])), sorted([self.c1, self.c3, self.c6, self.merge]))

    def test_chunks_the_tracker_bugs_and_only_the_run_window_fix_commits_with_a_tracker(self):
        meta = self.trace(self.tracker([TRACKER[1]]))
        self.assertEqual(sorted(sum(self.chunk_ids(meta), [])), sorted(["PROJ-12", self.c3, self.merge]))
        self.assertEqual((meta["fixCommits"], meta["fixCommitsInWindow"]), (3, 2))

    def test_leaves_out_each_item_that_the_class_cache_holds(self):
        with open(os.path.join(self.state, "classified.jsonl"), "w") as f:
            f.write(json.dumps({"id": self.c3, "defect": True}) + "\n")
        meta = self.trace()
        self.assertEqual(meta["toClassify"], 3)
        self.assertNotIn(self.c3, sum(self.chunk_ids(meta), []))

    def test_writes_chunks_of_the_chunk_size_with_the_fields_a_miner_reads(self):
        meta = self.trace(chunk=3)
        self.assertEqual([len(c) for c in self.chunk_ids(meta)], [3, 1])
        with open(os.path.join(self.cache, meta["chunks"][0])) as f:
            line = json.loads(f.readline())
        self.assertEqual(set(line), {"id", "source", "title", "commits", "files"})

    def test_the_trace_command_prints_what_it_writes_to_trace_json(self):
        out = subprocess.run(["python3", SCRIPT, "trace", "--repo-root", self.root, "--ref", "main", "--since", SINCE,
                              "--window-start", WINDOW, "--until", UNTIL, "--cache", self.cache, "--state",
                              self.state], check=True, stdout=subprocess.PIPE, text=True).stdout
        with open(os.path.join(self.cache, "trace.json")) as f:
            self.assertEqual(json.loads(out), json.load(f))


class TestFiles(unittest.TestCase):
    def test_knows_a_test_file_by_its_folder_or_its_name(self):
        for path in ("src/a.test.ts", "src/a.spec.js", "pkg/a_test.go", "tests/test_a.py", "a/__tests__/b.ts",
                     "src/CartTest.php", "spec/a_spec.rb", "e2e/flow.ts"):
            self.assertTrue(dm.is_test(path), path)

    def test_does_not_mistake_a_source_file_for_a_test_file(self):
        for path in ("src/latest.ts", "src/contest/a.ts", "GIT.md", "src/Test.ts", "src/attest.py"):
            self.assertFalse(dm.is_test(path), path)


def item(ident, files=("src/a/x.ts",), source="tracker", date="2026-10-20", window=True):
    return {"id": ident, "source": source, "date": date, "title": f"title {ident}", "commits": ["a" * 40],
            "files": list(files), "tested": any(dm.is_test(f) for f in files), "inWindow": window}


def label(ident, escape="boundary", level="unit", dimensions=(), condition="a condition", defect=True):
    return {"id": ident, "defect": defect, "kind": "a kind", "check": "a check", "specific": False,
            "escape": escape, "dimensions": list(dimensions), "condition": condition, "level": level}


class Hotspots(unittest.TestCase):
    def setUp(self):
        self.cache, self.state = tempfile.mkdtemp(), tempfile.mkdtemp()
        for folder in (self.cache, self.state):
            self.addCleanup(shutil.rmtree, folder)

    def prepare(self, items, labels, tracker=True, bugs=None, traced=None, cached=()):
        traced = len([i for i in items if i["source"] == "tracker"]) if traced is None else traced
        meta = {"since": SINCE, "windowStart": WINDOW, "until": UNTIL, "tracker": tracker,
                "bugs": traced if bugs is None else bugs, "traced": traced}
        with open(os.path.join(self.cache, "trace.json"), "w") as f:
            json.dump(meta, f)
        self.write(os.path.join(self.cache, "defects.jsonl"), items)
        os.makedirs(os.path.join(self.cache, "classified"), exist_ok=True)
        self.write(os.path.join(self.cache, "classified", "01.jsonl"), labels)
        self.write(os.path.join(self.state, "classified.jsonl"), cached)

    @staticmethod
    def write(path, records):
        with open(path, "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in records)

    def run_hotspots(self, *args, **kwargs):
        self.prepare(*args, **kwargs)
        return dm.hotspots(self.cache, self.state)

    def markdown(self, *args, **kwargs):
        self.run_hotspots(*args, **kwargs)
        with open(os.path.join(self.state, "defect-hotspots.md")) as f:
            return f.read()

    def table(self, text, heading):
        part = text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
        rows = [line for line in part.splitlines() if line.startswith("| ")][2:]
        return [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]


class HotspotsCache(Hotspots):
    def test_merges_the_miner_files_into_the_class_cache_and_drops_each_item_that_left_the_window(self):
        self.run_hotspots([item("PROJ-1"), item("PROJ-2")], [label("PROJ-2")],
                          cached=[label("PROJ-1"), label("PROJ-OLD")])
        with open(os.path.join(self.state, "classified.jsonl")) as f:
            self.assertEqual({json.loads(line)["id"] for line in f}, {"PROJ-1", "PROJ-2"})

    def test_stops_and_names_a_miner_id_that_the_trace_does_not_hold(self):
        with self.assertRaises(SystemExit) as stop:
            self.run_hotspots([item("PROJ-1")], [label("PROJ-1"), label("PROJ-99")])
        self.assertIn("PROJ-99", str(stop.exception.code))

    def test_stops_and_names_each_item_that_needs_a_class_and_has_none(self):
        old_commit = item("c0ffee", source="commit", window=False)
        with self.assertRaises(SystemExit) as stop:
            self.run_hotspots([item("PROJ-1"), item("PROJ-2"), old_commit], [label("PROJ-1")])
        self.assertIn("PROJ-2", str(stop.exception.code))
        self.assertNotIn("c0ffee", str(stop.exception.code))

    def test_writes_the_run_window_defects_for_the_themes(self):
        items = [item("PROJ-1"), item("PROJ-2", window=False), item("PROJ-3"), item("c0ffee", source="commit")]
        labels = [label("PROJ-1"), label("PROJ-2"), label("PROJ-3", defect=False), label("c0ffee")]
        self.run_hotspots(items, labels)
        with open(os.path.join(self.cache, "window-defects.jsonl")) as f:
            lines = [json.loads(line) for line in f]
        self.assertEqual([(d["id"], d["source"]) for d in lines], [("PROJ-1", "tracker"), ("c0ffee", "commit")])
        self.assertEqual(set(lines[0]), {"id", "source", "title", "kind", "check", "specific"})

    def test_the_hotspots_command_prints_the_counts_and_the_path(self):
        self.prepare([item("PROJ-1")], [label("PROJ-1")], bugs=2, traced=1)
        out = subprocess.run(["python3", SCRIPT, "hotspots", "--cache", self.cache, "--state", self.state],
                             check=True, stdout=subprocess.PIPE, text=True).stdout
        result = json.loads(out)
        self.assertEqual(result["path"], os.path.join(self.state, "defect-hotspots.md"))
        self.assertEqual((result["defects"], result["traced"], result["bugs"], result["skewed"]), (1, 1, 2, True))
        self.assertEqual(result["windowDefects"], {"tracker": 1, "commit": 0})


class HotspotsAreas(Hotspots):
    def test_counts_each_bug_once_in_each_folder_that_it_changed(self):
        items = [item("PROJ-1", ["src/a/x.ts", "src/a/y.ts", "src/b/z.ts"]), item("PROJ-2", ["src/a/w.ts", "src/b/v.ts"])]
        rows = self.table(self.markdown(items, [label("PROJ-1"), label("PROJ-2")]), "Hotspots")
        self.assertEqual({r[0]: r[1] for r in rows}, {"`src/a`": "2", "`src/b`": "2"})

    def test_lists_only_the_areas_that_two_or_more_bugs_changed(self):
        items = [item("PROJ-1", ["src/a/x.ts", "src/c/q.ts"]), item("PROJ-2", ["src/a/y.ts"])]
        rows = self.table(self.markdown(items, [label("PROJ-1"), label("PROJ-2")]), "Hotspots")
        self.assertEqual([r[0] for r in rows], ["`src/a`"])

    def test_leaves_test_files_and_lock_files_out_of_the_areas(self):
        files = ["src/a/x.ts", "src/a/__tests__/x.ts", "pnpm-lock.yaml", "Cargo.lock"]
        items = [item("PROJ-1", files), item("PROJ-2", files)]
        rows = self.table(self.markdown(items, [label("PROJ-1"), label("PROJ-2")]), "Hotspots")
        self.assertEqual([r[0] for r in rows], ["`src/a`"])

    def test_names_a_file_at_the_repo_root_by_a_dot(self):
        items = [item("PROJ-1", ["main.go"]), item("PROJ-2", ["main.go"])]
        rows = self.table(self.markdown(items, [label("PROJ-1"), label("PROJ-2")]), "Hotspots")
        self.assertEqual(rows[0][0], "`.`")

    def test_ranks_the_areas_by_bugs_and_keeps_the_top_25(self):
        items = [item(f"PROJ-{n}{k}", [f"area{n:02d}/x.ts"]) for n in range(30) for k in "ab"]
        items += [item(f"PROJ-9{k}", ["hot/x.ts"]) for k in "abc"]
        rows = self.table(self.markdown(items, [label(i["id"]) for i in items]), "Hotspots")
        self.assertEqual(len(rows), 25)
        self.assertEqual(rows[0][:2], ["`hot`", "3"])
        self.assertEqual(rows[1][0], "`area00`")

    def test_names_the_two_escape_types_most_missed_in_each_area(self):
        escapes = ["boundary", "combination", "boundary", "authz", "combination", "boundary"]
        items = [item(f"PROJ-{n}") for n in range(len(escapes))]
        labels = [label(i["id"], escape=e) for i, e in zip(items, escapes)]
        rows = self.table(self.markdown(items, labels), "Hotspots")
        self.assertEqual(rows[0][3], "boundary 3, combination 2")

    def test_counts_the_fixes_that_changed_a_test_file_overall_and_in_each_area(self):
        items = [item("PROJ-1", ["src/a/x.ts", "src/a/x.test.ts"]), item("PROJ-2", ["src/a/y.ts"])]
        text = self.markdown(items, [label("PROJ-1"), label("PROJ-2")])
        self.assertEqual(self.table(text, "Hotspots")[0][2], "1/2")
        self.assertIn("- With a test: 1/2 fixes changed a test file.\n", text)


class HotspotsBugList(Hotspots):
    def test_gives_coverage_and_a_skew_line_below_60_percent(self):
        text = self.markdown([item("PROJ-1")], [label("PROJ-1")], bugs=10, traced=5)
        self.assertIn("- Coverage: 5/10 tracker bugs trace to a commit in this repo (50%).\n", text)
        self.assertIn("- Skewed:", text)

    def test_gives_no_skew_line_at_60_percent_or_more(self):
        text = self.markdown([item("PROJ-1")], [label("PROJ-1")], bugs=10, traced=6)
        self.assertIn("(60%)", text)
        self.assertNotIn("Skewed", text)

    def test_names_the_fix_commits_as_the_source_and_gives_no_coverage_with_no_tracker(self):
        text = self.markdown([item("c0ffee", source="commit")], [label("c0ffee")], tracker=False, bugs=0, traced=0)
        self.assertIn("- Source: the fix commits of 2025-11-04..2026-11-04. Defects: 1.\n", text)
        self.assertNotIn("Coverage", text)

    def test_uses_only_the_tracker_bugs_as_the_bug_list_when_a_tracker_ran(self):
        items = [item(f"PROJ-{k}", ["src/a/x.ts"]) for k in "12"]
        items += [item(sha, ["lib/y.py"], source="commit") for sha in ("c0ffee", "facade")]
        text = self.markdown(items, [label(i["id"]) for i in items])
        self.assertEqual([r[0] for r in self.table(text, "Hotspots")], ["`src/a`"])
        self.assertIn("- Source: the tracker bugs resolved 2025-11-04..2026-11-04. Defects: 2.\n", text)

    def test_counts_only_the_items_that_fixed_behaviour(self):
        items = [item(f"PROJ-{k}", ["src/a/x.ts"]) for k in "12"] + [item(f"PROJ-{k}", ["src/b/x.ts"]) for k in "34"]
        labels = [label("PROJ-1"), label("PROJ-2"), label("PROJ-3"), label("PROJ-4", defect=False)]
        text = self.markdown(items, labels)
        self.assertEqual([r[0] for r in self.table(text, "Hotspots")], ["`src/a`"])
        self.assertIn("Defects: 3.", text)


class HotspotsEscapes(Hotspots):
    def test_reads_an_unknown_escape_type_as_other(self):
        rows = self.table(self.markdown([item("PROJ-1")], [label("PROJ-1", escape="typo")]), "What escapes")
        self.assertEqual(rows[0][:2], ["`other`", "1"])

    def test_gives_each_escape_type_its_most_common_level_cheapest_first_and_its_newest_condition(self):
        items = [item("PROJ-1", date="2026-05-01"), item("PROJ-2", date="2026-09-01"), item("PROJ-3")]
        labels = [label("PROJ-1", level="e2e", condition="older"), label("PROJ-2", level="unit", condition="newest"),
                  label("PROJ-3", escape="authz", level="made-up")]
        items[2]["date"] = "2026-01-01"
        rows = self.table(self.markdown(items, labels), "What escapes")
        self.assertEqual(rows[0], ["`boundary`", "2", "`unit`", "newest"])
        self.assertEqual(rows[1][2], "")

    def test_writes_a_table_cell_with_no_pipe_or_line_break(self):
        rows = self.table(self.markdown([item("PROJ-1")], [label("PROJ-1", condition="a | b\nc")]), "What escapes")
        self.assertEqual(rows[0][3], "a / b c")

    def test_counts_each_dimension_once_for_each_bug(self):
        items = [item("PROJ-1"), item("PROJ-2")]
        labels = [label("PROJ-1", dimensions=["Role", "role "]), label("PROJ-2", dimensions=["role", "flag"])]
        rows = self.table(self.markdown(items, labels), "Dimensions")
        self.assertEqual(rows, [["role", "2"], ["flag", "1"]])

    def test_stays_under_150_lines(self):
        items = [item(f"PROJ-{n}", [f"area{n % 50}/x.ts"]) for n in range(200)]
        labels = [label(i["id"], escape=dm.ESCAPES[n % 10], dimensions=[f"dim{n % 30}"]) for n, i in enumerate(items)]
        self.assertLess(len(self.markdown(items, labels).splitlines()), 150)


if __name__ == "__main__":
    unittest.main()
