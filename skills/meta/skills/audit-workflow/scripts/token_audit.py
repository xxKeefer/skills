#!/usr/bin/env python3
"""Measure the token spend of recent Claude Code sessions for /audit-workflow.

Reads the session transcripts under the projects folder. Counts each request once, by its
requestId, and prices it from the dated table below. Prints a markdown report: the totals, the
session baseline, the cost by session and by skill, the tool results by command shape with their
context debt, and the friction (hook denials, other denials, declines, and failed tool calls).

A command shape keeps each command name and, for a tool such as git, its subcommand. It keeps no
argument, with one limit: a regex is not a shell parser, so a `case` pattern or a quoted `$(...)`
that holds more quotes can show one word of an argument.

Run: python3 token_audit.py [--days 7] [--projects ~/.claude/projects]
"""
import argparse
import glob
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

PRICES_CHECKED = "2026-11-04"
PRICES_SOURCE = "https://platform.claude.com/docs/en/about-claude/pricing"
# USD for each million tokens: input, 5-minute cache write, 1-hour cache write, cache read, output.
PRICES = {
    "claude-fable-5-1": (10, 12.50, 20, 0.25, 50),
    "claude-opus-5-5": (4, 5, 8, 0.20, 20),
    "claude-sonnet-5-5": (2, 2.50, 4, 0.10, 10),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50),
}
# A request whose prompt is over the limit pays these prices for all of its tokens.
LONG_PROMPT = {"claude-haiku-5-5": (100_000, (0.50, 0.625, 1, 0.05, 2.50))}

SUBCOMMAND_TOOLS = {
    "brew", "bun", "cargo", "docker", "gh", "git", "go", "kubectl", "nix", "npm", "nx", "pip", "pip3",
    "pnpm", "terraform", "uv", "wt", "yarn",
}
KEYWORDS = {"!", "{", "}", "do", "done", "elif", "else", "esac", "fi", "if", "then", "time", "until", "while"}
ESCAPED = re.compile(r"\\.")
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
COMMENT = re.compile(r"(^|\s)#[^\n]*")
ARITHMETIC = re.compile(r"\$\(\([^)]*\)\)")
ARRAY = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*=\([^)]*\)")
OPERATOR = re.compile(r"([|;&()\n])")
REDIRECT = re.compile(r"^[0-9]*[<>]+")
ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
SUBCOMMAND = re.compile(r"^[a-z][a-z0-9-]*$")
HEAD_CHARACTER = re.compile(r"[A-Za-z\[]")
COMMAND_NAME = re.compile(r"^[A-Za-z0-9_\[$][\w.+\-\[\]$]*$")
DECLINED = "The user doesn't want to proceed"
TOP = 10


def shape(tool, tool_input):
    """Returns the tool name, plus the command heads of a Bash call, with no argument."""
    if tool != "Bash":
        return tool
    return "Bash: " + command_shape(str((tool_input or {}).get("command", "")))


def command_shape(command):
    """Returns each command head once, in order, without cd, so `cd x && sed` groups with `sed`."""
    before, marker, after = command.partition("<<")
    if marker:
        command = before + marker + after.split("\n", 1)[0]
    command = QUOTED.sub("quoted", ESCAPED.sub("_", command.replace("\\\n", " ")))
    # An unclosed quote: the rest of the command is quoted text.
    command = re.split(r"['\"]", command, maxsplit=1)[0]
    pieces = OPERATOR.split(ARRAY.sub(" ", ARITHMETIC.sub("0", COMMENT.sub(r"\1", command))))
    heads = []
    for index in range(0, len(pieces), 2):
        # The text after a closing parenthesis continues the outer command.
        if index and pieces[index - 1] == ")":
            continue
        words, i = pieces[index].split(), 0
        while i < len(words):
            redirect = REDIRECT.match(words[i])
            if redirect:
                i += 1 if redirect.end() < len(words[i]) else 2
            elif words[i] in KEYWORDS or ENV_ASSIGNMENT.match(words[i]) or not HEAD_CHARACTER.search(words[i]):
                i += 1
            else:
                break
        if i >= len(words):
            continue
        head = os.path.basename(words[i])
        if not COMMAND_NAME.match(head):
            continue
        if head in SUBCOMMAND_TOOLS and i + 1 < len(words) and SUBCOMMAND.match(words[i + 1]):
            head += " " + words[i + 1]
        heads.append(head)
    unique = list(dict.fromkeys(head for head in heads if head != "cd"))
    return " + ".join(unique or heads[:1])


def parse_time(text):
    return datetime.fromisoformat(str(text).replace("Z", "+00:00"))


def in_window(record, start, end):
    try:
        return start <= parse_time(record.get("timestamp")) <= end
    except ValueError:
        return False


def read_records(path):
    with open(path, errors="replace") as f:
        for line in f:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                yield record


def subagent_meta(path):
    try:
        with open(path[: -len(".jsonl")] + ".meta.json") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def transcript_files(projects, start):
    """Returns the session files, then the subagent files by spawn depth, so a parent comes first."""
    mains = sorted(glob.glob(os.path.join(projects, "*", "*.jsonl")))
    subagents = glob.glob(os.path.join(projects, "*", "*", "subagents", "*.jsonl"))
    subagents.sort(key=lambda path: (subagent_meta(path).get("spawnDepth", 1), path))
    return [path for path in mains + subagents if os.path.getmtime(path) >= start.timestamp()]


def token_counts(usage):
    """Returns input, 5-minute cache write, 1-hour cache write, cache read, and output tokens."""
    cache = usage.get("cache_creation") or {}
    hour = cache.get("ephemeral_1h_input_tokens") or 0
    minutes = cache.get("ephemeral_5m_input_tokens")
    if minutes is None:
        minutes = (usage.get("cache_creation_input_tokens") or 0) - hour
    return (
        usage.get("input_tokens") or 0,
        minutes,
        hour,
        usage.get("cache_read_input_tokens") or 0,
        usage.get("output_tokens") or 0,
    )


def rates(model, prompt):
    long_prompt = LONG_PROMPT.get(model)
    if long_prompt and prompt > long_prompt[0]:
        return long_prompt[1]
    return PRICES.get(model)


def result_tokens(content):
    if isinstance(content, str):
        return len(content) // 4
    if isinstance(content, list):
        text = "".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
        return len(text) // 4
    return 0


def result_text(content):
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return str(content or "")


def friction_kind(block, decision):
    decision = decision or {}
    if decision.get("decision") == "reject":
        if decision.get("source") == "hook":
            return "hook denial"
        if decision.get("source") == "user_reject":
            return "declined"
        return "denied"
    if block.get("is_error"):
        return "declined" if result_text(block.get("content")).startswith(DECLINED) else "failed"
    return None


def audit(projects, start, end):
    """Returns the spend of the requests in the window, by session, skill, and tool."""
    seen = set()
    tool_labels, tool_skills, cwd_of = {}, {}, {}
    totals = Counter()
    unpriced = Counter()
    sessions = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0, "baseline": None, "first": None})
    skills = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0})
    results, friction = [], Counter()
    per_1k = 0.0

    for path in transcript_files(projects, start):
        inherited = tool_skills.get(subagent_meta(path).get("toolUseId"))
        events = []
        for record in read_records(path):
            kind = record.get("type")
            sid = record.get("sessionId")
            if record.get("cwd") and sid not in cwd_of:
                cwd_of[sid] = os.path.basename(str(record["cwd"]).rstrip("/"))
            if kind == "system" and record.get("subtype") == "compact_boundary":
                events.append(None)
            elif kind == "assistant":
                skill = record.get("attributionSkill") or inherited
                message = record.get("message") or {}
                for block in message.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_labels[block.get("id")] = shape(block.get("name", "?"), block.get("input"))
                        tool_skills[block.get("id")] = skill
                rid = record.get("requestId")
                if not rid or rid in seen or not in_window(record, start, end):
                    continue
                seen.add(rid)
                counts = token_counts(message.get("usage") or {})
                model = message.get("model", "?")
                price = rates(model, sum(counts[:4]))
                if price is None:
                    unpriced[model] += 1
                    price = (0, 0, 0, 0, 0)
                cost = sum(c * p for c, p in zip(counts, price)) / 1e6
                tokens = sum(counts)
                for key, value in zip(("input", "write_5m", "write_1h", "cache_read", "output"), counts):
                    totals[key] += value
                totals["requests"] += 1
                totals["tokens"] += tokens
                totals["cost"] += cost
                totals["read_cost"] += counts[3] * price[3] / 1e6
                session = sessions[sid]
                session["requests"] += 1
                session["tokens"] += tokens
                session["cost"] += cost
                if session["first"] is None or record["timestamp"] < session["first"]:
                    session["first"] = record["timestamp"]
                if not record.get("isSidechain"):
                    if session["baseline"] is None:
                        session["baseline"] = sum(counts[:4])
                    per_1k += 1000 * price[3] / 1e6
                row = skills[skill or "(none)"]
                row["requests"] += 1
                row["tokens"] += tokens
                row["cost"] += cost
                events.append(price[3] / 1e6)
            elif kind == "user" and in_window(record, start, end):
                content = (record.get("message") or {}).get("content")
                for block in content if isinstance(content, list) else []:
                    if not isinstance(block, dict) or block.get("type") != "tool_result":
                        continue
                    label = tool_labels.get(block.get("tool_use_id"), "?")
                    row = {"tool": label, "sid": sid, "tokens": result_tokens(block.get("content")), "turns": 0, "debt": 0.0}
                    results.append(row)
                    events.append(row)
                    flagged = friction_kind(block, record.get("permissionDecision"))
                    if flagged:
                        friction[(flagged, label)] += 1

        price, turns = 0.0, 0
        for event in reversed(events):
            if event is None:
                price, turns = 0.0, 0
            elif isinstance(event, float):
                price += event
                turns += 1
            else:
                event["turns"] = turns
                event["debt"] = event["tokens"] * price

    def label(sid):
        session = sessions.get(sid)
        day = session["first"][:10] if session and session["first"] else "?"
        return f"{day} {cwd_of.get(sid, '?')} {str(sid)[:8]}"

    tools = defaultdict(lambda: {"calls": 0, "tokens": 0, "debt": 0.0})
    for row in results:
        tools[row["tool"]]["calls"] += 1
        tools[row["tool"]]["tokens"] += row["tokens"]
        tools[row["tool"]]["debt"] += row["debt"]
        row["session"] = label(row.pop("sid"))

    baselines = [s["baseline"] for s in sessions.values() if s["baseline"] is not None]
    return {
        "start": start,
        "end": end,
        "totals": {
            "requests": totals["requests"],
            "tokens": totals["tokens"],
            "input": totals["input"],
            "cache_write": totals["write_5m"] + totals["write_1h"],
            "cache_read": totals["cache_read"],
            "output": totals["output"],
            "cost": totals["cost"],
            "read_cost": totals["read_cost"],
        },
        "unpriced": dict(unpriced),
        "baseline": {
            "median": int(statistics.median(baselines)) if baselines else 0,
            "max": max(baselines, default=0),
            "per_1k": per_1k,
        },
        "sessions": sorted(
            ({"label": label(sid), **{k: s[k] for k in ("requests", "tokens", "cost", "baseline")}} for sid, s in sessions.items()),
            key=lambda row: -row["cost"],
        ),
        "skills": sorted(({"skill": k, **v} for k, v in skills.items()), key=lambda row: -row["cost"]),
        "tools": sorted(({"tool": k, **v} for k, v in tools.items()), key=lambda row: -row["debt"]),
        "results": sorted(results, key=lambda row: -row["debt"]),
        "friction": [
            {"kind": kind, "tool": tool, "count": count}
            for (kind, tool), count in sorted(friction.items(), key=lambda item: (-item[1], item[0]))
        ],
    }


def number(value):
    return f"{value or 0:,}"


def usd(value):
    return f"${value:,.2f}" if value >= 1 else f"${value:.4f}"


def table(title, header, rows, cells):
    suffix = f" (top {TOP} of {len(rows)})" if len(rows) > TOP else ""
    lines = [f"## {title}{suffix}", ""]
    if not rows:
        return lines + ["None.", ""]
    lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in cells(row)) + " |" for row in rows[:TOP]]
    return lines + [""]


def render(data):
    lines = [
        f"# Token audit: {data['start']:%Y-%m-%d} to {data['end']:%Y-%m-%d}",
        "",
        f"Prices checked {PRICES_CHECKED}: {PRICES_SOURCE}. A tool result's tokens are an estimate:"
        " its characters divided by 4.",
        "",
    ]
    totals = data["totals"]
    if not totals["requests"]:
        return "\n".join(lines + ["No requests in the window.", ""])
    share = totals["read_cost"] / totals["cost"] if totals["cost"] else 0
    lines += [
        "## Totals",
        "",
        "| Sessions | Requests | Input | Cache write | Cache read | Output | Cost | Cost per request | Cache-read share |",
        "|---|---|---|---|---|---|---|---|---|",
        f"| {len(data['sessions'])} | {totals['requests']} | {number(totals['input'])} | {number(totals['cache_write'])}"
        f" | {number(totals['cache_read'])} | {number(totals['output'])} | {usd(totals['cost'])}"
        f" | {usd(totals['cost'] / totals['requests'])} | {share:.0%} |",
        "",
    ]
    if data["unpriced"]:
        models = ", ".join(f"`{model}` ({count} requests)" for model, count in sorted(data["unpriced"].items()))
        lines += [f"Unpriced models, counted at $0: {models}.", ""]
    baseline = data["baseline"]
    lines += [
        "## Baseline",
        "",
        f"The input of the first main request of each session: median {number(baseline['median'])} tokens,"
        f" max {number(baseline['max'])}. Each 1,000 baseline tokens cost {usd(baseline['per_1k'])}"
        " over the window, at the cache-read price of each main request.",
        "",
    ]
    lines += table(
        "By session", ["Session", "Requests", "Tokens", "Cost", "Baseline"], data["sessions"],
        lambda r: [r["label"], r["requests"], number(r["tokens"]), usd(r["cost"]), number(r["baseline"])],
    )
    lines += table(
        "By skill", ["Skill", "Requests", "Tokens", "Cost"], data["skills"],
        lambda r: [r["skill"], r["requests"], number(r["tokens"]), usd(r["cost"])],
    )
    lines += table(
        "By tool", ["Tool", "Calls", "Result tokens", "Debt"], data["tools"],
        lambda r: [r["tool"], r["calls"], number(r["tokens"]), usd(r["debt"])],
    )
    lines += table(
        "Context debt", ["Tool", "Session", "Result tokens", "Turns after", "Debt"], data["results"],
        lambda r: [r["tool"], r["session"], number(r["tokens"]), r["turns"], usd(r["debt"])],
    )
    lines += table(
        "Friction", ["Kind", "Tool", "Count"], data["friction"],
        lambda r: [r["kind"], r["tool"], r["count"]],
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Token audit for /audit-workflow.")
    parser.add_argument("--days", type=int, default=7, help="The window: the last N days")
    parser.add_argument("--projects", default=os.path.expanduser("~/.claude/projects"))
    args = parser.parse_args()
    end = datetime.now(timezone.utc)
    print(render(audit(args.projects, end - timedelta(days=args.days), end)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
