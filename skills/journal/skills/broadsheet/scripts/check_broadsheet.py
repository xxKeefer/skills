#!/usr/bin/env python3
"""Checks a broadsheet page. Prints ok and exits 0, or prints each problem and exits 1."""
import re
import sys
from html.parser import HTMLParser

SECTIONS = ["masthead", "lead", "compass", "weather", "chores", "gaps", "the-ledger", "letters", "stale-shelf",
            "the-morgue", "editorial", "floor-plan", "honour-roll", "the-board", "back-pages"]
REMOVED = ["carried-over", "link-health"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
NOTE = re.compile(r"\b\d\d-[\w-]+/[^<>\n]*?\.md\b")
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.sections = set()
        self.link_depth = 0
        self.skip_depth = 0
        self.in_body = False
        self.scripts = 0
        self.stack = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for _, value in attrs:
            for found in PLACEHOLDER.findall(value or ""):
                self.problems.append(f"placeholder {found} is still on the page")
        if tag == "body":
            self.in_body = True
        if tag in ("style", "script"):
            self.skip_depth += 1
        if tag == "script":
            self.scripts += 1
        if a.get("id") in SECTIONS + REMOVED:
            self.sections.add(a["id"])
        classes = (a.get("class") or "").split()
        rows = [row for _, row in self.stack if row]
        if rows and tag == "select" and "choice" in classes:
            rows[-1]["choice"] = True
        if rows and tag in ("input", "textarea") and "comment" in classes:
            rows[-1]["comment"] = True
        row = {"id": a.get("data-id") or "", "choice": False, "comment": False} if "action" in classes else None
        if tag not in VOID:
            self.stack.append((tag, row))
        elif row:
            self.end_row(row)
        if self.in_body and "style" in a:
            self.problems.append(f'<{tag}> has an inline style. Use a class from the template: style="{a["style"]}"')
        if tag == "a":
            self.link_depth += 1
            href = a.get("href", "")
            if a.get("target") != "_blank":
                self.problems.append(f'link {href} has no target="_blank"')
            if "noopener" not in (a.get("rel") or ""):
                self.problems.append(f'link {href} has no rel="noopener"')

    def handle_endtag(self, tag):
        if any(open_tag == tag for open_tag, _ in self.stack):
            while True:
                open_tag, row = self.stack.pop()
                if row:
                    self.end_row(row)
                if open_tag == tag:
                    break
        if tag == "a":
            self.link_depth -= 1
        if tag in ("style", "script"):
            self.skip_depth -= 1

    def end_row(self, row):
        name = row["id"]
        if not name:
            self.problems.append("action row has no data-id")
            name = "with no data-id"
        elif name in self.ids:
            self.problems.append(f"action row id {name} is used twice")
        self.ids.add(row["id"])
        if not row["choice"]:
            self.problems.append(f"action row {name} has no choice control")
        if not row["comment"]:
            self.problems.append(f"action row {name} has no comment")

    def close(self):
        super().close()
        while self.stack:
            _, row = self.stack.pop()
            if row:
                self.end_row(row)

    def handle_data(self, data):
        for found in PLACEHOLDER.findall(data):
            self.problems.append(f"placeholder {found} is still on the page")
        if self.skip_depth or self.link_depth:
            return
        for found in NOTE.findall(data):
            self.problems.append(f"note {found} is not a link")


def main(path):
    page = Page()
    with open(path) as f:
        page.feed(f.read())
    page.close()
    problems = page.problems + [f"section #{s} is missing" for s in SECTIONS if s not in page.sections]
    problems += [f"section #{s} must not be on the page" for s in REMOVED if s in page.sections]
    if page.scripts > 1:
        problems.append(f"the page has {page.scripts} script blocks; only 1 is allowed")
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
