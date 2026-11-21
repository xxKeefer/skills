#!/usr/bin/env python3
import argparse
import datetime
import html.parser
import json
import os
import sys


class Ids(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "data-id" and value and value not in self.ids:
                self.ids.append(value)


def name_for(day):
    year, week, _ = day.isocalendar()
    return f"{year}-wk{week:02d}-broadsheet.html"


def row_ids(path):
    parser = Ids()
    with open(path, encoding="utf-8") as f:
        parser.feed(f.read())
    return parser.ids


def muted_ids(path, day):
    if not os.path.isfile(path):
        return []
    ids = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = [part.strip() for part in line.split("|")]
            if len(parts) != 2 or not parts[0]:
                continue
            row_id, rule = parts
            if rule == "veto":
                mute = True
            elif rule.startswith("snooze until "):
                try:
                    mute = day <= datetime.date.fromisoformat(rule[len("snooze until "):].strip())
                except ValueError:
                    continue
            else:
                continue
            if mute and row_id not in ids:
                ids.append(row_id)
    return ids


def edition(folder, day):
    path = os.path.join(folder, name_for(day))
    last = os.path.join(folder, name_for(day - datetime.timedelta(days=7)))
    has_last = os.path.isfile(last)
    return {
        "path": path,
        "exists": os.path.isfile(path),
        "last_path": last if has_last else None,
        "last_ids": row_ids(last) if has_last else [],
        "muted": muted_ids(os.path.join(folder, "broadsheet-memory.md"), day),
    }


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--date", type=datetime.date.fromisoformat, default=datetime.date.today())
    args = parser.parse_args(argv)
    json.dump(edition(args.folder, args.date), sys.stdout)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
