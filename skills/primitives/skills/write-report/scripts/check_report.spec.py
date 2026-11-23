#!/usr/bin/env python3
"""Tests for check_report.py. Run: python3 check_report.spec.py"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check_report.py")
WRITE = os.path.join(HERE, "write_report.py")
BLOCK = re.compile(r'(<script type="application/json" id="runs">)(.*?)(</script>)', re.S)
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def check(path):
    return subprocess.run(["python3", CHECK, path], capture_output=True, text=True, env=ENV)


def write(report, payload, folder):
    source = os.path.join(folder, "payload.json")
    with open(source, "w") as f:
        json.dump(payload, f)
    subprocess.run(["python3", WRITE, report, source], capture_output=True, text=True, env=ENV, check=True)


def payload(title="Run"):
    return {
        "title": "Report",
        "skill": "/x",
        "run": {
            "title": title,
            "answer": "Tick the rows.",
            "visuals": [{"question": "How many rows are open?", "bars": [["open", 2]]}],
            "columns": [{"key": "issue", "label": "Issue"}],
            "rows": [
                {"ticks": ["reply"], "cells": {"issue": "one"}},
                {"cells": {"issue": "two"}},
            ],
        },
    }


class CheckReport(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "report_x.html")
        write(self.path, payload("first"), self.dir)
        write(self.path, payload("second"), self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def data(self):
        with open(self.path, encoding="utf-8") as f:
            return json.loads(BLOCK.search(f.read()).group(2))

    def save(self, data):
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        body = json.dumps(data)
        text = BLOCK.sub(lambda m: m.group(1) + body + m.group(3), text, count=1)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def fails(self, fragment):
        result = check(self.path)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(fragment, result.stdout)
        self.assertIn("Fix:", result.stdout)
        self.assertIn(self.path + ":", result.stdout)

    def test_written_report_passes(self):
        result = check(self.path)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.strip(), "ok")

    def test_block_errors(self):
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(BLOCK.sub(lambda m: m.group(1) + "{bad" + m.group(3), text, count=1))
        self.fails("does not parse")
        self.save({"title": "t", "path": "p", "runs": []})
        self.fails("skill")
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("<html></html>")
        self.fails("no runs block")

    def test_shape_errors(self):
        data = self.data()
        data["runs"][0]["rows"][1]["id"] = data["runs"][0]["rows"][0]["id"]
        self.save(data)
        self.fails("duplicate row id")

        data = self.data()
        data["runs"][0]["run"] = 0
        self.save(data)
        self.fails("run numbers")

        data = self.data()
        del data["runs"][0]["columns"]
        self.save(data)
        self.fails("columns")

        data = self.data()
        del data["runs"][0]["rows"][0]["cells"]
        self.save(data)
        self.fails("cells")

        data = self.data()
        data["runs"][0]["rows"][0]["ticks"] = "reply"
        self.save(data)
        self.fails("bad `ticks`")

        data = self.data()
        del data["runs"][0]["visuals"]
        self.save(data)
        self.fails("no visual")

        data = self.data()
        data["runs"][0]["visuals"] = [{"question": "q", "fold": True, "bars": [["open", 2]]}]
        self.save(data)
        self.fails("no visual")

        data = self.data()
        data["runs"][0]["rows"] = 5
        self.save(data)
        self.fails("`rows` is not a list")


if __name__ == "__main__":
    unittest.main()
