#!/usr/bin/env python3
"""Run: python3 zsh_insights.spec.py"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

os.environ["TZ"] = "UTC"
time.tzset()

import zsh_insights as zi  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zsh_insights.py")
DAY = 86400
NOW = 1_800_000_000


def hist(*entries):
    """Builds extended-history bytes from (seconds ago, command) pairs."""
    return "".join(f": {NOW - ago}:0;{cmd}\n" for ago, cmd in entries).encode()


def entries(*pairs):
    return zi.parse_history(hist(*pairs))


class ParseHistory(unittest.TestCase):
    def test_reads_timestamp_and_command_from_extended_format(self):
        self.assertEqual(zi.parse_history(b": 100:0;git status\n: 200:3;ls -la\n"),
                         [(100, "git status"), (200, "ls -la")])

    def test_joins_a_continued_line_into_one_command(self):
        data = b": 100:0;echo one \\\ntwo\n: 200:0;ls\n"
        self.assertEqual(zi.parse_history(data), [(100, "echo one \ntwo"), (200, "ls")])

    def test_decodes_metafied_bytes(self):
        # zsh writes the byte 0x86 as 0x83 0xa6, and 0x92 as 0x83 0xb2.
        data = b": 100:0;echo \xe2\x83\xa6\x83\xb2\n"
        self.assertEqual(zi.parse_history(data), [(100, "echo \u2192")])

    def test_reads_plain_format_without_timestamps(self):
        self.assertEqual(zi.parse_history(b"git status\nls\n"), [(None, "git status"), (None, "ls")])

    def test_skips_blank_commands(self):
        self.assertEqual(zi.parse_history(b": 100:0;   \n: 200:0;ls\n"), [(200, "ls")])


class ParseAliases(unittest.TestCase):
    def test_reads_plain_and_quoted_definitions(self):
        text = "g=git\ngst='git status'\n-='cd -'\nsay='echo it'\\''s'\n"
        self.assertEqual(zi.parse_aliases(text),
                         {"g": "git", "gst": "git status", "-": "cd -", "say": "echo it's"})

    def test_skips_lines_it_cannot_parse(self):
        self.assertEqual(zi.parse_aliases("broken='open\ng=git\n"), {"g": "git"})


class Mask(unittest.TestCase):
    def test_masks_a_secret_env_assignment(self):
        self.assertEqual(zi.mask("GITHUB_TOKEN=abc123 gh pr list"), "GITHUB_TOKEN=*** gh pr list")

    def test_masks_secret_flags(self):
        self.assertEqual(zi.mask("login --password hunter2 --token=xyz"), "login --password *** --token=***")

    def test_masks_a_bearer_header(self):
        self.assertEqual(zi.mask("curl -H 'Authorization: Bearer abc.def'"), "curl -H 'Authorization: Bearer ***'")

    def test_masks_url_credentials(self):
        self.assertEqual(zi.mask("git clone https://me:s3cret@github.com/x/y"), "git clone https://***@github.com/x/y")

    def test_masks_known_token_prefixes(self):
        self.assertEqual(zi.mask("echo ghp_" + "a1B2" * 9), "echo ***")

    def test_masks_a_long_mixed_string(self):
        self.assertEqual(zi.mask("use Xk29fLq8Zr0pVb7Nw3Ty6Hm1Gd5Sa4Ce"), "use ***")

    def test_keeps_ordinary_commands(self):
        for cmd in ["git switch feat/proj-123-fix-the-long-branch-name-here",
                    "cd /Users/danielkeefer/studio/code/xxkeefer-skills",
                    "git show 3f786850e387550fdab836ed7e6dc881de23001b"]:
            self.assertEqual(zi.mask(cmd), cmd)


class Window(unittest.TestCase):
    def test_counts_only_the_window_but_keeps_all_time_totals(self):
        result = zi.analyse(entries((5 * DAY, "git status --short"),
                                    (100 * DAY, "git status --short")), {}, "90d", NOW)
        self.assertEqual(result["totals"], {"window": 1, "all_time": 2})

    def test_all_counts_everything(self):
        result = zi.analyse(entries((5 * DAY, "ls"), (400 * DAY, "ls")), {}, "all", NOW)
        self.assertEqual(result["totals"]["window"], 2)

    def test_falls_back_to_all_when_history_has_no_timestamps(self):
        result = zi.analyse([(None, "ls"), (None, "pwd")], {}, "90d", NOW)
        self.assertEqual(result["totals"]["window"], 2)
        self.assertFalse(result["window"]["timestamps"])


class Commands(unittest.TestCase):
    def test_ranks_long_repeated_commands_and_drops_short_or_rare_ones(self):
        rows = [(DAY, "pnpm run typecheck")] * 3 + [(DAY, "ls")] * 9 + [(DAY, "git fetch --prune")] * 2
        result = zi.analyse(entries(*rows, (200 * DAY, "pnpm run typecheck")), {}, "90d", NOW)
        self.assertEqual(result["commands"], [{"command": "pnpm run typecheck", "uses": 3, "all_time": 4}])

    def test_groups_commands_that_differ_only_by_a_masked_secret(self):
        rows = [(DAY, f"GITHUB_TOKEN=t{i} gh pr list") for i in range(3)]
        result = zi.analyse(entries(*rows), {}, "90d", NOW)
        self.assertEqual(result["commands"][0]["command"], "GITHUB_TOKEN=*** gh pr list")
        self.assertEqual(result["commands"][0]["uses"], 3)


class Prefixes(unittest.TestCase):
    def test_groups_commands_with_a_changing_argument(self):
        rows = [(DAY, f"git commit -m msg{i}") for i in range(4)]
        prefixes = zi.analyse(entries(*rows), {}, "90d", NOW)["prefixes"]
        self.assertEqual(prefixes[0]["prefix"], "git commit -m")
        self.assertEqual(prefixes[0]["uses"], 4)
        self.assertEqual(prefixes[0]["variants"], 4)
        self.assertEqual(len(prefixes[0]["examples"]), 3)

    def test_drops_a_prefix_when_a_longer_one_has_the_same_uses(self):
        rows = [(DAY, f"git commit -m msg{i}") for i in range(4)]
        names = [p["prefix"] for p in zi.analyse(entries(*rows), {}, "90d", NOW)["prefixes"]]
        self.assertNotIn("git commit", names)


class Sequences(unittest.TestCase):
    def test_counts_commands_that_follow_each_other_closely(self):
        rows = []
        for i in range(3):
            start = DAY * (i + 1)
            rows += [(start, "git add ."), (start - 30, "git commit -m x"), (start - 60, "git push")]
        sequences = zi.analyse(entries(*rows), {}, "90d", NOW)["sequences"]
        self.assertIn({"steps": ["git add", "git commit", "git push"], "uses": 3}, sequences)
        self.assertIn({"steps": ["git add", "git commit"], "uses": 3}, sequences)

    def test_a_long_gap_breaks_a_sequence(self):
        rows = []
        for i in range(3):
            start = DAY * (i + 1)
            rows += [(start, "git add ."), (start - 3600, "git commit -m x")]
        self.assertEqual(zi.analyse(entries(*rows), {}, "90d", NOW)["sequences"], [])

    def test_ignores_a_command_repeated_back_to_back(self):
        rows = [(DAY - i, "git status") for i in range(6)]
        self.assertEqual(zi.analyse(entries(*rows), {}, "90d", NOW)["sequences"], [])


class UnusedAliases(unittest.TestCase):
    def test_reports_the_longest_alias_whose_long_form_you_typed(self):
        aliases = {"g": "git", "gst": "git status"}
        rows = [(DAY, "git status")] * 3 + [(DAY, "gst")]
        unused = zi.analyse(entries(*rows), aliases, "90d", NOW)["unused_aliases"]
        self.assertEqual(unused, [{"alias": "gst", "expansion": "git status", "long_form_uses": 3, "alias_uses": 1}])

    def test_skips_aliases_that_save_nothing(self):
        aliases = {"ls": "ls -G", "grep": "grep --color=auto"}
        rows = [(DAY, "ls -G")] * 3
        self.assertEqual(zi.analyse(entries(*rows), aliases, "90d", NOW)["unused_aliases"], [])


class Summary(unittest.TestCase):
    def test_reports_top_programs_hours_and_months(self):
        rows = [(DAY, "git status"), (DAY, "git log"), (DAY, "ls")]
        result = zi.analyse(entries(*rows), {}, "90d", NOW)
        self.assertEqual(result["programs"][0], {"name": "git", "uses": 2})
        self.assertEqual(sum(result["hours"]), 3)
        self.assertEqual(result["months"], [{"month": "2027-01", "uses": 3, "top": ["git", "ls"]}])


class Render(unittest.TestCase):
    def setUp(self):
        self.analysis = zi.analyse(entries((DAY, "git status"), (DAY, "git status"), (DAY, "git status")),
                                   {"gst": "git status"}, "90d", NOW)
        self.suggestions = {
            "observations": ["Most of your work is git."],
            "suggestions": [
                {"kind": "alias", "name": "gpf", "definition": "git push --force-with-lease",
                 "module": "git.zsh", "uses": 9, "all_time": 20, "saved": 216, "why": "Typed 9 times."},
                {"kind": "function", "name": "mkcd", "definition": "mkcd() { mkdir -p \"$1\" && cd \"$1\" }",
                 "module": "nav.zsh", "uses": 4, "all_time": 4, "saved": 40, "why": "a < b"},
            ],
        }

    def test_numbers_each_suggestion_in_order(self):
        html = zi.render(self.analysis, self.suggestions)
        self.assertLess(html.index(">1<"), html.index("gpf"))
        self.assertLess(html.index(">2<"), html.index("mkcd"))

    def test_escapes_suggestion_text(self):
        html = zi.render(self.analysis, self.suggestions)
        self.assertIn("a &lt; b", html)
        self.assertNotIn("a < b", html)

    def test_shows_observations_and_unused_aliases(self):
        html = zi.render(self.analysis, self.suggestions)
        self.assertIn("Most of your work is git.", html)
        self.assertIn("gst", html)


class Cli(unittest.TestCase):
    def test_analyse_then_render_writes_a_report(self):
        tmp = tempfile.mkdtemp()
        paths = {name: os.path.join(tmp, name) for name in ["history", "aliases", "analysis.json",
                                                             "suggestions.json", "report.html"]}
        with open(paths["history"], "wb") as f:
            f.write(hist(*[(DAY, "git status")] * 3))
        with open(paths["aliases"], "w") as f:
            f.write("gst='git status'\n")
        out = subprocess.run([sys.executable, SCRIPT, "analyse", "--history", paths["history"],
                              "--aliases", paths["aliases"], "--window", "30d", "--now", str(NOW)],
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out)["unused_aliases"][0]["alias"], "gst")

        with open(paths["analysis.json"], "w") as f:
            f.write(out)
        with open(paths["suggestions.json"], "w") as f:
            json.dump({"observations": [], "suggestions": []}, f)
        subprocess.run([sys.executable, SCRIPT, "render", "--analysis", paths["analysis.json"],
                        "--suggestions", paths["suggestions.json"], "--out", paths["report.html"]],
                       check=True)
        with open(paths["report.html"]) as f:
            self.assertIn("zsh insights", f.read())


if __name__ == "__main__":
    unittest.main()
