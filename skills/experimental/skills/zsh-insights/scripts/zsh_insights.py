#!/usr/bin/env python3
"""Counts zsh history patterns for /zsh-insights, and renders its HTML report.

  zsh_insights.py analyse --history FILE --aliases FILE [--window 90d|all] [--now EPOCH]
  zsh_insights.py render --analysis FILE --suggestions FILE --out FILE
"""
import argparse
import html
import json
import re
import shlex
import sys
import time
from collections import Counter, defaultdict

MIN_USES = 3
MIN_COMMAND_LENGTH = 8
SEQUENCE_GAP = 300
TOP = 40

HEADER = re.compile(r": (\d+):\d+;(.*)", re.S)
WORD = re.compile(r"[a-z][a-z0-9:._-]*")
MASKS = [
    (re.compile(r"(\w+://)[^/\s:@]+:[^/\s@]+@"), r"\1***@"),
    (re.compile(r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]+"), r"\1 ***"),
    (re.compile(r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|CREDENTIALS?|PRIVATE_KEY)[A-Z0-9_]*)=\S+"),
     r"\1=***"),
    (re.compile(r"(?i)(--?(?:password|passwd|token|secret|api-?key)(?:=|\s+))\S+"), r"\1***"),
    (re.compile(r"\b(?:gh[pousr]_|github_pat_|glpat-|sk-|xox[abprs]-|npm_)[A-Za-z0-9_-]{10,}"), "***"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "***"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*"), "***"),
]
LONG_RUN = re.compile(r"[A-Za-z0-9_+=]{32,}")


def unmetafy(data):
    """Returns the bytes zsh meant, where 0x83 marks the next byte as XOR 0x20."""
    out = bytearray()
    meta = False
    for byte in data:
        if meta:
            out.append(byte ^ 0x20)
            meta = False
        elif byte == 0x83:
            meta = True
        else:
            out.append(byte)
    return bytes(out)


def parse_history(data):
    """Returns (timestamp or None, command) pairs, with continued lines joined."""
    entries = []
    continued = False
    for line in unmetafy(data).decode("utf-8", "replace").split("\n"):
        if continued:
            ts, cmd = entries[-1]
            entries[-1] = (ts, cmd + "\n" + line)
        else:
            match = HEADER.fullmatch(line)
            entries.append((int(match.group(1)), match.group(2)) if match else (None, line))
        continued = line.endswith("\\")
        if continued:
            ts, cmd = entries[-1]
            entries[-1] = (ts, cmd[:-1])
    return [(ts, cmd.strip()) for ts, cmd in entries if cmd.strip()]


def parse_aliases(text):
    """Returns name -> expansion from `alias -r` output, minus lines that do not parse."""
    aliases = {}
    for line in text.splitlines():
        try:
            tokens = shlex.split(line)
        except ValueError:
            continue
        if len(tokens) == 1 and "=" in tokens[0]:
            name, expansion = tokens[0].split("=", 1)
            aliases[name] = expansion
    return aliases


def mask(cmd):
    """Returns the command with secret-like values replaced by ***."""
    for pattern, replacement in MASKS:
        cmd = pattern.sub(replacement, cmd)

    def mixed(match):
        run = match.group(0)
        if re.search(r"[a-z]", run) and re.search(r"[A-Z]", run) and re.search(r"\d", run):
            return "***"
        return run

    return LONG_RUN.sub(mixed, cmd)


def shape(cmd):
    """Returns the program and its subcommand, such as `git commit`."""
    tokens = cmd.split()
    if len(tokens) > 1 and WORD.fullmatch(tokens[1]):
        return f"{tokens[0]} {tokens[1]}"
    return tokens[0]


def top(counter, n):
    return [name for name, _ in counter.most_common(n)]


def find_commands(window, all_time):
    uses = Counter(window)
    rows = [{"command": cmd, "uses": n, "all_time": all_time[cmd]}
            for cmd, n in uses.items() if n >= MIN_USES and len(cmd) >= MIN_COMMAND_LENGTH]
    rows.sort(key=lambda r: (-r["uses"] * len(r["command"]), r["command"]))
    return rows[:TOP]


def find_prefixes(window):
    uses = Counter()
    variants = defaultdict(list)
    for cmd in window:
        tokens = cmd.split()
        for k in range(2, min(len(tokens), 5)):
            prefix = " ".join(tokens[:k])
            uses[prefix] += 1
            if cmd not in variants[prefix]:
                variants[prefix].append(cmd)
    kept = {p: n for p, n in uses.items() if n >= MIN_USES and len(variants[p]) >= 2}
    longer_same = {p for p in kept for q, m in kept.items()
                   if q.startswith(p + " ") and len(q.split()) == len(p.split()) + 1 and m == kept[p]}
    rows = [{"prefix": p, "uses": n, "variants": len(variants[p]), "examples": variants[p][-3:][::-1]}
            for p, n in kept.items() if p not in longer_same]
    rows.sort(key=lambda r: (-r["uses"] * len(r["prefix"]), r["prefix"]))
    return rows[:TOP]


def find_sequences(timed):
    """Counts runs of 2 or 3 different shapes, each within SEQUENCE_GAP seconds of the last."""
    uses = Counter()
    for i in range(len(timed) - 1):
        steps = [timed[i]]
        for nxt in timed[i + 1:i + 3]:
            prev = steps[-1]
            if prev[0] is None or nxt[0] is None or not 0 <= nxt[0] - prev[0] <= SEQUENCE_GAP:
                break
            if shape(nxt[1]) == shape(prev[1]):
                break
            steps.append(nxt)
            uses[tuple(shape(cmd) for _, cmd in steps)] += 1
    rows = [{"steps": list(s), "uses": n} for s, n in uses.items() if n >= MIN_USES]
    rows.sort(key=lambda r: (-r["uses"], -len(r["steps"]), r["steps"]))
    return rows[:TOP]


def find_unused_aliases(window, aliases):
    useful = {name: exp for name, exp in aliases.items()
              if exp.strip() and len(name) < len(exp) and name != exp.split()[0]}
    by_length = sorted(useful.items(), key=lambda item: -len(item[1]))
    long_form = Counter()
    typed = Counter(cmd.split()[0] for cmd in window)
    for cmd in window:
        for name, exp in by_length:
            if cmd == exp or cmd.startswith(exp + " "):
                long_form[name] += 1
                break
    rows = [{"alias": name, "expansion": useful[name], "long_form_uses": n, "alias_uses": typed[name]}
            for name, n in long_form.items() if n >= MIN_USES]
    rows.sort(key=lambda r: (-r["long_form_uses"] * (len(r["expansion"]) - len(r["alias"])), r["alias"]))
    return rows[:TOP]


def analyse(entries, aliases, window, now):
    """Returns the counts the skill reads: summary, commands, prefixes, sequences, unused aliases."""
    entries = [(ts, mask(cmd)) for ts, cmd in entries]
    timestamps = any(ts is not None for ts, _ in entries)
    label = window if timestamps else "all"
    if label == "all":
        timed = entries
    else:
        start = now - int(label.rstrip("d")) * 86400
        timed = [(ts, cmd) for ts, cmd in entries if ts is not None and ts >= start]
    window_cmds = [cmd for _, cmd in timed]
    dated = [ts for ts, _ in entries if ts is not None]

    hours = [0] * 24
    for ts, _ in timed:
        if ts is not None:
            hours[time.localtime(ts).tm_hour] += 1

    months = defaultdict(Counter)
    for ts, cmd in entries:
        if ts is not None:
            months[time.strftime("%Y-%m", time.localtime(ts))][cmd.split()[0]] += 1

    return {
        "window": {
            "label": label,
            "timestamps": timestamps,
            "start": time.strftime("%Y-%m-%d", time.localtime(min(ts for ts, _ in timed if ts is not None))) if dated and timed else None,
            "end": time.strftime("%Y-%m-%d", time.localtime(max(dated))) if dated else None,
        },
        "totals": {"window": len(timed), "all_time": len(entries)},
        "programs": [{"name": n, "uses": c} for n, c in Counter(cmd.split()[0] for cmd in window_cmds).most_common(15)],
        "hours": hours,
        "months": [{"month": m, "uses": sum(c.values()), "top": top(c, 3)} for m, c in sorted(months.items())],
        "commands": find_commands(window_cmds, Counter(cmd for _, cmd in entries)),
        "prefixes": find_prefixes(window_cmds),
        "sequences": find_sequences(timed),
        "unused_aliases": find_unused_aliases(window_cmds, aliases),
    }


STYLE = """
body { font: 15px/1.5 -apple-system, system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; color: #222; }
h1 { margin-bottom: 0; } .sub { color: #666; margin-top: .25rem; }
table { border-collapse: collapse; width: 100%; margin: .5rem 0 1.5rem; }
th, td { text-align: left; padding: .35rem .5rem; border-bottom: 1px solid #ddd; vertical-align: top; }
th { background: #f5f5f5; } td.n { font-weight: bold; }
pre { margin: 0; white-space: pre-wrap; font-size: 13px; }
.bar { background: #4a7bd0; height: .8rem; display: inline-block; }
.hours { display: flex; align-items: flex-end; gap: 2px; height: 80px; }
.hours div { flex: 1; background: #4a7bd0; }
.reply { background: #fff8dc; padding: .75rem 1rem; border-left: 4px solid #e0b400; }
"""


def cell(value, code=False):
    text = html.escape(str(value))
    return f"<td><pre>{text}</pre></td>" if code else f"<td>{text}</td>"


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    return f"<table><tr>{head}</tr>{''.join(rows)}</table>"


def render(analysis, suggestions):
    """Returns the report HTML, with suggestions numbered from 1 in the order given."""
    w, totals = analysis["window"], analysis["totals"]
    span = f"{w['start']} to {w['end']}" if w["start"] else "no timestamps"
    parts = [f"<h1>zsh insights</h1><p class='sub'>Window {html.escape(w['label'])} ({html.escape(span)}): "
             f"{totals['window']} of {totals['all_time']} commands.</p>"]

    if suggestions.get("observations"):
        items = "".join(f"<li>{html.escape(o)}</li>" for o in suggestions["observations"])
        parts.append(f"<h2>At a glance</h2><ul>{items}</ul>")

    rows = [f"<tr><td class='n'>{i}</td>{cell(s['kind'])}{cell(s['name'])}{cell(s['definition'], code=True)}"
            f"{cell(s['module'])}{cell(s['uses'])}{cell(s['all_time'])}{cell(s['saved'])}{cell(s['why'])}</tr>"
            for i, s in enumerate(suggestions.get("suggestions", []), 1)]
    parts.append("<h2>Suggestions</h2>" + table(
        ["#", "Kind", "Name", "Definition", "Module", "Uses", "All time", "Keys saved", "Why"], rows))

    rows = [f"<tr>{cell(a['alias'])}{cell(a['expansion'], code=True)}{cell(a['long_form_uses'])}"
            f"{cell(a['alias_uses'])}</tr>" for a in analysis["unused_aliases"]]
    if rows:
        parts.append("<h2>Shortcuts you have but do not use</h2>" + table(
            ["Alias", "Expands to", "Long form typed", "Alias typed"], rows))

    peak = max([p["uses"] for p in analysis["programs"]] or [1])
    rows = [f"<tr>{cell(p['name'])}{cell(p['uses'])}<td><span class='bar' style='width:{100 * p['uses'] // peak}%'>"
            f"</span></td></tr>" for p in analysis["programs"]]
    parts.append("<h2>Usage</h2><h3>Top programs</h3>" + table(["Program", "Uses", ""], rows))

    peak = max(analysis["hours"]) or 1
    bars = "".join(f"<div title='{h}:00, {n}' style='height:{100 * n // peak}%'></div>"
                   for h, n in enumerate(analysis["hours"]))
    parts.append(f"<h3>Hour of day</h3><div class='hours'>{bars}</div>")

    rows = [f"<tr>{cell(m['month'])}{cell(m['uses'])}{cell(', '.join(m['top']))}</tr>" for m in analysis["months"]]
    if rows:
        parts.append("<h3>By month</h3>" + table(["Month", "Uses", "Top programs"], rows))

    parts.append("<p class='reply'>Reply in the chat with the numbers to apply, such as <code>1 3 5</code>. "
                 "To rename one, write <code>2 as gpl</code>.</p>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>zsh insights</title>"
            f"<style>{STYLE}</style></head><body>{''.join(parts)}</body></html>")


def main(argv):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("analyse")
    a.add_argument("--history", required=True)
    a.add_argument("--aliases", required=True)
    a.add_argument("--window", default="90d")
    a.add_argument("--now", type=float, default=None)
    r = sub.add_parser("render")
    r.add_argument("--analysis", required=True)
    r.add_argument("--suggestions", required=True)
    r.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    if args.command == "analyse":
        if args.window != "all" and not re.fullmatch(r"\d+d", args.window):
            parser.error("--window takes Nd, such as 30d, or all")
        with open(args.history, "rb") as f:
            entries = parse_history(f.read())
        with open(args.aliases) as f:
            aliases = parse_aliases(f.read())
        now = args.now if args.now is not None else time.time()
        json.dump(analyse(entries, aliases, args.window, now), sys.stdout, indent=1)
    else:
        with open(args.analysis) as f:
            analysis = json.load(f)
        with open(args.suggestions) as f:
            suggestions = json.load(f)
        with open(args.out, "w") as f:
            f.write(render(analysis, suggestions))


if __name__ == "__main__":
    main(sys.argv[1:])
