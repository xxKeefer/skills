#!/usr/bin/env python3
import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

LINK = re.compile(r"!?\[\[([^\]]+)\]\]")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
TASK = re.compile(r"^(\s*)[-*] \[(.)\] (.+)$")
BOLD = re.compile(r"\*\*|__")
EMPTY = re.compile(r"^\s*(?:[-*+]|\d+[.)])?\s*(?:\[.\])?\s*$")
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
PARSER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts", "occasions.py")
_spec = importlib.util.spec_from_file_location("occasions", PARSER)
occasions_parser = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(occasions_parser)


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta, key = {}, None
    for line in text[4:end].splitlines():
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            meta.setdefault(key, []).append(item.group(1).strip().strip("'\""))
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]") and not value.startswith("[["):
                meta[key] = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
            elif value:
                meta[key] = value.strip("'\"")
    return meta, text[end + 4:]


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith("."))
        for name in sorted(files):
            yield os.path.relpath(os.path.join(d, name), root)


def git_history(root):
    if not os.path.isdir(os.path.join(root, ".git")):
        return None
    p = subprocess.run(
        ["git", "-c", "core.quotepath=off", "log", "--format=@%at %ad", "--date=format:%H %u",
         "--name-status", "-M", "-l0"],
        cwd=root, capture_output=True, text=True,
    )
    if p.returncode:
        return None
    commits, current, alias = [], None, {}
    for line in p.stdout.splitlines():
        if line.startswith("@"):
            stamp, hour, weekday = line[1:].split()
            current = {"date": dt.datetime.fromtimestamp(int(stamp), dt.timezone.utc).date(),
                       "hour": int(hour), "weekday": int(weekday) - 1, "files": []}
            commits.append(current)
        elif line and current:
            status, *paths = line.split("\t")
            path = alias.get(paths[-1], paths[-1])
            if status.startswith("R"):
                alias[paths[0]] = path
            elif status.startswith("A"):
                alias[paths[0]] = None
            if path is not None and status != "R100":
                current["files"].append(path)
    return commits


def dirty_files(root):
    p = subprocess.run(["git", "-c", "core.quotepath=off", "status", "--porcelain", "-uall"],
                       cwd=root, capture_output=True, text=True)
    return {line[3:].split(" -> ")[-1].strip('"') for line in p.stdout.splitlines() if len(line) > 3}


def targets(body):
    found = []
    for raw in LINK.findall(CODE.sub("", body)):
        if "{{" in raw or "<%" in raw:
            continue
        t = re.split(r"[#|^]", raw, maxsplit=1)[0].strip()
        if t.lower().endswith(".md"):
            t = t[:-3]
        if t:
            found.append(t)
    return found


def top(rel):
    return rel.split(os.sep, 1)[0] if os.sep in rel else ""


def leaf_tasks(body):
    lines = body.splitlines()
    out = []
    for i, line in enumerate(lines):
        m = TASK.match(line)
        if not m:
            continue
        indent = len(m.group(1).expandtabs(4))
        nxt = next((l for l in lines[i + 1:] if l.strip()), "")
        n = TASK.match(nxt) or re.match(r"^(\s*)[-*] ", nxt)
        if n and len(n.group(1).expandtabs(4)) > indent:
            continue
        out.append((" ".join(BOLD.sub("", m.group(3)).split()), m.group(2).lower() == "x"))
    return out


def reflect(body, weekly=False):
    sections, inside, heading, lines = [], False, None, []

    def close():
        text = "\n".join(l.rstrip() for l in lines if not EMPTY.match(l)).strip()
        if text:
            sections.append({"heading": heading, "text": text})

    for line in body.splitlines():
        if re.match(r"^#{1,2}\s", line):
            if inside:
                close()
            starts = bool(re.match(r"^##\s.*\bReflect\b", line))
            inside = starts and weekly == bool(re.match(r"^##\s.*\bWeekly Reflect\b", line))
            heading, lines = None, []
        elif inside and line.startswith("### "):
            close()
            heading, lines = line[4:].strip(), []
        elif inside:
            lines.append(line)
    if inside:
        close()
    return sections


def journal_level(rel, meta):
    kind = meta.get("type", "")
    level = kind.split("/", 1)[1] if kind in ("journal/daily", "journal/weekly", "journal/monthly") else None
    name = os.path.splitext(os.path.basename(rel))[0].lower()
    m = re.fullmatch(r"(\d{4})-wk(\d{2})-(\w{3,4})", name)
    n = re.fullmatch(r"(\d{4})-(\d{2})-[a-z]{3}", name)
    guess = None
    try:
        if m and m.group(3) == "week":
            guess = ("weekly", dt.date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1))
        elif m and m.group(3) in DAYS:
            guess = ("daily", dt.date.fromisocalendar(int(m.group(1)), int(m.group(2)), DAYS.index(m.group(3)) + 1))
        elif n:
            guess = ("monthly", dt.date(int(n.group(1)), int(n.group(2)), 1))
    except ValueError:
        guess = None
    level = level or (guess[0] if guess else None)
    if not level:
        return None
    try:
        date = dt.date.fromisoformat(meta["date"]) if meta.get("date") else None
    except ValueError:
        date = None
    date = date or (guess[1] if guess and guess[0] == level else None)
    return (level, date) if date else None


def scan(root, journal, today, window, stale_days, archive_days, limit):
    commits = git_history(root)
    dirty = dirty_files(root) if commits else set()
    last = {}
    if commits:
        for c in commits:
            for f in c["files"]:
                last.setdefault(f, c["date"])

    def mtime(rel):
        return dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, rel)))

    def age(rel):
        key = rel.replace(os.sep, "/")
        d = last.get(key)
        if d is None or key in dirty:
            d = mtime(rel).date()
        return (today - d).days

    files = list(walk(root))
    names, paths = set(), set()
    for rel in files:
        base, ext = os.path.splitext(rel)
        names.add((os.path.basename(base) if ext == ".md" else os.path.basename(rel)).lower())
        paths.add((base if ext == ".md" else rel).replace(os.sep, "/").lower())

    tops = {d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")}
    jtop = os.path.relpath(journal, root).split(os.sep)[0]
    inbox = {d for d in tops if d.endswith("notes")}
    archive = {d for d in tops if d.endswith("archive")}
    meta_dirs = {d for d in tops if d.endswith("meta")}
    knowledge = {d for d in tops if d.endswith("knowledge")}
    skip = {jtop} | inbox | archive | meta_dirs

    notes = {}
    backlinks = defaultdict(list)
    broken = []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
        meta, body = frontmatter(text)
        notes[rel] = {"meta": meta, "body": body, "age": age(rel), "text": text}
        for t in targets(text):
            low = t.lower()
            if low in names or low in paths:
                backlinks[os.path.basename(low)].append(rel)
                backlinks[low].append(rel)
            elif top(rel):
                broken.append((t, rel))

    def links_to(rel):
        base = rel[:-3].replace(os.sep, "/").lower()
        srcs = set(backlinks.get(os.path.basename(base), [])) | set(backlinks.get(base, []))
        srcs.discard(rel)
        return srcs

    stale, orphans = [], []
    for rel, n in notes.items():
        if top(rel) in skip or not top(rel):
            continue
        srcs = links_to(rel)
        if not srcs:
            orphans.append(rel)
        if n["age"] >= stale_days and top(rel) not in knowledge:
            recent = sum(1 for s in srcs if notes[s]["age"] < stale_days)
            stale.append({"path": rel, "age_days": n["age"], "backlinks": len(srcs), "recent_backlinks": recent})

    archived = []
    for rel, n in notes.items():
        if top(rel) in archive:
            srcs = {s for s in links_to(rel) if top(s) not in archive}
            archived.append({"path": rel, "age_days": n["age"], "backlinks": len(srcs),
                             "delete_candidate": n["age"] >= archive_days and not srcs})

    recent = sorted(({"path": rel, "age_days": n["age"], "words": len(n["body"].split())}
                     for rel, n in notes.items() if top(rel) and top(rel) != jtop and n["age"] <= window),
                    key=lambda r: (r["age_days"], r["path"]))
    inbox_rows = [{"path": rel, "age_days": n["age"], "words": len(n["body"].split())}
                  for rel, n in notes.items() if top(rel) in inbox]

    start = today - dt.timedelta(days=window)
    dailies = []
    for rel, n in notes.items():
        if top(rel) == jtop and n["meta"].get("type") == "journal/daily" and n["meta"].get("date"):
            try:
                dailies.append((dt.date.fromisoformat(n["meta"]["date"]), rel, n))
            except ValueError:
                pass
    dailies.sort()
    present = {d for d, _, _ in dailies}
    missing = [str(start + dt.timedelta(days=i)) for i in range(window)
               if start + dt.timedelta(days=i) not in present]
    in_window = [x for x in dailies if start <= x[0] <= today]
    summaries = []
    for d, rel, n in in_window:
        quote = next((l[1:].strip() for l in n["body"].splitlines() if l.startswith(">")), "")
        summaries.append({"date": str(d), "path": rel, "summary": quote})

    runs, latest = {}, {}
    for d, _, n in dailies:
        tasks = dict(leaf_tasks(n["body"]))
        for task in list(runs):
            if tasks.get(task) is not False:
                if runs[task]["days"] >= 3:
                    latest[task] = runs[task]
                del runs[task]
        for task, done in tasks.items():
            if done:
                continue
            run = runs.setdefault(task, {"task": task, "days": 0, "first": str(d)})
            run["days"] += 1
            run["last"] = str(d)
    for task, run in runs.items():
        if run["days"] >= 3:
            latest[task] = run
    carried = sorted((r for r in latest.values() if r["last"] >= str(start)), key=lambda r: (-r["days"], r["task"]))

    occasions_path = os.path.join(journal, "occasions.md")
    occasions = open(occasions_path, encoding="utf-8").read() if os.path.isfile(occasions_path) else ""
    occasions_errors = occasions_parser.read(occasions, today)["errors"] if occasions else []
    due_on = {}

    def due(day):
        if day not in due_on:
            found = occasions_parser.read(occasions, day) if occasions else {"daily": [], "due": {"chores": []}}
            items = {task for task, _ in leaf_tasks("\n".join(found["daily"]))}
            items |= {" ".join(BOLD.sub("", item).split()) for item in found["due"]["chores"]}
            due_on[day] = items
        return due_on[day]

    def chores(rows):
        seen, ticked = Counter(), Counter()
        for d, _, n in rows:
            items = due(d)
            for task, done in dict(leaf_tasks(n["body"])).items():
                if task in items:
                    seen[task] += 1
                    ticked[task] += done
        return seen, ticked

    seen, ticked = chores(in_window)
    checklists = [{"task": t, "ticked": ticked[t], "seen": s, "rate": round(ticked[t] / s, 2)}
                  for t, s in seen.items()]
    checklists.sort(key=lambda c: (c["rate"], c["task"]))

    broken_nav = []
    for rel, n in notes.items():
        if top(rel) != jtop or n["age"] > window:
            continue
        if os.path.relpath(os.path.join(root, rel), journal).split(os.sep)[0] == "chronicles":
            continue
        for key in ("up", "prev", "next"):
            value = n["meta"].get(key)
            if not isinstance(value, str):
                continue
            for t in targets(value):
                if t.lower() not in names and t.lower() not in paths:
                    broken_nav.append({"path": rel, "key": key, "target": t})

    folders = []
    for d, dirs, fs in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith("."))
        rel = os.path.relpath(d, root)
        if rel == "." or rel.count(os.sep) > 1:
            continue
        inside = [r for r in notes if r.startswith(rel + os.sep)]
        ages = [notes[r]["age"] for r in inside]
        folders.append({
            "path": rel.replace(os.sep, "/"),
            "md": len(inside),
            "files": sum(1 for r in files if r.startswith(rel + os.sep)),
            "subfolders": len(dirs),
            "loose_md": sum(1 for f in fs if f.endswith(".md")),
            "newest_days": min(ages) if ages else None,
            "oldest_days": max(ages) if ages else None,
            "edited_in_window": sum(1 for a in ages if a <= window),
        })

    dirty_notes = [(f, mtime(f)) for f in sorted(dirty) if f.endswith(".md") and "/" in f
                   and not f.startswith(".") and os.path.isfile(os.path.join(root, f))] if commits else []

    def edits_since(since):
        found = Counter()
        if commits:
            for c in commits:
                if c["date"] >= since:
                    for f in c["files"]:
                        if f.endswith(".md") and "/" in f and f not in dirty:
                            found[f.split("/", 1)[0]] += 1
            for f, when in dirty_notes:
                if when.date() >= since:
                    found[f.split("/", 1)[0]] += 1
        else:
            for rel, n in notes.items():
                if top(rel) and today - dt.timedelta(days=n["age"]) >= since:
                    found[top(rel)] += 1
        return found

    edits, hours, weekdays, tags = edits_since(start), [0] * 24, [0] * 7, Counter()
    if commits:
        for c in commits:
            if c["date"] >= start:
                hours[c["hour"]] += 1
                weekdays[c["weekday"]] += 1
        for f, when in dirty_notes:
            if when.date() >= start:
                hours[when.hour] += 1
                weekdays[when.weekday()] += 1
    for rel, n in notes.items():
        if n["age"] <= window:
            value = n["meta"].get("tags", [])
            for t in (value if isinstance(value, list) else [value]):
                tags[t] += 1

    year_ago = today - dt.timedelta(days=365)
    reflections = []
    for rel, n in notes.items():
        if top(rel) != jtop:
            continue
        found = journal_level(rel, n["meta"])
        if not found or not year_ago <= found[1] <= today:
            continue
        sections = reflect(n["body"])
        if sections:
            reflections.append({"path": rel.replace(os.sep, "/"), "level": found[0], "date": str(found[1]),
                                "sections": sections})
        week = reflect(n["body"], weekly=True)
        monday = found[1] - dt.timedelta(days=found[1].weekday())
        if week and year_ago <= monday:
            reflections.append({"path": rel.replace(os.sep, "/"), "level": "weekly", "date": str(monday),
                                "sections": week})
    reflections.sort(key=lambda r: (r["date"], r["path"]), reverse=True)

    compass = []
    for days in (7, 30, 90, 365):
        since = today - dt.timedelta(days=days)
        rows = [x for x in dailies if since <= x[0] <= today]
        seen_w, ticked_w = chores(rows)
        found = edits_since(since)
        compass.append({
            "days": days,
            "dailies": len(rows),
            "edits": sum(found.values()),
            "chore_rate": round(sum(ticked_w.values()) / sum(seen_w.values()), 2) if seen_w else None,
            "busiest": [[f, c] for f, c in sorted(found.items(), key=lambda x: (-x[1], x[0]))[:3]],
            "reflections": sum(1 for r in reflections if r["date"] >= str(since)),
        })

    projects = []
    for ptop in sorted(d for d in tops if d.endswith("projects")):
        for rel in sorted(notes):
            parts = rel.split(os.sep)
            if parts[0] != ptop or parts[-1] != "MISSION.md" or len(parts) < 3:
                continue
            folder = os.path.dirname(rel) + os.sep
            meta = notes[rel]["meta"]
            projects.append({
                "project": parts[-2],
                "path": rel.replace(os.sep, "/"),
                "status": meta.get("status") or "active",
                "until": meta.get("until") or None,
                "changed_days": min(n["age"] for r, n in notes.items() if r.startswith(folder)),
            })

    grouped = defaultdict(list)
    for t, rel in broken:
        grouped[t].append(rel)
    broken_rows = [{"target": t, "count": len(srcs), "from": sorted(set(srcs))[:3]}
                   for t, srcs in sorted(grouped.items(), key=lambda x: (-len(x[1]), x[0]))]
    stale.sort(key=lambda s: -s["age_days"])
    archived.sort(key=lambda a: (not a["delete_candidate"], -a["age_days"]))
    orphans.sort()

    return {
        "today": str(today),
        "totals": {"stale": len(stale), "archive": len(archived), "orphans": len(orphans),
                   "broken": len(broken_rows), "broken_nav": len(broken_nav)},
        "window_days": window,
        "dates_from": "git" if commits else "mtime",
        "folders": folders,
        "journal": {"dailies_in_window": [s["date"] for s in summaries], "missing_days": missing,
                    "summaries": summaries, "carried": carried, "checklists": checklists,
                    "occasions_errors": occasions_errors, "broken_nav": broken_nav},
        "compass": compass,
        "reflections": reflections,
        "projects": projects,
        "inbox": inbox_rows,
        "recent": recent[:limit],
        "stale": stale[:limit],
        "archive": archived[:limit],
        "links": {"broken": broken_rows[:limit], "orphans": orphans[:limit]},
        "activity": {"edits_by_folder": dict(edits.most_common()), "hours": hours, "weekdays": weekdays,
                     "tags": [[t, c] for t, c in sorted(tags.items(), key=lambda x: (-x[1], x[0]))]},
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("vault")
    p.add_argument("--journal", required=True)
    p.add_argument("--today", default=str(dt.date.today()))
    p.add_argument("--window", type=int, default=7)
    p.add_argument("--stale", type=int, default=90)
    p.add_argument("--archive-days", type=int, default=180)
    p.add_argument("--limit", type=int, default=40)
    a = p.parse_args()
    out = scan(os.path.abspath(a.vault), os.path.abspath(a.journal), dt.date.fromisoformat(a.today),
               a.window, a.stale, a.archive_days, a.limit)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
