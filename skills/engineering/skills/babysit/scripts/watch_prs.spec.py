#!/usr/bin/env python3
import importlib.util
import json
import os
import stat
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "watch_prs.py")
spec = importlib.util.spec_from_file_location("watch_prs", SCRIPT)
watch_prs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watch_prs)

FAKE_GH = """#!/usr/bin/env python3
import os, sys
d = os.environ["FAKE_DIR"]
a = sys.argv[1:]
with open(os.path.join(d, "calls"), "a") as f:
    f.write(" ".join(a) + "\\n")
hook = os.path.join(d, "hook" if a[2:3] == ["1"] else "hook_" + a[2]) if a[0] == "pr" else ""
if hook and os.path.exists(hook):
    cmd = open(hook).read()
    os.remove(hook)
    os.system(cmd)
if a[0] == "pr":
    print(open(os.path.join(d, "pr_%s.json" % a[2])).read())
else:
    n = [x for x in a if x.startswith("number=")][0].split("=")[1]
    print(open(os.path.join(d, "threads_%s.json" % n)).read())
"""

NOTIFIER = '#!/bin/sh\necho "$1|$2" >> "$FAKE_DIR/alerts"\n'


def view(state="OPEN", head="a", base="main", merge="CLEAN", review="", checks=None):
    return {"state": state, "headRefName": head, "baseRefName": base, "mergeStateStatus": merge,
            "reviewDecision": review, "statusCheckRollup": checks if checks is not None else []}


def done_check(conclusion="SUCCESS"):
    return {"status": "COMPLETED", "conclusion": conclusion}


class Classify(unittest.TestCase):
    def test_table(self):
        cases = [
            (view(state="MERGED", checks=[done_check("FAILURE")]), 3, "done"),
            (view(state="CLOSED"), 0, "done"),
            (view(checks=[done_check("FAILURE")]), 2, "failed"),
            (view(merge="BEHIND"), 2, "stale"),
            (view(merge="DIRTY"), 0, "stale"),
            (view(checks=[done_check()]), 1, "threads"),
            (view(checks=[{"status": "IN_PROGRESS", "conclusion": ""}]), 0, "pending"),
            (view(checks=[done_check()], review="APPROVED"), 0, "ready"),
            (view(checks=[done_check()], review=""), 0, "ready"),
            (view(checks=[done_check()], review="REVIEW_REQUIRED"), 0, "pending"),
            (view(checks=[{"state": "ERROR"}]), 0, "failed"),
            (view(checks=[{"state": "PENDING"}]), 0, "pending"),
        ]
        for v, threads, want in cases:
            self.assertEqual(watch_prs.classify(v, threads), want, (v, threads))


class Env(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.home = os.path.join(t, "home")
        self.fake = os.path.join(t, "fake")
        bin_dir = os.path.join(t, "bin")
        for d in (self.home, self.fake, bin_dir, os.path.join(self.home, ".claude")):
            os.makedirs(d)
        for name, body in (("gh", FAKE_GH), ("notify", NOTIFIER)):
            p = os.path.join(bin_dir, name)
            with open(p, "w") as f:
                f.write(body)
            os.chmod(p, os.stat(p).st_mode | stat.S_IXUSR)
        self.notify = os.path.join(bin_dir, "notify")
        self.env = {**os.environ, "HOME": self.home, "FAKE_DIR": self.fake,
                    "PATH": bin_dir + os.pathsep + os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}
        self.set_notifier(self.notify)

    def tearDown(self):
        self.tmp.cleanup()

    def set_notifier(self, cmd):
        with open(os.path.join(self.home, ".claude", "agents-md.values.json"), "w") as f:
            json.dump({"notifier_command": cmd} if cmd is not None else {}, f)

    def pr(self, number, threads=0, **kw):
        with open(os.path.join(self.fake, "pr_%d.json" % number), "w") as f:
            json.dump(view(**kw), f)
        nodes = [{"isResolved": False}] * threads + [{"isResolved": True}]
        with open(os.path.join(self.fake, "threads_%d.json" % number), "w") as f:
            json.dump({"data": {"repository": {"pullRequest": {"reviewThreads": {"nodes": nodes}}}}}, f)

    def cli(self, *args):
        return subprocess.run(["python3", SCRIPT, *args], capture_output=True, text=True,
                              env=self.env, timeout=30)

    def state(self):
        with open(os.path.join(self.home, ".cache", "babysit", "state.json")) as f:
            return json.load(f)

    def read(self, name):
        try:
            with open(os.path.join(self.fake, name)) as f:
                return f.read().splitlines()
        except FileNotFoundError:
            return []


class Alerts(Env):
    def test_alert_only_on_change(self):
        self.pr(1, checks=[{"status": "IN_PROGRESS", "conclusion": ""}])
        self.cli("add", "o/r", "1")
        self.cli("poll")
        self.assertEqual(self.state()[0]["state"], "pending")
        self.assertEqual(self.read("alerts"), [])
        self.cli("poll")
        self.assertEqual(self.read("alerts"), [])
        self.pr(1, checks=[done_check("FAILURE")])
        self.cli("poll")
        self.assertEqual(self.read("alerts"), ["babysit|o/r#1 is failed"])
        self.cli("poll")
        self.assertEqual(len(self.read("alerts")), 1)
        self.assertEqual(self.state()[0]["state"], "failed")

    def test_notifier_none_or_absent(self):
        for cmd in ("none", None):
            self.set_notifier(cmd)
            self.pr(1, checks=[{"status": "IN_PROGRESS", "conclusion": ""}])
            self.cli("add", "o/r", "1")
            self.cli("poll")
            self.pr(1, checks=[done_check("FAILURE")])
            r = self.cli("poll")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(self.read("alerts"), [])
            os.remove(os.path.join(self.home, ".cache", "babysit", "state.json"))


class Concurrent(Env):
    def test_add_during_poll_is_kept(self):
        self.pr(1)
        self.pr(2)
        self.cli("add", "o/r", "1")
        with open(os.path.join(self.fake, "hook"), "w") as f:
            f.write("python3 %s add o/r 2" % SCRIPT)
        self.cli("poll")
        self.assertEqual([p["number"] for p in self.state()], [1, 2])


    def test_poll_during_add_is_kept(self):
        self.pr(1, checks=[{"status": "IN_PROGRESS", "conclusion": ""}])
        self.pr(2)
        self.cli("add", "o/r", "1")
        with open(os.path.join(self.fake, "hook_2"), "w") as f:
            f.write("python3 %s poll" % SCRIPT)
        self.cli("add", "o/r", "2")
        self.assertEqual([p["state"] for p in self.state()], ["pending", None])


class GhFailure(Env):
    def test_failed_gh_call_skips_that_pr_only(self):
        self.pr(1, checks=[{"status": "IN_PROGRESS", "conclusion": ""}])
        self.pr(2)
        self.cli("add", "o/r", "1")
        self.cli("add", "o/r", "2")
        os.remove(os.path.join(self.fake, "pr_2.json"))
        r = self.cli("poll")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([p["state"] for p in self.state()], ["pending", None])


class Stack(Env):
    def test_polls_lowest_only(self):
        self.pr(1, head="a", base="main")
        self.pr(2, head="b", base="a")
        self.cli("add", "o/r", "1")
        self.cli("add", "o/r", "2")
        open(os.path.join(self.fake, "calls"), "w").close()
        self.cli("poll")
        polled = [c for c in self.read("calls") if c.startswith("pr view")]
        self.assertEqual(len(polled), 1)
        self.assertIn("pr view 1 ", polled[0])
        self.pr(1, state="MERGED", head="a", base="main")
        self.cli("poll")
        open(os.path.join(self.fake, "calls"), "w").close()
        self.cli("poll")
        polled = [c for c in self.read("calls") if c.startswith("pr view")]
        self.assertEqual(len(polled), 1)
        self.assertIn("pr view 2 ", polled[0])


class Run(Env):
    def test_exits_when_none_open(self):
        self.pr(1, state="MERGED")
        self.cli("add", "o/r", "1")
        r = self.cli("run", "--interval", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state()[0]["state"], "done")
        self.assertFalse(os.path.exists(os.path.join(self.home, ".cache", "babysit", "run.pid")))

    def test_second_run_exits_at_once(self):
        self.pr(1)
        self.cli("add", "o/r", "1")
        open(os.path.join(self.fake, "calls"), "w").close()
        with open(os.path.join(self.home, ".cache", "babysit", "run.pid"), "w") as f:
            f.write(str(os.getpid()))
        r = self.cli("run", "--interval", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.read("calls"), [])


if __name__ == "__main__":
    unittest.main()
