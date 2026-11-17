#!/usr/bin/env python3
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

    def render(self, payload):
        env = {
            **os.environ,
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


if __name__ == "__main__":
    unittest.main()
