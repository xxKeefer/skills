#!/usr/bin/env python3
"""Run: python3 leak_check.spec.py"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leak_check.py")


class Env:
    def __init__(self, tc, paths, prompt="Add a retry to the upload client.\n"):
        self.dir = tempfile.mkdtemp()
        tc.addCleanup(lambda: shutil.rmtree(self.dir, ignore_errors=True))
        self.folder = os.path.join(self.dir, "folder")
        for p in paths:
            full = os.path.join(self.folder, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").close()
        os.makedirs(self.folder, exist_ok=True)
        self.prompt = os.path.join(self.dir, "prompt.txt")
        with open(self.prompt, "w") as f:
            f.write(prompt)

    def run(self):
        p = subprocess.run(
            [sys.executable, SCRIPT, self.folder, self.prompt],
            capture_output=True, text=True,
        )
        return p.returncode, p.stdout


class PathWords(unittest.TestCase):
    def test_lists_a_banned_word_in_a_file_name_with_its_path(self):
        code, out = Env(self, ["src/eval_runner.py"]).run()
        self.assertEqual(code, 1)
        self.assertIn("src/eval_runner.py: eval", out)

    def test_lists_a_banned_word_in_a_folder_name_split_by_each_separator(self):
        for name in ["benchmark-app", "arena.core", "judge app", "test/x"]:
            with self.subTest(name=name):
                code, out = Env(self, [name + "/f.txt"]).run()
                self.assertEqual(code, 1)
                self.assertIn(name.split("/")[0].split("-")[0].split(".")[0].split(" ")[0], out)


class PromptWords(unittest.TestCase):
    def test_lists_a_banned_word_in_the_prompt_in_any_case(self):
        code, out = Env(self, [], "Please TEST the parser.\n").run()
        self.assertEqual(code, 1)
        self.assertIn("prompt: test", out)

    def test_lists_a_plural_of_a_banned_word(self):
        code, out = Env(self, [], "Write some tests for it.\n").run()
        self.assertEqual(code, 1)
        self.assertIn("prompt: test", out)


class WholeWordsOnly(unittest.TestCase):
    def test_a_word_inside_another_word_is_not_listed(self):
        code, out = Env(self, ["contest/evaluate.py"], "Rework the latest scoreboard.\n").run()
        self.assertEqual(code, 0)
        self.assertEqual(out, "")


class CleanInput(unittest.TestCase):
    def test_clean_names_and_prompt_exit_0_with_no_output(self):
        code, out = Env(self, ["src/upload_client.py", "README.md"]).run()
        self.assertEqual(code, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
