#!/usr/bin/env python3
"""Checks a gazette page. Prints ok and exits 0, or prints each problem and exits 1."""
import re
import sys
from html.parser import HTMLParser

SECTIONS = ["masthead", "lead", "weather", "your-desk", "around-the-repos", "the-board", "honour-roll"]
TICKET = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
PR = re.compile(r"(?<![\w&])#\d+\b")
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.sections = set()
        self.link_depth = 0
        self.code_depth = 0
        self.skip_depth = 0
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for _, value in attrs:
            for found in PLACEHOLDER.findall(value or ""):
                self.problems.append(f"placeholder {found} is still on the page")
        if tag == "body":
            self.in_body = True
        if tag in ("style", "script"):
            self.skip_depth += 1
        if tag in ("code", "pre"):
            self.code_depth += 1
        if a.get("id") in SECTIONS:
            self.sections.add(a["id"])
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
        if tag == "a":
            self.link_depth -= 1
        if tag in ("code", "pre"):
            self.code_depth -= 1
        if tag in ("style", "script"):
            self.skip_depth -= 1

    def handle_data(self, data):
        for found in PLACEHOLDER.findall(data):
            self.problems.append(f"placeholder {found} is still on the page")
        if self.skip_depth or self.link_depth or self.code_depth:
            return
        for found in TICKET.findall(data):
            self.problems.append(f"ticket key {found} is not a link")
        for found in PR.findall(data):
            self.problems.append(f"PR {found} is not a link")


def main(path):
    page = Page()
    with open(path) as f:
        page.feed(f.read())
    problems = page.problems + [f"section #{s} is missing" for s in SECTIONS if s not in page.sections]
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
