#!/usr/bin/env python3
import json
import os
import re
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "statusline.sh")
FIX = os.path.join(HERE, "fixtures")


def fixture(name):
    with open(os.path.join(FIX, name), "rb") as f:
        return f.read()


class Env:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        self.cache = os.path.join(self.tmp.name, "cache")
        self.bin = os.path.join(self.tmp.name, "bin")
        os.makedirs(os.path.join(self.home, "p", "sub"))
        os.makedirs(self.bin)
        with open(os.path.join(self.bin, "date"), "wb") as f:
            f.write(fixture("fake_date"))
        os.chmod(os.path.join(self.bin, "date"), 0o755)

    def watch(self, entries):
        d = os.path.join(self.home, ".cache", "babysit")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "state.json"), "w") as f:
            json.dump(entries, f)

    def set_now(self, n):
        path = os.path.join(self.bin, "date")
        with open(path, "w") as f:
            f.write("#!/bin/sh\necho %d\n" % n)

    def render(self, payload, columns=None):
        env = {
            **os.environ,
            **({"COLUMNS": str(columns)} if columns else {}),
            "HOME": self.home,
            "XDG_CACHE_HOME": self.cache,
            "PATH": self.bin + os.pathsep + os.environ["PATH"],
        }
        return subprocess.run(
            ["bash", SCRIPT],
            input=payload.replace(b"@HOME@", self.home.encode()),
            capture_output=True,
            env=env,
            timeout=30,
        ).stdout


ANSI = re.compile(r"\x1b\[[0-9;]*m")


def transcript_line(tokens):
    return '{"message":{"usage":{"input_tokens":%d}}}\n' % tokens


def has_tokens(out, n):
    digits = str(n)
    pattern = digits[:-3] + ",?" + digits[-3:]
    return re.search(pattern.encode(), out) is not None


class Spec(unittest.TestCase):
    def setUp(self):
        self.env = Env()
        self.addCleanup(self.env.tmp.cleanup)

    def test_c1_full_payload_is_byte_equal(self):
        out = self.env.render(fixture("payload_full.json"))
        self.assertEqual(out, fixture("expected_full.out"))

    def test_c1_bare_payload_is_byte_equal(self):
        out = self.env.render(fixture("payload_bare.json"))
        self.assertEqual(out, fixture("expected_bare.out"))

    def test_c2_token_cache(self):
        path = os.path.join(self.env.tmp.name, "t.jsonl")
        payload = (
            b'{"cwd":"@HOME@","transcript_path":"'
            + path.encode()
            + b'","model":{"id":"claude-sonnet-4-6"}}'
        )
        with open(path, "w") as f:
            f.write(transcript_line(1111))
        self.assertTrue(has_tokens(self.env.render(payload), 1111))
        with open(path, "w") as f:
            f.write(transcript_line(2222))
        self.assertEqual(os.path.getsize(path), len(transcript_line(1111)))
        self.assertTrue(has_tokens(self.env.render(payload), 1111))
        with open(path, "w") as f:
            f.write(transcript_line(3333) + transcript_line(4444))
        self.assertTrue(has_tokens(self.env.render(payload), 4444))

    def test_token_cache_stays_bounded(self):
        path = os.path.join(self.env.tmp.name, "t.jsonl")
        payload = (
            b'{"cwd":"@HOME@","transcript_path":"'
            + path.encode()
            + b'","model":{"id":"claude-sonnet-4-6"}}'
        )
        cache_dir = os.path.join(self.env.cache, "statusline")
        os.makedirs(cache_dir)
        with open(os.path.join(cache_dir, "tokens"), "w") as f:
            for i in range(300):
                f.write("/old/%d\t10\t5\n" % i)
        with open(path, "w") as f:
            f.write(transcript_line(1111))
        self.assertTrue(has_tokens(self.env.render(payload), 1111))
        with open(os.path.join(cache_dir, "tokens")) as f:
            lines = f.read().splitlines()
        self.assertLessEqual(len(lines), 50)
        self.assertTrue(lines[-1].startswith(path + "\t"))

    def chips(self, entries, columns, now=1700000000):
        self.env.set_now(now)
        self.env.watch(entries)
        out = self.env.render(fixture("payload_bare.json"), columns).decode()
        return out.split("\n")[0]

    def test_c8_order_and_width(self):
        states = ["done", "ready", "pending", "threads", "stale", "failed"]
        entries = [
            {"number": 100 + i, "state": st, "threads": 2, "done_at": 1699999999}
            for i, st in enumerate(states)
        ]
        line = self.chips(entries, 100)
        plain = ANSI.sub("", line)
        self.assertEqual(len(plain), 100)
        order = [plain.index(n) for n in ("105", "104", "103", "102", "101", "100")]
        self.assertEqual(order, sorted(order))
        self.assertIn("\033[97;41m \u00d7 105 \033[0m", line)
        self.assertIn(" \u25c62 103 ", plain)

    def test_c9_done_expiry(self):
        e = lambda at: [{"number": 7, "state": "done", "threads": 0, "done_at": at}]
        self.assertIn("7", ANSI.sub("", self.chips(e(1700000000 - 600), 80)).split("\u00b7")[-1][-12:])
        self.assertNotIn(" 7 ", ANSI.sub("", self.chips(e(1700000000 - 601), 80)))

    def test_c10_pin_and_ticker(self):
        entries = [{"number": 200 + i, "state": "pending", "threads": 0} for i in range(8)]
        entries += [{"number": 1, "state": "failed", "threads": 0}]
        a = ANSI.sub("", self.chips(entries, 40, 1700000000))
        b = ANSI.sub("", self.chips(entries, 40, 1700000001))
        for line in (a, b):
            self.assertEqual(len(line), 40)
            self.assertIn(" \u00d7 1 ", line)
        window = lambda l: l[l.index(" \u00d7 1 ") + 7:]
        self.assertEqual(window(a)[1:], window(b)[:-1])
        self.assertNotEqual(a, b)

    def test_c11_no_state_file_unchanged(self):
        out = self.env.render(fixture("payload_bare.json"))
        self.assertEqual(out, fixture("expected_bare.out"))


if __name__ == "__main__":
    unittest.main()
