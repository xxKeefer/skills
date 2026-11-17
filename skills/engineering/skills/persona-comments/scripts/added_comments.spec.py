#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "added_comments.py")


def diff(path, lines, start=1):
    head = "diff --git a/%s b/%s\n--- a/%s\n+++ b/%s\n@@ -0,0 +%d,%d @@\n" % (
        path, path, path, path, start, len(lines))
    return head + "".join(l + "\n" for l in lines)


def run(text, *args):
    p = subprocess.run([sys.executable, SCRIPT, *args], input=text, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class Languages(unittest.TestCase):
    def test_hash_comment_lists_with_new_file_line(self):
        for ext in ("py", "sh"):
            text = "--- a/a.%s\n+++ b/a.%s\n@@ -1,1 +1,3 @@\n keep\n+x = 1\n+# why\n" % (ext, ext)
            code, out, err = run(text)
            self.assertEqual(code, 0, err)
            self.assertEqual(out, "a.%s:3: # why\n" % ext)

    def test_slash_comment_in_ts(self):
        text = "+++ b/a.ts\n@@ -0,0 +1,2 @@\n+const a = 1\n+// why\n"
        self.assertEqual(run(text)[1], "a.ts:2: // why\n")

    def test_block_comment_over_lines(self):
        text = "+++ b/a.ts\n@@ -0,0 +1,4 @@\n+/* first\n+ second\n+ third */\n+const a = 1\n"
        self.assertEqual(
            run(text)[1],
            "a.ts:1: /* first\na.ts:2: second\na.ts:3: third */\n",
        )

    def test_html_comment_in_vue(self):
        text = "+++ b/a.vue\n@@ -0,0 +1,1 @@\n+<div><!-- why --></div>\n"
        self.assertEqual(run(text)[1], "a.vue:1: <!-- why -->\n")

    def test_dash_comment_in_sql(self):
        text = "+++ b/a.sql\n@@ -0,0 +1,1 @@\n+select 1 -- why\n"
        self.assertEqual(run(text)[1], "a.sql:1: -- why\n")


class Skips(unittest.TestCase):
    def test_removed_and_context_lines_give_no_output(self):
        text = "+++ b/a.py\n@@ -1,3 +1,2 @@\n # kept\n-# gone\n+x = 1\n"
        self.assertEqual(run(text), (0, "", ""))

    def test_unknown_extension_gives_no_output(self):
        text = "+++ b/a.txt\n@@ -0,0 +1,1 @@\n+# note\n"
        self.assertEqual(run(text), (0, "", ""))

    def test_shebang_on_line_one_is_skipped(self):
        text = "+++ b/a.sh\n@@ -0,0 +1,2 @@\n+#!/bin/sh\n+# why\n"
        self.assertEqual(run(text)[1], "a.sh:2: # why\n")

    def test_marker_inside_a_string_is_skipped(self):
        text = '+++ b/a.ts\n@@ -0,0 +1,2 @@\n+const u = "http://x.test"\n+const s = `a // b`\n'
        self.assertEqual(run(text), (0, "", ""))
        text = '+++ b/a.py\n@@ -0,0 +1,1 @@\n+s = "a # b"\n'
        self.assertEqual(run(text), (0, "", ""))

    def test_trailing_comment_after_code_is_listed(self):
        text = "+++ b/a.py\n@@ -0,0 +1,1 @@\n+x = 1  # why\n"
        self.assertEqual(run(text)[1], "a.py:1: # why\n")

    def test_string_then_trailing_comment(self):
        text = '+++ b/a.ts\n@@ -0,0 +1,1 @@\n+const u = "http://x" // why\n'
        self.assertEqual(run(text)[1], "a.ts:1: // why\n")

    def test_lone_quote_does_not_hide_a_trailing_comment(self):
        text = "+++ b/a.rs\n@@ -0,0 +1,1 @@\n+fn f<'a>(x: &'a str) -> &'a str { x } // why\n"
        self.assertEqual(run(text)[1], "a.rs:1: // why\n")
        text = "+++ b/a.sh\n@@ -0,0 +1,1 @@\n+echo don't # why\n"
        self.assertEqual(run(text)[1], "a.sh:1: # why\n")

    def test_apostrophe_in_the_comment_does_not_hide_it(self):
        text = "+++ b/a.rs\n@@ -0,0 +1,1 @@\n+fn f(x: &'a str) {} // don't do this\n"
        self.assertEqual(run(text)[1], "a.rs:1: // don't do this\n")
        text = "+++ b/a.sh\n@@ -0,0 +1,1 @@\n+echo it's # don't\n"
        self.assertEqual(run(text)[1], "a.sh:1: # don't\n")

    def test_single_quote_never_opens_a_string(self):
        text = "+++ b/a.ts\n@@ -0,0 +1,1 @@\n+const s = 'a // b'\n"
        self.assertEqual(run(text)[1], "a.ts:1: // b'\n")

    def test_escaped_quote_keeps_the_string_open(self):
        text = '+++ b/a.py\n@@ -0,0 +1,1 @@\n+s = "a\\" # b"\n'
        self.assertEqual(run(text), (0, "", ""))

    def test_unclosed_double_quote_or_backtick_does_not_hide_a_comment(self):
        text = "+++ b/a.ts\n@@ -0,0 +1,1 @@\n+x = `a // why\n"
        self.assertEqual(run(text)[1], "a.ts:1: // why\n")
        text = '+++ b/a.sh\n@@ -0,0 +1,1 @@\n+echo 5" # why\n'
        self.assertEqual(run(text)[1], "a.sh:1: # why\n")

    def test_hash_inside_a_shell_word_is_skipped(self):
        text = "+++ b/a.sh\n@@ -0,0 +1,2 @@\n+echo $#\n+n=${#arr[@]}\n"
        self.assertEqual(run(text), (0, "", ""))


class Paths(unittest.TestCase):
    def test_quoted_non_ascii_path_is_decoded_and_scanned(self):
        text = '+++ "b/caf\\303\\251.py"\n@@ -0,0 +1,1 @@\n+# why\n'
        self.assertEqual(run(text)[1], "caf\u00e9.py:1: # why\n")

    def test_quoted_path_with_a_quote_or_tab_escape(self):
        text = '+++ "b/a\\"b\\t.py"\n@@ -0,0 +1,1 @@\n+# why\n'
        self.assertEqual(run(text)[1], 'a"b\t.py:1: # why\n')


class Hunks(unittest.TestCase):
    def test_removed_line_does_not_move_the_line_number(self):
        text = "+++ b/a.py\n@@ -1,2 +1,2 @@\n keep\n-old\n+# why\n"
        self.assertEqual(run(text)[1], "a.py:2: # why\n")

    def test_new_hunk_resets_the_line_and_an_open_block(self):
        text = "+++ b/a.ts\n@@ -0,0 +1,1 @@\n+/* open\n@@ -10,0 +20,1 @@\n+const a = 1\n"
        self.assertEqual(run(text)[1], "a.ts:1: /* open\n")

    def test_no_newline_marker_does_not_move_the_line_number(self):
        text = "+++ b/a.py\n@@ -1,1 +1,2 @@\n-old\n\\ No newline at end of file\n+x = 1\n+# why\n"
        self.assertEqual(run(text)[1], "a.py:2: # why\n")

    def test_each_file_gets_its_own_line_numbers(self):
        text = (
            "+++ b/a.py\n@@ -0,0 +1,2 @@\n+x = 1\n+# one\n"
            "+++ b/b.py\n@@ -0,0 +5,1 @@\n+# two\n"
        )
        self.assertEqual(run(text)[1], "a.py:2: # one\nb.py:5: # two\n")


class Input(unittest.TestCase):
    def test_empty_diff_exits_zero_with_no_output(self):
        self.assertEqual(run(""), (0, "", ""))

    def test_diff_with_no_comment_exits_zero_with_no_output(self):
        self.assertEqual(run(diff("a.py", ["x = 1"])), (0, "", ""))

    def test_reads_a_path_argument(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        p = os.path.join(d, "x.diff")
        with open(p, "w") as f:
            f.write("+++ b/a.py\n@@ -0,0 +1,1 @@\n+# why\n")
        self.assertEqual(run("", p)[1], "a.py:1: # why\n")


if __name__ == "__main__":
    unittest.main()
