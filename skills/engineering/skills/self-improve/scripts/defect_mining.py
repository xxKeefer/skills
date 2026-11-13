#!/usr/bin/env python3
"""Trace a repo's bugs and fix commits for /engineering:self-improve, and write its defect hotspots.

  trace     Reads the first-parent line of the default branch and the tracker bugs. Writes
            defects.jsonl, the miner chunks of the items that need a class, and trace.json to the
            cache folder.
  hotspots  Merges the miner files into the class cache in the state folder, writes
            defect-hotspots.md there, and writes the run window's defects to the cache folder.

Run: python3 defect_mining.py trace --repo-root <dir> --ref <ref> --since <date> --window-start <date>
       --until <date> --cache <folder> --state <folder> [--tracker <file>] [--chunk <n>]
     python3 defect_mining.py hotspots --cache <folder> --state <folder>
"""
import argparse
import glob
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

ESCAPES = ["boundary", "combination", "state-transition", "interruption", "contract", "authz", "data-config",
           "secrets-logging", "regression", "other"]
LEVELS = ["unit", "integration", "contract", "e2e", "none"]
CHUNK = 25
AREAS = 25
AREA_FLOOR = 2
DIMENSIONS = 15
SKEW = 0.6
FIX = re.compile(r"fix|bug", re.I)
KEY = re.compile(r"(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9]*-[0-9]+)")
TEST_FOLDERS = {"test", "tests", "__tests__", "spec", "specs", "e2e"}
TEST_NAME = re.compile(r"\.(test|spec)\.|_(test|spec)\.|^test_|[a-z0-9](Test|Tests)\.")
LOCK_FILES = {"package-lock.json", "pnpm-lock.yaml", "go.sum"}


def parse_time(text):
    text = text.strip().replace("Z", "+00:00")
    moment = datetime.fromisoformat(text) if "T" in text else datetime.strptime(text[:10], "%Y-%m-%d")
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def is_test(path):
    """Returns true for a file in a test folder, or a file whose name marks it as a test."""
    *folders, name = path.split("/")
    return bool(TEST_FOLDERS.intersection(folders) or TEST_NAME.search(name))


def is_lock(path):
    name = posixpath.basename(path)
    return name.endswith(".lock") or name in LOCK_FILES


def read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def write_lines(path, records):
    with open(path, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def commits(root, ref, since, until):
    """Returns the commits of the window on the first-parent line of the ref, each with the files it changed."""
    args = ["git", "-C", root, "log", ref, "--first-parent", "-m", "--name-only", f"--since={since}",
            f"--until={until}", "--format=%x1e%H%x1f%cI%x1f%B%x1d"]
    out = subprocess.run(args, check=True, stdout=subprocess.PIPE, text=True).stdout
    result = []
    for record in out.split("\x1e")[1:]:
        head, _, names = record.partition("\x1d")
        sha, date, message = head.split("\x1f", 2)
        files = [n for n in names.splitlines() if n.strip()]
        result.append({"sha": sha, "date": date, "message": message.strip(), "files": files})
    return result


def item(ident, source, date, title, found, in_window):
    files = sorted({f for c in found for f in c["files"]})
    return {"id": ident, "source": source, "date": date[:10], "title": title, "commits": [c["sha"] for c in found],
            "files": files, "tested": any(is_test(f) for f in files), "inWindow": in_window}


def needs_class(entry, tracker):
    """Returns true for a tracker bug, and for a fix commit that the hotspots or the themes use."""
    return entry["source"] == "tracker" or not tracker or entry["inWindow"]


def trace(root, ref, since, window_start, until, cache, state, tracker_path=None, chunk=CHUNK):
    """Joins the tracker bugs to their commits, lists the other fix commits, and chunks the items to classify."""
    log = commits(root, ref, since, until)
    start = parse_time(window_start)
    bugs = read_lines(tracker_path) if tracker_path else []
    by_key = {b["id"].upper(): b["id"] for b in bugs if not b.get("commits")}
    found = {b["id"]: [] for b in bugs}
    for c in log:
        for key in {k.upper() for k in KEY.findall(c["message"])}:
            if key in by_key:
                found[by_key[key]].append(c)
    for b in bugs:
        for prefix in b.get("commits") or []:
            found[b["id"]] += [c for c in log if c["sha"].startswith(prefix)]
    items, used = [], set()
    for b in bugs:
        if found[b["id"]]:
            used.update(c["sha"] for c in found[b["id"]])
            items.append(item(b["id"], "tracker", b["date"], b.get("title", ""), found[b["id"]],
                              parse_time(b["date"][:10]) >= start))
    for c in log:
        if c["sha"] not in used and FIX.search(c["message"]):
            items.append(item(c["sha"], "commit", c["date"], c["message"].splitlines()[0], [c],
                              parse_time(c["date"]) >= start))
    known = {entry["id"] for entry in read_lines(os.path.join(state, "classified.jsonl"))}
    todo = [i for i in items if needs_class(i, bool(bugs)) and i["id"] not in known]
    folder = os.path.join(cache, "defect-chunks")
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
    names = []
    for n in range(0, len(todo), chunk):
        name = os.path.join("defect-chunks", f"{n // chunk + 1:02d}.jsonl")
        fields = ("id", "source", "title", "commits", "files")
        write_lines(os.path.join(cache, name), [{k: i[k] for k in fields} for i in todo[n:n + chunk]])
        names.append(name)
    write_lines(os.path.join(cache, "defects.jsonl"), items)
    tracked = [i for i in items if i["source"] == "tracker"]
    fixes = [i for i in items if i["source"] == "commit"]
    meta = {
        "since": since, "windowStart": window_start, "until": until, "tracker": bool(bugs),
        "bugs": len(bugs), "traced": len(tracked), "trackerInWindow": sum(i["inWindow"] for i in tracked),
        "fixCommits": len(fixes), "fixCommitsInWindow": sum(i["inWindow"] for i in fixes),
        "toClassify": len(todo), "chunks": names,
    }
    write_json(os.path.join(cache, "trace.json"), meta)
    return meta


def cell(text):
    return " ".join(str(text or "").replace("|", "/").split())


def cheapest_common(levels):
    counts = Counter(level for level in levels if level in LEVELS)
    if not counts:
        return ""
    return min(counts, key=lambda level: (-counts[level], LEVELS.index(level)))


def top_escapes(escapes, limit):
    counts = Counter(escapes)
    return sorted(counts, key=lambda e: (-counts[e], ESCAPES.index(e)))[:limit], counts


def render(meta, defects):
    since, until = meta["since"][:10], meta["until"][:10]
    source = (f"the tracker bugs resolved {since}..{until}" if meta["tracker"]
              else f"the fix commits of {since}..{until}")
    tested = sum(d["tested"] for d in defects)
    lines = ["# Defect hotspots", "", "Written by `/engineering:self-improve`. Do not edit.", "",
             f"- Source: {source}. Defects: {len(defects)}."]
    if meta["tracker"] and meta["bugs"]:
        share = meta["traced"] / meta["bugs"]
        lines.append(f"- Coverage: {meta['traced']}/{meta['bugs']} tracker bugs trace to a commit in this repo "
                     f"({round(100 * share)}%).")
        if share < SKEW:
            lines.append("- Skewed: under 60 percent of the bugs trace to a commit, so the table favours the "
                         "areas whose commits name their bug.")
    lines.append(f"- With a test: {tested}/{len(defects)} fixes changed a test file.")

    areas = {}
    for d in defects:
        for folder in {posixpath.dirname(f) or "." for f in d["files"] if not is_test(f) and not is_lock(f)}:
            areas.setdefault(folder, []).append(d)
    hot = [a for a in areas if len(areas[a]) >= AREA_FLOOR]
    ranked = sorted(hot, key=lambda a: (-len(areas[a]), a))[:AREAS]
    lines += ["", "## Hotspots", "", "| Area | Bugs | With a test | Usually missed |", "| --- | --- | --- | --- |"]
    for area in ranked:
        group = areas[area]
        names, counts = top_escapes([d["escape"] for d in group], 2)
        missed = ", ".join(f"{e} {counts[e]}" for e in names)
        lines.append(f"| `{area}` | {len(group)} | {sum(d['tested'] for d in group)}/{len(group)} | {missed} |")

    names, counts = top_escapes([d["escape"] for d in defects], len(ESCAPES))
    lines += ["", "## What escapes", "", "| Escape type | Bugs | Cheapest level | Example condition |",
              "| --- | --- | --- | --- |"]
    for escape in names:
        group = [d for d in defects if d["escape"] == escape]
        newest = max(group, key=lambda d: (d["date"], d["id"]))
        level = cheapest_common(d.get("level") for d in group)
        shown = f"`{level}`" if level else ""
        lines.append(f"| `{escape}` | {counts[escape]} | {shown} | {cell(newest.get('condition'))} |")

    dimensions = Counter()
    for d in defects:
        dimensions.update({str(x).strip().lower() for x in d.get("dimensions") or [] if str(x).strip()})
    lines += ["", "## Dimensions", "", "| Dimension | Bugs |", "| --- | --- |"]
    for name in sorted(dimensions, key=lambda x: (-dimensions[x], x))[:DIMENSIONS]:
        lines.append(f"| {cell(name)} | {dimensions[name]} |")
    return "\n".join(lines) + "\n"


def hotspots(cache, state):
    """Merges the miner classes into the cache, writes defect-hotspots.md, and writes the run window's defects."""
    with open(os.path.join(cache, "trace.json")) as f:
        meta = json.load(f)
    items = read_lines(os.path.join(cache, "defects.jsonl"))
    ids = {i["id"] for i in items}
    cache_file = os.path.join(state, "classified.jsonl")
    classes = {c["id"]: c for c in read_lines(cache_file)}
    mined = [c for path in sorted(glob.glob(os.path.join(cache, "classified", "*.jsonl"))) for c in read_lines(path)]
    unknown = [c["id"] for c in mined if c["id"] not in ids]
    if unknown:
        sys.exit(f"These IDs are not in defects.jsonl: {', '.join(unknown)}")
    classes.update({c["id"]: c for c in mined})
    missing = [i["id"] for i in items if needs_class(i, meta["tracker"]) and i["id"] not in classes]
    if missing:
        sys.exit(f"These items need a class and have none: {', '.join(missing)}")
    write_lines(cache_file, [classes[i["id"]] for i in items if i["id"] in classes])

    joined = []
    for i in items:
        c = classes.get(i["id"])
        if c and c.get("defect") and needs_class(i, meta["tracker"]):
            entry = {**i, **c}
            entry["escape"] = c.get("escape") if c.get("escape") in ESCAPES else "other"
            joined.append(entry)
    bug_source = "tracker" if meta["tracker"] else "commit"
    defects = [d for d in joined if d["source"] == bug_source]
    path = os.path.join(state, "defect-hotspots.md")
    with open(path, "w") as f:
        f.write(render(meta, defects))

    fields = ("id", "source", "title", "kind", "check", "specific")
    window = [{k: d.get(k) for k in fields} for d in joined if d["inWindow"]]
    write_lines(os.path.join(cache, "window-defects.jsonl"), window)
    return {
        "path": path, "defects": len(defects), "traced": meta["traced"], "bugs": meta["bugs"],
        "skewed": bool(meta["tracker"] and meta["bugs"] and meta["traced"] / meta["bugs"] < SKEW),
        "windowDefects": {s: sum(d["source"] == s for d in window) for s in ("tracker", "commit")},
    }


def main():
    parser = argparse.ArgumentParser(description="Defect mining for /engineering:self-improve.")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("trace", help="Join the bugs to their commits, and chunk the items to classify.")
    run.add_argument("--repo-root", required=True)
    run.add_argument("--ref", required=True, help="The default branch, such as origin/main")
    run.add_argument("--since", required=True, help="The start of the 12 months")
    run.add_argument("--window-start", required=True, help="The start of the run window")
    run.add_argument("--until", required=True)
    run.add_argument("--cache", required=True)
    run.add_argument("--state", required=True, help="The repo's state folder, which holds classified.jsonl")
    run.add_argument("--tracker", help="JSON lines: {id, date, title, commits?}. Leave out with no tracker.")
    run.add_argument("--chunk", type=int, default=CHUNK, help="Items in each miner chunk")
    build = commands.add_parser("hotspots", help="Merge the classes and write defect-hotspots.md.")
    build.add_argument("--cache", required=True)
    build.add_argument("--state", required=True)
    args = parser.parse_args()
    if args.command == "trace":
        result = trace(args.repo_root, args.ref, args.since, args.window_start, args.until, args.cache, args.state,
                       args.tracker, args.chunk)
    else:
        result = hotspots(args.cache, args.state)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
