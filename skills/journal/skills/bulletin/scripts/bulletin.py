#!/usr/bin/env python3
import argparse
import datetime
import html.parser
import json
import os
import re
import sys

ENTRY = re.compile(r'<article class="entry" data-date="(\d{4}-\d\d-\d\d)">.*?</article>', re.S)
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "template.html")
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


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def state(folder, day):
    path = os.path.join(folder, name_for(day))
    exists = os.path.isfile(path)
    entries = list(ENTRY.finditer(read(path))) if exists else []
    days = [m.group(1) for m in entries]
    last_ids = []
    since = None
    if entries:
        parser = Ids()
        parser.feed(entries[0].group(0))
        last_ids = list(dict.fromkeys(parser.ids))
        since = (day - datetime.date.fromisoformat(days[0])).days
    return {
        "path": path,
        "exists": exists,
        "today_present": day.isoformat() in days,
        "days": days,
        "days_since_last": since,
        "last_ids": last_ids,
        "week_start": (day - datetime.timedelta(days=day.weekday())).isoformat(),
    }


def add(path, entry_file, day):
    match = re.match(r"(\d{4})-wk(\d\d)-bulletin\.html$", os.path.basename(path))
    year, week, _ = day.isocalendar()
    if not match or (int(match.group(1)), int(match.group(2))) != (year, week):
        print(f"{day} is not in the week of {os.path.basename(path)}", file=sys.stderr)
        return 1
    entry = read(entry_file)
    if not entry.endswith("\n"):
        entry += "\n"
    if os.path.isfile(path):
        text = read(path)
        if day.isoformat() in [m.group(1) for m in ENTRY.finditer(text)]:
            print(f"{path} has an entry for {day}", file=sys.stderr)
            return 1
    else:
        text = read(TEMPLATE).replace("{{year}}", str(year)).replace("{{week}}", f"{week:02d}")
    at = text.find(OPEN)
    if at < 0:
        print(f"{path} has no entries section", file=sys.stderr)
        return 1
    at += len(OPEN)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text[:at] + entry + text[at:])
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
