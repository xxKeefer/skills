#!/usr/bin/env python3
"""Run: python3 token_audit.spec.py"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

import token_audit as ta

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token_audit.py")
START = datetime(2026, 10, 28, tzinfo=timezone.utc)
END = datetime(2026, 11, 4, tzinfo=timezone.utc)
SID = "11111111-aaaa-bbbb-cccc-000000000001"
OPUS = "claude-opus-5-5"
OPUS_READ = 0.20 / 1e6


def ts(day, minute=0):
    return f"2026-11-{day:02d}T10:{minute:02d}:00.000Z"


def usage(inp=0, w5=0, w1=0, read=0, out=0):
    return {
        "input_tokens": inp,
        "cache_creation_input_tokens": w5 + w1,
        "cache_read_input_tokens": read,
        "output_tokens": out,
        "cache_creation": {"ephemeral_5m_input_tokens": w5, "ephemeral_1h_input_tokens": w1},
    }


def request(rid, at, model=OPUS, skill=None, tools=(), sid=SID, cwd="/work/app", sidechain=False, **tokens):
    content = [{"type": "tool_use", "id": i, "name": n, "input": x} for i, n, x in tools]
    record = {
        "type": "assistant",
        "requestId": rid,
        "timestamp": at,
        "sessionId": sid,
        "cwd": cwd,
        "isSidechain": sidechain,
        "message": {"model": model, "content": content or [{"type": "text", "text": "ok"}], "usage": usage(**tokens)},
    }
    if skill:
        record["attributionSkill"] = skill
    return record


def result(at, tool_use_id, content, error=False, decision=None, sid=SID):
    block = {"type": "tool_result", "tool_use_id": tool_use_id, "content": content, "is_error": error}
    record = {"type": "user", "timestamp": at, "sessionId": sid, "message": {"role": "user", "content": [block]}}
    if decision:
        record["permissionDecision"] = decision
    return record


def compact(at, sid=SID):
    return {"type": "system", "subtype": "compact_boundary", "timestamp": at, "sessionId": sid}


class Workspace(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, path, records, raw=()):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            for record in records:
                f.write(json.dumps(record) + "\n")
            for line in raw:
                f.write(line + "\n")
        return full

    def session(self, records, sid=SID):
        return self.write(f"-work-app/{sid}.jsonl", records)

    def subagent(self, agent, tool_use_id, records, depth=1, sid=SID):
        self.write(f"-work-app/{sid}/subagents/agent-{agent}.jsonl", records)
        meta = os.path.join(self.root, "-work-app", sid, "subagents", f"agent-{agent}.meta.json")
        with open(meta, "w") as f:
            json.dump({"toolUseId": tool_use_id, "spawnDepth": depth}, f)

    def run_audit(self):
        return ta.audit(self.root, START, END)


class Cost(Workspace):
    def test_prices_each_token_class(self):
        self.session([request("r1", ts(1), inp=1000, w5=2000, w1=3000, read=4000, out=5000)])
        totals = self.run_audit()["totals"]
        self.assertAlmostEqual(totals["cost"], (1000 * 4 + 2000 * 5 + 3000 * 8 + 4000 * 0.20 + 5000 * 20) / 1e6)
        self.assertEqual(totals["tokens"], 15_000)

    def test_counts_a_request_once_across_blocks_and_files(self):
        record = request("r1", ts(1), out=1000)
        self.session([record, record])
        self.session([record], sid="22222222-aaaa-bbbb-cccc-000000000002")
        totals = self.run_audit()["totals"]
        self.assertEqual(totals["requests"], 1)
        self.assertAlmostEqual(totals["cost"], 0.02)

    def test_haiku_prompt_over_100k_uses_the_higher_prices(self):
        self.session([
            request("r1", ts(1), model="claude-haiku-5-5", read=100_000, out=1000),
            request("r2", ts(1, 1), model="claude-haiku-5-5", read=100_001, out=1000),
        ])
        low = (100_000 * 0.01 + 1000 * 0.50) / 1e6
        high = (100_001 * 0.05 + 1000 * 2.50) / 1e6
        self.assertAlmostEqual(self.run_audit()["totals"]["cost"], low + high)

    def test_lists_an_unknown_model_as_unpriced(self):
        self.session([request("r1", ts(1), model="claude-new-9", out=1000), request("r2", ts(1, 1), out=1000)])
        data = self.run_audit()
        self.assertEqual(data["unpriced"], {"claude-new-9": 1})
        self.assertAlmostEqual(data["totals"]["cost"], 0.02)

    def test_skips_requests_outside_the_window(self):
        self.session([
            request("r0", "2026-10-27T23:59:59.000Z", out=1000),
            request("r1", ts(1), out=1000),
            request("r2", "2026-11-04T00:00:01.000Z", out=1000),
        ])
        self.assertEqual(self.run_audit()["totals"]["requests"], 1)

    def test_skips_tool_results_outside_the_window(self):
        self.session([
            request("r0", "2026-10-27T10:00:00.000Z", out=10, tools=[("t1", "Edit", {})]),
            result("2026-10-27T10:01:00.000Z", "t1", "Error.", error=True),
            request("r1", ts(1), out=10),
        ])
        data = self.run_audit()
        self.assertEqual(data["friction"], [])
        self.assertEqual(data["tools"], [])

    def test_skips_a_file_last_changed_before_the_window(self):
        path = self.session([request("r1", ts(1), out=1000)])
        old = (START - timedelta(days=1)).timestamp()
        os.utime(path, (old, old))
        self.assertEqual(self.run_audit()["totals"]["requests"], 0)

    def test_skips_a_line_that_is_not_json(self):
        self.write(f"-work-app/{SID}.jsonl", [request("r1", ts(1), out=1000)], raw=["not json{"])
        self.assertEqual(self.run_audit()["totals"]["requests"], 1)


class Sessions(Workspace):
    def test_session_cost_includes_its_subagents(self):
        self.session([request("r1", ts(1), out=1000, tools=[("t1", "Agent", {"prompt": "x"})])])
        self.subagent("a1", "t1", [request("s1", ts(1, 1), sidechain=True, out=1000)])
        sessions = self.run_audit()["sessions"]
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]["label"], "2026-11-01 app 11111111")
        self.assertEqual(sessions[0]["requests"], 2)
        self.assertAlmostEqual(sessions[0]["cost"], 0.04)

    def test_baseline_is_the_input_of_the_first_main_request(self):
        self.session([
            request("r1", ts(1, 5), inp=10, w1=20_000, read=5_000, out=500, tools=[("t1", "Agent", {})]),
            request("r2", ts(1, 9), read=40_000, out=10),
        ])
        self.subagent("a1", "t1", [request("s1", ts(1, 1), sidechain=True, w1=3_000, out=10)])
        data = self.run_audit()
        self.assertEqual(data["sessions"][0]["baseline"], 25_010)
        self.assertEqual(data["baseline"]["median"], 25_010)
        self.assertEqual(data["baseline"]["max"], 25_010)
        self.assertAlmostEqual(data["baseline"]["per_1k"], 2 * 1000 * OPUS_READ)

    def test_attributes_cost_to_the_skill_and_its_subagents(self):
        self.session([
            request("r1", ts(1), out=1000),
            request("r2", ts(1, 1), skill="engineering:mob-review", out=1000, tools=[("t1", "Agent", {})]),
        ])
        self.subagent("a1", "t1", [request("s1", ts(1, 2), sidechain=True, out=1000, tools=[("t2", "Agent", {})])])
        self.subagent("a0", "t2", [request("s2", ts(1, 3), sidechain=True, out=1000)], depth=2)
        skills = {row["skill"]: row for row in self.run_audit()["skills"]}
        self.assertEqual(skills["engineering:mob-review"]["requests"], 3)
        self.assertAlmostEqual(skills["engineering:mob-review"]["cost"], 0.06)
        self.assertEqual(skills["(none)"]["requests"], 1)


class Tools(Workspace):
    def test_debt_is_result_tokens_times_later_reads_until_compaction(self):
        self.session([
            request("r1", ts(1), out=10, tools=[("t1", "Read", {"file_path": "/x"})]),
            result(ts(1, 1), "t1", "x" * 4000),
            request("r2", ts(1, 2), out=10),
            request("r2", ts(1, 2), out=10),
            request("r3", ts(1, 3), out=10),
            compact(ts(1, 4)),
            request("r4", ts(1, 5), out=10),
        ])
        row = self.run_audit()["results"][0]
        self.assertEqual(row["tool"], "Read")
        self.assertEqual(row["tokens"], 1000)
        self.assertEqual(row["turns"], 2)
        self.assertAlmostEqual(row["debt"], 1000 * 2 * OPUS_READ)

    def test_groups_tools_by_command_shape(self):
        self.session([
            request("r1", ts(1), out=10, tools=[
                ("t1", "Bash", {"command": "git log --oneline -5"}),
                ("t2", "Bash", {"command": "git log -p notes.txt"}),
                ("t3", "Read", {"file_path": "/x"}),
            ]),
            result(ts(1, 1), "t1", "a" * 400),
            result(ts(1, 1), "t2", [{"type": "text", "text": "b" * 800}, {"type": "image", "source": {}}]),
            result(ts(1, 1), "t3", "c" * 40),
            request("r2", ts(1, 2), out=10),
        ])
        tools = {row["tool"]: row for row in self.run_audit()["tools"]}
        self.assertEqual(tools["Bash: git log"]["calls"], 2)
        self.assertEqual(tools["Bash: git log"]["tokens"], 300)
        self.assertAlmostEqual(tools["Bash: git log"]["debt"], 300 * OPUS_READ)
        self.assertEqual(tools["Read"]["calls"], 1)

    def test_sorts_friction_by_kind(self):
        hook = {"decision": "reject", "source": "hook", "reasonType": "hook"}
        safety = {"decision": "reject", "source": "config", "reasonType": "safetyCheck"}
        user = {"decision": "reject", "source": "user_reject"}
        self.session([
            request("r1", ts(1), out=10, tools=[
                ("t1", "Bash", {"command": "git stash"}),
                ("t2", "Bash", {"command": "pnpm exec vitest run"}),
                ("t3", "Read", {"file_path": "/x"}),
                ("t4", "Bash", {"command": "rm -rf build"}),
                ("t5", "Edit", {}),
                ("t6", "Edit", {}),
                ("t7", "AskUserQuestion", {}),
                ("t8", "Read", {"file_path": "/y"}),
            ]),
            result(ts(1, 1), "t1", "Blocked by the hook.", error=True, decision=hook),
            result(ts(1, 1), "t2", "Exit code 1", error=True),
            result(ts(1, 1), "t3", "The user doesn't want to proceed with this tool use.", error=True),
            result(ts(1, 1), "t4", "Denied.", error=True, decision=safety),
            result(ts(1, 1), "t5", "<tool_use_error>File has not been read yet.", error=True),
            result(ts(1, 1), "t6", "<tool_use_error>File has not been read yet.", error=True),
            result(ts(1, 1), "t7", "Rejected.", error=True, decision=user),
            result(ts(1, 1), "t8", "fine"),
        ])
        friction = self.run_audit()["friction"]
        self.assertEqual({(row["kind"], row["tool"]): row["count"] for row in friction}, {
            ("hook denial", "Bash: git stash"): 1,
            ("failed", "Bash: pnpm exec"): 1,
            ("declined", "Read"): 1,
            ("denied", "Bash: rm"): 1,
            ("failed", "Edit"): 2,
            ("declined", "AskUserQuestion"): 1,
        })
        self.assertEqual((friction[0]["kind"], friction[0]["tool"]), ("failed", "Edit"))


class Shape(unittest.TestCase):
    def check(self, command, expected):
        self.assertEqual(ta.shape("Bash", {"command": command}), "Bash: " + expected)

    def test_keeps_the_subcommand_of_a_known_tool(self):
        self.check("git log --oneline -5", "git log")

    def test_drops_the_arguments_of_other_commands(self):
        self.check("grep -r hunter2 src", "grep")

    def test_lists_each_head_of_a_compound_command_once_without_cd(self):
        self.check("cd /repo && git status --short | head -5 ; git status", "git status + head")

    def test_keeps_cd_when_it_is_the_only_command(self):
        self.check("cd /repo", "cd")

    def test_reads_a_new_line_as_a_new_command(self):
        self.check("git status\ngit log", "git status + git log")

    def test_joins_a_line_that_ends_in_a_backslash(self):
        self.check("nx test \\\n  Secret.spec.ts \\\n  Other.spec.ts", "nx test")

    def test_skips_shell_keywords(self):
        self.check("for f in a b; do cat $f; done", "for + cat")

    def test_ignores_a_quoted_separator(self):
        self.check('grep -n ";" notes.md', "grep")

    def test_skips_a_redirect_and_its_target(self):
        self.check("for d in a; do cat $d; done > /tmp/out.txt", "for + cat")
        self.check("> /tmp/log.txt echo hi", "echo")
        self.check("cat a 2>/dev/null 2>&1 | head", "cat + head")

    def test_skips_an_array_value(self):
        self.check("NEW=(a/SKILL.md b/SKILL.md); echo $NEW", "echo")

    def test_skips_an_env_assignment_with_a_quoted_value(self):
        self.check('FOO="a b" make', "make")

    def test_reads_a_command_substitution(self):
        self.check("files=$(git diff --name-only | grep vue)", "git diff + grep")

    def test_reads_the_text_after_a_substitution_as_arguments(self):
        self.check("git diff $(git merge-base origin/main HEAD) HEAD --stat", "git diff + git merge-base")

    def test_ignores_an_escaped_operator(self):
        self.check("grep -E foo\\|bar notes.md \\; find", "grep")

    def test_ignores_arithmetic(self):
        self.check("echo $((after-out+scope)) ; ls", "echo + ls")

    def test_ignores_a_comment(self):
        self.check("# step one: reviewed head\ngit status # check", "git status")
        self.check("echo ${#items}; ls", "echo + ls")

    def test_skips_a_part_with_no_command_name(self):
        self.check("ls *notes(N/) ; HEAD~2 x ; -name y ; d[0],d.get z", "ls")

    def test_keeps_a_test_bracket_as_a_head(self):
        self.check("[ -d notes ] && ls", "[ + ls")

    def test_skips_env_assignments(self):
        self.check("FOO=1 BAR=x pnpm exec vitest run", "pnpm exec")

    def test_ignores_a_heredoc_body(self):
        self.check("python3 - <<'EOF'\nimport os\nprint(1)\nEOF", "python3")

    def test_ignores_operators_inside_quotes(self):
        self.check("rg -n 'a|b && c' src", "rg")

    def test_uses_the_base_name_of_a_path(self):
        self.check("/usr/bin/python3 -V", "python3")

    def test_drops_a_subcommand_slot_that_holds_a_flag(self):
        self.check("git -C /repo log", "git")

    def test_falls_back_to_the_first_word_on_unbalanced_quotes(self):
        self.check("echo 'oops && ls", "echo")

    def test_names_only_the_tool_for_other_tools(self):
        self.assertEqual(ta.shape("Read", {"file_path": "/secret"}), "Read")


class Render(Workspace):
    def test_report_has_every_section_and_no_argument(self):
        self.session([
            request("r1", ts(1), out=10, tools=[("t1", "Bash", {"command": "curl -H 'token: hunter2' api"})]),
            result(ts(1, 1), "t1", "denied", error=True, decision={"decision": "reject", "source": "hook"}),
            request("r2", ts(1, 2), out=10),
        ])
        text = ta.render(self.run_audit())
        for heading in ("## Totals", "## Baseline", "## By session", "## By skill", "## By tool", "## Context debt", "## Friction"):
            self.assertIn(heading, text)
        self.assertIn("Prices checked " + ta.PRICES_CHECKED, text)
        self.assertIn("Bash: curl", text)
        self.assertNotIn("hunter2", text)

    def test_tables_show_the_top_ten(self):
        for n in range(12):
            sid = f"{n:08d}-aaaa"
            self.session([request(f"r{n}", ts(1, n), sid=sid, out=1000 * (n + 1))], sid=sid)
        text = ta.render(self.run_audit())
        self.assertIn("## By session (top 10 of 12)", text)
        section = text.split("## By session")[1].split("\n## ")[0]
        self.assertEqual(section.count("\n| 2026-"), 10)
        self.assertIn("00000011", section)
        self.assertNotIn("00000000", section)

    def test_says_so_when_the_window_is_empty(self):
        self.assertIn("No requests in the window.", ta.render(self.run_audit()))

    def test_cli_reads_the_last_days(self):
        now = datetime.now(timezone.utc)
        recent = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        old = (now - timedelta(days=9)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.session([request("r1", recent, out=1000), request("r0", old, out=1000)])
        command = [sys.executable, SCRIPT, "--days", "7", "--projects", self.root]
        out = subprocess.run(command, capture_output=True, text=True, check=True).stdout
        totals = out.split("## Totals")[1]
        self.assertIn("\n| 1 | 1 |", totals)


if __name__ == "__main__":
    unittest.main()
