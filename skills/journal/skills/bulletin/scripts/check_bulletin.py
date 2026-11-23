#!/usr/bin/env python3
"""Checks a bulletin page. Prints ok and exits 0, or prints each problem and exits 1."""
import datetime
import os
import re
import sys
from html.parser import HTMLParser

BANNED = {"select", "textarea", "script", "input", "button"}
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.entries = []
        self.cur = None
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        for _, value in attrs:
            for found in PLACEHOLDER.findall(value or ""):
                self.problems.append(f"placeholder {found} is still on the page")
        if tag == "style":
            self.skip += 1
        if tag in BANNED:
            self.problems.append(f"<{tag}> is not allowed on a bulletin")
        if "action" in classes or "choice" in classes or "comment" in classes:
            self.problems.append(f"class {' '.join(classes)} is a suggestion row or choice control")
        if tag == "article" and "entry" in classes:
            self.cur = {"date": a.get("data-date") or "", "masthead": False}
            self.entries.append(self.cur)
        if self.cur is not None and "masthead" in classes:
            self.cur["masthead"] = True

    def handle_endtag(self, tag):
        if tag == "style":
            self.skip -= 1
        if tag == "article":
            self.cur = None

    def handle_data(self, data):
        if self.skip:
            return
        for found in PLACEHOLDER.findall(data):
            self.problems.append(f"placeholder {found} is still on the page")


def problems(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    page = Page()
    page.feed(text)
    found = list(dict.fromkeys(page.problems))
    match = re.match(r"(\d{4})-wk(\d\d)-bulletin\.html$", os.path.basename(path))
    week = (int(match.group(1)), int(match.group(2))) if match else None
    if not page.entries:
        found.append("the page has no entry")
    seen = []
    for entry in page.entries:
        date = entry["date"]
        if not entry["masthead"]:
            found.append(f"entry {date} has no masthead")
        try:
            day = datetime.date.fromisoformat(date)
        except ValueError:
            found.append(f"entry date {date!r} is not a date")
            continue
        if date in seen:
            found.append(f"two entries for {date}")
        if seen and date > seen[-1]:
            found.append(f"entry {date} is below an older entry")
        if week and day.isocalendar()[:2] != week:
            found.append(f"entry {date} is outside week {week[0]}-wk{week[1]:02d}")
        seen.append(date)
    return found


def main(argv):
    if len(argv) != 1:
        print("usage: check_bulletin.py <bulletin.html>", file=sys.stderr)
        return 2
    found = problems(argv[0])
    if found:
        print("\n".join(found))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
