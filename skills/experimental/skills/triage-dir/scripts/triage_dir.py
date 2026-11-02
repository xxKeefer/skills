#!/usr/bin/env python3
"""Scans a directory for /triage-dir, moves its items into category folders, and reports on them.

  triage_dir.py scan DIR
  triage_dir.py summary --scan FILE --plan FILE
  triage_dir.py apply --scan FILE --plan FILE
  triage_dir.py render --scan FILE --plan FILE
"""
import argparse
import html
import json
import os
import subprocess
import sys
import time

ACTIONS = ["delete", "archive", "keep"]
PARTIAL = (".crdownload", ".part", ".download")
REPORT = "triage.html"
FILE_BATCH = 200

STYLE = """
body { font: 15px/1.5 -apple-system, system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; color: #222; }
h1 { margin-bottom: 0; } .sub { color: #666; margin-top: .25rem; }
h2 { margin-top: 2.5rem; }
table { border-collapse: collapse; width: 100%; margin: .5rem 0 1.5rem; }
th, td { text-align: left; padding: .35rem .5rem; border-bottom: 1px solid #ddd; vertical-align: top; }
th { background: #f5f5f5; }
.action { font-size: 13px; font-weight: normal; padding: .1rem .5rem; border-radius: 1rem; color: #fff; }
.delete { background: #c0392b; } .archive { background: #d68910; } .keep { background: #1e8449; }
"""


def human(size):
    """Returns a size in decimal units, as Finder shows it."""
    if size < 1000:
        return f"{size} B"
    for unit in ["KB", "MB", "GB", "TB"]:
        size /= 1000
        if size < 1000 or unit == "TB":
            return f"{size:.1f} {unit}"


def skipped(name):
    return name.startswith(".") or name.endswith(PARTIAL) or name == REPORT


def tree_size(path):
    return sum(os.lstat(os.path.join(root, name)).st_size
               for root, _, files in os.walk(path) for name in files)


def file_types(paths):
    """Returns the MIME type of each path, read from its content, in the same order."""
    types = []
    for start in range(0, len(paths), FILE_BATCH):
        chunk = paths[start:start + FILE_BATCH]
        result = subprocess.run(["file", "-b", "--mime-type", "--", *chunk], capture_output=True, text=True)
        types += result.stdout.splitlines()
    return types


def scan(directory):
    """Returns each top-level item of the directory with its kind, type, size, and modified date."""
    directory = os.path.realpath(os.path.expanduser(directory))
    items = []
    for entry in sorted(os.scandir(directory), key=lambda e: e.name.lower()):
        if skipped(entry.name):
            continue
        folder = entry.is_dir(follow_symlinks=False)
        stat = entry.stat(follow_symlinks=False)
        items.append({"name": entry.name, "kind": "folder" if folder else "file", "type": "folder",
                      "size": tree_size(entry.path) if folder else stat.st_size,
                      "modified": time.strftime("%Y-%m-%d", time.localtime(stat.st_mtime))})
    files = [i for i in items if i["kind"] == "file"]
    for i, type_ in zip(files, file_types([os.path.join(directory, i["name"]) for i in files])):
        i["type"] = type_
    return {"dir": directory, "scanned": time.strftime("%Y-%m-%d"), "items": items}


def plan_problems(scan, plan):
    """Returns why the plan does not fit the scan: a bad name or action, or an item not placed exactly once."""
    problems, names, placed = [], set(), {}
    for c in plan["categories"]:
        name = c["name"]
        if not name or "/" in name or name.startswith("."):
            problems.append(f"{name}: not a plain folder name")
        elif name.lower() in names:
            problems.append(f"{name}: same name as another category")
        names.add(name.lower())
        if c["action"] not in ACTIONS:
            problems.append(f"{name}: action must be keep, archive, or delete")
        if not c["items"]:
            problems.append(f"{name}: has no items")
        for item in c["items"]:
            placed[item] = placed.get(item, 0) + 1
    scanned = [i["name"] for i in scan["items"]]
    for item in scanned:
        if item not in placed:
            problems.append(f"{item}: not in any category")
        elif placed[item] > 1:
            problems.append(f"{item}: in more than one category")
    problems += [f"{item}: not in the scan" for item in placed if item not in scanned]
    return problems


def disk_problems(scan, plan):
    """Returns each category folder that already exists, and each item that is gone from the directory."""
    path = lambda name: os.path.join(scan["dir"], name)
    return ([f"{c['name']}: already exists in the directory" for c in plan["categories"]
             if os.path.lexists(path(c["name"]))]
            + [f"{i['name']}: no longer in the directory" for i in scan["items"]
               if not os.path.lexists(path(i["name"]))])


def apply(scan, plan):
    """Moves each item into its category folder, or returns the problems and moves nothing."""
    problems = plan_problems(scan, plan) or disk_problems(scan, plan)
    if problems:
        return problems
    for c in plan["categories"]:
        folder = os.path.join(scan["dir"], c["name"])
        os.mkdir(folder)
        for name in c["items"]:
            os.rename(os.path.join(scan["dir"], name), os.path.join(folder, name))
    return []


def categories(scan, plan):
    """Returns the categories with their items largest first, ordered delete, archive, keep, then largest first."""
    by_name = {i["name"]: i for i in scan["items"]}
    result = []
    for c in plan["categories"]:
        items = sorted((by_name[n] for n in c["items"]), key=lambda i: -i["size"])
        dates = [i["modified"] for i in items]
        result.append({**c, "items": items, "size": sum(i["size"] for i in items),
                       "oldest": min(dates), "newest": max(dates)})
    return sorted(result, key=lambda c: (ACTIONS.index(c["action"]), -c["size"]))


def dates(c):
    return c["oldest"] if c["oldest"] == c["newest"] else f"{c['oldest']} to {c['newest']}"


def plural(n, one, many=None):
    return f"{n} {one}" if n == 1 else f"{n} {many or one + 's'}"


def md(text):
    return str(text).replace("|", "\\|")


def summary(scan, plan):
    """Returns a markdown table of each category with its action, item count, size, and three largest items."""
    rows = ["| Category | Action | Items | Size | Largest |", "|---|---|---|---|---|"]
    for c in categories(scan, plan):
        largest = ", ".join(md(i["name"]) for i in c["items"][:3])
        rows.append(f"| {md(c['name'])} | {c['action']} | {len(c['items'])} | {human(c['size'])} | {largest} |")
    return "\n".join(rows)


def cell(value):
    return f"<td>{html.escape(str(value))}</td>"


def badge(action):
    action = html.escape(action)
    return f"<span class='action {action}'>{action}</span>"


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    return f"<table><tr>{head}</tr>{''.join(rows)}</table>"


def render(scan, plan):
    """Returns the report HTML: a summary table, then one section per category that lists its items."""
    cats = categories(scan, plan)
    count = sum(len(c["items"]) for c in cats)
    size = sum(c["size"] for c in cats)
    parts = [f"<h1>Triage: {html.escape(scan['dir'])}</h1><p class='sub'>Scanned {html.escape(scan['scanned'])}. "
             f"{plural(count, 'item')}, {human(size)}, in {plural(len(cats), 'category', 'categories')}.</p>"]
    rows = [f"<tr>{cell(c['name'])}<td>{badge(c['action'])}</td>{cell(len(c['items']))}{cell(human(c['size']))}"
            f"{cell(dates(c))}</tr>" for c in cats]
    parts.append(table(["Category", "Action", "Items", "Size", "Modified"], rows))
    for c in cats:
        rows = [f"<tr>{cell(i['name'])}{cell(i['type'])}{cell(human(i['size']))}{cell(i['modified'])}</tr>"
                for i in c["items"]]
        parts.append(f"<h2>{html.escape(c['name'])} {badge(c['action'])}</h2><p>{html.escape(c['reason'])}</p>"
                     f"<p class='sub'>{plural(len(c['items']), 'item')}, {human(c['size'])}, modified {dates(c)}.</p>"
                     + table(["Name", "Type", "Size", "Modified"], rows))
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>Triage</title>"
            f"<style>{STYLE}</style></head><body>{''.join(parts)}</body></html>")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scan").add_argument("dir")
    for name in ["summary", "apply", "render"]:
        p = sub.add_parser(name)
        p.add_argument("--scan", required=True)
        p.add_argument("--plan", required=True)
    args = parser.parse_args(argv)

    if args.command == "scan":
        json.dump(scan(args.dir), sys.stdout, indent=1)
        return 0

    scanned, plan = load(args.scan), load(args.plan)
    problems = apply(scanned, plan) if args.command == "apply" else plan_problems(scanned, plan)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1

    if args.command == "summary":
        print(summary(scanned, plan))
    elif args.command == "apply":
        print(f"Moved {plural(len(scanned['items']), 'item')} into {plural(len(plan['categories']), 'folder')}.")
    else:
        path = os.path.join(scanned["dir"], REPORT)
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(scanned, plan))
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
