#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "rerun_findings.py")


def finding(**kw):
    base = {"adversary": "opus", "title": "T", "command": "echo boom; exit 1", "evidence": "boom"}
    base.update(kw)
    return base


class RerunFindings(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)

    def run_script(self, findings, *args):
        path = os.path.join(self.dir, "findings.json")
        with open(path, "w") as f:
            f.write(findings if isinstance(findings, str) else json.dumps(findings))
        return subprocess.run(
            ["python3", SCRIPT, path, *args],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def result(self, findings, *args):
        r = self.run_script(findings, *args)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def reason(self, f, *args):
        out = self.result([f], *args)
        self.assertEqual(out["kept"], [])
        return out["dropped"][0]["reason"]

    def test_failing_command_with_evidence_is_kept_with_output_and_exit(self):
        out = self.result([finding(cwd=self.dir)])
        self.assertEqual(out["dropped"], [])
        kept = out["kept"][0]
        self.assertEqual(kept["title"], "T")
        self.assertEqual(kept["adversary"], "opus")
        self.assertEqual(kept["exit"], 1)
        self.assertIn("boom", kept["output"])

    def test_evidence_on_stderr_counts(self):
        out = self.result([finding(command="echo boom >&2; exit 3")])
        self.assertEqual(out["kept"][0]["exit"], 3)

    def test_command_runs_in_its_cwd(self):
        with open(os.path.join(self.dir, "marker.txt"), "w") as f:
            f.write("marker-content\n")
        out = self.result([finding(command="cat marker.txt; exit 1", evidence="marker-content", cwd=self.dir)])
        self.assertEqual(len(out["kept"]), 1)

    def test_passing_command_is_dropped(self):
        self.assertEqual(self.reason(finding(command="echo boom")), "passed on re-run")

    def test_failure_without_evidence_is_dropped(self):
        self.assertEqual(self.reason(finding(command="echo other; exit 1")), "evidence not in output")

    def test_missing_command_is_dropped(self):
        f = finding()
        del f["command"]
        self.assertEqual(self.reason(f), "no command")

    def test_blank_command_is_dropped(self):
        self.assertEqual(self.reason(finding(command="  ")), "no command")

    def test_missing_evidence_is_dropped(self):
        self.assertEqual(self.reason(finding(evidence="")), "no evidence")

    def test_blank_evidence_is_dropped(self):
        self.assertEqual(self.reason(finding(evidence="  ")), "no evidence")

    def test_command_that_cannot_start_is_dropped_and_the_rest_still_run(self):
        out = self.result([finding(title="bad", command="echo a\u0000b; exit 1"), finding(title="good")])
        self.assertEqual([k["title"] for k in out["kept"]], ["good"])
        self.assertEqual([(d["title"], d["reason"]) for d in out["dropped"]], [("bad", "cannot run")])

    def test_command_over_timeout_is_dropped(self):
        self.assertEqual(self.reason(finding(command="sleep 5; echo boom; exit 1"), "--timeout", "1"), "timed out")

    def test_missing_cwd_folder_is_dropped(self):
        f = finding(cwd=os.path.join(self.dir, "gone"))
        self.assertEqual(self.reason(f), "cwd not found")

    def test_mixed_findings_keep_order_and_split(self):
        out = self.result([finding(title="a"), finding(title="b", command="true"), finding(title="c")])
        self.assertEqual([k["title"] for k in out["kept"]], ["a", "c"])
        self.assertEqual([d["title"] for d in out["dropped"]], ["b"])

    def test_output_that_is_not_utf8_is_still_checked(self):
        out = self.result([finding(command="printf '\\xff boom\\n'; exit 1")])
        self.assertEqual(len(out["kept"]), 1)

    def test_command_that_is_not_text_is_dropped(self):
        self.assertEqual(self.reason(finding(command=["pytest"])), "no command")

    def test_evidence_that_is_not_text_is_dropped(self):
        self.assertEqual(self.reason(finding(evidence=1)), "no evidence")

    def test_timeout_kills_the_child_processes_of_the_shell(self):
        start = time.monotonic()
        self.assertEqual(self.reason(finding(command="sleep 30; echo boom; exit 1"), "--timeout", "1"), "timed out")
        self.assertLess(time.monotonic() - start, 10)

    def test_cwd_that_is_not_text_is_dropped(self):
        self.assertEqual(self.reason(finding(cwd=["a"])), "cwd not found")

    def test_missing_findings_file_exits_1_with_one_line(self):
        r = subprocess.run(["python3", SCRIPT, os.path.join(self.dir, "gone.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(len(r.stdout.strip().splitlines()), 1, r.stdout)
        self.assertIn("cannot read", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_malformed_json_exits_1_with_one_line(self):
        r = self.run_script("{not json")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(len(r.stdout.strip().splitlines()), 1, r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_non_list_exits_1(self):
        r = self.run_script({"title": "T"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("list", r.stdout)

    def test_non_object_finding_exits_1(self):
        r = self.run_script(["text"])
        self.assertEqual(r.returncode, 1)
        self.assertIn("finding 1", r.stdout)


class PlantedBug(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)
        files = {
            "calc.py": "def add(a, b):\n    return a - b\n",
            "test_calc.py": (
                "import unittest\n"
                "from calc import add\n\n"
                "class TestAdd(unittest.TestCase):\n"
                "    def test_adds(self):\n"
                "        self.assertEqual(add(2, 3), 5)\n\n"
                "    def test_zero(self):\n"
                "        self.assertEqual(add(0, 0), 0)\n"
            ),
        }
        for name, text in files.items():
            with open(os.path.join(self.repo, name), "w") as f:
                f.write(text)
        git = ["git", "-C", self.repo, "-c", "user.name=t", "-c", "user.email=t@example.com"]
        subprocess.run(git + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "."], check=True)
        subprocess.run(git + ["commit", "-q", "-m", "planted bug"], check=True)

    def test_proven_finding_is_kept_and_unproven_one_is_dropped(self):
        findings = [
            finding(title="add subtracts", cwd=self.repo, evidence="AssertionError: -1 != 5",
                    command="python3 -m unittest test_calc.TestAdd.test_adds"),
            finding(adversary="sonnet", title="add breaks on zero", cwd=self.repo, evidence="AssertionError",
                    command="python3 -m unittest test_calc.TestAdd.test_zero"),
        ]
        path = os.path.join(self.repo, "findings.json")
        with open(path, "w") as f:
            json.dump(findings, f)
        r = subprocess.run(
            ["python3", SCRIPT, path],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual([k["title"] for k in out["kept"]], ["add subtracts"])
        self.assertEqual([(d["title"], d["reason"]) for d in out["dropped"]],
                         [("add breaks on zero", "passed on re-run")])


if __name__ == "__main__":
    unittest.main()
