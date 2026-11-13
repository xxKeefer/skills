#!/usr/bin/env python3
"""Run: python3 review_mining.spec.py"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import review_mining as rm

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "review_mining.py")
SINCE = "2026-08-01"
UNTIL = "2026-08-31"


def stamp(day, hour=12):
    return f"2026-08-{day:02d}T{hour:02d}:00:00Z"


def thread(author="alice", typename="User", resolved=False, outdated=False, body="Use a guard here.",
           path="src/a.ts"):
    who = {"__typename": typename, "login": author} if author else None
    comment = {"author": who, "body": body, "url": "https://example.test/c"}
    return {"isResolved": resolved, "isOutdated": outdated, "path": path, "comments": {"nodes": [comment]}}


def pr(number, day, *threads):
    return {"number": number, "mergedAt": stamp(day), "reviewThreads": {"nodes": list(threads)}}


def run(run_id, day, workflow="CI", workflow_id=1, branch="feature/x", sha=None, status="failure", hour=12):
    return {"id": run_id, "name": workflow, "workflow_id": workflow_id, "event": "pull_request",
            "head_branch": branch, "head_sha": sha or f"sha{run_id}", "created_at": stamp(day, hour),
            "html_url": f"https://example.test/runs/{run_id}", "conclusion": status}


def failed_job(name, step):
    steps = [{"name": "Checkout", "conclusion": "success"}, {"name": step, "conclusion": "failure"}]
    return {"name": name, "conclusion": "failure", "steps": steps}


class FakeGitHub:
    """Answers the gh calls of review_mining from fixed data, and keeps GitHub's result cap."""

    def __init__(self, prs=(), runs=(), jobs=None, default_branch="main"):
        self.prs, self.runs, self.jobs = list(prs), list(runs), jobs or {}
        self.default_branch = default_branch
        self.calls = []

    def __call__(self, args):
        self.calls.append(args)
        endpoint = args[1]
        fields = dict(args[i + 1].split("=", 1) for i, a in enumerate(args) if a == "-f")
        if endpoint == "graphql":
            return self.search(fields)
        if endpoint.endswith("/jobs"):
            return {"jobs": self.jobs.get(int(endpoint.split("/")[-2]), [])}
        if endpoint.endswith("/actions/runs"):
            return self.list_runs(fields)
        return {"default_branch": self.default_branch}

    def search(self, fields):
        low, high = fields["q"].split("merged:")[1].split("..")
        found = [p for p in self.prs if low <= p["mergedAt"] <= high]
        visible = found[:rm.CAP]
        start = int(fields.get("after", 0))
        page = visible[start:start + rm.PR_PAGE]
        end = start + len(page)
        info = {"hasNextPage": end < len(visible), "endCursor": str(end)}
        return {"data": {"search": {"issueCount": len(found), "pageInfo": info, "nodes": page}}}

    def list_runs(self, fields):
        found = [r for r in self.runs if r["conclusion"] == fields["status"]]
        if "head_sha" in fields:
            found = [r for r in found if r["head_sha"] == fields["head_sha"]]
        else:
            low, high = fields["created"].split("..")
            found = [r for r in found if low <= r["created_at"] <= high]
        size, page = int(fields["per_page"]), int(fields.get("page", 1))
        visible = found[:rm.CAP]
        return {"total_count": len(found), "workflow_runs": visible[(page - 1) * size:page * size]}


class Base(unittest.TestCase):
    def setUp(self):
        self.cache = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.cache)
        saved = rm.gh, rm.CAP, rm.PR_PAGE, rm.RUN_PAGE
        self.addCleanup(self.restore, saved)

    @staticmethod
    def restore(saved):
        rm.gh, rm.CAP, rm.PR_PAGE, rm.RUN_PAGE = saved

    def fetch(self, fake, sample=150, chunk=150):
        rm.gh = fake
        rm.fetch("acme/shop", SINCE, UNTIL, self.cache, sample=sample, chunk=chunk)
        return fake

    def read(self, name):
        with open(os.path.join(self.cache, name)) as f:
            return f.read()

    def lines(self, name):
        return [json.loads(line) for line in self.read(name).splitlines()]

    def meta(self):
        return json.loads(self.read("meta.json"))


class FetchReviewThreads(Base):
    def test_writes_one_numbered_line_for_each_thread_of_a_pr_merged_in_the_window(self):
        late = {"number": 3, "mergedAt": "2026-09-02T12:00:00Z", "reviewThreads": {"nodes": [thread()]}}
        self.fetch(FakeGitHub(prs=[pr(1, 5, thread(), thread()), pr(2, 10, thread()), late]))
        threads = self.lines("threads.jsonl")
        self.assertEqual([(t["id"], t["pr"]) for t in threads], [("t1", 1), ("t2", 1), ("t3", 2)])

    def test_splits_the_window_while_the_search_passes_the_result_cap(self):
        rm.CAP, rm.PR_PAGE = 3, 2
        self.fetch(FakeGitHub(prs=[pr(n, n, thread()) for n in range(1, 11)]))
        self.assertEqual(sorted(t["pr"] for t in self.lines("threads.jsonl")), list(range(1, 11)))

    def test_names_a_bot_by_its_login_and_every_other_author_human(self):
        prs = [pr(1, 5, thread("copilot-pull-request-reviewer", "Bot"), thread("renovate[bot]"), thread("alice"),
                   thread(None))]
        self.fetch(FakeGitHub(prs=prs))
        self.assertEqual([t["author"] for t in self.lines("threads.jsonl")],
                         ["copilot-pull-request-reviewer", "renovate[bot]", "human", "human"])

    def test_reads_an_outdated_thread_as_changed_before_its_resolved_state(self):
        prs = [pr(1, 5, thread(resolved=True, outdated=True), thread(resolved=True), thread(outdated=True), thread())]
        self.fetch(FakeGitHub(prs=prs))
        self.assertEqual([t["outcome"] for t in self.lines("threads.jsonl")], ["changed", "closed", "changed", "open"])

    def test_keeps_no_human_login_and_cuts_the_body_to_500_characters(self):
        self.fetch(FakeGitHub(prs=[pr(1, 5, thread("alice", body="x" * 900))]))
        self.assertNotIn("alice", self.read("threads.jsonl"))
        self.assertEqual(len(self.lines("threads.jsonl")[0]["body"]), 500)


class FetchFailedRuns(Base):
    def test_lists_every_failed_run_in_the_window_while_the_list_passes_the_cap(self):
        rm.CAP, rm.RUN_PAGE = 3, 2
        runs = [run(100 + d, d) for d in range(1, 11)] + [run(200, 5, status="success"), run(300, 31)]
        self.fetch(FakeGitHub(runs=runs))
        self.assertEqual(sorted(r["run"] for r in self.lines("runs.jsonl")), list(range(101, 111)))

    def test_drills_the_failed_jobs_and_steps_of_the_newest_runs_only(self):
        jobs = {110: [failed_job("lint", "Run lint"), {"name": "unit", "conclusion": "success", "steps": []}]}
        fake = self.fetch(FakeGitHub(runs=[run(100 + d, d) for d in range(1, 11)], jobs=jobs), sample=2)
        drilled = {r["run"]: r["failed"] for r in self.lines("runs.jsonl") if "failed" in r}
        self.assertEqual(drilled, {109: [], 110: [{"job": "lint", "step": "Run lint"}]})
        self.assertEqual(len([c for c in fake.calls if c[1].endswith("/jobs")]), 2)

    def test_marks_a_sampled_run_flaky_when_the_same_workflow_passed_on_its_sha(self):
        runs = [run(1, 5, sha="aaa"), run(2, 5, sha="aaa", status="success", hour=13),
                run(3, 6, sha="bbb"), run(4, 6, sha="bbb", workflow="Lint", workflow_id=2, status="success")]
        self.fetch(FakeGitHub(runs=runs))
        self.assertEqual({r["run"]: r["flaky"] for r in self.lines("runs.jsonl")}, {1: True, 3: False})


class FetchMeta(Base):
    def test_counts_threads_by_source_and_outcome_and_runs_by_workflow_and_branch(self):
        prs = [pr(1, 5, thread(outdated=True), thread(), thread("copilot", "Bot", resolved=True))]
        runs = [run(1, 5), run(2, 6, branch="main"), run(3, 7, workflow="Lint", workflow_id=2)]
        self.fetch(FakeGitHub(prs=prs, runs=runs))
        meta = self.meta()
        self.assertEqual(meta["mergedPrs"], 1)
        self.assertEqual(meta["review"]["human"], {"threads": 2, "changed": 1, "closed": 0, "open": 1})
        self.assertEqual(meta["review"]["bot"], {"threads": 1, "changed": 0, "closed": 1, "open": 0})
        self.assertEqual(meta["review"]["bots"], {"copilot": 1})
        self.assertEqual(meta["ci"]["failedRuns"], 3)
        self.assertEqual(meta["ci"]["byWorkflow"], {"CI": 2, "Lint": 1})
        self.assertEqual(meta["defaultBranch"], "main")
        self.assertEqual(meta["ci"]["onDefaultBranch"], 1)
        self.assertEqual(meta["ci"]["sample"], 3)

    def test_groups_the_sampled_runs_by_workflow_job_and_step(self):
        jobs = {1: [failed_job("lint", "Run lint")], 2: [failed_job("lint", "Run lint")]}
        self.fetch(FakeGitHub(runs=[run(1, 5), run(2, 6), run(3, 7)], jobs=jobs))
        self.assertEqual(self.meta()["ci"]["surfaces"], [
            {"workflow": "CI", "job": "lint", "step": "Run lint", "runs": 2, "flaky": 0, "ids": ["r2", "r1"]},
            {"workflow": "CI", "job": None, "step": None, "runs": 1, "flaky": 0, "ids": ["r3"]},
        ])


class FetchChunks(Base):
    def test_writes_human_and_bot_chunks_of_the_chunk_size(self):
        bot = thread("copilot", "Bot", outdated=True, body="Line one\nline two", path="src/b.ts")
        self.fetch(FakeGitHub(prs=[pr(1, 5, thread(), thread(), thread(), bot)]), chunk=2)
        self.assertEqual(sorted(os.listdir(os.path.join(self.cache, "chunks"))),
                         ["bot-01.txt", "human-01.txt", "human-02.txt"])
        self.assertEqual(self.read("chunks/bot-01.txt"), "[t4|copilot|changed|src/b.ts] Line one line two\n")
        self.assertEqual(self.read("chunks/human-02.txt"), "[t3|human|open|src/a.ts] Use a guard here.\n")


class FetchCache(Base):
    def test_makes_no_call_when_the_cache_holds_the_window(self):
        self.fetch(FakeGitHub(prs=[pr(1, 5, thread())]))
        fake = self.fetch(FakeGitHub())
        self.assertEqual(fake.calls, [])
        self.assertEqual(len(self.lines("threads.jsonl")), 1)

    def test_the_fetch_command_prints_the_cached_meta(self):
        self.fetch(FakeGitHub(prs=[pr(1, 5, thread())]))
        result = subprocess.run(["python3", SCRIPT, "fetch", "--repo", "acme/shop", "--since", SINCE,
                                 "--until", UNTIL, "--cache", self.cache], capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), self.meta())


class Floor(unittest.TestCase):
    def test_needs_the_larger_of_2_items_and_1_per_100_items_of_the_source(self):
        self.assertFalse(rm.meets_floor(1, 10))
        self.assertTrue(rm.meets_floor(2, 150))
        self.assertFalse(rm.meets_floor(2, 250))
        self.assertTrue(rm.meets_floor(3, 250))


class Themes(Base):
    def setUp(self):
        super().setUp()
        human = [thread(outdated=True), thread(outdated=True), thread(), thread(resolved=True)]
        bot = [thread("copilot", "Bot", outdated=True), thread("copilot", "Bot"), thread("copilot", "Bot", resolved=True)]
        runs = [run(1, 5), run(2, 6), run(3, 7, sha="ccc"), run(4, 7, sha="ccc", status="success", hour=13)]
        self.fetch(FakeGitHub(prs=[pr(1, 5, *human, *bot)], runs=runs))

    def themes(self, draft, prior=None):
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)
        args = ["python3", SCRIPT, "themes", "--cache", self.cache, "--draft", os.path.join(folder, "draft.json")]
        with open(args[-1], "w") as f:
            json.dump(draft, f)
        if prior is not None:
            args += ["--prior", os.path.join(folder, "prior.json")]
            with open(args[-1], "w") as f:
                json.dump(prior, f)
        return subprocess.run(args, capture_output=True, text=True)

    def result(self, draft, prior=None):
        result = self.themes(draft, prior)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def by_slug(self, draft, prior=None):
        return {t["slug"]: t for t in self.result(draft, prior)["themes"]}

    def test_counts_each_outcome_and_rates_per_100_items_of_its_own_source(self):
        guard = self.by_slug([{"slug": "guard", "source": "human", "ids": ["t1", "t2", "t3"]}])["guard"]
        self.assertEqual((guard["count"], guard["changed"], guard["closed"], guard["open"], guard["rate"]),
                         (3, 2, 0, 1, 75.0))

    def test_marks_a_theme_mostly_ignored_when_fewer_than_half_its_threads_changed(self):
        themes = self.by_slug([{"slug": "acted", "source": "human", "ids": ["t1", "t2", "t3"]},
                               {"slug": "noise", "source": "bot", "ids": ["t5", "t6", "t7"]}])
        self.assertFalse(themes["acted"]["mostlyIgnored"])
        self.assertTrue(themes["noise"]["mostlyIgnored"])

    def test_rates_a_ci_theme_per_100_sampled_runs_and_counts_its_flaky_runs(self):
        flake = self.by_slug([{"slug": "flake", "source": "ci", "ids": ["r3"]}])["flake"]
        self.assertEqual((flake["count"], flake["flaky"], flake["rate"]), (1, 1, 33.3))

    def test_marks_whether_each_theme_meets_the_floor(self):
        themes = self.by_slug([{"slug": "one", "source": "human", "ids": ["t1"]},
                               {"slug": "two", "source": "human", "ids": ["t1", "t2"]}])
        self.assertEqual((themes["one"]["floor"], themes["two"]["floor"]), (False, True))

    def test_marks_every_theme_baseline_with_no_last_run(self):
        result = self.result([{"slug": "guard", "source": "human", "ids": ["t1"]}])
        self.assertEqual((result["themes"][0]["trend"], result["dropped"]), ("baseline", []))

    def test_marks_every_theme_baseline_when_the_last_run_file_is_missing(self):
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)
        draft = os.path.join(folder, "draft.json")
        with open(draft, "w") as f:
            json.dump([{"slug": "guard", "source": "human", "ids": ["t1"]}], f)
        result = subprocess.run(["python3", SCRIPT, "themes", "--cache", self.cache, "--draft", draft,
                                 "--prior", os.path.join(folder, "none.json")], capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)["themes"][0]["trend"], "baseline")

    def test_compares_each_slug_with_the_rate_of_the_last_run(self):
        prior = {"window": "x", "themes": [{"slug": "up", "source": "human", "rate": 10.0},
                                           {"slug": "down", "source": "human", "rate": 90.0},
                                           {"slug": "same", "source": "human", "rate": 50.0},
                                           {"slug": "gone", "source": "bot", "rate": 5.0}]}
        result = self.result([{"slug": "up", "source": "human", "ids": ["t1"]},
                              {"slug": "down", "source": "human", "ids": ["t1", "t2"]},
                              {"slug": "same", "source": "human", "ids": ["t1", "t2"]},
                              {"slug": "fresh", "source": "human", "ids": ["t3"]}], prior)
        self.assertEqual({t["slug"]: t["trend"] for t in result["themes"]},
                         {"up": "rising", "down": "declining", "same": "steady", "fresh": "new"})
        self.assertEqual([t["slug"] for t in result["dropped"]], ["gone"])

    def test_writes_to_the_cache_what_it_prints(self):
        result = self.result([{"slug": "guard", "source": "human", "ids": ["t1"]}])
        self.assertEqual(json.loads(self.read("themes.json")), result)

    def test_stops_and_names_an_id_that_the_cache_does_not_hold(self):
        result = self.themes([{"slug": "guard", "source": "human", "ids": ["t1", "t99"]}])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("t99", result.stderr)


if __name__ == "__main__":
    unittest.main()
