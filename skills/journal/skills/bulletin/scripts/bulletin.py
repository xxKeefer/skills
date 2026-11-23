#!/usr/bin/env python3
import argparse
import datetime
import html.parser
import json
import re
import sys
from pathlib import Path

ENTRY = re.compile(r'<article class="entry" data-date="(\d{4}-\d\d-\d\d)">.*?</article>', re.S)
NAME = re.compile(r"(\d{4})-wk(\d\d)-bulletin\.html$")
TEMPLATE = Path(__file__).resolve().parent.parent / "template.html"
OPEN = '<main id="entries">\n'


class Ids(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "data-id" and value:
                self.ids.append(value)


def name_for(day):
    year, week, _ = day.isocalendar()
    return f"{year}-wk{week:02d}-bulletin.html"


def week_of(name):
    match = NAME.match(name)
    return (int(match.group(1)), int(match.group(2))) if match else None


def load(path, day):
    if path.is_file():
        return path.read_text(encoding="utf-8")
    year, week, _ = day.isocalendar()
    text = TEMPLATE.read_text(encoding="utf-8")
    return text.replace("{{year}}", str(year)).replace("{{week}}", f"{week:02d}")


def state(folder, day):
    path = Path(folder) / name_for(day)
    exists = path.is_file()
    entries = list(ENTRY.finditer(path.read_text(encoding="utf-8"))) if exists else []
    days = [m.group(1) for m in entries]
    last_ids = []
    since = None
    if entries:
        parser = Ids()
        parser.feed(entries[0].group(0))
        last_ids = list(dict.fromkeys(parser.ids))
        since = (day - datetime.date.fromisoformat(days[0])).days
    return {
        "path": str(path),
        "exists": exists,
        "today_present": day.isoformat() in days,
        "days": days,
        "days_since_last": since,
        "last_ids": last_ids,
        "week_start": (day - datetime.timedelta(days=day.weekday())).isoformat(),
    }


def add(path, entry_file, day):
    path = Path(path)
    if week_of(path.name) != day.isocalendar()[:2]:
        print(f"{day} is not in the week of {path.name}", file=sys.stderr)
        return 1
    entry = Path(entry_file).read_text(encoding="utf-8")
    if not entry.endswith("\n"):
        entry += "\n"
    text = load(path, day)
    if day.isoformat() in [m.group(1) for m in ENTRY.finditer(text)]:
        print(f"{path} has an entry for {day}", file=sys.stderr)
        return 1
    at = text.find(OPEN)
    if at < 0:
        print(f"{path} has no entries section", file=sys.stderr)
        return 1
    at += len(OPEN)
    path.write_text(text[:at] + entry + text[at:], encoding="utf-8")
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("state")
    s.add_argument("folder")
    s.add_argument("--date", type=datetime.date.fromisoformat, default=datetime.date.today())
    a = sub.add_parser("add")
    a.add_argument("path")
    a.add_argument("entry")
    a.add_argument("--date", type=datetime.date.fromisoformat, default=datetime.date.today())
    args = parser.parse_args(argv)
    if args.cmd == "state":
        json.dump(state(args.folder, args.date), sys.stdout)
        print()
        return 0
    return add(args.path, args.entry, args.date)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
